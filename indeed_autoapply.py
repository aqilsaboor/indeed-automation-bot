from time import sleep
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from urllib.parse import urlparse
from track_job_json import update_job_json
from openpyxl import Workbook, load_workbook
from datetime import datetime
import os
import json
from seleniumbase import Driver
import configparser
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load configuration from config file
config = configparser.ConfigParser()
config.read('config.ini')

# Extract necessary job details from the config file
email = config['JobDetails']['email']
Password = config['JobDetails']['Password']
first_name = config['JobDetails']['first_name']
last_name = config['JobDetails']['last_name']
phone_no = config['JobDetails']['phone_no']
job_zipcode = config['JobDetails']['job_zipcode']

# Function to manage implicit waiting and pauses in execution
def wait(driver):
    driver.implicitly_wait(3)
    sleep(2)

# Function to initialize the browser driver using SeleniumBase and undetected-chromedriver
def setup_driver():
    driver = Driver(uc=True, headless=False)
    return driver

# Function to handle login to Indeed using Google credentials
def login_to_indeed(driver):
    print('\n\nStart: Hit login page URL\n')
    driver.get('https://secure.indeed.com/auth?hl=en_PK&co=PK&continue=https%3A%2F%2Fpk.indeed.com%2F%3Fr%3Dus&tmpl=desktop&from=gnav-util-homepage&jsContinue=https%3A%2F%2Fonboarding.indeed.com%2Fonboarding%3Fhl%3Den_PK%26co%3DPK%26from%3Dgnav-homepage&empContinue=https%3A%2F%2Faccount.indeed.com%2Fmyaccess')

    sleep(5)
    
    # Click on Google login button and switch to the new window
    driver.find_element(By.ID, 'login-google-button').click()
    main_window = driver.current_window_handle
    sleep(2)
    all_windows = driver.window_handles
    for window in all_windows:
        if window != main_window:
            driver.switch_to.window(window)
            break
        
    # Enter email and proceed with Google login
    email_input = driver.find_element(By.ID, "identifierId")
    email_input.send_keys(email)
    sleep(4.8)
    
    driver.find_element(By.XPATH, '//span[text()="Next"]//parent::button').click()
    sleep(7.3)
    
    # Enter password and continue
    email_input = driver.find_element(By.XPATH, '//input[@aria-label="Enter your password"]')
    email_input.send_keys(str(Password))
    sleep(8.1)
    
    driver.find_element(By.XPATH, '//span[text()="Next"]//parent::button').click()
    sleep(8)
    
    # Complete login process by clicking 'Continue' button if present
    try: 
        driver.find_element(By.XPATH, '//span[text()="Continue"]//parent::button').click()
        sleep(7.3)
    except:
        pass   
    
    driver.switch_to.window(main_window)
    print("Login Successful!\n")

# Function to upload a resume if not already uploaded
def upload_resume(driver, file_path: str):
    upload_resume = driver.find_elements(By.XPATH, "//span[text()='Upload a resume']") 

    if upload_resume:  # If no resume is found, upload a new one
        print('Resume not found --- Start uploading process...')
        track = None
        try:
            upload_resume = driver.find_element(By.CSS_SELECTOR, "input[type='file'][accept='.pdf,.txt,.docx,.doc,.rtf']")
            track = True
        except:
            print('Failed to find an upload resume tag')
            track = False
        if track:
            try:
                upload_resume.send_keys(file_path)
            except:
                print('Invalid resume file path')
        
    else:  # If resume is already uploaded, select it
        print('Resume already uploaded')
        try:
            cv_select = driver.find_element(By.CSS_SELECTOR, 'div > div > fieldset > div')
            cv_select.click()  
            wait(driver)
            print('Resume selected successfully')
        except:
            print('Failed to select resume')

# Function to apply for a job by automating the job application form filling
def apply_for_job(driver, job_url, job_info, resume_pdf_path: str):
    Submit = False

    print('\nApply to this job URL: ', job_url)
    driver.get(job_url)

    # Check if the job has already been applied to
    try:
        driver.find_element('xpath', "//span[text()='Applied']")
        applied = True
    except: 
        applied = False

    # If the job has not been applied to, proceed with the application
    if not applied:
        try:
            print('\nStart: Click on Apply Button\n')
            apply_btn = driver.find_element('xpath', "//span[text()='Apply now']")
            apply_btn.click()
            wait(driver)
            print('\nEnd: Click on Apply Button\n')
        except Exception as e:
            print(f"Error applying: {e}")

        # Fill in personal details (first name, last name, etc.)
        sleep(5.1)
        try:
            print('\nAdding first name\n')
            f_name_input = driver.find_element(By.XPATH, '//input[@id="input-firstName"]')
            f_name_input.send_keys(Keys.CONTROL + "a")  
            f_name_input.send_keys(Keys.DELETE)  
            f_name_input.send_keys(str(first_name))
            
            print('\nAdding last name\n')
            l_name_input = driver.find_element(By.XPATH, '//input[@id="input-lastName"]')
            l_name_input.send_keys(Keys.CONTROL + "a") 
            l_name_input.send_keys(Keys.DELETE)  
            l_name_input.send_keys(str(last_name))
            
            print('\nAdding city name\n')
            city_name_input = driver.find_element(By.XPATH, '//input[@id="input-location.city"]')
            city_name_input.send_keys(Keys.CONTROL + "a") 
            city_name_input.send_keys(Keys.DELETE)  
            city_name_input.send_keys(str(job_zipcode))  
            
            print('\nAdding phone number\n')
            phone_no_input = driver.find_element(By.XPATH, '//input[@id="input-phoneNumber"]')
            phone_no_input.send_keys(Keys.CONTROL + "a")  
            phone_no_input.send_keys(Keys.DELETE)  
            phone_no_input.send_keys(str(phone_no))  
            
            print('\nClicking on continue button\n')
            continue_buttons = driver.find_elements(By.XPATH, '//span[text()="Continue"]//parent::button')
            for btn in continue_buttons:
                try:
                    driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable(btn))
                    btn.click()
                    print('Clicked on the continue button.')
                except Exception as e:
                    pass
        except Exception as e:
            print("Error in personal details page: ", e)
        sleep(5)

        # Upload resume
        print('\nUploading resume\n')
        upload_resume(driver, file_path=resume_pdf_path)

        # Final submission process
        sleep(5)
        print('\nClicking on continue button\n')
        continue_buttons = driver.find_elements(By.XPATH, '//span[text()="Continue"]//parent::button')
        for btn in continue_buttons:
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable(btn))
                btn.click()
                print('Clicked on the continue button.')
            except Exception as e:
                pass
        sleep(5)

        # Submit the application
        try:
            print("Submitting the application")
            submit_application = driver.find_element(By.XPATH, "//button[span[text()='Submit your application']]")
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_application)
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable(submit_application))
            submit_application.click()
            print('Application submitted successfully')
            Submit = True
            sleep(5)
        except Exception as e:
            print('Error submitting the application:', e)

    else: 
        print("\n\nApplication already submitted")
        job_title, job_type, job_link = job_info[0], job_info[1], job_url
        job_log = [job_title] + [job_type] + ['Failed - Application already submitted'] + [job_link]
        update_job_json(file_path="track.json", job_data=job_log)
        Submit = "Any"

    # Log the result of the application process
    if Submit == True:
        job_title, job_type, job_link = job_info[0], job_info[1], job_url
        job_log = [job_title] + [job_type] + ['Success - Application submitted'] + [job_link]
        update_job_json(file_path="track.json", job_data=job_log)
    elif Submit == False:
        job_title, job_type, job_link = job_info[0], job_info[1], job_url
        job_log = [job_title] + [job_type] + ['Failed - Application not Submitted'] + [job_link]
        track_json = "track.json"
        update_job_json(file_path=track_json, job_data=job_log)
