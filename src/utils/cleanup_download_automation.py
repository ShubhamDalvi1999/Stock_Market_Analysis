import os
import shutil
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def ensure_directory_structure():
    """Create and ensure all required directories exist."""
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    # Define all required directories
    directories = {
        'download_automation': os.path.join(project_root, "download_automation"),
        'raw_files': os.path.join(project_root, "download_automation", "Raw_Files"),
        'processed_files': os.path.join(project_root, "download_automation", "Processed_Files"),
        'filtered_files': os.path.join(project_root, "download_automation", "Filtered_Files"),
        'archive': os.path.join(project_root, "download_automation", "Archive"),
        'temp_downloads': os.path.join(project_root, "temp_downloads")
    }
    
    # Create directories if they don't exist
    for dir_path in directories.values():
        os.makedirs(dir_path, exist_ok=True)
        logger.info(f"Ensured directory exists: {dir_path}")
    
    return directories

def cleanup_temp_downloads(temp_dir):
    """Clean up temporary downloads directory."""
    if os.path.exists(temp_dir):
        for file in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    logger.info(f"Deleted temporary file: {file}")
            except Exception as e:
                logger.error(f"Error deleting temporary file {file}: {e}")

def archive_old_files(raw_dir, archive_dir):
    """Archive files older than 7 days."""
    current_time = datetime.now()
    for file in os.listdir(raw_dir):
        file_path = os.path.join(raw_dir, file)
        if os.path.isfile(file_path):
            file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            days_old = (current_time - file_time).days
            
            if days_old > 7:
                timestamp = file_time.strftime('%Y%m%d_%H%M%S')
                archive_name = f"{os.path.splitext(file)[0]}_{timestamp}{os.path.splitext(file)[1]}"
                archive_path = os.path.join(archive_dir, archive_name)
                
                try:
                    shutil.move(file_path, archive_path)
                    logger.info(f"Archived old file: {file} -> {archive_name}")
                except Exception as e:
                    logger.error(f"Error archiving file {file}: {e}")

def cleanup_download_automation():
    """Clean up and organize download automation directory."""
    logger.info("Starting cleanup process...")
    
    # Ensure directory structure
    directories = ensure_directory_structure()
    
    # Clean up temporary downloads
    cleanup_temp_downloads(directories['temp_downloads'])
    
    # Archive old files
    archive_old_files(directories['raw_files'], directories['archive'])
    
    # Clean up empty directories
    logger.info("\nCleaning up empty directories...")
    for root, dirs, files in os.walk(directories['download_automation'], topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            try:
                if not os.listdir(dir_path):
                    # Don't remove the main required directories
                    if dir_path not in directories.values():
                        os.rmdir(dir_path)
                        logger.info(f"Removed empty directory: {dir_path}")
            except Exception as e:
                logger.error(f"Error removing directory {dir_path}: {e}")
    
    logger.info("\nCleanup complete!")

if __name__ == "__main__":
    print("Starting cleanup of download_automation directory...")
    cleanup_download_automation() 