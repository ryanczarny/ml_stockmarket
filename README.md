# Using ML to predict stock market changes 
I was interested in looking at the influence of social media and news publications on the overall stock market value of a given company. For this, relatively simple, version of the script, I ended up pulling data from Youtube and Google News. The job would run every 5 minutes and determine the current price of the stock, based on Yahoo Finance, the number of articles published within the last hour searching on the companies name, and the number of Youtube videos posted within the last hour searching on the companies name. I also took the headers from the articles and YT videos and weighted them for positive and negative words found in the titles. 

The first thing to do was the setup a python script that would use the urls to scrape the content from them. I had previous work writing HTML so I thought it would be easiest to parse the raw HTML. Using urllib, I pulled the html for Google News as well as YT Search and decoded it. 

```
url = 'https://news.google.com/search?q=' + query + '%20when%3A1h&hl=en-US&gl=US&ceid=US%3Aen'
yt_url = 'https://www.youtube.com/results?search_query=' + query + '&sp=EgIIAQ%253D%253D'

req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()

html = webpage.decode("utf-8")
```

At that point, I looked for the anchors that each site was using to reference either the article or the video and pulled that information (as well as iterating through the words in the title to determine if they had positive or negative context. 

For Google News

```
for line in range(len(html)):
    if html[line].startswith("</a") and html[line+1].startswith("<h3 class="):
        counter += 1
        article_name = html[line+3].upper().split(" ")
        for word in article_name:
            if word in pos_words:
                positive_inf += 1
            elif word in neg_words:
                negative_inf += 1
```
For YT
```
for line in range(len(html_yt)):
    if html_yt[line].startswith('"url"') and html_yt[line+1].startswith('"runs"') and html_yt[line+2].startswith('"text"'):
        counter_yt += 1
        youtube_title = html_yt[line+2].split(" ")
        for word in youtube_title:
            if word in pos_words:
                yt_pos_words +=1
            elif word in neg_words:
                yt_neg_words += 1
```
The values were then appended to a csv file for each company that was being queried. The script was then run every 5 minutes in using a bash script (a cron job would work just as well, and probably better for this).
```
#!/bin/bash

for ((n=0;n<5000000000;n++))
do
 python3 page_scrape.py
 sleep 300s
done
```
Given that I added additional features to be captured after the script had initially started running, I wrote a script that would clean up rows that didn't contain all of the data that I wanted for the machine learning script. It can be found in the companies directory and called convert_ml.py. This script dumps the prepared files into the 'ml_files' directory and they are ready to be read for fitting. Additionally, it calculated the change in price between the given row and the next, thereby relating the future change in price to the current values. 

Finally, we are going to build the ML script. I used SKLearn's Linear Regression and Random Forest models for this section. Additionally, models were generated for each company individually, with the idea that certain parameters might experience different weights based on the company, and since the company was not a parameter I was introducing to the models, I split them out. 

Reading in the prepared csv file that we generated above, I did a double check of the data and filled any 'nan' values with 0 in the dataframe. Then, the model is trained on the training set, which is split by sklearns train_test_split function. After fitting, I used the models to predict on the total original dataframe and wrote out the original value and values predicted by each model. 

From there, I read in those output files and determined if they were true positives (the value went up and it was predicted to go up), true negatives (the value went down and it was predicted to go down), false positives (the value went down and it was predicted to go up), and false negatives (the value went up and it was predicted to go down).

The accuracy was determined (tp + tn) / total and what I termed the critical failure as well (fp) / total in the analysis.py script in the 'results' directory.  Overall, the scripts tended to be conservatively wrong, as in they predicted it would go down when it went up. Not really surprising as the stock market is much more complex than the number of articles and videos and the positive/negative context of their titles. 
