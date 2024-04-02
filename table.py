from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import pytesseract
import csv
import os
import re
from io import BytesIO
import time
from datetime import datetime

# Get the current date
current_date = datetime.now().date()

# Function to write data to CSV file
def ToCSV(row_data):
    # Check if the directory exists, if not, create it
    if not os.path.exists('CASE_TABLE'):
        os.makedirs('CASE_TABLE')
    
    csv_file_path = f'CASE_TABLE/{current_date}-table.csv'

    with open(csv_file_path, 'a', newline='') as csvfile:
        fieldnames = [
            'Sr. No.', 
            'Zonal Bench', 
            'Diary Number', 
            'Case Number/Location Code', 
            'Party Name', 
            'Order Date', 
            'Case Status', 
            'Scraped Date'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header only if file is empty
        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow(row_data)

# Function to extract table data and write to CSV
def Extract_Text_toCSV(driver):
    datas = driver.find_elements(By.XPATH, '//*[@id="block-system-main"]/div/div/div[2]/table/tbody/tr')

    for data in datas:
        # Extract data from each row
        row_data = {
            'Sr. No.': data.find_element(By.XPATH, './td[1]').text,
            'Zonal Bench': data.find_element(By.XPATH, './td[2]/a').text,
            'Diary Number': data.find_element(By.XPATH, './td[3]/a').text,
            'Case Number/Location Code': data.find_element(By.XPATH, './td[4]/a').text,
            'Party Name': data.find_element(By.XPATH, './td[5]/a').text,
            'Order Date': data.find_element(By.XPATH, './td[6]/a').text,
            'Case Status': data.find_element(By.XPATH, './td[7]/a').text,
            'Scraped Date': current_date
        }

        # Save data to CSV file
        ToCSV(row_data)

# Function to delete PNG files from a folder
def DeleteIMGFiles(folder_path):
    try:
        # Get list of files in the folder
        files = os.listdir(folder_path)
        # Iterate over files and delete .png files
        for file in files:
            if file.endswith('.png'):
                os.remove(os.path.join(folder_path, file))
                print(f"Deleted: {file}")
        
        print("All .png files deleted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

# URL of the website
url = 'https://www.greentribunal.gov.in/judgementOrder/zonalbenchwise'

# Setting up Chrome WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get(url)
driver.maximize_window()
time.sleep(1)

'''ZONAL BENCH'''
dropdown = Select(driver.find_element(By.NAME ,'zone_type'))
dropdown.select_by_value('1')

'''SEARCH BY'''
dropdown = Select(driver.find_element(By.NAME ,'order_by'))
dropdown.select_by_value('3')

'''CAPTCHA IMAGE'''
if not os.path.exists('CaptchaImg'):
    os.makedirs('CaptchaImg')

current_datetime = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
img_download_path = f'CaptchaImg/{current_datetime}.png'
screenshot = driver.get_screenshot_as_png()
image = Image.open(BytesIO(screenshot))

crop_image = (1600, 680, 2000, 750)
cropped_image = image.crop(crop_image)
cropped_image.save(img_download_path) 

if img_download_path is not None:
    image_path = img_download_path
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image) 
    cleaned_text = re.sub(r'[^a-zA-Z0-9]', '', text)[:5]
    print("Extracted Text:", cleaned_text)
else:
    print("Not Able to find")

# Fill captcha input with extracted text
captcha_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,'txtInput')))
captcha_input.clear()
captcha_input.send_keys(cleaned_text)

time.sleep(1)

'''FROM DATE'''
input_field = driver.find_element(By.ID ,'fromdate')
input_field.clear()
input_field.send_keys('03/03/2024')

'''TO DATE'''
input_field = driver.find_element(By.ID ,'todate')
input_field.clear()
input_field.send_keys('29/03/2024')

time.sleep(1)

'''SEARCH BUTTON'''
wait = WebDriverWait(driver, 10)  
element = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@class='btn-default btn-custom' and text()='Search']"))) 
element.click() 
print('search button clicked')

# Find the div element to scroll down
div_element = driver.find_element(By.XPATH, '//*[@id="block-system-main"]/div/div')
# Execute JavaScript to scroll to the bottom of the div element
driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", div_element)
time.sleep(2)

'''PAGINATION'''
wait = WebDriverWait(driver, 10)
'''CHANGE PAGE RANGE ACCORDINGLY IN range() FUNCTION'''
# CHANE THE PAGENATION RANGE HERE : DEFAULT IS 1 TO 27 PAGES
for page_number in range(1, 28):  # Assuming there are 27 pages, adjust the range accordingly
    try:
        # Find pagination link for the current page number
        pagination_link = wait.until(EC.element_to_be_clickable((By.XPATH, f'//ul[@class="pagination"]/li/a[text()="{page_number}"]')))
        # Click on pagination link
        pagination_link.click()
        time.sleep(2)  # Wait for page to load

        # Extract table data and write to CSV
        Extract_Text_toCSV(driver)
        print(f"Page {page_number} saved")
        
        # Scroll down the div element
        div_element = driver.find_element(By.XPATH, '//*[@id="block-system-main"]/div/div')
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", div_element)
        time.sleep(2)
    except Exception as e:
        print(f"Error occurred: {e}")

# Quit the WebDriver
driver.quit()

# Delete PNG files from the captcha folder
DeleteIMGFiles('CaptchaImg')