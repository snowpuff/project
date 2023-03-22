# Import the required modules
from bs4 import BeautifulSoup
import requests
import re
from concurrent.futures import ThreadPoolExecutor
import threading
from urllib.parse import urljoin
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as sa
import os.path

# Open the file with crawled links
crawled_txt = open("crawled.txt", "r")
# Create a set of crawled links from the file
crawledpages = set(line.strip() for line in crawled_txt)

# file for writing review collected links
review_collected = open("reviewcollectedpages.txt", "r+")
reviewcollected = set(line.strip() for line in review_collected)

# Create a sentiment analyzer object 
sss = sa()

# Define a function that gets reviews from a given url and page number and adds them to li list
def getreviews(url, pageno):
    print(f"Obtaining comments from {pageno} page of {total} ")
    page = requests.get(url)
    s = BeautifulSoup(page.content, 'html.parser')
    comments = s.find_all('div', {"class": 't-ZTKy'})

    for com in comments:
        try:
            txt = com.text
            if txt.endswith("READ MORE"):
                txt = txt[:-9]
            lock.acquire()
            li.append(txt+"\n")  
            lock.release()
        except:
            pass

# Loop through each link in crawledpages that is not in reviewcollected 
for i in crawledpages-reviewcollected:
    try:
        # Extract product name from link
        pname = re.search("com/(.*)/p/", i)
        pnm = pname[1]
        # Create filename by joining current working directory path with product name and '.txt' extension
        filename = os.path.join(os.getcwd(),"reviews",pnm+".csv")
        # create and open file with that name
        f = open(filename, "w",encoding="utf-8")
        # get review page link present in last 'a' of div < class = col JOpGWq >
        p1 = requests.get(i)
        bs1 = BeautifulSoup(p1.content, 'html.parser')
        o = bs1.find('div', {'class': 'col JOpGWq'})
        v = o.find_all('a')
        p1url = urljoin("https://flipkart.com", v[-1].get('href'))
        #get total no of review pages available
        page = requests.get(p1url)
        s = BeautifulSoup(page.content, 'html.parser')
        pagecontent = s.find('div', {"class": "_2MImiq _1Qnn1K"})
        try:
            spancontent = pagecontent.find('span')
            text = re.sub(",", "", spancontent.text) 
            r = re.search("of ([\d]*)", text)  
            total = int(r[1])
        except:
            total=1
        #list where reviews of product will be stored
        li = []
        lock = threading.Lock()

        # mm=max(1,min(total//4,50))
        executor = ThreadPoolExecutor(max_workers=12)
        #create url for each review page from  1 to toal and submit to thread pool
        for j in range(1, total+1):
            url = p1url+"&page="+str(j)
            executor.submit(getreviews, url, j)
        executor.shutdown(wait=True)
        #get positive negative neutral and compound scores for a product using vaderSentiment analyzer
        pos = 0
        neg = 0
        neu = 0
        compound = 0
        #write all the reviews to file /reviews/productname.txt and also compute scores

        if len(li)==0:
            continue
        for j in li:
            f.write(j+','+str(sss.polarity_scores(j)['pos']))
            f.write(','+str(sss.polarity_scores(j)['neg'])+',')
            f.write(str(sss.polarity_scores(j)['neu'])+','+str(sss.polarity_scores(j)['compound'])+'\n')
            pos += sss.polarity_scores(j)['pos']
            neg += sss.polarity_scores(j)['neg']
            neu += sss.polarity_scores(j)['neu']
            compound += sss.polarity_scores(j)['compound']
        #write the scores in csv file along with link
        with open("rr.csv","a+",encoding="utf-8") as rr:
            rr.write(i+',')
            rr.write(str(pos/len(li))+',')
            rr.write(str(neg/len(li))+',')
            rr.write(str(neu/len(li))+',')
            rr.write(str(compound/len(li))+'\n')
        #write the link to review collected
        review_collected.write(i+'\n')
        print("Total Comments: ", len(li))
        print("***********completed**********")
        f.close()
    #write all errors in errors.txt and if file is created delete it.
    except Exception as e:
        with open("errors.txt", "a+") as err:
            err.write(i+'\n')
            err.write(str(e)+'\n')
            err.write("****************\n")


crawled_txt.close()
review_collected.close()
