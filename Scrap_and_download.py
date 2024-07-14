import os
import time
import shutil
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Define the URL
url = "https://www.samco.in/bhavcopy-nse-bse-mcx"

driver_path = "D:\\Apache Spark Project Stock market analysis\\chromedriver-win64\\chromedriver.exe"  

# Define the download directory
downloads_folder = "C:\\Users\\ASUS\\Downloads"
destination_folder = "D:\\Apache Spark Project Stock market analysis\\download_automation\\Raw_Files"

service = Service(driver_path)

chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": downloads_folder,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

driver = webdriver.Chrome(service=service)


try:

    #------------------------------------------------------------------------------------------------------------#
    # --CODE FOR CHECKING  THE FILES # 

    # Open the URL
    driver.get(url)

    # Wait for the table to load
    time.sleep(2)  # Adjust this as needed

    # Find the current date
    today_date = datetime.now().strftime('%m-%d-%Y')
    
    #getting the latest data on the website by setting todays date
    try:
        to_date_input = driver.find_element(By.ID, "end_date")
        to_date_input.clear()
        to_date_input.send_keys(today_date)
        to_date_input.send_keys(Keys.RETURN)
        
        # time.sleep(2)  # Allow time for the date to be set

        # Locate and click the "Show" button
        show_button = driver.find_element(By.ID, "Show")
        show_button.click()

        print("Successfully set today's date and clicked the 'Show' button.")

    except Exception as e:
        print(f"An error occurred: {e}")

    # Wait for the NEW TABLE to load
    time.sleep(5)  
    print("Waited for the new table to load")

    # Re-fetch the rows after updating the date
    table = driver.find_element(By.ID, "calculator")
    rows = table.find_elements(By.TAG_NAME, "tr")
    num_rows=len(rows)
    print("There are total ",len(rows)," in the table now")
    print("Tranersing from ",num_rows-1,"-To-",num_rows-4," reverse")

    time.sleep(5) 
   # Collect NSE CSV links and dates
    nse_links = []
    for row in rows[num_rows-1: (num_rows-3)-1 :-1 ]:  # check the lastest 3 rows as 2 might be holidays
        cells = row.find_elements(By.TAG_NAME, "td")
        # if the cell 3 which is NSEFO exist and has a type element parse it
        if cells and cells[3].find_elements(By.TAG_NAME, "a"):
            date = cells[1].text
            link = cells[3].find_element(By.TAG_NAME, "a").get_attribute('href')
            nse_links.append((date, link))
            print("Parsed ",date,"and got",link)

    time.sleep(2) 

    #------------------------------------------------------------------------------------------------------------#
    # --CODE FOR DOWNLOADING THE FILES # 

    # Download the latest two NSE FNO CSV files
    try:
        # Loop through links and download files
        for i, (date, link) in enumerate(nse_links):
            driver.get(link)
            file_name = f"{date}.csv"  # Assuming the file is a CSV, append the correct extension
            download_path = os.path.join(downloads_folder, file_name)
            
            # Wait for the file to download (check if file exists)
            timeout = 10  # Adjust timeout as needed
            downloaded = False
            start_time = time.time()
            
            while not downloaded and time.time() - start_time < timeout:
                if os.path.exists(download_path):
                    downloaded = True
                time.sleep(1)
            
            if downloaded:
                # Move the file to destination folder
                dst_file = os.path.join(destination_folder, file_name)
                shutil.move(download_path, dst_file)
                print(f"Moved {file_name} to {destination_folder}")
            else:
                print(f"File {file_name} not downloaded within timeout.")

    except Exception as e:
        print(f"Error occurred: {e}")


    #------------------------------------------------------------------------------------------------------------#
    # --CODE FOR MOVING THE FILES # 

    # Ensure destination folder exists
    os.makedirs(destination_folder, exist_ok=True)

    # Move files based on dates in nse_links
    for item in nse_links:
        try:
            date_str, link = item
            # Convert date_str to date object
            date = datetime.strptime(date_str, "%d-%m-%Y").date()
            
            # Construct the filename as per the format 20240711_NSEFO.csv
            filename = date.strftime("%Y%m%d") + "_NSEFO.csv"
            
            # Check if the file exists in downloads folder
            src_file = os.path.join(downloads_folder, filename)
            
            print("File Found")

            if os.path.exists(src_file):
                # Move the file to destination folder
                dst_file = os.path.join(destination_folder, filename)
                shutil.move(src_file, dst_file)
                print(f"Moved {filename} to {destination_folder}")
            else:
                print(f"File {filename} not found in {downloads_folder}")

        except Exception as e:
            print(f"Error processing {date_str}: {e}")
        

finally:
    # Close the driver
    driver.quit()


