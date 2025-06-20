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
            
            # Check if login was successful
            if page.url == "https://www.instagram.com/":
                print("Login successful!")
                time.sleep(2)  # Tambah delay agar sidebar pasti muncul
                page.wait_for_selector('svg[aria-label="Menu"]')
                page.click('svg[aria-label="Menu"]')
            else:
                print("Login failed. Please check your credentials.")
            
            # Debug: Screenshot dan print URL setelah login
            page.screenshot(path='after_login.png')
            print('Current URL:', page.url)
            
            # Klik ikon menu/settings terlebih dahulu
            page.wait_for_selector('svg[aria-label="Settings"]')
            page.click('svg[aria-label="Settings"]')
            
            # Setelah menu terbuka, klik 'Your activity'
            page.wait_for_selector('span:has-text("Your activity")')
            page.click('span:has-text("Your activity")')
            
            # Wait for a moment to see the result
            time.sleep(5)
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        
        finally:
            # Close browser
            browser.close()

if __name__ == "__main__":
    # Replace these with your Instagram credentials
    USERNAME = "dgfr111"
    PASSWORD = "dancok26"
    
    login_instagram(USERNAME, PASSWORD)

