import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Define the URL
url = "https://www.samco.in/bhavcopy-nse-bse-mcx"

driver_path = "D:\\Apache Spark Project Stock market analysis\\chromedriver-win64\\chromedriver.exe"  

# Define the download directory
download_dir = "D:\\Apache Spark Project Stock market analysis"

service = Service(driver_path)

# Set up the Chrome WebDriver
# options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Run headless Chrome
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=service)


try:
    # Open the URL
    driver.get(url)

    # Wait for the table to load
    time.sleep(5)  # Adjust this as needed

    # Find the table
    table = driver.find_element(By.ID, "calculator")
    
    # Get all rows of the table
    rows = table.find_elements(By.TAG_NAME, "tr")

    # Find the current date
    # current_date = datetime.now().strftime('%d-%m-%Y')
    
   # Collect NSE CSV links and dates
    nse_links = []
    for row in rows[1:]:  # Skip the header row
        cells = row.find_elements(By.TAG_NAME, "td")
        if cells and cells[2].find_elements(By.TAG_NAME, "a"):
            date = cells[1].text
            link = cells[2].find_element(By.TAG_NAME, "a").get_attribute('href')
            nse_links.append((date, link))

    # Sort links by date in descending order and get the latest one
    nse_links.sort(reverse=True)

    # Download the latest two NSE CSV files
    for i in range(2):  # Change to download more links if needed
        latest_nse_link = nse_links[i][1]
        driver.get(latest_nse_link)
        file_name = latest_nse_link.split('/')[-1]
        download_path = os.path.join(download_dir, file_name)
        
     # Check if the download is complete within 60 seconds
        timeout = time.time() + 10  # 60 seconds timeout
        while not os.path.exists(download_path) or download_path.endswith('.crdownload'):
            if time.time() > timeout:
                print(f"Timeout occurred while waiting for download: {download_path}")
                break
            time.sleep(1)
        
        if os.path.exists(download_path):
            print(f"Downloaded: {download_path}")
        else:
            print(f"Download failed: {download_path}")

finally:
    # Close the driver
    driver.quit()
