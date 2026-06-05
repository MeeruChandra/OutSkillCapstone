from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserCreate, UserResponse, Token
from services import UserService
from auth import AuthService, TokenService, get_current_active_user
from logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    logger.info(f"Registration request received for username: {user_data.username}")
    try:
        user_service = UserService(db)
        user = user_service.create_user(user_data)
        logger.info(f"User registered successfully: {user_data.username}")
        return user
    except HTTPException as e:
        logger.warning(f"Registration failed for {user_data.username}: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during registration for {user_data.username}: {str(e)}", exc_info=True)
        raise


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login and receive JWT token"""
    logger.info(f"Login request received for username: {form_data.username}")
    try:
        auth_service = AuthService(db)
        user = auth_service.authenticate_user(form_data.username, form_data.password)

        if not user:
            logger.warning(f"Login failed for username: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = TokenService.create_access_token(data={"sub": user.username})
        logger.info(f"User logged in successfully: {form_data.username}")
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during login for {form_data.username}: {str(e)}", exc_info=True)
        raise


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user = Depends(get_current_active_user)):
    """Get current user information"""
    logger.debug(f"User info request for: {current_user.username}")
    return current_user
