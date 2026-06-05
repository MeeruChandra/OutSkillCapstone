# E-Commerce API Tests

This directory contains test cases for the e-commerce API.

## Test Structure

- `test_auth.py` - Authentication tests including the `authenticate_user` method

## Running Tests

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run all tests
```bash
pytest
```

### Run specific test file
```bash
pytest tests/test_auth.py
```

### Run specific test
```bash
pytest tests/test_auth.py::TestAuthenticateUser::test_authenticate_user_success
```

### Run with verbose output
```bash
pytest -v
```

### Run with coverage
```bash
pytest --cov=. --cov-report=html
```

## Test Coverage

The `test_auth.py` file includes the following test scenarios:

1. **test_authenticate_user_success** - Valid username (`standard_user`) and password (`pass123`)
2. **test_authenticate_user_wrong_password** - Correct username but wrong password
3. **test_authenticate_user_nonexistent_username** - Non-existent username
4. **test_authenticate_user_empty_password** - Empty password string
5. **test_authenticate_user_empty_username** - Empty username string
6. **test_authenticate_user_case_sensitive_username** - Case sensitivity test
7. **test_authenticate_user_returns_correct_user_object** - Validates User object structure
8. **test_authenticate_inactive_user** - Authentication with inactive user
9. **test_authenticate_user_with_special_characters_in_password** - Special characters in password

## Test Fixtures

- `db_session` - Creates an in-memory SQLite database for each test
- `test_user` - Creates a test user with username `standard_user` and password `pass123`
- `auth_service` - Creates an AuthService instance with test database session
