# from playwright.sync_api import Playwright, sync_playwright
#
# def run(playwright: Playwright, *, url: str) -> dict:
#     browser = playwright.chromium.launch(headless=False)
#     page = browser.new_page()
#     page.set_viewport_size({"width": 1600, "height": 900})  # Set the viewport size
#     page.goto(url)
#     title = page.title()  # Retrieve the page's title
#     browser.close()  # Ensure the browser is closed
#     return {'url': url, 'title': title}
#
# def main() -> None:
#     # Use sync_playwright context manager to close the Playwright instance automatically
#     with sync_playwright() as playwright:
#         result = run(playwright, url='https://www.google.com')
#         print(result)
#
# if __name__ == '__main__':
#     main()
#
#
#
import asyncio
from playwright.async_api import Page, Playwright, Response, async_playwright

# Variables
EMAIL = "groovewgana@gmail.com"
PASSWORD = "HiG@na2024"
url = "https://www.linkedin.com/login"
role="Data Analyst"
location = "United States"

async def job_search(page: Page, role: str, location: str) -> None:
   # Click on the "Jobs" icon
   jobs_icon = page.locator('a.global-nav__primary-link[href*="jobs"]')
   await jobs_icon.click()
   print('Clicked on Jobs icon')
   await asyncio.sleep(5)

   #Search for specified role and location
   role_search = page.get_by_label('Search by title, skill, or company')
   await role_search.fill(role)
   print('role filled')
   await asyncio.sleep(5)


async def open_browser(playwright: Playwright, url: str)-> None:
   #opening browser in UI Visible mode
   browser = await playwright.chromium.launch(headless=False)

   #opening a new browser page
   page = await browser.new_page(viewport={'width': 1600, 'height': 900})

   try:
      #opening the url in the browser page
      await page.goto(url)

      await asyncio.sleep(1)

      # Wait for the email input to be visible and fill it
      email_input = page.get_by_label('Email or phone')
      #expect(email_input).to_be_visible()
      await email_input.fill(EMAIL)

      # Wait for the password input to be visible and fill it
      password_input = page.get_by_label('Password')
      #expect(password_input).to_be_visible()
      await password_input.fill(PASSWORD)

      # #Unchecking remember me
      # checkbox = page.locator('input#rememberMeOptIn-checkbox')
      # await checkbox.set_checked(False)
      # await asyncio.sleep(10)

      # Click the login button
      login_button = page.locator('button.btn__primary--large[type="submit"]')
      #expect(login_button).to_be_visible()
      await login_button.click()

      # await asyncio.sleep(10)

      if(page.locator('#input__email_verification_pin').is_visible()==True):
         #Entering verification code
         verification_code_input = page.locator('#input__email_verification_pin')
         user_input = input("Enter the verification code: ")
         await verification_code_input.fill(user_input)

         #Submitting verification
         submit_button = page.locator('#email-pin-submit-button')
         await submit_button.click()
      else:
         print(f'No code required')

      await asyncio.sleep(10)

      # Proceed to job search after login
      await job_search(page, role, location)

   except Exception as e:
      print(f'Error occured: {e}')

   finally:
      #Closing broswer session
      await browser.close()



async def main() -> None:
   async with async_playwright() as playwright:
      await open_browser(
         playwright=playwright,
         url=url,
      )

if __name__ == '__main__':
   asyncio.run(main())





