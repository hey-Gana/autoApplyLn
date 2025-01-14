import math
from playwright.sync_api import Playwright, sync_playwright
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from bs4 import BeautifulSoup

# Variables
EMAIL = "groovewgana@gmail.com"
PASSWORD = "HiG@na2024"
url = "https://www.linkedin.com/login"
role = "Data Analyst"
location = "United States"
params_to_remove = ["currentJobId" , "distance", "geoId"]

def extract_jobs(page) -> None:
   """
   Extract job links from the current page and print them.
   :param page: Playwright Page object
   """
   all_job_ids =[]
   print("Extracting jobs into an Excel sheet")

   # Parse the URL -splits it into its different components such as scheme , netloc , path, params, query etc
   parsed_url = urlparse(page.url)

   # Parse the query parameters into a dictionary - parse_qs gives a dictionary of key:value pair of all the query components
   #Eg: "currentJobID":"331092309", "keywords": "Data Analyst" etc.
   #Removes the & in query component
   query_params = parse_qs(parsed_url.query)

   # Remove specified parameters
   for param in params_to_remove:
      query_params.pop(param, None)

   # Reconstruct the query string
   updated_query = urlencode(query_params, doseq=True)

   # Reconstruct the URL with the updated query string
   updated_url = urlunparse(
      (
         parsed_url.scheme,
         parsed_url.netloc,
         parsed_url.path,
         parsed_url.params,
         updated_query,
         parsed_url.fragment,
      )
   )

   target_url = updated_url+"&start={}"
   #print(f"Target URL: {target_url}")

   # Get the number of jobs from the page
   try:
      text = page.locator("small span").inner_text()
      number_of_jobs_filtered = int(text.split(" ")[0])  # e.g., '647 results' -> 647
      print(f"Number of jobs filtered: {number_of_jobs_filtered}")
   except Exception as e:
      print(f"Error while fetching the number of jobs: {e}")
      return


   number_of_pages = math.ceil(number_of_jobs_filtered/25)
   print(f"Number of pages : {number_of_pages}")

   for i in range (number_of_pages):
      paginated_url = target_url.format(i*25)
      print(f"Paginated URL : {paginated_url}")
      page.goto(target_url)
      print("In Paginated URL")
      #Page load time
      page.wait_for_timeout(10000)
      # Wait for the job list container to load
      page.wait_for_selector('div.scaffold-layout__list', timeout=10000)
      # Get job ids of jobs listed in the current page
      try:
         html_response = page.content()
         soup = BeautifulSoup(html_response, 'html.parser')

         # Select job items using a stable structure
         job_items = soup.find_all('li', attrs={'data-occludable-job-id': True})

         if not job_items:
            print("No jobs found on the current page.")
            continue

         # Extract and print job IDs
         for job in job_items:
            job_ids = job.get('data-occludable-job-id')
            print(job_ids)

         # print(f"Extracted {len(job_ids)} job IDs.")
         # for job_id in job_ids:
         #    print(job_id)

         all_job_ids.append(job_ids)

      except Exception as e:
         print(f"Error while fetching job_ids: {e}")
         return

   print(f"Total extracted job IDs: {len(all_job_ids)}")
   for job_id in all_job_ids:
      print(job_id)


def apply_jobs(page):
   print("Applying for jobs")

def job_search(page, role, location):
   navbar = page.get_by_label("Global Navigation")
   navbar.is_visible()

   job_icon = page.get_by_role("link", name="Jobs")
   job_icon.is_visible()
   job_icon.click()
   print('Clicked on Jobs icon')
   page.wait_for_timeout(2000)

   role_search = page.get_by_role("combobox", name="Search by title, skill, or")
   role_search.fill(role)
   print('Role filled')
   page.wait_for_timeout(2000)
   loc_search = page.get_by_role("combobox", name="City, state, or zip code")
   loc_search.fill(location)
   click_loc_search = page.get_by_label("Global Navigation").get_by_text(location, exact=True)
   click_loc_search.click()
   print('Location filled')
   page.wait_for_timeout(2000)

   job_posting_date = page.get_by_label("Date posted filter. Clicking")
   job_posting_date.click()
   date_option = page.get_by_text("Past 24 hours", exact=True)
   date_option.click()
   page.wait_for_timeout(5000)
   show_jobs = page.get_by_role("button", name="Apply current filter to show")
   show_jobs.click()
   print('Date Filter Applied')
   page.wait_for_timeout(5000)

   easy_apply = page.get_by_label("Easy Apply filter.")
   easy_apply.click()
   print('Easy Apply Clicked')
   page.wait_for_timeout(5000)

   extract_jobs(page)

def open_browser(playwright: Playwright, url: str):
   browser = playwright.chromium.launch(headless=True)
   page = browser.new_page(viewport={'width': 1600, 'height': 900})

   try:
      page.goto(url)
      page.wait_for_timeout(1000)

      email_input = page.get_by_label('Email or phone')
      email_input.fill(EMAIL)

      password_input = page.get_by_label('Password')
      password_input.fill(PASSWORD)

      checkbox = page.get_by_text("Keep me logged in")
      checkbox.click()

      login_button = page.locator('button.btn__primary--large[type="submit"]')
      login_button.click()

      page.wait_for_timeout(5000)
      print("Login successful!!!")

      job_search(page, role, location)

   except Exception as e:
      print(f'Error occurred: {e}')

   finally:
      browser.close()

def main():
   with sync_playwright() as playwright:
      open_browser(
         playwright=playwright,
         url=url
      )

if __name__ == '__main__':
   main()
