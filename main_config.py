import configparser
import os
import pandas as pd
from indeed_autoapply import setup_driver, login_to_indeed, apply_for_job
from Indeed_Scrapper import IndeedScrapper

config = configparser.ConfigParser()
config.read('config.ini')

# Access the parameters
job_title = config['JobDetails']['job_title']
job_zipcode = config['JobDetails']['job_zipcode']
job_pages = config['JobDetails']['job_pages']
resume_pdf = config['JobDetails']['resume_pdf']

if job_title and job_zipcode and job_pages and resume_pdf:
    # to scrape job profile details like JD, company name, job title etc
    runtest = IndeedScrapper()
    runtest.scrapper(job_title, job_zipcode, job_pages)

    # store those details in CSV file
    df = pd.read_csv('IndeedData.csv')
    df_list = df.values.tolist()
    job_data = [[i[0], i[4], i[-1]] for i in df_list]
    
    # Set up driver and perform applying operations
    driver = setup_driver()
    login_to_indeed(driver)  

    for i,single_row in enumerate(job_data):
        if i == 8:
            driver.close()
            driver.quit()
            driver = setup_driver()
            login_to_indeed(driver)  

        job_url = single_row[-1]
        rest_of = single_row[:-1]
        print("\n\nStarting the application process...")
        apply_for_job(driver, job_url, rest_of, resume_pdf)
        print("\nJob application process completed.", '\n\n')
        
    
    driver.close()
    driver.quit()
else:
    print('\nThere is a missing input parameter')

