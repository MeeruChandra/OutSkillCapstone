"""
Test cases for authentication module.
Tests the authenticate_user method with various scenarios.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from models import User
from auth import AuthService, PasswordHasher


# Test database setup (in-memory SQLite)
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Create a fresh database session for each test.
    Sets up tables before test and tears down after.
    """
    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Create session
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_user(db_session):
    """
    Create a test user with username 'standard_user' and password 'pass123'.
    """
    password_hasher = PasswordHasher()
    hashed_password = password_hasher.get_password_hash("pass123")

    user = User(
        username="standard_user",
        email="standard_user@test.com",
        hashed_password=hashed_password,
        first_name="Standard",
        last_name="User",
        is_active=True
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


@pytest.fixture(scope="function")
def auth_service(db_session):
    """
    Create an AuthService instance with test database session.
    """
    return AuthService(db_session)


class TestAuthenticateUser:
    """Test suite for authenticate_user method"""

    def test_authenticate_user_success(self, auth_service, test_user):
        """
        Test successful authentication with correct username and password.
        """
        # Arrange
        username = "standard_user"
        password = "pass123"

        # Act
        authenticated_user = auth_service.authenticate_user(username, password)

        # Assert
        assert authenticated_user is not None
        assert authenticated_user.username == username
        assert authenticated_user.email == "standard_user@test.com"
        assert authenticated_user.is_active is True

    def test_authenticate_user_wrong_password(self, auth_service, test_user):
        """
        Test authentication fails with incorrect password.
        """
        # Arrange
        username = "standard_user"
        wrong_password = "wrongpassword"

        # Act
        authenticated_user = auth_service.authenticate_user(username, wrong_password)

        # Assert
        assert authenticated_user is None

    def test_authenticate_user_nonexistent_username(self, auth_service, test_user):
        """
        Test authentication fails with non-existent username.
        """
        # Arrange
        username = "nonexistent_user"
        password = "pass123"

        # Act
        authenticated_user = auth_service.authenticate_user(username, password)

        # Assert
        assert authenticated_user is None

    def test_authenticate_user_empty_password(self, auth_service, test_user):
        """
        Test authentication fails with empty password.
        """
        # Arrange
        username = "standard_user"
        password = ""

        # Act
        authenticated_user = auth_service.authenticate_user(username, password)

        # Assert
        assert authenticated_user is None

    def test_authenticate_user_empty_username(self, auth_service, db_session):
        """
        Test authentication fails with empty username.
        """
        # Arrange
        username = ""
        password = "pass123"

        # Act
        authenticated_user = auth_service.authenticate_user(username, password)

        # Assert
        assert authenticated_user is None

    def test_authenticate_user_case_sensitive_username(self, auth_service, test_user):
        """
        Test authentication is case-sensitive for username.
        """
        # Arrange
        username = "STANDARD_USER"  # Different case
        password = "pass123"

        # Act
        authenticated_user = auth_service.authenticate_user(username, password)

        # Assert
        assert authenticated_user is None

    def test_authenticate_user_returns_correct_user_object(self, auth_service, test_user):
        """
        Test that authenticate_user returns a User object with all expected attributes.
        """
        # Arrange
        username = "standard_user"
        password = "pass123"

        # Act
        authenticated_user = auth_service.authenticate_user(username, password)

        # Assert
        assert isinstance(authenticated_user, User)
        assert authenticated_user.id is not None
        assert authenticated_user.username == "standard_user"
        assert authenticated_user.email == "standard_user@test.com"
        assert authenticated_user.first_name == "Standard"
        assert authenticated_user.last_name == "User"
        assert authenticated_user.is_active is True
        assert authenticated_user.hashed_password is not None
        assert authenticated_user.created_at is not None

    def test_authenticate_inactive_user(self, auth_service, db_session):
        """
        Test authentication of an inactive user (should still authenticate but is_active=False).
        """
        # Arrange - Create inactive user
        password_hasher = PasswordHasher()
        hashed_password = password_hasher.get_password_hash("pass123")

        inactive_user = User(
            username="inactive_user",
            email="inactive@test.com",
            hashed_password=hashed_password,
            is_active=False
        )

        db_session.add(inactive_user)
        db_session.commit()

        # Act
        authenticated_user = auth_service.authenticate_user("inactive_user", "pass123")

        # Assert
        assert authenticated_user is not None
        assert authenticated_user.is_active is False

    def test_authenticate_user_with_special_characters_in_password(self, auth_service, db_session):
        """
        Test authentication with special characters in password.
        """
        # Arrange - Create user with special character password
        password_hasher = PasswordHasher()
        special_password = "p@ss!123#$%"
        hashed_password = password_hasher.get_password_hash(special_password)

        user = User(
            username="special_user",
            email="special@test.com",
            hashed_password=hashed_password,
            is_active=True
        )

        db_session.add(user)
        db_session.commit()

        # Act
        authenticated_user = auth_service.authenticate_user("special_user", special_password)

        # Assert
        assert authenticated_user is not None
        assert authenticated_user.username == "special_user"
