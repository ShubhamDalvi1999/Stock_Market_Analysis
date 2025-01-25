import os
import shutil
from datetime import datetime
import logging

class DirectoryStructure:
    """Class to manage project directory structure."""
    def __init__(self, base_dir=None):
        if base_dir is None:
            # Go up three levels from utils directory to reach project root
            current_dir = os.path.dirname(os.path.abspath(__file__))
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
        
        # Define directory structure
        self.PROJECT_ROOT = base_dir
        self.DATA_DIR = os.path.join(base_dir, 'data')
        self.RAW_DIR = os.path.join(self.DATA_DIR, 'raw')
        self.PROCESSED_DIR = os.path.join(self.DATA_DIR, 'processed')
        self.ARCHIVE_DIR = os.path.join(self.DATA_DIR, 'archive')
        self.TEMP_DIR = os.path.join(base_dir, 'temp')
        self.LOGS_DIR = os.path.join(base_dir, 'logs')

        # Create all directories
        self.create_directory_structure()

    def create_directory_structure(self):
        """Create the entire directory structure if it doesn't exist."""
        directories = [
            self.DATA_DIR,
            self.RAW_DIR,
            self.PROCESSED_DIR,
            self.ARCHIVE_DIR,
            self.TEMP_DIR,
            self.LOGS_DIR
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)

# Set up logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(os.path.join('logs', 'file_manager.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DataPipelineManager:
    def __init__(self, base_dir=None):
        """Initialize the data pipeline manager with directory structure."""
        self.dir_structure = DirectoryStructure(base_dir)
        
        self.directories = {
            'raw': self.dir_structure.RAW_DIR,
            'processed': self.dir_structure.PROCESSED_DIR,
            'archive': self.dir_structure.ARCHIVE_DIR,
            'temp': self.dir_structure.TEMP_DIR
        }
        
        # Log directory structure
        for dir_type, dir_path in self.directories.items():
            logger.info(f"Initialized {dir_type} directory: {dir_path}")

    def clear_directory(self, dir_type):
        """Clear all CSV files from specified directory."""
        if dir_type not in self.directories:
            raise ValueError(f"Invalid directory type: {dir_type}")
        
        dir_path = self.directories[dir_type]
        logger.info(f"Clearing files from {dir_type} directory: {dir_path}")
        
        files_cleared = 0
        for file in os.listdir(dir_path):
            if file.endswith('.csv'):
                file_path = os.path.join(dir_path, file)
                try:
                    os.remove(file_path)
                    files_cleared += 1
                    logger.info(f"Deleted: {file}")
                except Exception as e:
                    logger.error(f"Error deleting {file}: {e}")
        
        return files_cleared

    def archive_files(self, source_dir_type, archive_suffix=None):
        """Archive files from specified directory with timestamp."""
        if source_dir_type not in self.directories:
            raise ValueError(f"Invalid source directory type: {source_dir_type}")
        
        source_dir = self.directories[source_dir_type]
        archive_dir = self.directories['archive']
        
        if archive_suffix is None:
            archive_suffix = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        files_archived = 0
        for file in os.listdir(source_dir):
            if file.endswith('.csv'):
                # Create archive filename with timestamp
                base_name, ext = os.path.splitext(file)
                archive_name = f"{base_name}_{archive_suffix}{ext}"
                
                source_path = os.path.join(source_dir, file)
                archive_path = os.path.join(archive_dir, archive_name)
                
                try:
                    shutil.copy2(source_path, archive_path)
                    files_archived += 1
                    logger.info(f"Archived {file} to {archive_name}")
                except Exception as e:
                    logger.error(f"Error archiving {file}: {e}")
        
        return files_archived

    def move_to_processed(self):
        """Move files from raw to processed directory after transformation."""
        raw_dir = self.directories['raw']
        processed_dir = self.directories['processed']
        
        # First archive the existing processed files
        self.archive_files('processed')
        
        # Clear the processed directory
        self.clear_directory('processed')
        
        # Move files from raw to processed
        files_moved = 0
        for file in os.listdir(raw_dir):
            if file.endswith('.csv'):
                source_path = os.path.join(raw_dir, file)
                dest_path = os.path.join(processed_dir, file)
                
                try:
                    shutil.move(source_path, dest_path)
                    files_moved += 1
                    logger.info(f"Moved {file} to processed directory")
                except Exception as e:
                    logger.error(f"Error moving {file} to processed: {e}")
        
        return files_moved

    def get_directory_path(self, dir_type):
        """Get the absolute path for a specific directory type."""
        if dir_type not in self.directories:
            raise ValueError(f"Invalid directory type: {dir_type}")
        return self.directories[dir_type]

def main():
    """Main function to demonstrate usage."""
    manager = DataPipelineManager()
    
    # Example usage
    logger.info("Starting file management operations...")
    
    # Clear raw files directory
    files_cleared = manager.clear_directory('raw')
    logger.info(f"Cleared {files_cleared} files from raw directory")
    
    # After transformation (commented out as example)
    # files_moved = manager.move_to_processed()
    # logger.info(f"Moved {files_moved} files to processed directory")

if __name__ == "__main__":
    main() 