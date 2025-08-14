from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from typing import Optional, List, Annotated
from datetime import datetime
import re
from email_validator import validate_email, EmailNotValidError

PasswordStr = Annotated[str, Field(min_length=8, max_length=128)]
UsernameStr = Annotated[str, Field(min_length=3, max_length=50)]
EmailStr = Annotated[str, Field(max_length=100)]

class UserBase(BaseModel):
    model_config = ConfigDict(
        #direct sqlalchemy model validation
        from_attributes=True,
        #Validates field values on assignment, not just initalization, add this to other schemas
        validate_assignment=True,
        #use enum values inside JSON? what does that even mean
        use_enum_values=True,
    
        #shows specific actual value of the invalid field in errors
        str_strip_whitespace=True,

        json_schema_extra={
            "example": {
                "username": "john_doe",
                "email": "john@example.com"
            }
        }
    )

class UserCreate(BaseModel):
    ''' considerations: XSS attacks, invalid data entry, brute force attacks'''

    username: UsernameStr
    email: EmailStr
    password: PasswordStr
    confirm_password: str
    
    @field_validator('username')
    @classmethod 
    def validate_username(cls, username:str) -> str:
        if not username:
            raise ValueError('Username is required')
        
        username = username.strip().lower()

        # this can be simplified 
        if not re.match(r'^[a-z0-9_]+$', username):
            raise ValueError('Username can only be alphanumeric characters and underscores')
        # why dictionary
        reserved_words = {'admin', 'api', 'root', 'user', 'login', 'register'} 
        if username in reserved_words:
            raise ValueError('This username is reserved')
        return username

    @field_validator('email')
    @classmethod 
    def validate_email(cls, email:str) -> str:
        if not email:
            raise ValueError('Email is required')
        
        try:
            validated = validate_email(email, check_deliverability=False)
            return validated.email.lower()
        except EmailNotValidError as e:
            raise ValueError(f'Invalid email {str(e)}')
        
    
    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, password: str) -> str:
        ''' 
        OWASP recommendations implemented in validation of strength
        Entropy: 94^8 ( 26 + 26 + 10 + 32 = 94 ^ 8 (character min))
        '''

        if not password:
            raise ValueError('Password is required')
        
        if len(password) < 8:
            raise ValueError('Password length must be at least 8 characters')
        
        if not re.search(r'[A-Z]', password):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', password):
            raise ValueError('Password must have at least 1 lowercase letter')
        
        if not re.search(r'\d', password):
            raise ValueError('Password must contain at least 1 number')
        # there has to be a better way to do this TODO: find a module to import or create one to get rid of this nastyness
        if not re.search(r'[!@#$%^&*(),.?:{}|<>]', password):
            raise ValueError('This password is easy to guess. Pick a new one or make this one stronger.')
        return password
    
    @model_validator(mode='after')
    def passwords_match(self) -> 'UserCreate':
        if self.password != self.confirm_password:
            raise ValueError('Passwords do not match')
        return self 
    
class UserLogin(BaseModel):
    username_or_email:str
    password: str

    
    @field_validator('username_or_email')
    @classmethod
    def validate_login(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError('Username or email is required')
        
        value = value.strip().lower()

        if len(value) > 100:
            raise ValueError('Username or email invalid: Length Error')
        
        return value
    
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    current_password: Optional[str] = None
    new_password: Optional[PasswordStr] = None

    @model_validator(mode='after')
    def validate_password_change(self) -> 'UserUpdate':
        if self.new_password and not self.current_password:
            raise ValueError('Current password is required to set a new password')
        return self
    
class UserResponse(BaseModel):
    id: int 
    username: str
    email: Optional[str] = None
    tokens: int = 100
    created_at: datetime
    updated_at: Optional[datetime] = None

    review_count: Optional[int] = 0
    unlocked_count: Optional[int] = 0
    average_rating: Optional[float] = None

    model_config = ConfigDict(
        from_attributes=True
    )

class UserPublicProfile(BaseModel):
    id: int
    username: str
    created_at: datetime
    review_count: int = 0
    average_rating: Optional[float] = None

    top_genres: List[str] = []
    favorite_artists: List[str] = []


class TokenResponse(BaseModel):
    '''
    JWT auth
    Access Token: 15 min
    Refresh Token: 7 days
    '''
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    expires_in: int = 900
    user: UserResponse


class TokenPayload(BaseModel):
    sub: int
    exp: int
    iat: int
    jti: Optional[str] = None







