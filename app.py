import math
from playwright.sync_api import Playwright, sync_playwright

# Variables
EMAIL = "groovewgana@gmail.com"
PASSWORD = "HiG@na2024"
url = "https://www.linkedin.com/login"
role = "Data Analyst"
location = "United States"

def extract_jobs(page):
    all_job_ids = []
    print("Extracting jobs into an Excel sheet")
    page_url = page.url
    print(f"Page URL: {page_url}")
    target_url = page_url + "&start={}"

    try:
        text = page.locator("small span").inner_text()
        number_of_jobs_filtered = int(text.split(" ")[0])  # Fixed: split and take first element
        print(f"Number of jobs filtered: {number_of_jobs_filtered}")
    except Exception as e:
        print(f"Error while fetching number of jobs: {e}")
        return

    number_of_pages = math.ceil(number_of_jobs_filtered / 25)
    print(f"Number of pages: {number_of_pages}")

    for i in range(number_of_pages):
        paginated_url = target_url.format(i * 25)
        print(f"Visiting: {paginated_url}")
        page.goto(paginated_url)
        page.wait_for_selector('div.scaffold-layout__list-container', timeout=30000)

        # Scroll to the bottom of the page to trigger dynamic loading
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(5000)

        try:
            job_items = page.query_selector_all('div.scaffold-layout__list-container li.jobs-search-results__list-item')

            if not job_items:
                print(f"No jobs found on page {i + 1}.")
                continue

            job_ids = [job.get_attribute('data-occludable-job-id') for job in job_items]
            print(f"Extracted {len(job_ids)} job IDs from page {i + 1}.")

            all_job_ids.extend(job_ids)

        except Exception as e:
            print(f"Error while fetching job IDs on page {i + 1}: {e}")
            continue

    print(f"Total extracted job IDs: {len(all_job_ids)}")
    for job_id in all_job_ids:
        print(job_id)

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

def main():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.set_viewport_size({"width": 1600, "height": 900})

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

if __name__ == '__main__':
    main()
