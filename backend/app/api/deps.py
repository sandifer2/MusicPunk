from typing import Optional, Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import TokenManager
from app.models.user import User

security = HTTPBearer() #OAuth2.0 standard token form Auth: Bearer <token>

async def get_current_user(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
        db: Annotated[Session, Depends(get_db)]) -> User:
    '''
    need to look back on this an understand deeper
     Dependency that extracts and validates the JWT from request headers.
    This is THE CORE of your auth - it runs on every protected endpoint.
    
    Flow:
    1. FastAPI extracts "Authorization: Bearer <token>" header
    2. We verify the token signature and expiration
    3. We fetch the user from database
    4. We return the user object for the endpoint to use
    '''
    token = credentials.credentials
    payload = TokenManager.verify_token(token, token_type="access")

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        user_id = int(payload.get("sub"))
    except(TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive User"
        )
    
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]

async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db) ) -> Optional[User]:
    '''
    Optional Auth, returns user or None
    for endpoints for anonymous and auth users w/ diff behavior ie browse songs
    maybe implement maybe not
    '''
    if not credentials:
        return None
    
    try:
        return await get_current_user(credentials, db)
    except HTTPException:
        # invalid token
        return None
    
OptionalUser = Annotated[Optional[User], Depends(get_current_user_optional)]

async def get_current_active_user(current_user: CurrentUser) -> User:
    '''
    additional checkpoint for active user if extra verification is needed
    Depenency Chaining: outcome of one task depends on success of another
    '''
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user


async def get_admin_user(current_user: CurrentUser) -> User:
    '''TODO: Implement later for admin dashboard'''
    pass
    
# TODO: Implement rate limiting with Redis

        

