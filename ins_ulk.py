from patchright.sync_api import sync_playwright
import time

def login_instagram(username, password):
    with sync_playwright() as p:
        try:
            # Launch browser
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            
            # Navigate to Instagram
            page.goto("https://www.instagram.com")
            
            # Wait for the login form to be visible
            page.wait_for_selector('input[name="username"]')
            
            # Fill in login credentials
            page.fill('input[name="username"]', username)
            page.fill('input[name="password"]', password)
            
            # Click login button
            page.click('button[type="submit"]')
            
            # Wait for navigation after login
            page.wait_for_load_state('networkidle')
            
            # Handle 'Save login info' dialog
            try:
                page.get_by_role("button", name="Not now").click(timeout=5000)
                print("Clicked 'Not now' on save login info dialog.")
            except Exception:
                print("'Save login info' dialog did not appear or could not be clicked.")
            
            # Handle 'Turn on notifications' dialog
            try:
                page.get_by_role("button", name="Not Now").click(timeout=5000)
                print("Clicked 'Not Now' on turn on notifications dialog.")
            except Exception:
                print("'Turn on notifications' dialog did not appear or could not be clicked.")
            
            # Check if login was successful
            if "instagram.com" in page.url:
                print("Login successful!")
                time.sleep(3)  # Wait for page to settle

                # Click on the 'More' button to open the menu
                print("Clicking on 'More' button...")
                page.locator("text=More").last.click()
                page.wait_for_load_state('networkidle')

                # Click on 'Settings' from the menu
                print("Clicking on 'Settings'...")
                page.locator('a:has-text("Settings")').click()
                page.wait_for_load_state('networkidle')

                # After menu opens, click 'Your activity'
                print("Clicking on 'Your activity'...")
                page.get_by_text("Your activity").click()

            else:
                print("Login failed. Please check your credentials.")
            
            # Debug: Screenshot dan print URL setelah login
            page.screenshot(path='after_login.png')
            print('Current URL:', page.url)
            
            # Wait for a moment to see the result
            time.sleep(5)
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        
        finally:
            # Close browser
            browser.close()

if __name__ == "__main__":
    # Replace these with your Instagram credentials
    USERNAME = "example_instagram_username"
    PASSWORD = "example_instagram_password"
    
    login_instagram(USERNAME, PASSWORD)

