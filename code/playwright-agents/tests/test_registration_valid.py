import time
import pytest
from playwright.sync_api import Page, expect


class TestUserRegistration:
    """User Registration Test Suite"""

    def test_successful_registration_with_valid_data(self, page: Page):
        """
        Test Case 1.1 - Successful Registration with Valid Data

        Objective: Verify that a new user can register successfully with valid information

        Expected Result:
        - User is successfully registered
        - Redirected to account overview page or success confirmation
        - Welcome message displayed
        """

        # 1. Navigate to https://parabank.parasoft.com/parabank/register.htm
        page.goto("https://parabank.parasoft.com/parabank/register.htm")

        # Generate unique username to avoid duplicates
        timestamp = str(int(time.time()))
        unique_username = f"johndoe{timestamp}"

        # 2. Fill in all required fields

        # First Name: "John"
        page.fill('input[id="customer.firstName"]', "John")

        # Last Name: "Doe"
        page.fill('input[id="customer.lastName"]', "Doe")

        # Address: "123 Main Street"
        page.fill('input[id="customer.address.street"]', "123 Main Street")

        # City: "New York"
        page.fill('input[id="customer.address.city"]', "New York")

        # State: "NY"
        page.fill('input[id="customer.address.state"]', "NY")

        # Zip Code: "10001"
        page.fill('input[id="customer.address.zipCode"]', "10001")

        # Phone: "555-1234"
        page.fill('input[id="customer.phoneNumber"]', "555-1234")

        # SSN: "123-45-6789"
        page.fill('input[id="customer.ssn"]', "123-45-6789")

        # Username: Generate a unique username
        page.fill('input[id="customer.username"]', unique_username)

        # Password: "SecurePass123"
        page.fill('input[id="customer.password"]', "SecurePass123")

        # Confirm: "SecurePass123"
        page.fill('input[id="repeatedPassword"]', "SecurePass123")

        # 3. Click "Register" button
        page.click('input[value="Register"]')

        # Expected Result: User is successfully registered
        # Wait for navigation to complete
        page.wait_for_load_state("networkidle")

        # Verify welcome message is displayed
        expect(page.locator("h1.title")).to_contain_text("Welcome")

        # Verify we're on the account page (success confirmation)
        # The page should show "Your account was created successfully"
        expect(page.locator("text=Your account was created successfully")).to_be_visible()

        # Verify the username is displayed in the welcome message
        expect(page.locator(f"text={unique_username}")).to_be_visible()

        print(f"Test passed! User '{unique_username}' was successfully registered.")
