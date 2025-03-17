# LinkedIn Job Auto Apply Script

## Overview
AutoApplyLn is an automation tool designed to simplify job applications on LinkedIn. This project uses **Node.js** for the backend and **Python** for automation scripting.<br>
This Python script automates the process of easy-applying for jobs on LinkedIn using Playwright and BeautifulSoup.<br>
It allows users to filter job postings based on criteria - role, location, and posting date, and then easy apply to jobs that meet their preferences.<br>
It also scrapes the jobs and associated recruiter information[linkedin profile] to enable its users to grow their network while applying for jobs automatically.<br>
All job application data and reports are stored in an Excel file, `linkedinjobs.xlsx`, which includes recruiter details, application status, and the dates when jobs were scraped and applied.<br>
The Excel file gets updated at the end of the script execution.<br>

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
- Node.JS installed (if not installed, download Node.js from [here](https://nodejs.org/en))
- NPM installed (`npm install`)

## Installation and Setup

- **Step 1: Clone the Repository**<br>
Open a terminal or command prompt and cd to the directory where you would like to clone this repository to. Then run:
```sh
git clone https://github.com/hey-Gana/autoApplyLn.git
```
Navigate into the Repository: Change your directory into the project directory.
```sh
cd autoApplyLn
```
- **Step 2: Install Dependencies**<br>
Verify Node.js, npm, python and pip are installed and running.
```sh
node -v
npm -v
python3 --version
pip3 --version
```
After confirming their installation, install Node.js dependencies:
```sh
npm install
```
Install required python libraries:
```sh
pip3 install -r requirements.txt
```
- **Step 3: Run the Application**<br>
- Start the Node.js application:
```sh
node app.js
```
### **Step 4: Run the Automation Script (Optional)**
To manually trigger the automation script:<br>
1. Create a file: config.py and store values of your details:
```sh
# Config file generated from form submission
fname = "First Name"
lname = "Last Name"
email = "Email Address"
pw = "Password"
role = "Role you wish to apply for"
loc = "Location you wish to apply in"
yoe = "Years Of Experience in the role you are applying"
resume = "Resume_name.pdf"
head = True or False [True - run without browser head runner; False - run with a browser runner]
```
2. Copy the resume file into the directory of the app.js. Ensure the resume variable in config.py file matches the name of the resume copied to this directory.
3. Manually trigger the automation script:
```sh
python3 auto.py
```
<br><br>
The application should now be running at: 
```sh
http://127.0.0.1:3000
```

## Future Feature Developments 

- **Cover Letter & Resume Customization**: Auto-generate cover letters based on job descriptions.
- **Enhanced Tracking Dashboard**: Provide a GUI dashboard to track applications visually. Dashboard information would provide insight on location(city) where most jobs are listed, highest salary paying locations, % match of job roles with resume etc.
- **Expand functionality to all job portals**: Extend auto apply feature to other job portals such as Indeed, Glassdoor, Monster, SimplyHired etc.


