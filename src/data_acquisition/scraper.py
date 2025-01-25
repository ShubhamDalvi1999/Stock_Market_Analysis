import os
import time
import shutil
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

class Logger:
    """Handles all logging operations."""
    def __init__(self, log_dir='logs', log_file='data_acquisition.log'):
        self.log_dir = log_dir
        self.log_file = log_file
        self.setup_logging()
        
    def setup_logging(self):
        """Set up logging configuration."""
        os.makedirs(self.log_dir, exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(os.path.join(self.log_dir, self.log_file)),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('data_acquisition')
        return self.logger

class PathManager:
    """Manages all path-related operations."""
    def __init__(self, logger):
        self.logger = logger
        self.setup_paths()
        
    def setup_paths(self):
        """Set up all required paths and directories."""
        self.project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.driver_path = os.path.join(self.project_root, "chromedriver-win64", "chromedriver.exe")
        self.downloads_folder = os.path.join(self.project_root, "temp_downloads")
        
        # Setup data directories
        self.data_dir = os.path.join(self.project_root, "data")
        self.raw_dir = os.path.join(self.data_dir, "raw")
        self.processed_dir = os.path.join(self.data_dir, "processed")
        self.archive_dir = os.path.join(self.data_dir, "archive")
        
        # Create all required directories
        os.makedirs(self.downloads_folder, exist_ok=True)
        os.makedirs(self.raw_dir, exist_ok=True)
        os.makedirs(self.processed_dir, exist_ok=True)
        os.makedirs(self.archive_dir, exist_ok=True)
        
        self.logger.info(f"Using ChromeDriver path: {self.driver_path}")
        self.logger.info(f"Downloads folder: {self.downloads_folder}")
        self.logger.info(f"Raw data directory: {self.raw_dir}")
        self.logger.info(f"Processed data directory: {self.processed_dir}")
        self.logger.info(f"Archive directory: {self.archive_dir}")

class ChromeDriverManager:
    """Manages Chrome WebDriver setup and operations."""
    def __init__(self, path_manager, logger):
        self.path_manager = path_manager
        self.logger = logger
        self.driver = None
        
    def setup_chrome_options(self):
        """Configure Chrome options."""
        chrome_options = Options()
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": os.path.abspath(self.path_manager.downloads_folder),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        chrome_options.add_argument('--headless')
        return chrome_options
        
    def initialize_driver(self):
        """Initialize and configure Chrome WebDriver."""
        try:
            chrome_options = self.setup_chrome_options()
            service = Service(executable_path=self.path_manager.driver_path)
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 20)
            self.logger.info("Successfully initialized Chrome driver")
            return self.driver
        except Exception as e:
            self.logger.error(f"Error initializing Chrome driver: {str(e)}")
            raise
            
    def cleanup(self):
        """Clean up Chrome driver resources."""
        try:
            if self.driver:
                self.driver.quit()
                self.logger.info("Chrome driver closed")
        except Exception as e:
            self.logger.error(f"Error closing Chrome driver: {str(e)}")

class DataScraper:
    """Handles the main scraping operations."""
    def __init__(self, driver_manager, path_manager, logger):
        self.driver_manager = driver_manager
        self.path_manager = path_manager
        self.logger = logger
        self.url = "https://www.samco.in/bhavcopy-nse-bse-mcx"
        
    def wait_for_download(self, download_path, timeout=30):
        """Wait for file to be downloaded."""
        start_time = time.time()
        while not os.path.exists(download_path) and time.time() - start_time < timeout:
            time.sleep(1)
        return os.path.exists(download_path)
        
    def clear_old_files(self):
        """Clear old files from raw directory."""
        self.logger.info("Clearing old files from raw directory...")
        for file in os.listdir(self.path_manager.raw_dir):
            if file.endswith('.csv'):
                file_path = os.path.join(self.path_manager.raw_dir, file)
                try:
                    # Move to archive instead of deleting
                    archive_path = os.path.join(self.path_manager.archive_dir, 
                                              f"{os.path.splitext(file)[0]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
                    shutil.move(file_path, archive_path)
                    self.logger.info(f"Archived: {file}")
                except Exception as e:
                    self.logger.error(f"Error archiving {file}: {str(e)}")
                    
    def get_download_links(self):
        """Get download links for the latest two days."""
        driver = self.driver_manager.driver
        wait = self.driver_manager.wait
        
        driver.get(self.url)
        self.logger.info(f"Opened URL: {self.url}")
        time.sleep(5)
        
        table = wait.until(EC.presence_of_element_located((By.ID, "calculator")))
        rows = table.find_elements(By.TAG_NAME, "tr")
        self.logger.info(f"Found {len(rows)} rows in table")
        
        nse_links = []
        for row in rows[1:]:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 3:
                nsefo_cell = cells[3]
                if nsefo_cell.find_elements(By.TAG_NAME, "a"):
                    date = cells[1].text
                    link = nsefo_cell.find_element(By.TAG_NAME, "a").get_attribute('href')
                    nse_links.append((date, link))
                    self.logger.info(f"Found link for date {date}")
        
        return nse_links[-2:]  # Return last two entries
        
    def download_files(self, nse_links):
        """Download files from the provided links."""
        for date, link in nse_links:
            try:
                self.logger.info(f"Downloading file for {date}")
                self.driver_manager.driver.get(link)
                
                date_obj = datetime.strptime(date, "%d-%m-%Y")
                filename = f"{date_obj.strftime('%Y%m%d')}_NSEFO.csv"
                download_path = os.path.join(self.path_manager.downloads_folder, filename)
                
                if self.wait_for_download(download_path):
                    dst_file = os.path.join(self.path_manager.raw_dir, filename)
                    shutil.move(download_path, dst_file)
                    self.logger.info(f"Successfully downloaded and moved {filename}")
                else:
                    self.logger.error(f"Download failed for {filename}")
            except Exception as e:
                self.logger.error(f"Error processing {date}: {str(e)}")
                
    def cleanup_downloads(self):
        """Clean up temporary downloads folder."""
        try:
            if os.path.exists(self.path_manager.downloads_folder):
                shutil.rmtree(self.path_manager.downloads_folder)
                self.logger.info("Cleaned up temporary downloads folder")
        except Exception as e:
            self.logger.error(f"Error cleaning up downloads folder: {str(e)}")

def main():
    """Main execution function."""
    # Initialize components
    logger = Logger().logger
    path_manager = PathManager(logger)
    driver_manager = ChromeDriverManager(path_manager, logger)
    
    try:
        # Initialize driver
        driver_manager.initialize_driver()
        
        # Initialize scraper and perform operations
        scraper = DataScraper(driver_manager, path_manager, logger)
        scraper.clear_old_files()
        
        nse_links = scraper.get_download_links()
        if len(nse_links) < 2:
            raise Exception(f"Could not find two files to download. Found only: {len(nse_links)}")
            
        logger.info("Found latest two files to download:")
        for date, _ in nse_links:
            logger.info(f"- {date}")
            
        scraper.download_files(nse_links)
        
    except TimeoutException as e:
        logger.error(f"Timeout error: {str(e)}")
    except WebDriverException as e:
        logger.error(f"WebDriver error: {str(e)}")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        
    finally:
        driver_manager.cleanup()
        scraper.cleanup_downloads()

if __name__ == "__main__":
    main()


