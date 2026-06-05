import re
from playwright.sync_api import Playwright, sync_playwright, expect


def test_run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://playwright.dev/python/")
    page.get_by_role("button", name="Python").click()
    page.get_by_label("Main", exact=True).get_by_role("link", name="Python", exact=True).click()
    page.get_by_role("link", name="Get started").click()
    page.get_by_role("link", name="How to install Playwright").click()
    page.get_by_role("link", name="Actions").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    test_run(playwright)
