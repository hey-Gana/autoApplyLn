# LinkedIn Job Auto Apply Script

## Overview

This Python script automates the process of easy-applying for jobs on LinkedIn using Playwright and BeautifulSoup. It allows users to filter job postings based on criteria - role, location, and posting date, and then easy apply to jobs that meet their preferences.

## Features Implemented

- **Automated LinkedIn login**: Uses stored credentials for automatic authentication.
- **Job Filtering**: Filters job postings based on predefined criteria of the user.
- **Resume Upload Support**: Enable users to upload different resumes for different job roles.
- **Auto Apply**: Clicks the 'Easy Apply' button on matching job postings and applies for the jobs listed.
- **Data Extraction**: Extracts job details and processes them for tracking purposes.
- **Application Tracking**: Generates a report of applied jobs and HR contacts which assists users to expand their network and improve chances of getting hired. 
- **Data Security and Privacy**: Since the application is hosted in local server, user's data will not be uploaded or leaked in the internet.

## Prerequisites

Before running the script, ensure you have the following:

- Python 3.8+
- Playwright installed (`pip install playwright`)
- BeautifulSoup (`pip install beautifulsoup4`)
- A LinkedIn account 
- Playwright browsers installed (`playwright install`)

## Future Feature Developments 

- **Cover Letter & Resume Customization**: Auto-generate cover letters based on job descriptions.
- **Enhanced Tracking Dashboard**: Provide a GUI dashboard to track applications visually. Dashboard information would provide insight on location(city) where most jobs are listed, highest salary paying locations, % match of job roles with resume etc.

