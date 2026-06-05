import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright


@pytest.fixture(scope="session")
def browser_context_args():
    """Configure browser context arguments"""
    return {
        "viewport": {"width": 1280, "height": 720},
        "ignore_https_errors": True,
    }


@pytest.fixture(scope="session")
def playwright():
    """Start Playwright"""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright: Playwright):
    """Launch browser"""
    browser = playwright.chromium.launch(headless=False, slow_mo=500)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser, browser_context_args):
    """Create a new browser context for each test"""
    context = browser.new_context(**browser_context_args)
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext):
    """Create a new page for each test"""
    page = context.new_page()
    yield page
    page.close()
