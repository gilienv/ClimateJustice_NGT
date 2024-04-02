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
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Get the current date
current_date = datetime.now().date()
# Print the current date
# print("Current date:", current_date)

def Extract_Text_toCSV(driver):
    try:
        FilingNumber = driver.find_element(By.XPATH, '//div[@class="table-responsive"]/table/tbody/tr/td/div/font').text.strip()
        # print(FilingNumber)
        FilingDate = driver.find_element(By.XPATH, '//*[@id="block-system-main"]/div/div/div[1]/table/tbody/tr[1]/td[4]/font').text.strip()
        PartyName = driver.find_element(By.XPATH, '//*[@id="block-system-main"]/div/div/div[1]/table/tbody/tr[2]/td[2]/font').text.strip()
        PetitionerAdvocate = driver.find_element(By.XPATH, '//*[@id="block-system-main"]/div/div/div[1]/table/tbody/tr[3]/td[2]/font').text.strip()
        RespondentAdvocate = driver.find_element(By.XPATH, '//*[@id="block-system-main"]/div/div/div[1]/table/tbody/tr[3]/td[4]/font').text.strip()
        Act = driver.find_element(By.XPATH, '//*[@id="block-system-main"]/div/div/div[1]/table/tbody/tr[4]/td[2]/font').text.strip()
        CaseNumber = driver.find_element(By.XPATH, '//*[@id="block-system-main"]/div/div/div[1]/table/tbody/tr[5]/td[2]/font').text.strip()
        RegisteredOn = driver.find_element(By.XPATH, '//*[@id="block-system-main"]/div/div/div[1]/table/tbody/tr[5]/td[4]/font').text.strip()
        LastListed = driver.find_element(By.XPATH, '//*[@id="block-system-main"]/div/div/div[1]/table/tbody/tr[6]/td[2]/font').text.strip()
        try:
            NextHearingDate = driver.find_element(By.XPATH, '//*[@id="block-system-main"]/div/div/div[1]/table/tbody/tr[6]/td[4]/font').text.strip()
        except NoSuchElementException:
            NextHearingDate = ''  # If element not found, set it to an empty string
        CaseStatus = driver.find_element(By.XPATH, '//*[@id="block-system-main"]/div/div/div[1]/table/tbody/tr[7]/td[2]/font').text.strip()

        '''COLLAPSE EVENT'''
        collapsible_div = driver.find_element(By.ID ,"headingOne")
        # Click on the element to expand it
        collapsible_div.click()
        wait = WebDriverWait(driver, 10)

        Petitioner = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="collapseOne"]/div/div/table/tbody/tr/td[1]'))).text.strip()
        # print('P :', Petitioner)  
        Respondent = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="collapseOne"]/div/div/table/tbody/tr/td[2]'))).get_attribute("innerHTML").replace("<br>", "\n").strip()
        # print('R :', Respondent)
        ScrapedDate = current_date

        # CSV file Save in Date & Time Format 
        # Check if the directory exists, if not, create it
        if not os.path.exists('CASE_DETAILS'):
            os.makedirs('CASE_DETAILS')
        
        # Assign Current Date
        csv_file_path = f'CASE_DETAILS/{current_date}-details.csv'

        # Write header only if file does not exist
        if not os.path.isfile(csv_file_path):
            with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([    
                    'S. No.',
                    'Filing Number', 
                    'Filing Date', 
                    'Party Name', 
                    'Petitioner Advocate(s)', 
                    'Respondent Advocate(s)',
                    'Act', 
                    'Case Number',
                    'Registered On',
                    'Last Listed',
                    'Next Hearing Date',
                    'Case Status',
                    'Petitioner',
                    'Respondent',
                    'Scraped Date'
                ])

        # Count existing rows to determine the serial number for the new row
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csv_file:
            existing_rows = len(list(csv.reader(csv_file)))

        # Append data to the CSV file
        with open(csv_file_path, 'a', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([
                existing_rows,
                FilingNumber,
                FilingDate,
                PartyName,
                PetitionerAdvocate,
                RespondentAdvocate,
                Act,
                CaseNumber,
                RegisteredOn,
                LastListed,
                NextHearingDate,
                CaseStatus,
                Petitioner,
                Respondent,
                ScrapedDate,
            ])
        print(f"Case details saved to {csv_file_path}")

    except TimeoutException:
        print("Timeout occurred while waiting for the elements to load.")

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

'''MAIN SCRIPT'''
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
button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@class='btn-default btn-custom' and text()='Search']"))) 
button.click() 
print('clicked search button')

'''PAGINATION'''
wait = WebDriverWait(driver, 10)
'''CHANGE PAGE RANGE ACCORDINGLY IN range() FUNCTION'''
# CHANE THE PAGENATION RANGE HERE : DEFAULT IS 1 TO 27 PAGES
for page_number in range(1, 28):  # Assuming there are 28 pages, adjust the range accordingly
    try:
        # Find pagination link for the current page number
        pagination_link = wait.until(EC.element_to_be_clickable((By.XPATH, f'//ul[@class="pagination"]/li/a[text()="{page_number}"]')))  
        # Click on pagination link
        pagination_link.click()
        time.sleep(2)  # Wait for page to load

        '''CLICK EACH 0F 20 CASE STATUS ROW'''
        '''CHANGE ROWS RANGE ACCORDINGLY IN BELOW range() FUNCTION'''
        # CHANE THE ROW RANGE HERE : DEFAULT IS 1 TO 20 ROWS
        for row_number in range(1, 21):  # Assuming there are 20 rows
            try:
                # Find the specific row based on row_number
                row_xpath = f'//*[@id="block-system-main"]/div/div/div[2]/table/tbody/tr[{row_number}]'
                row = driver.find_element(By.XPATH, row_xpath)
                # Find the Case Status link in the current row
                try:
                    CaseStatus = row.find_element(By.XPATH, './td[7]/a')
                    CaseStatus.click()
                    print(f'CaseDetails - {(page_number - 1) * 20 + row_number} OR {row_number} of 20 of Page.No - {page_number} saved')
                    # Extract table data and write to CSV
                    Extract_Text_toCSV(driver)
                    # Click the back button
                    back = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="buttonarea"]/a'))) 
                    back.click() 
                    print('back')
                except Exception as e:
                    print(f"Error occurred while processing row: {e}")
            except Exception as e:
                print(f"Error occurred: {e}")
        
        print(f"Page {page_number} all data saved")
        
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
