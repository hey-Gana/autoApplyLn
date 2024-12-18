# Import libraries
from playwright.sync_api import sync_playwright, expect, Page

# Variables
EMAIL = "groovewgana@gmail.com"
PASSWORD = "HiG@na2024"

def hitUrl(page:Page,EMAIL, PASSWORD):
    page.goto("https://www.linkedin.com/login")
    print(EMAIL,PASSWORD)


if __name__ == "__main__":
    hitUrl(EMAIL,PASSWORD)






# def login(page, email, password):
#     # Navigate to LinkedIn login page
#     page.goto("https://www.linkedin.com/login")
#
#     # Wait for the email input to be visible and fill it
#     email_input = page.get_by_label('Email or phone')
#     expect(email_input).to_be_visible()
#     email_input.fill(email)
#
#     # Wait for the password input to be visible and fill it
#     password_input = page.get_by_label('Password')
#     expect(password_input).to_be_visible()
#     password_input.fill(password)
#
#     # Click the login button
#     login_button = page.get_by_role('button', name='Sign in')
#     expect(login_button).to_be_visible()
#     login_button.click()
#
#     # Optionally, verify successful login by checking the presence of a specific element
#     # For example, check if the profile avatar is visible
#     try:
#         page.wait_for_selector('img.profile-rail-card__image', timeout=10000)
#         print("Login successful!")
#     except:
#         print("Login failed or took too long.")
#
# def main():
#     with sync_playwright() as p:
#         # Launch the browser (you can set headless=False to see the browser actions)
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context()
#         page = context.new_page()
#
#         # Perform login
#         login(page, EMAIL, PASSWORD)
#
#         # Keep the browser open for a while to see the result (optional)
#         page.wait_for_timeout(5000)  # Wait for 5 seconds
#
#         # Close browser
#         # context.close()
#         # browser.close()
#
# if __name__ == "__main__":
#     main()
