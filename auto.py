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
import asyncio, requests, pandas as pd
import math

from playwright.async_api import Page, Playwright, Response, async_playwright
from bs4 import BeautifulSoup

# Variables
EMAIL = "groovewgana@gmail.com"
PASSWORD = "HiG@na2024"
url = "https://www.linkedin.com/login"
role="Data Analyst"
location = "United States"

# async def extract_jobs(page: Page) -> None:
#    print("Extracting jobs into an excel sheet")
#    #print(page.url)
#    target_url = page.url
#
#    # Get the number of jobs from the page
#    try:
#       text = await page.locator("small span").inner_text()
#       number_of_jobs_filtered = int(text.split(" ")[0])  # eg: '647 results' -> 647
#       print(f"Number of jobs filtered: {number_of_jobs_filtered}")
#    except Exception as e:
#       print(f"Error while fetching number of jobs: {e}")
#       return
#
#    html_response = await page.content()
#    soup = BeautifulSoup(html_response, 'html.parser')
#
#
# # Find all <a> tags which contain links
#    links = soup.find_all("a", href=True)
#
#    # Extract the href attribute from each <a> tag
#    for link in links:
#       all_links = [link.get('href')]
#       if "/jobs/view/" in link['href']:
#          job_links.append(link['href'])
#
#
#    print(all_links)
#    print("Length: ", len(all_links) )
#    print(job_links)

# # Store the HTML response
   # response_html = await page.content()
   #
   # # Parse the response with BeautifulSoup
   # soup = BeautifulSoup(response_html, "html.parser")
   #
   # # Extract job cards
   # jobs = []
   # job_cards = soup.find_all("div", class_="ember-view")
   # print(f"Found {len(job_cards)} job cards.")
   #
   # for job_card in job_cards:
   #    try:
   #       # Extract job details
   #       job_title = job_card.find("h3", class_="base-search-card__title").get_text(strip=True)
   #       print("jobs_title: "+job_title)
   #       company_name = job_card.find("h4", class_="base-search-card__subtitle").get_text(strip=True)
   #       print("jobs_subtitle: "+ company_name)
   #       location = job_card.find("span", class_="job-search-card__location").get_text(strip=True)
   #       print("jobs_loc: "+location)
   #       job_url = job_card.find("a", class_="base-card__full-link")["href"]
   #       print("jobs_url: "+job_url)
   #
   #       jobs.append({
   #          "Job Title": job_title,
   #          "Company": company_name,
   #          "Location": location,
   #          "Job URL": job_url
   #       })
   #    except Exception as e:
   #       print(f"Error parsing job card: {e}")
   #
   #    if jobs:
   #       df = pd.DataFrame(jobs)
   #       df.to_excel("linkedin_jobs_response_data.xlsx", index=False, engine="openpyxl")
   #       print("Job data saved to linkedin_jobs_response_data.xlsx")
   #    else:
   #       print("No job data found.")
   #
   #
   # print(jobs)
   # # Calculate the number of pages to iterate over
   # loops = math.ceil(number_of_jobs_filtered / 25)
   # print(f"Total pages to process: {loops}")
   #
   #
   # # Initialize a list to store job IDs
   # job_ids = []
   #
   # for i in range(loops):
   #    try:
   #       # Format the URL for pagination
   #       paginated_url = target_url.format(i)
   #       print(f"Fetching page: {paginated_url}")
   #
   #       # Make the GET request to fetch data
   #       res = requests.get(paginated_url)
   #
   #       if res.status_code != 200:
   #          print(f"Failed to fetch data for page {i}, status code: {res.status_code}")
   #          continue
   #
   #       # Parse the HTML response
   #       soup = BeautifulSoup(res.text, 'html.parser')
   #
   #       # Find all job items
   #       all_jobs_on_this_page = soup.find_all("li")
   #       for job in all_jobs_on_this_page:
   #          try:
   #             jobid = job.find("div", {"class": "base-card"}).get('data-entity-urn').split(":")[3]
   #             job_ids.append(jobid)
   #          except Exception as inner_e:
   #             print(f"Error extracting job ID on page {i}: {inner_e}")
   #             continue
   #
   #    except Exception as e:
   #       print(f"Error processing page {i}: {e}")
   #       continue
   #
   # print("Extracted Job IDs:")
   # print(job_ids)

async def extract_jobs(page: Page) -> None:
   """
   Extract job links from the current page and print them.

   :param page: Playwright Page object
   """
   print("Extracting jobs into an Excel sheet")
   target_url = page.url
   print(f"Target URL: {target_url}")

   # Get the number of jobs from the page
   try:
      text = await page.locator("small span").inner_text()
      number_of_jobs_filtered = int(text.split(" ")[0])  # e.g., '647 results' -> 647
      print(f"Number of jobs filtered: {number_of_jobs_filtered}")
   except Exception as e:
      print(f"Error while fetching the number of jobs: {e}")
      return

   # Get the page content
   try:
      html_response = await page.content()
      soup = BeautifulSoup(html_response, 'html.parser')
   #    # Find all <a> tags which contain links
   #    links = soup.find_all("a", href=True)
   #    job_links = []
   #
   #    print("# of Links in page: ", len(links))
   #    for link in links:
   #       print(link)
   #
   #    # Filter job links
   #    for link in links:
   #       href = link.get('href')
   #       if "/jobs/view/" in href:
   #          job_links.append(href)
   #
   #    # Print job links and their count
   #    print(f"Extracted {len(job_links)} job links:")
   #    for job_link in job_links:
   #       print(job_link)
   #


      #Finds element on web page where the job cards are mentioned
      elements = soup.find('div', {'class': 'scaffold-layout__list', 'tabindex': '-1'})
      # Extract href links from the elements
      href_links = []
      for element in elements:
         links = element.find_all('a', href=True)  # Find all <a> tags with href attribute
         for link in links:
            href_links.extend(link['href'])

      print(len(href_links))
      for i in range(len(href_links)):
         print(href_links[i])

   except Exception as e:
      print(f"Error while extracting job links: {e}")

#document.querySelectorAll('ul.rjmNTMLkNvPwnJnFTCybgSFpgYGQ li')

#document.querySelector("li#ember440 a[href]")

# steps to do:
# Parse the html response and extract the list items under the unordered list
# Find the ids
# For each id, extract the href

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
   await asyncio.sleep(2)

   #Search for specified role and location
   role_search = page.get_by_role("combobox", name="Search by title, skill, or")
   await role_search.fill(role)
   print('Role filled')
   await asyncio.sleep(2)
   loc_search = page.get_by_role("combobox", name="City, state, or zip code")
   await loc_search.fill(location)
   click_loc_search = page.get_by_label("Global Navigation").get_by_text(location, exact=True)
   await click_loc_search.click()
   print('Location filled')
   await asyncio.sleep(2)

   #Search filter for date
   job_posting_date = page.get_by_label("Date posted filter. Clicking")
   await job_posting_date.click()
   date_option = page.get_by_text("Past 24 hours", exact=True)
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





