from bs4 import BeautifulSoup
import requests
import pandas as pd



def web_scraping():
    books = []
    for i in range(1,20):
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
            
    df = pd.DataFrame(books,columns=['book_title','price','rating'])
    df.to_csv('data/books.csv',index=False)

