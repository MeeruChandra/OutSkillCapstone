# ParaBank Test Plan - Basic Operations

## Application Overview

**ParaBank** is a demonstration online banking application developed by Parasoft for testing purposes. It simulates a complete banking platform with both web interface and web service APIs (SOAP/REST).

### Key Features
- User registration and authentication
- Account management
- Fund transfers
- Bill payment
- Transaction history
- ATM services (withdraw, deposit, balance inquiry)

---

## Test Plan Scope

This test plan covers **basic operations** including:
1. User Registration
2. User Login/Logout
3. Account Overview
4. Fund Transfers
5. Bill Payment
6. Account History
7. Navigation and UI Elements

---

## Test Environment

- **Application URL**: https://parabank.parasoft.com/parabank/index.htm
- **Browsers**: Chrome, Firefox, Edge, Safari
- **Test Data**: Mock user accounts and transaction data
- **Test Type**: Functional, UI, End-to-End

---

## Test Suites

### Suite 1: User Registration

#### Test Case 1.1 - Successful Registration with Valid Data
**Objective**: Verify that a new user can register successfully with valid information

**Preconditions**: User is not already registered

**Test Steps**:
1. Navigate to https://parabank.parasoft.com/parabank/register.htm
2. Fill in all required fields:
   - First Name: "John"
   - Last Name: "Doe"
   - Address: "123 Main Street"
   - City: "New York"
   - State: "NY"
   - Zip Code: "10001"
   - Phone: "555-1234"
   - SSN: "123-45-6789"
   - Username: "johndoe123"
   - Password: "SecurePass123"
   - Confirm: "SecurePass123"
3. Click "Register" button

**Expected Result**: 
- User is successfully registered
- Redirected to account overview page or success confirmation
- Welcome message displayed

---

#### Test Case 1.2 - Registration with Mismatched Passwords
**Objective**: Verify password confirmation validation

**Test Steps**:
1. Navigate to registration page
2. Fill all fields correctly
3. Enter "Password123" in Password field
4. Enter "Password456" in Confirm field
5. Click "Register"

**Expected Result**: 
- Error message: "Passwords do not match"
- Registration not completed
- User remains on registration page

---

#### Test Case 1.3 - Registration with Missing Required Fields
**Objective**: Verify field validation for required fields

**Test Steps**:
1. Navigate to registration page
2. Leave one or more required fields empty
3. Click "Register"

**Expected Result**: 
- Error messages displayed for empty required fields
- Registration not completed

---

#### Test Case 1.4 - Registration with Duplicate Username
**Objective**: Verify unique username enforcement

**Test Steps**:
1. Register a user with username "testuser123"
2. Attempt to register another user with same username "testuser123"

**Expected Result**: 
- Error message: "Username already exists"
- Registration not completed

---

### Suite 2: User Login and Authentication

#### Test Case 2.1 - Successful Login with Valid Credentials
**Objective**: Verify user can login with correct credentials

**Preconditions**: User account exists

**Test Steps**:
1. Navigate to https://parabank.parasoft.com/parabank/index.htm
2. Enter valid username in Username field
3. Enter valid password in Password field
4. Click "Log In" button

**Expected Result**: 
- User successfully authenticated
- Redirected to account overview page
- User's name displayed in welcome message

---

#### Test Case 2.2 - Login with Invalid Username
**Objective**: Verify login fails with incorrect username

**Test Steps**:
1. Navigate to login page
2. Enter invalid username "nonexistentuser"
3. Enter any password
4. Click "Log In"

**Expected Result**: 
- Error message: "Invalid username or password"
- User remains on login page
- Not authenticated

---

#### Test Case 2.3 - Login with Invalid Password
**Objective**: Verify login fails with incorrect password

**Test Steps**:
1. Navigate to login page
2. Enter valid username
3. Enter incorrect password
4. Click "Log In"

**Expected Result**: 
- Error message: "Invalid username or password"
- User not authenticated

---

#### Test Case 2.4 - Login with Empty Credentials
**Objective**: Verify validation for empty fields

**Test Steps**:
1. Navigate to login page
2. Leave username and password fields empty
3. Click "Log In"

**Expected Result**: 
- Error message displayed
- Login not processed

---

#### Test Case 2.5 - Logout Functionality
**Objective**: Verify user can logout successfully

**Preconditions**: User is logged in

**Test Steps**:
1. Login successfully
2. Click "Log Out" link/button

**Expected Result**: 
- User session terminated
- Redirected to login page or home page
- User cannot access account pages without re-authentication

---

### Suite 3: Account Overview

#### Test Case 3.1 - View Account Overview
**Objective**: Verify user can view account information

**Preconditions**: User is logged in with at least one account

**Test Steps**:
1. Login successfully
2. Navigate to Accounts Overview page (default landing page)

**Expected Result**: 
- All user accounts displayed
- Account numbers visible
- Account balances shown
- Account types indicated (Checking, Savings, etc.)

---

#### Test Case 3.2 - View Account Details
**Objective**: Verify user can access detailed account information

**Test Steps**:
1. Login successfully
2. Click on an account number from overview

**Expected Result**: 
- Account details page displayed
- Shows account number, type, balance
- Transaction history visible
- Available balance displayed

---

### Suite 4: Fund Transfer

#### Test Case 4.1 - Successful Fund Transfer Between Own Accounts
**Objective**: Verify funds can be transferred between user's accounts

**Preconditions**: 
- User is logged in
- User has at least 2 accounts
- Source account has sufficient balance

**Test Steps**:
1. Navigate to "Transfer Funds" page
2. Enter amount: "100.00"
3. Select source account from dropdown
4. Select destination account from dropdown
5. Click "Transfer" button

**Expected Result**: 
- Success message: "Transfer Complete" or similar
- Amount deducted from source account
- Amount added to destination account
- Transaction reflected in both account histories

---

#### Test Case 4.2 - Transfer with Insufficient Funds
**Objective**: Verify system prevents overdraft

**Test Steps**:
1. Navigate to "Transfer Funds" page
2. Enter amount greater than source account balance
3. Select source and destination accounts
4. Click "Transfer"

**Expected Result**: 
- Error message: "Insufficient funds"
- Transfer not completed
- Account balances unchanged

---

#### Test Case 4.3 - Transfer with Invalid Amount (Negative)
**Objective**: Verify validation for negative amounts

**Test Steps**:
1. Navigate to "Transfer Funds" page
2. Enter negative amount: "-50.00"
3. Select accounts
4. Click "Transfer"

**Expected Result**: 
- Error message: "Invalid amount"
- Transfer not processed

---

#### Test Case 4.4 - Transfer with Zero Amount
**Objective**: Verify validation for zero amount

**Test Steps**:
1. Navigate to "Transfer Funds" page
2. Enter amount: "0.00"
3. Select accounts
4. Click "Transfer"

**Expected Result**: 
- Error message: "Amount must be greater than zero"
- Transfer not processed

---

#### Test Case 4.5 - Transfer to Same Account
**Objective**: Verify system handles transfer to same account

**Test Steps**:
1. Navigate to "Transfer Funds" page
2. Enter valid amount
3. Select same account as both source and destination
4. Click "Transfer"

**Expected Result**: 
- Error message: "Cannot transfer to same account" OR
- Transfer completes with no net change (depending on business rules)

---

### Suite 5: Bill Payment

#### Test Case 5.1 - Successful Bill Payment
**Objective**: Verify user can pay a bill

**Preconditions**: 
- User is logged in
- Payee exists or can be added
- Account has sufficient funds

**Test Steps**:
1. Navigate to "Bill Pay" page
2. Enter payee name: "Electric Company"
3. Enter payee address information
4. Enter payee account: "ACC123456"
5. Enter amount: "150.00"
6. Select account to pay from
7. Click "Send Payment"

**Expected Result**: 
- Success message: "Bill Payment Complete"
- Amount deducted from selected account
- Payment recorded in transaction history

---

#### Test Case 5.2 - Bill Payment with Insufficient Funds
**Objective**: Verify insufficient funds validation

**Test Steps**:
1. Navigate to "Bill Pay" page
2. Enter all payee information
3. Enter amount greater than account balance
4. Click "Send Payment"

**Expected Result**: 
- Error message: "Insufficient funds"
- Payment not processed
- Balance unchanged

---

#### Test Case 5.3 - Bill Payment with Missing Payee Information
**Objective**: Verify required field validation

**Test Steps**:
1. Navigate to "Bill Pay" page
2. Leave one or more required payee fields empty
3. Enter valid amount
4. Click "Send Payment"

**Expected Result**: 
- Error messages for missing fields
- Payment not processed

---

### Suite 6: Account History and Transactions

#### Test Case 6.1 - View Complete Account History
**Objective**: Verify user can view all transactions

**Preconditions**: 
- User is logged in
- Account has transaction history

**Test Steps**:
1. Navigate to "Accounts Overview"
2. Click on account number
3. View transaction history

**Expected Result**: 
- All transactions displayed
- Shows date, description, debit/credit, balance
- Transactions in chronological order (newest first or oldest first)

---

#### Test Case 6.2 - View Transaction Details
**Objective**: Verify user can view detailed transaction information

**Test Steps**:
1. Navigate to account history
2. Click on a specific transaction

**Expected Result**: 
- Transaction details page displayed
- Shows transaction ID, date, type, amount
- Shows description and involved accounts

---

#### Test Case 6.3 - Filter Transactions by Date Range
**Objective**: Verify transaction filtering functionality

**Test Steps**:
1. Navigate to "Find Transactions" page
2. Select an account
3. Enter date range (from and to dates)
4. Click "Find Transactions"

**Expected Result**: 
- Only transactions within specified date range displayed
- Correct transaction count shown

---

#### Test Case 6.4 - Filter Transactions by Amount
**Objective**: Verify amount-based filtering

**Test Steps**:
1. Navigate to "Find Transactions" page
2. Select an account
3. Enter specific amount
4. Click "Find Transactions"

**Expected Result**: 
- Only transactions matching the amount displayed
- Results accurate

---

### Suite 7: Navigation and UI

#### Test Case 7.1 - Navigate Through All Main Menu Items
**Objective**: Verify all navigation links work correctly

**Test Steps**:
1. Login successfully
2. Click each main menu item:
   - Open New Account
   - Accounts Overview
   - Transfer Funds
   - Bill Pay
   - Find Transactions
   - Update Contact Info
   - Request Loan
   - Log Out

**Expected Result**: 
- Each page loads successfully
- No broken links
- Appropriate content displayed for each page

---

#### Test Case 7.2 - Home Link Navigation
**Objective**: Verify home link returns to main page

**Test Steps**:
1. Navigate to any internal page
2. Click "Home" link

**Expected Result**: 
- Returns to home/overview page
- No errors

---

#### Test Case 7.3 - About Us and Contact Pages
**Objective**: Verify informational pages load

**Test Steps**:
1. Click "About" link
2. Verify content loads
3. Click "Contact" link
4. Verify contact information displayed

**Expected Result**: 
- Both pages load successfully
- Content displayed correctly

---

#### Test Case 7.4 - Forgot Login Info Functionality
**Objective**: Verify password recovery process

**Test Steps**:
1. From login page, click "Forgot login info?" link
2. Enter required information
3. Submit request

**Expected Result**: 
- Password recovery page displayed
- Help information or recovery process initiated

---

#### Test Case 7.5 - Admin Page Access
**Objective**: Verify admin functionality (if accessible)

**Test Steps**:
1. Navigate to "Admin Page"
2. Attempt to access admin functions

**Expected Result**: 
- Admin page loads (if authorized)
- Appropriate access controls in place

---

## Test Data Requirements

### User Test Data
| Username | Password | First Name | Last Name | Account Type |
|----------|----------|------------|-----------|--------------|
| testuser1 | Pass123! | John | Doe | Checking + Savings |
| testuser2 | Pass456! | Jane | Smith | Checking |
| testuser3 | Pass789! | Bob | Johnson | Savings |

### Transaction Test Data
- Small transfer: $50.00
- Medium transfer: $500.00
- Large transfer: $5,000.00
- Edge cases: $0.01, $0.00, negative values

### Payee Test Data
- Electric Company
- Water Utility
- Credit Card Company

---

## Test Execution Strategy

### Priority Levels
1. **P0 (Critical)**: Login, Registration, Fund Transfer
2. **P1 (High)**: Bill Pay, Account Overview, Logout
3. **P2 (Medium)**: Transaction History, Navigation
4. **P3 (Low)**: Informational Pages, Admin Features

### Test Execution Order
1. Execute P0 tests first (smoke tests)
2. Execute P1 tests if P0 passes
3. Execute P2 and P3 tests for comprehensive coverage

### Pass/Fail Criteria
- **Pass**: All expected results match actual results
- **Fail**: Any deviation from expected results
- **Blocked**: Cannot execute due to dependencies

---

## Defect Reporting

### Defect Template
- **Defect ID**: Unique identifier
- **Test Case ID**: Reference to failed test case
- **Summary**: Brief description
- **Steps to Reproduce**: Detailed steps
- **Expected Result**: What should happen
- **Actual Result**: What actually happened
- **Severity**: Critical, High, Medium, Low
- **Priority**: P0, P1, P2, P3
- **Environment**: Browser, OS, URL
- **Attachments**: Screenshots, logs

---

## Test Deliverables

1. Test Plan Document (this document)
2. Test Case Specifications
3. Test Execution Report
4. Defect Report
5. Test Summary Report
6. Traceability Matrix

---

## Risks and Assumptions

### Risks
- Application availability/downtime
- Test data cleanup between test runs
- Session timeout during testing
- Network connectivity issues

### Assumptions
- Application is accessible at specified URL
- Test environment is stable
- User has necessary permissions
- Sample accounts can be created for testing

---

## Exit Criteria

Testing is complete when:
1. All P0 and P1 test cases executed
2. 90% of all test cases passed
3. All critical defects resolved
4. All high-priority defects reviewed and addressed
5. Test summary report approved

---

## Automation Recommendations

The following test suites are good candidates for automation:
- User Registration (Suite 1)
- User Login/Logout (Suite 2)
- Fund Transfer (Suite 4)
- Account Overview (Suite 3)

**Recommended Tools**: 
- Playwright (as available in current project)
- Selenium WebDriver
- Cypress

---

## Sign-off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Test Lead | | | |
| Project Manager | | | |
| QA Manager | | | |

---

**Document Version**: 1.0  
**Last Updated**: June 4, 2026  
**Prepared By**: QA Team
