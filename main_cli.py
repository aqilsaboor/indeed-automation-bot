import os
import pandas as pd
from indeed_autoapply import setup_driver, login_to_indeed, apply_for_job
from Indeed_Scrapper import IndeedScrapper

def main():
    print("Job Application Automation CLI")
    # takes required input parameters
    job_title = input("Enter the Job Title: ")
    job_zipcode = input("Enter the Job Zipcode: ")
    job_pages = input("Enter the Number of Job Pages: ")
    resume_pdf = input('Please Input Resume Full Path')

    if job_title and job_zipcode and job_pages and resume_pdf:
        # to scrape job profile details like JD, company name, job title etc
        runtest = IndeedScrapper()
        runtest.scrapper(job_title, job_zipcode, job_pages)

        # store those details in CSV file
        df = pd.read_csv('IndeedData.csv')
        df_list = df.values.tolist()
        job_data = [[i[0], i[4], i[-1]] for i in df_list]
        

        # Set up driver and perform applying operations
        print('Setting up Driver')
        print('Wait for one minute')
        driver = setup_driver()
        login_to_indeed(driver)  # Logging into Indeed

        for single_row in job_data:
            job_url = single_row[-1]
            rest_of = single_row[:-1]
            print("Starting the application process...")
            apply_for_job(driver, job_url, rest_of, resume_pdf)
            print("Job application process completed.", '\n\n')
           
        
        driver.close()
        driver.quit()
    else:
        print('There is a missing input parameter')

if __name__ == "__main__":
    main()