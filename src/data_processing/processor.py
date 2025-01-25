import os
import logging
from datetime import datetime
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, regexp_replace

class Logger:
    """Handles all logging operations."""
    def __init__(self, log_dir='logs', log_file='data_processing.log'):
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
        self.logger = logging.getLogger('data_processing')
        return self.logger

class PathManager:
    """Manages all path-related operations."""
    def __init__(self, logger):
        self.logger = logger
        self.setup_paths()
        
    def setup_paths(self):
        """Set up all required paths and directories."""
        self.project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.data_dir = os.path.join(self.project_root, "data")
        self.raw_dir = os.path.join(self.data_dir, "raw")
        self.processed_dir = os.path.join(self.data_dir, "processed")
        
        # Ensure directories exist
        os.makedirs(self.raw_dir, exist_ok=True)
        os.makedirs(self.processed_dir, exist_ok=True)
        
        self.logger.info(f"Raw data directory: {self.raw_dir}")
        self.logger.info(f"Processed data directory: {self.processed_dir}")

class SparkManager:
    """Manages Spark session and operations."""
    def __init__(self, logger):
        self.logger = logger
        self.spark = None
        
    def initialize_spark(self):
        """Initialize Spark session."""
        try:
            self.spark = SparkSession.builder \
                .appName("Stock_Derivatives_Analysis") \
                .master("local[2]") \
                .config("spark.driver.tempDir", "temp") \
                .config("spark.sql.broadcastTimeout", "3600") \
                .config("spark.cleaner.referenceTracking.cleanCheckpoints", "true") \
                .getOrCreate()
            
            # Create temp directory if it doesn't exist
            os.makedirs("temp", exist_ok=True)
            
            self.logger.info("Successfully initialized Spark session")
            return self.spark
        except Exception as e:
            self.logger.error(f"Error initializing Spark session: {str(e)}")
            raise
            
    def cleanup(self):
        """Clean up Spark session."""
        try:
            if self.spark:
                # Stop the Spark session
                self.spark.stop()
                self.logger.info("Spark session stopped")
                
                # Clean up temp directory
                if os.path.exists("temp"):
                    import shutil
                    try:
                        shutil.rmtree("temp")
                        self.logger.info("Cleaned up temp directory")
                    except Exception as e:
                        self.logger.warning(f"Could not clean temp directory: {str(e)}")
        except Exception as e:
            self.logger.error(f"Error stopping Spark session: {str(e)}")

class DataProcessor:
    """Handles the main data processing operations."""
    def __init__(self, spark_manager, path_manager, logger):
        self.spark_manager = spark_manager
        self.path_manager = path_manager
        self.logger = logger
        
    def get_latest_files(self):
        """Get the latest two CSV files from raw directory."""
        try:
            files = [f for f in os.listdir(self.path_manager.raw_dir) if f.endswith('.csv')]
            files.sort(reverse=True)  # Sort in descending order
            if len(files) < 2:
                raise Exception(f"Not enough files in raw directory. Found only: {len(files)}")
            return files[:2]  # Return latest two files
        except Exception as e:
            self.logger.error(f"Error getting latest files: {str(e)}")
            raise
            
    def read_data(self, filename):
        """Read CSV file into Spark DataFrame."""
        try:
            file_path = os.path.join(self.path_manager.raw_dir, filename)
            df = self.spark_manager.spark.read \
                .option("header", "true") \
                .option("inferSchema", "true") \
                .csv(file_path)
            self.logger.info(f"Successfully read {filename}")
            return df
        except Exception as e:
            self.logger.error(f"Error reading {filename}: {str(e)}")
            raise

    def get_last_thursday(self):
        """Calculate the last Thursday of the current month."""
        try:
            today = pd.Timestamp.now()
            last_day = today.replace(day=1) + pd.offsets.MonthEnd()
            
            last_thursday = last_day
            while last_thursday.weekday() != 3:  # 3 represents Thursday
                last_thursday -= pd.Timedelta(days=1)
                
            expiry_date = last_thursday.strftime("%d-%b-%Y")
            self.logger.info(f"Calculated expiry date: {expiry_date}")
            return expiry_date
        except Exception as e:
            self.logger.error(f"Error calculating last Thursday: {str(e)}")
            raise
            
    def process_data(self, current_data, previous_data):
        """Process the data according to business requirements."""
        try:
            # Select required columns
            self.logger.info("Selecting required columns...")
            curr_data = current_data.select("INSTRUMENT", "SYMBOL", "EXPIRY_DT", "OPTION_TYP", 
                                         "CLOSE", "OPEN_INT", "CHG_IN_OI")
            prev_data = previous_data.select("INSTRUMENT", "SYMBOL", "EXPIRY_DT", "OPTION_TYP", 
                                          "CLOSE", "OPEN_INT", "CHG_IN_OI")

            # Filter for FUTIDX or FUTSTK
            self.logger.info("Filtering by instrument type...")
            curr_data = curr_data.filter(col("INSTRUMENT").isin(["FUTIDX", "FUTSTK"]))
            prev_data = prev_data.filter(col("INSTRUMENT").isin(["FUTIDX", "FUTSTK"]))
            
            # Get last Thursday for expiry date filtering
            expiry_date = self.get_last_thursday()
            
            # Filter by expiry date
            self.logger.info(f"Filtering by expiry date: {expiry_date}")
            curr_data = curr_data.filter(col("EXPIRY_DT") == expiry_date)
            prev_data = prev_data.filter(col("EXPIRY_DT") == expiry_date)
            
            self.logger.info(f"Records after filtering - Current: {curr_data.count()}, Previous: {prev_data.count()}")
            
            return curr_data, prev_data
            
        except Exception as e:
            self.logger.error(f"Error processing data: {str(e)}")
            raise
            
    def save_processed_data(self, curr_data, prev_data, curr_filename, prev_filename):
        """Save processed data to CSV files."""
        try:
            # Generate filenames
            curr_filtered_filename = f"Filtered_{curr_filename.split('.')[0]}"
            prev_filtered_filename = f"Filtered_{prev_filename.split('.')[0]}"
            
            # Save as Spark CSV files
            self.logger.info("Saving as Spark CSV files...")
            curr_data.write.format("csv").mode("overwrite").option("header", "true") \
                .save(os.path.join(self.path_manager.processed_dir, curr_filtered_filename))
            prev_data.write.format("csv").mode("overwrite").option("header", "true") \
                .save(os.path.join(self.path_manager.processed_dir, prev_filtered_filename))
            
            # Save as Pandas CSV files
            self.logger.info("Saving as Pandas CSV files...")
            curr_data.toPandas().to_csv(
                os.path.join(self.path_manager.processed_dir, f"{curr_filtered_filename}.csv"),
                index=False
            )
            prev_data.toPandas().to_csv(
                os.path.join(self.path_manager.processed_dir, f"{prev_filtered_filename}.csv"),
                index=False
            )
            
            self.logger.info(f"Saved processed files: {curr_filtered_filename}, {prev_filtered_filename}")
            
            # Export visualization data
            self.export_visualization_data(curr_data, prev_data)
            
        except Exception as e:
            self.logger.error(f"Error saving processed data: {str(e)}")
            raise

    def classify_oi_pattern(self, price_change, oi_change):
        """Classify OI pattern based on price and OI changes."""
        if price_change > 0 and oi_change > 0:
            return 'Long Build-up'
        elif price_change < 0 and oi_change > 0:
            return 'Short Build-up'
        elif price_change < 0 and oi_change < 0:
            return 'Long Unwinding'
        elif price_change > 0 and oi_change < 0:
            return 'Short Covering'
        else:
            return 'No Clear Pattern'

    def export_visualization_data(self, curr_data, prev_data):
        """Export processed data for visualization."""
        try:
            # Create visualization data directory if it doesn't exist
            viz_dir = os.path.join(self.path_manager.data_dir, "visualization")
            os.makedirs(viz_dir, exist_ok=True)
            
            self.logger.info("Preparing visualization data...")
            
            # Convert Spark DataFrames to Pandas
            curr_df = curr_data.toPandas()
            prev_df = prev_data.toPandas()
            
            # Merge current and previous data
            merged_df = pd.merge(
                curr_df,
                prev_df[['INSTRUMENT', 'SYMBOL', 'CLOSE', 'OPEN_INT']],
                on=['INSTRUMENT', 'SYMBOL'],
                suffixes=('', '_prev')
            )
            
            # Calculate required metrics
            merged_df['PRICE_CHANGE'] = merged_df['CLOSE'] - merged_df['CLOSE_prev']
            merged_df['PRICE_CHANGE_PCT'] = (merged_df['PRICE_CHANGE'] / merged_df['CLOSE_prev']) * 100
            merged_df['OI_CHANGE_PCT'] = (merged_df['CHG_IN_OI'] / merged_df['OPEN_INT_prev']) * 100
            
            # Apply OI pattern classification
            merged_df['OI_PATTERN'] = merged_df.apply(
                lambda x: self.classify_oi_pattern(x['PRICE_CHANGE'], x['CHG_IN_OI']), 
                axis=1
            )
            
            # Select final columns for visualization
            viz_df = merged_df[[
                'INSTRUMENT', 'SYMBOL', 'EXPIRY_DT', 'OPTION_TYP',
                'CLOSE', 'CLOSE_prev', 'PRICE_CHANGE', 'PRICE_CHANGE_PCT',
                'OPEN_INT', 'OPEN_INT_prev', 'CHG_IN_OI', 'OI_CHANGE_PCT',
                'OI_PATTERN'
            ]]
            
            # Export analysis data
            analysis_file = f"Processed_{datetime.now().strftime('%Y%m%d')}_Analysis.csv"
            viz_df.to_csv(os.path.join(viz_dir, analysis_file), index=False)
            self.logger.info(f"Exported analysis data to {analysis_file}")
            
            # Create and export summary statistics
            summary_df = pd.DataFrame({
                'Metric': [
                    'Total Records',
                    'Unique Instruments',
                    'Unique Symbols',
                    'Long Build-up Count',
                    'Short Build-up Count',
                    'Long Unwinding Count',
                    'Short Covering Count'
                ],
                'Value': [
                    len(viz_df),
                    len(viz_df['INSTRUMENT'].unique()),
                    len(viz_df['SYMBOL'].unique()),
                    len(viz_df[viz_df['OI_PATTERN'] == 'Long Build-up']),
                    len(viz_df[viz_df['OI_PATTERN'] == 'Short Build-up']),
                    len(viz_df[viz_df['OI_PATTERN'] == 'Long Unwinding']),
                    len(viz_df[viz_df['OI_PATTERN'] == 'Short Covering'])
                ]
            })
            
            summary_file = f"Summary_{datetime.now().strftime('%Y%m%d')}.csv"
            summary_df.to_csv(os.path.join(viz_dir, summary_file), index=False)
            self.logger.info(f"Exported summary statistics to {summary_file}")
            
        except Exception as e:
            self.logger.error(f"Error exporting visualization data: {str(e)}")
            raise

def main():
    """Main execution function."""
    # Initialize components
    logger = Logger().logger
    path_manager = PathManager(logger)
    spark_manager = SparkManager(logger)
    
    try:
        # Initialize Spark
        spark_manager.initialize_spark()
        
        # Initialize processor and perform operations
        processor = DataProcessor(spark_manager, path_manager, logger)
        
        # Get latest files
        latest_files = processor.get_latest_files()
        logger.info(f"Processing files: {latest_files}")
        
        # Read data
        current_data = processor.read_data(latest_files[0])
        previous_data = processor.read_data(latest_files[1])
        
        # Process data
        curr_processed, prev_processed = processor.process_data(current_data, previous_data)
        
        # Save processed data
        processor.save_processed_data(curr_processed, prev_processed, latest_files[0], latest_files[1])
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        
    finally:
        spark_manager.cleanup()

if __name__ == "__main__":
    main() 