# Green Tribunal Case Records Scraper


<p align="center"><img src="https://socialify.git.ci/KAMRANKHANALWI/ClimateJustice/image?font=Source%20Code%20Pro&amp;language=1&amp;name=1&amp;pattern=Circuit%20Board&amp;theme=Dark" alt="project-image"></p>


A short internship project at the interface of **#SemanticClimate** and **#IndiaJusticeReports** conducted at **#NIPGR**, New Delhi. 

This Python script extracts case details from [National Green Tribunal](https://www.greentribunal.gov.in/judgementOrder/zonalbenchwise) website using Selenium WebDriver. The main parameters for each record are saved to a CSV file along wth date of scraping. The script navigates through the website, enters search parameters, solves CAPTCHA, extracts case details, and returns a CSV file.
A second aim is to create a folder for each case record and push all related files into that folder. 


## Dependencies
- **Selenium**: A Python library for automating web browsers.
- **Pytesseract**: Python binding to the Tesseract OCR engine for extracting text from images.
- **PIL (Python Imaging Library)**: Required for image manipulation.
- **Chrome WebDriver**: WebDriver for Chrome browser. Automatically managed by `webdriver_manager`.

## Usage
1. Ensure you have Python installed on your system and an code editor like VS Code to run the code.
2. Also Download ChromeDriver from here:
   [ChromeDriver Download Page](https://chromedriver.chromium.org/downloads)
3. Install the required dependencies using pip:
   ```
   pip install selenium pytesseract pillow webdriver-manager
   ```
3. Run the scripts using Python accordingly:
   ```
   python details.py
   ```
   ```
   python table.py
   ```

## How It Works
1. The script opens a Chrome browser and navigates to a specified URL.
2. It selects options from dropdown menus, captures a CAPTCHA image, extracts text from the image, and fills in the CAPTCHA field.
3. It enters search parameters such as date range and clicks the search button.
4. You can change the date range in the code accordingly like 'FROM DATE 03/03/2024 TO DATE 29/03/2024' by searching the word 'date' in VS Code (Ctrl + F)
5. It iterates through pagination and extracts case details for each page.
6. You can set the page range of which you want to extract the data like : 1 to 27 (goes till 26 page) by searching the word 'range' in the code.
7. Case details are saved to a CSV file named with the current date and time in the particular directory.


## Files
- **details.py**: Python script file 1.
- **table.py**: Python script file 2.
- **CASE_DETAILS**: Directory where the **details.py** CSV files are saved.
- **CASE_TABLE**: Directory where the **table.py** CSV files are saved.
- **CaptchaImg**: Directory where CAPTCHA images are saved.


## Important Notes
- Ensure an active internet connection as the script interacts with a live website.
- The script assumes the structure of the website remains unchanged. Any changes in the website structure may require modifications to the XPath expressions used in the script.


## Support and Assistance
If you encounter any difficulties during the process of downloading dependencies or executing the Python scripts, feel free to reach out for assistance. You can contact me via email at [khankamranalwi@gmail.com](mailto:khankamranalwi@gmail.com) or message me on WhatsApp at [+91 9304816286](https://wa.me/919304816286). I'm here to help you resolve any issues and ensure a smooth experience with the setup and usage of the provided scripts.
