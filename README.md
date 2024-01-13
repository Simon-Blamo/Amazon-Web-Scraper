# Amazon Web Scraper
This Python project aims to assess the credibility of product reviews on Amazon by analyzing reviewer profiles and estimating bias. The script utilizes Selenium for web scraping and is designed to evaluate the likelihood of biased reviews for a given product.

## Features
**Automated Web Scraping:** Utilizes Selenium for automated web browsing, allowing the extraction of customer reviews and reviewer profiles.

**Reviewer Bias Estimation:** Analyzes reviews made by each reviewer to estimate their likelihood of bias. The script considers the distribution of ratings (1-star and 5-star) as indicators.

**Adjusted Average Score Calculation:** Provides an adjusted average score for the product reviews, incorporating the estimated bias of individual reviewers.

## Getting Started
1. Clone the repository:
   
   `git clone https://github.com/Simon-Blamo/Amazon-Web-Scraper.git`
2. Install Dependencies:

   `pip install selenium webdriver_manager`
3. Run the Program:

   `python main.py`
4. Follow On-screen Instructions.
   
  Choose to analyze the default product or enter a custom product URL.
  The script will output results, including biased users and overall statistics.

## Disclaimer
This project is meant for educational and research purposes. Please be aware of the legal and ethical implications of web scraping and adhere to the terms of service of the websites being scraped.


Developed Fall '23.
