import math
from playwright.sync_api import Playwright, sync_playwright
from bs4 import BeautifulSoup
from openpyxl import Workbook, load_workbook
import os
import pandas as pd
from datetime import datetime

# Variables
EMAIL = "groovewgana@gmail.com"
PASSWORD = "HiG@na2024"
url = "https://www.linkedin.com/login"
role = "Senior Data Analyst"
location = "United States"
all_job_ids = []
filename = "LinkedInJobs.xlsx"

def applyJobs(page):
   print("Applying for jobs by reading url from excel")

def dupe_remove(filename):
   # Getting filepath of the workbook
   cwd = os.getcwd()
   filepath = os.path.join(cwd, filename)
   print("File path:", filepath)

   # Create DataFrame from the Excel file
   df = pd.read_excel(filepath)

   # Remove duplicates and reset the index
   df.drop_duplicates(inplace=True)
   df.reset_index(drop=True, inplace=True)

   # Print the updated DataFrame and its count
   print("Updated DataFrame after removing duplicates:")
   print(df.to_string())

   # Write the updated DataFrame back to the Excel file
   df.to_excel(filepath, index=False)
   print("Updated data has been saved to the Excel file.")

def write_to_excel():
   """
    Writes extracted job IDs and related data into an Excel sheet.
   """
   # print(all_job_ids)
   # print(len(all_job_ids))
   sheet_name = "JobData"

   #Check if file already exists
   if os.path.exists(filename):
      workbook = load_workbook(filename)
      sheet = workbook.active  # Access the default sheet
      print("File exists already")
   else:
      #Create a new workboook
      workbook = Workbook()
      # Rename the default first sheet to 'JobData'
      sheet = workbook.active  # Access the default sheet
      sheet.title = "JobData"
      #Columns to be added
      sheet.append(["Job ID","Job URL", "Date","HR ID", "Applied Status"])

   # # Check if the sheet exists, otherwise create it
   # if sheet_name in workbook.sheetnames:
   #    sheet = workbook[sheet_name]

   today_date = datetime.today().strftime('%Y-%m-%d')

   #Writing into the sheet
   for job_id in all_job_ids:
      joburl = f"https://www.linkedin.com/jobs/view/{job_id}"
      sheet.append([job_id,joburl,today_date,None,None])

   #save the workbook
   workbook.save(filename)
   #print(f"Saved {filename}")
   dupe_remove(filename)

def extract_job_ids(page):
   #Code for extracting job ids-
   paginated_url = page.url
   print(f"Paginated URL : {paginated_url}")
   page.goto(paginated_url)
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

      # Extract and print job IDs
      for job in job_items:
         job_ids = job.get('data-occludable-job-id')
         #print(job_ids)
         all_job_ids.append(job_ids)

   except Exception as e:
      print(f"Error while fetching job_ids: {e}")
      return

   #Print the total number of job ids extracted for the given user inputs
   # print(f"Total extracted job IDs: {len(all_job_ids)}")
   # for job_id in all_job_ids:
   #    print(job_id)

def extract_jobs(page) -> None:
   """
   Extract job links from the current page and print them.
   :param page: Playwright Page object
   """
   #print("Extracting jobs into an Excel sheet")

   #target_url = page.url+"&start={}"
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

   #Code for hitting each page url:
   print("Hitting each url attempt")

   #wait for buttons to load
   #page.wait_for_selector("li[data-test-pagination-page-btn]", timeout=5000)

   buttons = page.locator("ul.jobs-search-pagination__pages li.jobs-search-pagination__indicator button")
   tot_buttons = buttons.count()
   print("Total Number of pages extracted: ",tot_buttons)
   url_list = []
   if tot_buttons != number_of_pages : #and number_of_pages<=1
      print("No Match")
   else: print("Math Matches")

   if tot_buttons > 1:
      for i in range(tot_buttons):
         try:
            print(f"Opening Paginated button in new window {i + 1}")

            # Click the button
            buttons.nth(i).click()

            # Wait for content to load (adjust selector for your use case)
            page.wait_for_timeout(5000)
            #page.wait_for_selector("div.jobs-search-results-list", timeout=5000)
            # Print current page information
            current_page = page.locator("div.jobs-search-pagination").inner_text()
            print(f"Currently on: {page.url}")

            # Extract jobs on the new page
            extract_job_ids(page)

         except Exception as e:
            print(f"Error clicking button {i + 1}: {e}")

   elif number_of_pages == 1:
      extract_job_ids(page)


   write_to_excel()
   applyJobs(page)

def job_search(page, role, location):
   navbar = page.get_by_label("Global Navigation")
   navbar.is_visible()

   job_icon = page.get_by_role("link", name="Jobs", exact=True)
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
   page.wait_for_timeout(5000)
   date_option = page.get_by_text("Past 24 hours", exact=True)
   date_option.click()
   page.wait_for_timeout(5000)
   show_jobs = page.get_by_role("button", name="Apply current filter to show")
   show_jobs.click()
   print('Date Filter Applied')
   page.wait_for_timeout(5000)

   # Check if "No matching jobs found." message appears
   check = page.get_by_text("No matching jobs found.")
   if check.count() > 0:
      print("No Jobs found for the given constraints of role, location, and time of posting")
      return

   easy_apply = page.get_by_label("Easy Apply filter.")
   easy_apply.click()
   print('Easy Apply Clicked')
   page.wait_for_timeout(5000)

   # Check if "No matching jobs found." message appears
   check = page.get_by_text("No matching jobs found.")
   if check.count() > 0:
      print("No Jobs found for the given constraints of role, location, and time of posting")
      return

   extract_jobs(page)

def open_browser(playwright: Playwright, url: str):
   browser = playwright.chromium.launch(headless=False)
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

