# Game Price Comparison from Online Stores

## Project Description

This project consists of two main components:

1. **Data Scraping**:
A Python script (`scraping.py`) responsible for scraping game prices from the websites of three popular stores: Media Expert, RTV Euro AGD and X-Kom. The collected data is saved to an Excel file called `ALL_OFFERS.xlsx`.

2. **Data Analysis**:
A Jupyter Notebook (`analysis.ipynb`) contains code for cleaning the collected data, eliminating outliers and visualizing the distribution of game prices and comparing prices between stores using charts.

## Project Structure

- **`scraping.py`**: A script for scraping game price data.

- **`analysis.ipynb`**: A notebook for data analysis (cleaning, eliminating outliers, visualizations).
- **`ALL_OFFERS.xlsx`**: Output file containing the data collected during scraping.

## Required libraries
```pip install beautifulsoup4 selenium pandas matplotlib seaborn numpy```
