# Data Processing Flow Documentation

## Overview
This document outlines the data processing workflow for the Stock Market Analysis project. The process is designed to handle stock market derivatives data, specifically focusing on futures and index data.

## Architecture

The data processing system is built with a modular architecture consisting of four main components:

1. **Logger**: Handles all logging operations
2. **PathManager**: Manages file paths and directory structures
3. **SparkManager**: Manages Spark session lifecycle
4. **DataProcessor**: Handles the core data transformation logic

### Directory Structure
```
project_root/
├── data/
│   ├── raw/           # Raw CSV files from data acquisition
│   ├── processed/     # Processed and filtered data
│   └── archive/       # Archived historical data
├── logs/              # Application logs
└── temp/              # Temporary Spark files
```

## Processing Flow

### 1. Initialization
- Set up logging configuration
- Create necessary directories
- Initialize Spark session with optimized configurations

### 2. Data Loading
```python
# Get latest two CSV files from raw directory
files = [f for f in os.listdir(raw_dir) if f.endswith('.csv')]
files.sort(reverse=True)
current_data, previous_data = files[:2]
```

### 3. Data Transformation
The transformation process includes several steps:

#### a. Column Selection
Selected columns:
- INSTRUMENT
- SYMBOL
- EXPIRY_DT
- OPTION_TYP
- CLOSE
- OPEN_INT
- CHG_IN_OI

#### b. Instrument Filtering
```python
# Filter for specific instrument types
data = data.filter(col("INSTRUMENT").isin(["FUTIDX", "FUTSTK"]))
```

#### c. Expiry Date Filtering
- Calculate last Thursday of current month
- Filter data for the calculated expiry date
```python
expiry_date = last_thursday.strftime("%d-%b-%Y")
data = data.filter(col("EXPIRY_DT") == expiry_date)
```

### 4. Data Storage
The processed data is saved in two formats:

#### a. Spark CSV Format
```python
data.write.format("csv")
    .mode("overwrite")
    .option("header", "true")
    .save(processed_dir)
```

#### b. Pandas CSV Format
```python
data.toPandas().to_csv(processed_file, index=False)
```

## Error Handling

The system implements comprehensive error handling:

1. **File Operations**
   - Checks for minimum required files
   - Validates file formats and contents
   - Handles file read/write errors

2. **Data Processing**
   - Validates data transformations
   - Handles missing or invalid data
   - Tracks record counts at each step

3. **Spark Operations**
   - Manages Spark session lifecycle
   - Handles temporary directory cleanup
   - Manages memory and resource allocation

## Logging

Detailed logging is implemented at each step:

```
%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

Log levels:
- INFO: Normal operation events
- ERROR: Critical issues requiring attention
- WARNING: Non-critical issues

## Performance Considerations

1. **Spark Configuration**
   ```python
   SparkSession.builder
       .config("spark.driver.tempDir", "temp")
       .config("spark.sql.broadcastTimeout", "3600")
       .config("spark.cleaner.referenceTracking.cleanCheckpoints", "true")
   ```

2. **Memory Management**
   - Efficient column selection
   - Early filtering to reduce data size
   - Proper cleanup of temporary files

## Usage

To run the data processing:

```bash
python src/data_processing/processor.py
```

The script will:
1. Process the latest two CSV files from the raw directory
2. Apply all transformations
3. Save results in the processed directory
4. Generate detailed logs in the logs directory

## Dependencies

- Python 3.x
- PySpark
- Pandas
- Python Standard Library (os, logging, datetime) 