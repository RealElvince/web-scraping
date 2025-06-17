from bs4 import BeautifulSoup
import requests
import pandas as pd



def web_scraping():
    books = []
    for i in range(5,10):
        URL = f"https://books.toscrape.com/catalogue/page-{i}.html"
        page_to_scrape = requests.get(URL)
        print(page_to_scrape)

        soup = BeautifulSoup(page_to_scrape.text,'html.parser')


        # book titles
        ol = soup.find('ol')

        articles = ol.find_all('article',class_="product_pod")


        for article in articles:
            image = article.find('img')
            title = image.attrs['alt']
            star = article.find('p')
            star =  star['class'][1]

            price = article.find('p',class_='price_color').text
            price = price[2:]
            price = (float(price))
            books.append([title,price,star])
            
    df = pd.DataFrame(books,columns=['Book_Title','Price($)','Rating'])
    df.to_csv('books.csv',mode='a',header=False,index=False)

web_scraping()