from urllib.request import urlopen
from urllib.request import Request, urlopen
from datetime import datetime
from yahoo_fin import stock_info as si
from word_dict import *

now = datetime.now()

queries = ['disney','netflix','tesla','united','amazon','microsoft','bitcoin','dogecoin','universal+studios','shell','bp','twitter','metaverse','berkshire','alibaba','nvidia','apple','google','united+healthcare','p+and+g','thermo+fischer','cisco','adobe','coca+cola','costco','intel','wells+fargo','morgan+stanley','trans+global+group+inc']
tickers = ['DIS','NFLX','TSLA','UAL','AMZN','MSFT','BTC','DOGE-USD','UVV','RDS-A','BP','TWTR','FB','BRK-A','BABA','NVDA','AAPL','GOOG','UNH','PG','TMO','CSCO','ADBE','KO','COST','INTC','WFC','MS','TGGI']


for i in range(len(queries)):
    try:
        query = queries[i]
        url = 'https://news.google.com/search?q=' + query + '%20when%3A1h&hl=en-US&gl=US&ceid=US%3Aen'
        yt_url = 'https://www.youtube.com/results?search_query=' + query + '&sp=EgIIAQ%253D%253D'
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()

        html = webpage.decode("utf-8")
        file_name = query + "_stats.csv"
        output_file = open("./companies/" + file_name,'a+')

        html = html.split(">")
        counter = 0 
        positive_inf = 0
        negative_inf = 0
        for line in range(len(html)):
            if html[line].startswith("</a") and html[line+1].startswith("<h3 class="):
                counter += 1
                article_name = html[line+3].upper().split(" ")
                for word in article_name:
                    if word in pos_words:
                        positive_inf += 1
                    elif word in neg_words:
                        negative_inf += 1
        
        req = Request(yt_url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage_yt = urlopen(req).read()
        html_yt = webpage_yt.decode("utf-8")
        html_yt = html_yt.split("{")
        counter_yt = 0
        yt_pos_words = 0
        yt_neg_words = 0
        for line in range(len(html_yt)):
            if html_yt[line].startswith('"url"') and html_yt[line+1].startswith('"runs"') and html_yt[line+2].startswith('"text"'):
                counter_yt += 1
                youtube_title = html_yt[line+2].split(" ")
                for word in youtube_title:
                    if word in pos_words:
                        yt_pos_words +=1
                    elif word in neg_words:
                        yt_neg_words += 1

        price = si.get_live_price(tickers[i])
        output_file.write(str(now) + "," + query + "," + str(counter) + "," + str(price) + ',' + str(positive_inf) + ',' + str(negative_inf)+',' + str(counter_yt)+ ',' + str(yt_pos_words)+',' + str(yt_neg_words)+ "\n")
        output_file.close()
    except:
        continue
print("done at " + str(now))