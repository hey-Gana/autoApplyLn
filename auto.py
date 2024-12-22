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
import asyncio, requests
import math

from playwright.async_api import Page, Playwright, Response, async_playwright
from bs4 import BeautifulSoup

# Variables
EMAIL = "groovewgana@gmail.com"
PASSWORD = "HiG@na2024"
url = "https://www.linkedin.com/login"
role="Data Analyst"
location = "United States"

async def extract_jobs(page: Page) -> None:
   print("Extracting jobs into an excel sheet")
   #print(page.url)
   target_url = page.url

   text = await page.locator("small span").inner_text()
   #print(text)

   #Splitting text into result and converting its type to integer
   #eg: 647 results ---> 647
   number_of_jobs_filtered = int(text.split(" ")[0])
   print(number_of_jobs_filtered)

   loops = math.ceil(number_of_jobs_filtered/25)

   for i in range(0,loops):
      #Invoking the get request for API to get the response after hitting the target_url
      res = requests.get(target_url.format(i))
      #parses the html response from the get request
      soup = BeautifulSoup(res.text,'html.parser')
      #Extracts all the <li> elements
      alljobs_on_this_page=soup.find_all("li")
      print(alljobs_on_this_page)



   soup=BeautifulSoup(res.text,'html.parser')
   alljobs_on_this_page=soup.find_all("li")

   for x in range(0,len(alljobs_on_this_page)):
      jobid = alljobs_on_this_page[x].find("div",{"class":"base-card"}).get('data-entity-urn').split(":")[3]
      l.append(jobid)


async def apply_jobs(page: Page) -> None:
   print("Applying for jobs")
   #print(page.url)


async def job_search(page: Page, role: str, location: str) -> None:
   #Verify Navbar is loaded and jobs icon is visible
   navbar = page.get_by_label("Global Navigation")
   await navbar.is_visible()
   job_icon = page.get_by_role("link", name="Jobs")
   await job_icon.is_visible()

   # Click on the "Jobs" icon
   await job_icon.click()
   print('Clicked on Jobs icon')
   await asyncio.sleep(5)

   #Search for specified role and location
   role_search = page.get_by_role("combobox", name="Search by title, skill, or")
   await role_search.fill(role)
   print('Role filled')
   await asyncio.sleep(5)
   loc_search = page.get_by_role("combobox", name="City, state, or zip code")
   await loc_search.fill(location)
   click_loc_search = page.get_by_label("Global Navigation").get_by_text(location, exact=True)
   await click_loc_search.click()
   print('Location filled')
   await asyncio.sleep(5)

   #Search filter for date
   job_posting_date = page.get_by_label("Date posted filter. Clicking")
   await job_posting_date.click()
   date_option = page.get_by_text("Past week", exact=True)
   await date_option.click()
   await asyncio.sleep(5)
   show_jobs = page.get_by_role("button", name="Apply current filter to show")
   await show_jobs.click()
   print('Date Filter Applied')
   await asyncio.sleep(5)

   #Easy Apply Option
   easy_apply = page.get_by_label("Easy Apply filter.")
   await easy_apply.click()
   print('Easy Apply Clicked')
   await asyncio.sleep(5)

   #Extract job listings
   await extract_jobs(page)

   # #Apply for job
   # await apply_jobs(page)

async def open_browser(playwright: Playwright, url: str)-> None:
   #opening browser in UI Visible mode
   browser = await playwright.chromium.launch(headless=True)

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

      #Unchecking remember me
      checkbox = page.get_by_text("Keep me logged in")
      await checkbox.click()
      #checkbox = page.locator("input#rememberMeOptIn-checkbox")
      # if await checkbox.is_checked():
      #    await checkbox.set_checked(False)
      #await asyncio.sleep(10)

      # Click the login button
      login_button = page.locator('button.btn__primary--large[type="submit"]')
      #expect(login_button).to_be_visible()
      await login_button.click()

      await asyncio.sleep(5)
      print("Login successful!!!")

      # #If asked for verification pin
      # if(page.locator('#input__email_verification_pin').is_visible()==True):
      #    #Entering verification code
      #    verification_code_input = page.locator('#input__email_verification_pin')
      #    user_input = input("Enter the verification code: ")
      #    await verification_code_input.fill(user_input)
      #
      #    #Submitting verification
      #    submit_button = page.locator('#email-pin-submit-button')
      #    await submit_button.click()
      # else:
      #    print(f'No code required')

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
         url=url
      )

if __name__ == '__main__':
   asyncio.run(main())





