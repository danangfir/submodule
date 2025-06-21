import asyncio
from camoufox.async_api import AsyncCamoufox
from browserforge.fingerprints import Screen

async def login_instagram(username, password):
    async with AsyncCamoufox() as browser:
        try:
            # Launch browser and create page
            page = await browser.new_page()
            
            # Navigate to Instagram
            await page.goto("https://www.instagram.com")
            
            # Wait for the login form to be visible
            await page.wait_for_selector('input[name="username"]')
            
            # Fill in login credentials
            await page.fill('input[name="username"]', username)
            await page.fill('input[name="password"]', password)
            
            # Click login button
            await page.click('button[type="submit"]')
            
            # Wait for navigation after login
            await page.wait_for_load_state('networkidle')
            
            # Handle 'Save login info' dialog
            try:
                await page.get_by_role("button", name="Not now").click(timeout=5000)
                print("Clicked 'Not now' on save login info dialog.")
            except Exception:
                print("'Save login info' dialog did not appear or could not be clicked.")
            
            # Handle 'Turn on notifications' dialog
            try:
                await page.get_by_role("button", name="Not Now").click(timeout=5000)
                print("Clicked 'Not Now' on turn on notifications dialog.")
            except Exception:
                print("'Turn on notifications' dialog did not appear or could not be clicked.")
            
            # Check if login was successful
            if "instagram.com" in page.url:
                print("Login successful!")
                await asyncio.sleep(3)  # Wait for page to settle

                # Click on the 'More' button to open the menu
                print("Clicking on 'More' button...")
                await page.locator("text=More").last.click()
                await page.wait_for_load_state('networkidle')

                # Click on 'Settings' from the menu
                print("Clicking on 'Settings'...")
                await page.locator('a:has-text("Settings")').click()
                await page.wait_for_load_state('networkidle')

                # After menu opens, click 'Your activity'
                print("Clicking on 'Your activity'...")
                await page.get_by_text("Your activity").click()

            else:
                print("Login failed. Please check your credentials.")
            
            # Debug: Screenshot dan print URL setelah login
            await page.screenshot(path='after_login.png')
            print('Current URL:', page.url)
            
            # Wait for a moment to see the result
            await asyncio.sleep(5)
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")

async def main():
    # Replace these with your Instagram credentials
    USERNAME = "dgfr111"
    PASSWORD = "dancok26"
    
    await login_instagram(USERNAME, PASSWORD)

if __name__ == "__main__":
    asyncio.run(main())
    