# Code for web scraping challenge for UC Davis bootcamp
# written by George Bigham

from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from splinter.exceptions import ElementDoesNotExist
import re

# executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
# browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    # scrapes several sites and returns mars_data
    mars_data = {}

    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=True)


    # scrapes article titles and news from mars.nasa.gov
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    titles = []
    news = []

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')   
    article = soup.find('li', class_='slide')
        
    news_title = article.find('div', class_="content_title").text.strip()
    news_p = article.find('div', class_="article_teaser_body").text.strip()
       
    latest_news = {"news_title":news_title, "news_p":news_p}
    mars_data["article"] = latest_news

    # scrape featured space image url from jpl.nasa.gov
    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(featured_image_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image_url = soup.find('article', class_='carousel_item')['style']
    image_url = image_url.partition("'")[2].partition("'")[0]
    featured_image_url = 'https://www.jpl.nasa.gov' + image_url

    mars_data["featured_image"] = featured_image_url

    # scrape latest weather info from nasa mars twitter
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    tweets = soup.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    latest_weather = ""
    for tweet in tweets:
        if tweet.text[0:7] == "InSight":
            latest_weather = tweet.text

    mars_data["weather"] = latest_weather

    # scrape high quality hemisphere image urls from USGS
    hemispheres = ['Cerberus', 'Schiaparelli', 'Syrtis Major', 'Valles Marineris']
    hemisphere_image_urls = []

    for i in range(len(hemispheres)):
        hemisphere = hemispheres[i].replace(" ", "_").lower()
        url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/' + hemisphere + '_enhanced'
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        hem_url = soup.find('div', class_='downloads')
        hemisphere_image_urls.append({"title" : hemispheres[i], \
                                      "img_url" : hem_url.find('a')['href']})
    
    mars_data["hemisphere_images"] = hemisphere_image_urls

    return mars_data