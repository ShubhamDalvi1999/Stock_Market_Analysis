<h2 align="center">
Stock Market Analysis Dashboard with Apache Spark and Plotly Dash
<img src="https://media.giphy.com/media/hvRJCLFzcasrR4ia7z/giphy.gif" width="28">
</h2>


<p align="center"> 
  <samp>
    <br>
    「 I am a data engineer with a passion for big data, distributed computing, cloud solutions, and data visualization 」
    <br>
    <br>
  </samp>
</p>

<div align="center">
<a href="https://git.io/typing-svg"><img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&random=false&width=435&lines=Spark+%7C+DataBricks+%7C+Power+BI+;Snowflake+%7C+Azure+%7C+AWS;3+yrs+of+IT+experience+as+Analyst+%40+;Accenture+;Passionate+Data+Engineer+" alt="Typing SVG" /></a>
</div>

<p align="center">
 <a href="https://www.linkedin.com/in/shubham-dalvi-21603316b" target="_blank">
  <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="yourprofile"/>
 </a>
</p>
<br />


<!-- About Section -->
# About Me

<p>
 <img align="right" width="350" src="/assets/programmer.gif" alt="Coding gif" />
  
 ✌️ &emsp; Enjoy solving data problems <br/><br/>
 ❤️ &emsp; Passionate about big data technologies, cloud platforms, and data visualizations<br/><br/>
 📧 &emsp; Reach me: shubhamdworkmail@gmail.com<br/><br/>
</p>

<br/>
<br/>
![p1](https://github.com/user-attachments/assets/2879b5bd-1d1a-4121-995e-252101931e56)
![p2](https://github.com/user-attachments/assets/9d108df9-0629-4343-b9f3-9818fcc1a143)
![p3](https://github.com/user-attachments/assets/80531bd8-1b52-403a-833b-efd4223797c1)
![p4](https://github.com/user-attachments/assets/a3b79ee3-2831-4787-8241-5ad5697958bb)

<br/>

## Skills and Technologies
![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Apache Spark](https://img.shields.io/badge/-Apache%20Spark-E25A1C?style=flat-square&logo=apache-spark&logoColor=white)
![Plotly](https://img.shields.io/badge/-Plotly-3F4F75?style=flat-square&logo=plotly&logoColor=white)
![Dash](https://img.shields.io/badge/-Dash-008DE4?style=flat-square&logo=dash&logoColor=white)
![Pandas](https://img.shields.io/badge/-Pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![Git](https://img.shields.io/badge/-Git-F05032?style=flat-square&logo=git&logoColor=white)
![VSCode](https://img.shields.io/badge/-VSCode-007ACC?style=flat-square&logo=visual-studio-code&logoColor=white)

## Project Overview
This project implements a real-time stock market analysis dashboard using Apache Spark for data processing and Plotly Dash for interactive visualization. The system analyzes market trends, detects build-up patterns, and provides actionable insights through an intuitive interface.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Architecture](#project-architecture)
- [Data Processing](#data-processing)
- [Dashboard Components](#dashboard-components)
- [Installation and Usage](#installation-and-setup)

## Features
- Real-time market data processing
- Build-up pattern detection (Long/Short)
- Interactive price and open interest analysis
- Pattern distribution visualization
- Dynamic filtering by instrument and symbol
- Responsive dark-themed UI

## Project Architecture
The project consists of three main components:

### Data Acquisition
- Scrapes market data from SAMCO
- Processes raw NSEFO data files
- Archives historical data

### Data Processing
- PySpark-based data transformation
- Build-up pattern detection
- Statistical analysis

### Visualization
- Interactive Plotly Dash dashboard
- Real-time data updates
- Multiple analysis views

## Data Processing
The system processes market data through several stages:

### Raw Data Collection
- Downloads latest NSEFO data
- Validates data integrity
- Archives historical files

### Transformation
- Filters relevant instruments
- Calculates price and OI changes
- Identifies market patterns

### Analysis
- Generates market statistics
- Detects build-up patterns
- Prepares visualization data

## Dashboard Components
1. Market Overview:
   - Total records and statistics
   - Instrument and symbol counts
   - Pattern distribution

2. Analysis Charts:
   - Price Analysis
   - Open Interest Analysis
   - Build-up Analysis
   - Pattern Distribution

3. Pattern Detection:
   - Long Build-up
   - Short Build-up
   - Long Unwinding
   - Short Covering

## Project Structure

```
project_root/
├── data/               # Data files
│   ├── raw/           # Raw downloaded files from SAMCO
│   ├── processed/     # Transformed and processed files
│   └── archive/       # Historical data archives
├── src/               # Source code
│   ├── data_acquisition/  # Scripts for data downloading
│   │   └── scraper.py    # Web scraper for SAMCO data
│   ├── data_processing/  # Data transformation scripts
│   └── utils/           # Utility scripts
│       └── file_manager.py  # File management utilities
├── temp/              # Temporary files
└── logs/              # Log files
```

## Recent Enhancements
- Improved dashboard UI with better component alignment
- Enhanced dropdown styling and functionality
- Optimized chart dimensions and text sizes
- Added comprehensive error handling
- Implemented modular code structure
- Enhanced data processing pipeline

## Installation and Setup
1. Clone the repository
2. Install required dependencies:
```bash
pip install -r requirements.txt
```
3. Configure your environment variables
4. Run the application:
```bash
python app.py
```

## Components

### Data Acquisition
- `scraper.py`: Downloads the latest two available NSEFO files from SAMCO website

### Data Processing
- Contains scripts for data transformation and analysis

### Utilities
- `file_manager.py`: Manages file operations, directory structure, and data pipeline

## Usage

1. To download latest data:
```bash
python src/data_acquisition/scraper.py
```

2. To process data (after downloading):
```bash
python src/data_processing/transform_data.py
```

## Data Flow
1. Raw data is downloaded to `data/raw/`
2. Data is processed and saved to `data/processed/`
3. Previous versions are automatically archived to `data/archive/`

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

---
Feel free to contribute or reach out if you have any questions or suggestions!
