from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from pwdlib import PasswordHash
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import TokenData
from config import get_settings
from logger import get_logger

logger = get_logger(__name__)
settings = get_settings()

# Password hashing context
pwd_context = PasswordHash.recommended()
logger.info("Password hashing context initialized")

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")
logger.info("OAuth2 authentication scheme configured")


class PasswordHasher:
    """
    Password hashing service following Single Responsibility Principle.
    Handles only password hashing and verification.
    """

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        try:
            result = pwd_context.verify(plain_password, hashed_password)
            logger.debug(f"Password verification result: {result}")
            return result
        except Exception as e:
            logger.error(f"Password verification failed: {str(e)}", exc_info=True)
            return False

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a password"""
        try:
            hashed = pwd_context.hash(password)
            logger.debug("Password hashed successfully")
            return hashed
        except Exception as e:
            logger.error(f"Password hashing failed: {str(e)}", exc_info=True)
            raise


class TokenService:
    """
    JWT token service following Single Responsibility Principle.
    Handles token creation and validation.
    """

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        try:
            to_encode = data.copy()
            if expires_delta:
                expire = datetime.utcnow() + expires_delta
            else:
                expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)

            to_encode.update({"exp": expire})
            encoded_jwt = jwt.encode(
                to_encode,
                settings.secret_key,
                algorithm=settings.algorithm
            )
            logger.info(f"Access token created for user: {data.get('sub')}")
            logger.debug(f"Token expires at: {expire}")
            return encoded_jwt
        except Exception as e:
            logger.error(f"Failed to create access token: {str(e)}", exc_info=True)
            raise

    @staticmethod
    def decode_access_token(token: str) -> TokenData:
        """Decode and validate JWT token"""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token,
                settings.secret_key,
                algorithms=[settings.algorithm]
            )
            username: str = payload.get("sub")
            if username is None:
                logger.warning("Token payload missing 'sub' field")
                raise credentials_exception
            logger.debug(f"Token decoded successfully for user: {username}")
            return TokenData(username=username)
        except JWTError as e:
            logger.warning(f"JWT validation failed: {str(e)}")
            raise credentials_exception
        except Exception as e:
            logger.error(f"Unexpected error decoding token: {str(e)}", exc_info=True)
            raise credentials_exception


class AuthService:
    """
    Authentication service following Single Responsibility Principle.
    Handles user authentication logic.
    """

    def __init__(self, db: Session):
        self.db = db
        self.password_hasher = PasswordHasher()

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate user with username and password"""
        logger.info(f"Authentication attempt for user: {username}")
        try:
            user = self.db.query(User).filter(User.username == username).first()
            if not user:
                logger.warning(f"Authentication failed: User '{username}' not found")
                return None
            if not self.password_hasher.verify_password(password, user.hashed_password):
                logger.warning(f"Authentication failed: Invalid password for user '{username}'")
                return None
            logger.info(f"User '{username}' authenticated successfully")
            return user
        except Exception as e:
            logger.error(f"Authentication error for user '{username}': {str(e)}", exc_info=True)
            return None

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        try:
            logger.debug(f"Fetching user by username: {username}")
            user = self.db.query(User).filter(User.username == username).first()
            if user:
                logger.debug(f"User '{username}' found")
            else:
                logger.debug(f"User '{username}' not found")
            return user
        except Exception as e:
            logger.error(f"Error fetching user '{username}': {str(e)}", exc_info=True)
            return None


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get current authenticated user.
    Follows Dependency Inversion Principle.
    """
    logger.debug("Validating current user from token")
    try:
        token_data = TokenService.decode_access_token(token)
        auth_service = AuthService(db)
        user = auth_service.get_user_by_username(username=token_data.username)

        if user is None:
            logger.warning(f"User not found for token username: {token_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        logger.debug(f"Current user validated: {user.username}")
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error validating current user: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to get current active user.
    Follows Open/Closed Principle - extends get_current_user without modifying it.
    """
    logger.debug(f"Checking if user '{current_user.username}' is active")
    if not current_user.is_active:
        logger.warning(f"Inactive user attempted access: {current_user.username}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    logger.debug(f"Active user validated: {current_user.username}")
    return current_user


if __name__ == "__main__":
    # Example usage for testing purposes
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    # Create a test database session
    engine = create_engine("sqlite:///./ecommerce.db")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    auth_service = AuthService(db)

    # Test password hashing and verification
    password = "testpassword"
    hashed_password = auth_service.password_hasher.get_password_hash(password)
    assert auth_service.password_hasher.verify_password(password, hashed_password)

    # Test token creation and decoding
    token_data = {"sub": "testuser"}
    token = TokenService.create_access_token(data=token_data)
    decoded_data = TokenService.decode_access_token(token)
    assert decoded_data.username == "testuser"

    logger.info("All tests passed successfully")