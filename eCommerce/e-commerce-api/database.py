from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import get_settings
from logger import get_logger

logger = get_logger(__name__)
settings = get_settings()

# Create database engine
logger.info(f"Initializing database engine with URL: {settings.database_url}")
try:
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False}  # Needed for SQLite
    )
    logger.info("Database engine created successfully")
except Exception as e:
    logger.error(f"Failed to create database engine: {str(e)}", exc_info=True)
    raise

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
logger.info("Database session factory configured")

# Create Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency injection for database session.
    Follows Dependency Inversion Principle.
    """
    logger.debug("Creating database session")
    db = SessionLocal()
    try:
        yield db
        logger.debug("Database session completed successfully")
    except Exception as e:
        logger.error(f"Database session error: {str(e)}", exc_info=True)
        raise
    finally:
        db.close()
        logger.debug("Database session closed")
