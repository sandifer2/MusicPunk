from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone

from app.database import get_db
from app.models.user import User
from app.models.token_transaction import TokenTransaction
from app.schemas.user import UserCreate, UserLogin, UserResponse, TokenResponse
from app.schemas.token_transaction import TransactionType
from app.core.security import PasswordManager, TokenManager
from app.api.deps import CurrentUser, get_current_user
from app.services.token_service import TokenService
from app.core.config import settings
import secrets

router = APIRouter(prefix='/auth', tags=["authentication"])
security = HTTPBearer()

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    '''
    User Registration Enpoint
    1. validate with pydantic schema
    2. Check for existing in db
    3. hash pw
    4. create w/ signup bonus
    5. generate auth tokens
    6. return auth tokens

    Security:
    - bycrypt hasing with salt
    - immediate token gen
    - atomic transations 

    '''

    existing_user = db.query(User).filter(
        (User.username == user_data.username) |
        (User.email == user_data.email)
    ).first()

    if existing_user:
        if existing_user.username == user_data.username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already exists"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )
    hashed_pw = PasswordManager.hash_password(user_data.password)

    signup_bonus = TokenService.get_signup_bonus()

    try:
        new_user = User(
            username=user_data.username,
            email=user_data.username,
            password_hash=hashed_pw,
            tokens=signup_bonus,
            is_Active=True
        )
        db.add(new_user)
        db.flush()

        signup_transaction = TokenTransaction(
            user_id=new_user.id,
            amount=signup_bonus,
            balance_after=signup_bonus,
            TransactionType=TransactionType.SIGNUP_BONUS,
            idempotency_key=f"signup_{new_user.id}_{secrets.token_urlsafe(8)}"
        )
        db.add(signup_transaction)

        db.commit()
        db.refresh(new_user)

    except IntegrityError as e:
        #someone else registered between check and db commit
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed. Username or email may be taken. Please try again."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed. Please try again."
        )
    
    access_token = TokenManager.create_access_token(new_user.id)
    refresh_token = TokenManager.create_refresh_token(new_user.id)


    user_response = UserResponse(
         id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        tokens=new_user.tokens,
        created_at=new_user.created_at,
        updated_at=new_user.updated_at,
        review_count=0  
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_SECONDS * 60, 
        user=user_response
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    '''
    TODO: Add rate limiting with redis 
    '''

    #case insensitive
    user = db.query(User).filter(
        (User.username == credentials.username_or_email) |
        (User.email == credentials.username_or_email)
    ).first()

    #prevents enum attacks ;), generic for user not found and wrong pw
    auth_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    if not user:
        # still run pw hash, prevents timing attacks 
        PasswordManager.verify_password(
            credentials.password,
            "$212.dummy.hash.to.maintain.constant.time.operation.for.hashing.pws"
        )
        raise auth_error
    if not PasswordManager.verify_password(credentials.password, user.password_hash):
        raise auth_error
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivaed. I would say contact support but we dont have any. So create a new one"
        )
        
    access_token = TokenManager.create_access_token(user.id)
    refresh_token = TokenManager.create_refresh_token(user.id)

    review_count = len(user.reviews) if user.reviews else 0

    user_response = UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        tokens=user.tokens,
        created_at=user.created_at,
        updated_at=user.updated_at,
        review_count=review_count
    )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=user_response
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    '''
    Refresh Token Endpoint for when access (15 min) token expires but refresh(7 days) is active
    '''

    payload = TokenManager.verify_token(refresh_token, token_type="refresh")
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate" : "Bearer"}
        )
    
    try:
        user_id = int(payload.get("sub"))
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated"
        )
    
    review_count = len(user.reviews) if user.reviews else 0
    new_access_token = TokenManager.create_access_token(user.id)

    user_response = UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        tokens=user.tokens,
        created_at=user.created_at,
        updated_at=user.updated_at,
        review_count=review_count
    )
    
    #still using same 7 day token here 
    return TokenResponse(
        access_token= new_access_token,
        refresh_token=refresh_token,  
        token_type="Bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=user_response
    )


