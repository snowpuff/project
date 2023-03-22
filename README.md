# Flipkart Product Review Crawler
This project allows you to crawl product pages on Flipkart.com and extract their reviews and get percentage of positive negative neutral and compound reviews/

Add one or more initial product links to uncrawled.txt, Each link should be on a separate line.
After adding the links to "uncrawled.txt", run the "crawler.py" script.
```
python crawler.py <time_in_seconds>
```
the script will run for specified seconds and add crawled links to crawled.txt 
Running scripts again will start from where you left of so script can be manually stopped while running.

Run getreviews.py: After the crawling process is complete, you can extract the reviews using the "getreviews.py" script. This script will extract the reviews for all products in "crawled.txt" and save them in separate files in the "/reviews" directory. It will also generate a CSV file ("rr.csv") containing the positive, negative, neutral, and compound scores for each review, along with the product link. To run the script, enter the following command in the command prompt:
```
python getreviews.py
```
**Requirements**
This project requires the following Python libraries to be installed:

* bs4
* requests
* vaderSentiment

These need to be installed using pip.
