import asyncio
import re
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
            
            # Navigate to Your Activity -> Likes to unlike posts
            print("Navigating to Your Activity > Likes...")
            # Using get_by_text is a reliable way to find these navigation elements
            await page.get_by_text("More").last.click()
            await page.wait_for_timeout(1000) # Wait for the menu to appear
            await page.get_by_text("Your activity").last.click()
            await page.wait_for_load_state("networkidle")
            
            # Click "Select" to enter bulk action mode
            await page.get_by_text("Select").last.click()
            await page.wait_for_load_state("networkidle")
            print("In bulk selection mode.")

            # Select all visible items on the page
            checkboxes = page.locator('div[aria-label="Toggle checkbox"]')
            count = await checkboxes.count()
            
            if count > 0:
                print(f"Found {count} items to unlike.")
                for i in range(count):
                    await checkboxes.nth(i).click()
                    # A small delay to mimic human behavior
                    await asyncio.sleep(0.3) 

                print("All items selected. Clicking 'Unlike'.")
                # The 'Unlike' button at the bottom has dynamic text (e.g., "45 selected Unlike").
                # We use a regular expression to match it reliably.
                await page.get_by_role("button", name=re.compile(r"selected Unlike")).click()
                await page.wait_for_timeout(1000) # Give the confirmation dialog time to appear

                # Now, click the "Unlike" button inside the confirmation dialog.
                # Scoping the search to the dialog makes it unambiguous.
                await page.get_by_role("dialog").get_by_role("button", name="Unlike").click()
                print(f"Successfully unliked {count} items.")
            else:
                print("No liked items found to select.")

            # Wait a moment to observe the result before the script ends
            await asyncio.sleep(5)

        except Exception as e:
            print(f"An error occurred: {e}")

async def main():
    # Replace these with your Instagram credentials
    USERNAME = "dgfr111"
    PASSWORD = "dancok26"
    
    await login_instagram(USERNAME, PASSWORD)

if __name__ == "__main__":
    asyncio.run(main())
    