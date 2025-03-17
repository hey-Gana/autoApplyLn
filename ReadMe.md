# LinkedIn Job Auto Apply Script

## Overview

This Python script automates the process of easy-applying for jobs on LinkedIn using Playwright and BeautifulSoup. It allows users to filter job postings based on criteria like role, location, and posting date, and then apply to jobs that meet their preferences.

## Features

- **Automated LinkedIn login**: Uses stored credentials for automatic authentication.
- **Job Filtering**: Filters job postings based on predefined criteria.
- **Auto Apply**: Clicks the 'Easy Apply' button on matching job postings.
- **Data Extraction**: Extracts job details for tracking purposes.
- **Application Tracking**: Generates a report of applied jobs and HR contacts.

## Prerequisites

Before running the script, ensure you have the following:

- Python 3.8+
- Playwright installed (`pip install playwright`)
- BeautifulSoup (`pip install beautifulsoup4`)
- A LinkedIn account with relevant job preferences set
- Playwright browsers installed (`playwright install`)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/linkedin-auto-apply.git
   cd linkedin-auto-apply
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install Playwright browsers:
   ```bash
   playwright install
   ```


## Usage

1. Open `auto.py` and set up your LinkedIn credentials and job preferences.
2. Run the script:
   ```bash
   python auto.py
   ```
3. The script will log in, search for jobs, apply, and store applied job details.

## Function Explanations

### `login_to_linkedin(page)`

- Logs into LinkedIn using stored credentials.
- Navigates to the login page and fills in username and password.

## Feature Development in Progress

- **Resume Upload Support**: Enable users to upload different resumes for different job roles.
- **Cover Letter Customization**: Auto-generate cover letters based on job descriptions.
- **Multi-Account Support**: Allow job applications from multiple LinkedIn accounts.
- **Enhanced Tracking Dashboard**: Provide a GUI to track applications visually.

