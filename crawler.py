# Import the required modules
from bs4 import BeautifulSoup as bs
import requests
import sys
from urllib.parse import urljoin
from time import time
import threading
from concurrent.futures import ThreadPoolExecutor


# Open the files for reading and writing crawled and uncrawled links
crawled_txt=open("crawled.txt","r+")
uncrawled_txt=open("uncrawled.txt","r+")
# Create sets of crawled and uncrawled links from the files
crawled=set(line.strip() for line in crawled_txt)
uncrawled=set(line.strip() for line in uncrawled_txt)
# Create an empty set for temporary storage of obtained links
temp=set()
# Get the stop time from the command line 
stoptime=time()+int(sys.argv[1])
# Create a lock object for thread synchronization
lock = threading.Lock()

# function that crawls links from a given url and adds them to temp set if they contain '/p/'
def crawler(url):
    print("Obtaining links from",url)
    obj=requests.get(url)
    soup = bs(obj.content,'html.parser')
    for i in soup.find_all('a'):
        link=urljoin("https://flipkart.com",i.get('href'))
        if '/p/' in link and (link not in crawled):
            lock.acquire()
            temp.add(link)
            lock.release()
            
# Loop until stop time is reached 
while(time()<stoptime):
    try:
        # no.of.threads=max(1,min(len(uncrawled)//4,50))
        executor = ThreadPoolExecutor(max_workers=12)
        for url in uncrawled:
            executor.submit(crawler, url)
        executor.shutdown(wait=True)
        # Update crawled set with uncrawled set
        crawled.update(uncrawled)
        # set temp as new uncrawled set
        uncrawled=temp
        # clear the temp set
        temp=set()
        print("Crawled:",len(crawled))
        print("Uncrawled:",len(uncrawled))
        
    except:
        print("No urls in uncrawled or link does not exist")
print("writing to files")

# Write all crawled links to crawled.txt file
for i in crawled:
    crawled_txt.write(i+'\n')

# Write all uncrowded links to uncrewed.txt file    
for i in uncrawled:
    uncrawled_txt.write(i+'\n')
    
# Close both files     
uncrawled_txt.close()
crawled_txt.close()

