from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import secrets
import bcrypt
import jwt
from jwt.exceptions import InvalidTokenError
from app.core.config import settings

class PasswordManager:
    '''
    handles hashing and verification w/ bcrypt
    '''
    @staticmethod
    def hash_password(password: str) -> str:
        '''
        hash/salt with bcrpt
        pw -> bytes -> add salt -> hash w/salt -> return 64 encoded pw
        '''
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt(rounds=settings.BCRYPT_ROUNDS)
        hashed = bcrypt.hashpw(password_bytes, salt)

        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')

        return bcrypt.checkpw(password_bytes, hashed_bytes)
    
class TokenManager:
    '''
    Handles JWT tokens
    JWT Structure: header.payload.signature
    - Header: {"alg": "HS256", "typ": "JWT"}
    - Payload: {"sub": user_id, "exp": expiry, ...}
    - Signature: HMACSHA256(header + payload, secret)
    '''

    @staticmethod
    def create_access_token(user_id: int) -> str:
        '''
        short lived token for API access
        ref JWT standard token claims
        '''
        now = datetime.now(timezone.utc)
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        payload = {
            "sub": str(user_id),
            "exp": expire,
            "iat": now,
            "type": "access",
            "jti": secrets.token_urlsafe(16)
        }

        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
    
    @staticmethod
    def create_refresh_token(user_id: int) -> str:
        '''
        create long exp token to retrieve new access token
        store in httpOnly cookies, can be ss revoked(check against db), prevents token confusion
        '''
        now = datetime.now(timezone.utc)
        expire = now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        payload = {
            "sub": str(user_id),
            "exp": expire,
            "iat": now,
            "type": "refresh",
            "jti": secrets.token_urlsafe(16)
        }

        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm= settings.ALGORITHM
        )
    
    @staticmethod
    def verify_token(token: str, token_type: str = "access") -> Optional[Dict[str, Any]]:
        '''
        verify and decode jwt token
        security checks: signation verification, expiration, token type, algortithm 
        '''
        try: 
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )

            if payload.get("type") != token_type:
                return None
            
            return payload
        except InvalidTokenError as e:
            '''all jwt error'''
            return None
        
    @staticmethod
    def extract_user_id(token: str) -> Optional[int]:
        '''WARNING: only use for non security critical operations, use verify_token for auth'''
        payload = TokenManager.verify_token(token)
        if payload:
            try:
                return int(payload.get("sub"))
            except(TypeError, ValueError):
                return None
        return None
    
class SecurityUtils:
    '''security helper fns'''
    @staticmethod
    def generate_secure_token(length: int=32) -> str:
        '''
        crypt. secure random token for:
        pw reset, email verif, API key, session ids
        '''
        return secrets.token_urlsafe(length)
    

    @staticmethod 
    def is_strong_password(password: str) -> tuple[bool, str]:
        '''
        OWASP Reqs:
        - 8 chars
        - 1 upper and 1 lower
        - 1 number
        - 1 special
        '''
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        
        if not any(c.isupper() for c in password):
            return False, "Password must contain uppercase letter"
        
        if not any(c.islower() for c in password):
            return False, "Password must contain lowercase letter"
        
        if not any(c.isdigit() for c in password):
            return False, "Password must contain number"
        
        special_chars = "!@#$%^&*(),.?:{}|<>"
        if not any(c in special_chars for c in password):
            return False, "Password must contain special character"
        
        return True, "Password is strong"
