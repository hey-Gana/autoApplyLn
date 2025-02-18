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
role = "ceo"
location = "United States"
all_job_ids = []
filename = "LinkedInJobs.xlsx"

"""Questions to ask user"""
#Years of experience - by default 1
yoe = 1
#Do you need sponsorship - by default: No
ans = "No"


def fill_form(page):
    labels = page.locator("label[for]").all()  # Get all labels with a "for" attribute

    for label in labels:
        input_id = label.get_attribute("for")  # Get the associated input field ID
        if input_id:
            input_element = page.locator(f"xpath=//*[@id='{input_id}']")

            try:
                input_type = input_element.get_attribute("type")
                tag_name = input_element.evaluate("(el) => el.tagName.toLowerCase()")  # Get tag name

                if input_type == "text":
                    input_element.fill("1")  # Fill text fields with "1"
                    print(f"Filled '{label.inner_text().strip()}' with '1'")

                elif input_type == "radio":
                    option = input_element.locator("input[value='Yes']")
                    if option.count() > 0:
                        option.first.check()  # Select "Yes" if available
                        print(f"Selected 'Yes' for '{label.inner_text().strip()}'")
                    else:
                        print(f"Skipped '{label.inner_text().strip()}' (No 'Yes' option)")

                elif tag_name == "select":
                    try:
                        input_element.select_option("Yes")  # Try selecting "Yes"
                        print(f"Selected 'Yes' for '{label.inner_text().strip()}'")
                    except:
                        print(f"Skipped '{label.inner_text().strip()}' (Option 'Yes' not found)")

            except Exception as e:
                print(f"Skipped '{label.inner_text().strip()}' due to error: {e}")

# def extract_questions(page):
#     # Get all labels with a "for" attribute
#     labels = page.locator("label[for]").all()
#
#     text_questions = []
#     radio_questions = []
#     dropdown_questions = []
#
#     for label in labels:
#         input_id = label.get_attribute("for")  # Get the "for" attribute
#         if input_id:
#             # Locate the corresponding input element
#             input_element = page.locator(f"xpath=//*[@id='{input_id}']")
#             input_type = input_element.get_attribute("type")
#
#             question = label.inner_text().strip()  # Extract the question text
#
#             # Categorize based on input type
#             if input_type == "text":
#                 text_questions.append(question)
#             elif input_type == "radio":
#                 radio_questions.append(question)
#             elif input_element.evaluate("(el) => el.tagName.toLowerCase()") == "select":
#                 dropdown_questions.append(question)  # Check if it's a dropdown (select element)
#
#     # Print extracted questions
#     print("\nText Input Questions:")
#     for q in text_questions:
#         print("-", q)
#
#     print("\nRadio Button Questions:")
#     for q in radio_questions:
#         print("-", q)
#
#     print("\nDropdown Questions:")
#     for q in dropdown_questions:
#         print("-", q)


def applyJobs(page,filename):
    print("In Applying for jobs by reading from excel")
    #reading job url from excel and storing in an array
    # cwd = os.getcwd()
    # filepath = os.path.join(cwd,"/","chk.pdf")
    # print("File path:", filepath)

    workbook = load_workbook(filename)
    worksheet = workbook.active
    job_id_url = []
    for i,row in enumerate(worksheet):
        if i == 0: #Skips Column Heading
            continue
        url = row[1].value
        job_id_url.append(url)
    # print("_____JOB URLS FROM EXCEL______")
    # print(job_id_url)
    # count =0
    # for job in job_id_url:
    #     count+=1
    # print(count)

    #Hitting each page
    # for job in job_id_url:
    #     page.goto(job)
    #     print(f"In page url:{job}")
    #     page.wait_for_timeout(3000)

    #opening a page and applying
    page.goto("https://www.linkedin.com/jobs/view/4157818530 ")
    #wait for page to load
    page.wait_for_timeout(5000)
    recruiter = page.get_by_role("heading", name="Meet the hiring team").is_visible()
    if recruiter is True:
        print("Recruiter is present")
    else:
        print("No recruiter")

    #resume path
    rname = "/Users/ganapathisubramaniam/GIT Backup/Projects/gwg_autoApplyLn/autoApplyLn/chk1.pdf"

    #Clicking on the Easy Apply button
    try:
        # Index starts at 0
        easyApply = page.locator('button[aria-label^="Easy Apply to"]').nth(1)
        easyApply.scroll_into_view_if_needed()
        easyApply.click()
        page.wait_for_timeout(5000)

        dialog_box = page.get_by_role("heading", name="Contact info").is_visible()
        if dialog_box is True:

            print("opened the dialog box")
            page.get_by_label("Mobile phone number").fill("0000001")
            page.get_by_label("Continue to next step").click()

            #This didnt work as the upload dialog box was not closing, hence used filechooser method from playwright
            # page.locator("label").filter(has_text="Upload resume")
            # # #print(f"filepath: {filepath}")
            # ck = page.locator("label").filter(has_text="Upload resume").click()
            # ck.set_input_files(rname)

            with page.expect_file_chooser() as fc_info:
                page.locator("label").filter(has_text="Upload resume").click()  # Click upload button
            file_chooser = fc_info.value  # Capture the file chooser event
            file_chooser.set_files(rname)  # Set the file for upload
            print("Resume uploaded successfully")
            page.wait_for_timeout(5000)
            page.get_by_label("Continue to next step").click()

            page.wait_for_timeout(5000)
            #extract_questions(page)
            fill_form(page)


        else:
            print("Error in opening the dialog box after clicking on Easy Apply Button.")
        page.wait_for_timeout(5000)
    except Exception as e:
        print(f"Error due to {e}")
        return


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

    # buttons = page.locator("li[data-test-pagination-page-btn]")
    # tot_buttons = buttons.count()
    # print(tot_buttons)
    # url_list = []
    # if tot_buttons != number_of_pages : #and number_of_pages<=1
    #     print("No Match")
    # else: print("Math Matches")
    # if tot_buttons>1:
    #     for i in range(0,tot_buttons):
    #         try:
    #             print(f"Opening Paginated button in new window {i+1}")
    #             # Click the button
    #             buttons.nth(i).click()
    #             # Wait for content to load (adjust selector for your use case)
    #             page.wait_for_timeout(5000)
    #             #page.wait_for_selector("div.jobs-search-results-list", timeout=5000)
    #             # Print current page information
    #             current_page = page.locator("div.jobs-search-pagination").inner_text()
    #             print(f"Currently on: {current_page}")
    #             print(page.url)
    #             #extract_job_ids(page)
    #
    #         except Exception as e:
    #             print(f"Error clicking button {i + 1}: {e}")
    #
    # elif number_of_pages==1:
    #     #extract_job_ids(page)
    #     print("Chill")
    #
    # #write_to_excel()
    applyJobs(page,filename)

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

        job_icon = page.get_by_role("link", name="Jobs", exact=True)
        job_icon.is_visible()
        job_icon.click()
        print('Clicked on Jobs icon')
        page.wait_for_timeout(2000)

        applyJobs(page,filename)

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



