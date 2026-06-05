from playwright.sync_api import sync_playwright

def take_screenshot():
    # Launch Chromium browser
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navigate to the website
        print("Navigating to page...")
        page.goto("https://www.saucedemo.com/")
        
        # 1. Standard viewport screenshot
        page.screenshot(path="standard_view.png")
        print("Saved standard viewport screenshot.")
        
         # Target an element using a CSS selector
        element = page.locator('[data-test="username"]')
        element.screenshot(path="userName_only.png")
        # Masks specified locators with a pink/magenta box by default
        page.screenshot(
            path="masked_page.png", 
            mask=[page.locator('[data-test="password"]')]
        )

        # 2. Full-page screenshot (captures scrolled content)
        page.screenshot(path="full_page.png", full_page=True)
        print("Saved full-page screenshot.")
        
        # Clean up
        browser.close()
 
   
if __name__ == "__main__":
    take_screenshot()