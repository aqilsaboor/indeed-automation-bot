from seleniumbase import Driver
from HandyWrappers import HandyWrappers
import json
import os
import csv
from selenium.webdriver.common.by import By


class IndeedScrapper:
    
    def scrapper(self, job_title: str, job_location: str, total_page: int):
        
        print('Start: Job data scrapping process begins')
        
        # Initialize job title and location variables for the search URL
        Job_Title = job_title
        Job_Location = str(job_location)
        total_pages = int(total_page)

        # Format the job title and location to fit Indeed's URL structure
        Job_Title_for_link = Job_Title.replace(" ", "+")
        Job_Location_for_link = Job_Location.replace(" ", "+")
        base_url = f'https://pk.indeed.com/jobs?q={Job_Title_for_link}&l={Job_Location_for_link}&start='

        # Define CSV file name and the fieldnames for the job data
        csv_file = 'IndeedData.csv'
        fieldnames = ['Job Title', 'Location', 'Company Name', 'Pay', 'Job Type', 'Description', 'Location or Zipcode', 'href']

        # Load existing jobs from CSV to avoid duplicates during the scraping process
        existing_jobs = set()
        if os.path.exists(csv_file):
            with open(csv_file, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    existing_jobs.add((row['Job Title'], row['Company Name']))

        # Open the CSV file in append mode to add new jobs
        with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            # Write CSV headers if the file is new or empty
            if os.path.getsize(csv_file) == 0:
                writer.writeheader()

            # Iterate through the specified number of pages for job listings
            for page in range(int(total_pages)):
                page_url = f"{base_url}{page * 10}"  # Update URL to point to the correct page
                driver = Driver(uc=True, headless=False)
                helpers = HandyWrappers(driver)
                driver.get(page_url)
                driver.implicitly_wait(5)

                # Check if there are no job results
                if not helpers.isElementPresent('//h1[text()= " did not match any jobs."]', 'xpath'):
                    # Get the job URLs and titles for "Easily apply" jobs
                    job_urls = driver.find_elements(By.XPATH, '//span[text()="Easily apply"]//parent::span//parent::div//parent::div//parent::div//child::a')
                    job_title_elements = driver.find_elements(By.XPATH, '//span[text()="Easily apply"]//parent::span//parent::div//parent::div//parent::div//child::a//child::span')

                    hrefs = []
                    jobs_titles = []

                    # Extract URLs from job elements
                    for element in job_urls:
                        if element.text != "View similar jobs with this employer":
                            try:
                                href = element.get_attribute('href')
                                if '/rc/clk?jk=' in href:
                                    hrefs.append(href)  # Only add valid job URLs
                            except Exception as e:
                                print(f"Error retrieving href: {e}")

                    # Extract job titles from elements
                    for element in job_title_elements:
                        try:
                            jobs_title = element.text
                            jobs_titles.append(jobs_title)
                        except Exception as e:
                            print(f"Error retrieving job title: {e}")

                    # Prepare job titles and URLs for processing
                    list_of_jobs = [job.replace("full details of ", "") for job in jobs_titles]

                    # Process each job and scrape details
                    for job, href in zip(list_of_jobs, hrefs):
                        try:
                            # Click on each job to get full details
                            helpers.ClickElement(Locator=f'//div//h2//a[@aria-label="full details of {job}"]', LocatorType='xpath')

                            # Scrape company name from the job listing
                            company_name = helpers.GetElementAttribute(f'//span[text()="{job}"]//ancestor::div//div[@data-company-name]//a[contains(@aria-label, "(opens in a new tab)")]', 'xpath', 'aria-label')
                            company_name = company_name.split(" (")[0]  # Remove unnecessary text from company name
                        except:
                            continue

                        # Skip if the job already exists in the CSV
                        if (job, company_name) in existing_jobs:
                            print(f"Skipping duplicate job: {job} at {company_name}")
                            continue

                        # Extract pay details from job listing
                        try:
                            pay = helpers.GetElementText('//h3[text()="Pay"]//parent::div//div[text()]', 'xpath')
                        except:
                            try:
                                pay = helpers.GetElementText('//div[@id="jobDescriptionText"]//p[contains(., "Pay")]', 'xpath')[5:]
                            except:
                                pay = 'N/A'

                        # Extract job type from the listing
                        try:
                            job_type = helpers.GetElementlistofText('//h3[text()="Job type"]//parent::div//div[text()]', 'xpath')
                            job_type = ', '.join(job_type)
                        except:
                            try:
                                job_type = helpers.GetElementText('//div[@id="jobDescriptionText"]//p[contains(., "Job Type")]', 'xpath')[11:]
                            except:
                                job_type = 'N/A'

                        # Extract job description from the listing
                        try:
                            description = helpers.GetElementlistofText('//div[@id="jobDescriptionText"]//*[self::div or self::p or self::li]', 'xpath')
                            description = ' '.join(description)
                        except:
                            description = 'N/A'

                        # Create a dictionary for the current job and print it
                        data = {
                            'Job Title': job,
                            'Location': Job_Location,
                            'Company Name': company_name,
                            'Pay': pay,
                            'Job Type': job_type,
                            'Description': description,
                            'Location or Zipcode': Job_Location,
                            'href': href
                        }
                        print(json.dumps(data, indent=4))

                        # Write the job data to the CSV file
                        writer.writerow(data)
                        existing_jobs.add((job, company_name))  # Add the job to the set to avoid future duplicates

                else:
                    print('No job postings available on this page')

                # Close the browser after scraping the current page
                driver.close()
                driver.quit()

        print('End: Scraping process finished\n\n')
