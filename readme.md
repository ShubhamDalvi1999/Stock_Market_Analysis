<h2 align="center">
  Welcome to My Data Engineering Project!
  <img src="https://media.giphy.com/media/hvRJCLFzcasrR4ia7z/giphy.gif" width="28">
</h2>

<a href="https://komarev.com/ghpvc/?username=yourusername">
  <img align="right" src="https://komarev.com/ghpvc/?username=yourusername&label=Visitors&color=0e75b6&style=flat" alt="Profile visitor" />
</a>

[![wakatime](https://wakatime.com/badge/user/yourbadge.svg)](https://wakatime.com/@yourbadge)

<!-- Intro  -->
<h3 align="center">
        <samp>&gt; Hey There!, I am
                <b><a target="_blank" href="https://yourwebsite.com">Your Name</a></b>
        </samp>
</h3>

<p align="center"> 
  <samp>
    <a href="https://www.google.com/search?q=Your+Name">「 Google Me 」</a>
    <br>
    「 I am a data engineer with a passion for big data and distributed computing 」
    <br>
    <br>
  </samp>
</p>

<p align="center">
 <a href="https://yourwebsite.com" target="blank">
  <img src="https://img.shields.io/badge/Website-DC143C?style=for-the-badge&logo=medium&logoColor=white" alt="yourwebsite" />
 </a>
 <a href="https://linkedin.com/in/yourprofile" target="_blank">
  <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="yourprofile"/>
 </a>
 <a href="https://twitter.com/yourhandle" target="_blank">
  <img src="https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white" />
 </a>
 <a href="https://instagram.com/yourhandle" target="_blank">
  <img src="https://img.shields.io/badge/Instagram-fe4164?style=for-the-badge&logo=instagram&logoColor=white" alt="yourhandle" />
 </a> 
 <a href="https://facebook.com/yourhandle" target="_blank">
  <img src="https://img.shields.io/badge/Facebook-20BEFF?&style=for-the-badge&logo=facebook&logoColor=white" alt="yourhandle"  />
 </a> 
</p>
<br />

<!-- About Section -->
 # About me
 
<p>
 <img align="right" width="350" src="/assets/programmer.gif" alt="Coding gif" />
  
 ✌️ &emsp; Enjoy solving complex data problems <br/><br/>
 ❤️ &emsp; Passionate about big data technologies and distributed systems<br/><br/>
 📧 &emsp; Reach me anytime: your.email@example.com<br/><br/>
 💬 &emsp; Ask me about anything [here](https://github.com/yourusername/yourrepository/issues)

</p>

<br/>
<br/>
<br/>

## Skills and Technologies

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PySpark](https://img.shields.io/badge/PySpark-E25A1C?style=for-the-badge&logo=apache-spark&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-013243?style=for-the-badge&logo=matplotlib&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![VSCode](https://img.shields.io/badge/Visual_Studio-0078d7?style=for-the-badge&logo=visual%20studio&logoColor=white)

<br/>

## Project Overview

This project focuses on analyzing NSE (National Stock Exchange) data using PySpark. The primary objective is to process and transform historical futures data to identify trading signals based on changes in open interest and closing prices. This project demonstrates advanced data engineering techniques and PySpark functionalities.

## Table of Contents
- [Technologies Used](#technologies-used)
- [Skills Demonstrated](#skills-demonstrated)
- [Data Preprocessing](#data-preprocessing)
- [Data Transformation](#data-transformation)
- [Analysis and Filtering](#analysis-and-filtering)
- [Saving Results](#saving-results)
- [Visualizing Data](#visualizing-data)
- [Usage Instructions](#usage-instructions)
- [Contributing](#contributing)
- [License](#license)

## Technologies Used
- **PySpark**: For distributed data processing.
- **Pandas**: For data manipulation and transformation.
- **Matplotlib**: For data visualization.
- **Jupyter Notebook**: For interactive data analysis.

## Skills Demonstrated
- **Data Engineering**: Efficient handling and processing of large datasets.
- **PySpark**: Advanced usage of PySpark DataFrame operations and SQL functions.
- **Data Transformation**: Converting and cleaning data for analysis.
- **Data Analysis**: Identifying trading signals based on predefined conditions.
- **Visualization**: Plotting data distributions for insights.
- **Performance Optimization**: Using repartitioning and coalescing techniques to manage large datasets.

## Data Preprocessing
### Initial Setup
The project begins with the initialization of PySpark and reading the CSV files containing futures data for different dates.

```python
import findspark
findspark.init()

from pyspark.sql import SparkSession

df = SparkSession.builder.appName("NSEProject").getOrCreate()

currentdf = df.read.option("header", "true").option("inferSchema", "true").csv("fo03MAY2023bhav.csv")
prevdf = df.read.option("header", "true").option("inferSchema", "true").csv("fo02MAY2023bhav.csv")
