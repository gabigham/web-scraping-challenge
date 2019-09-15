# Code for web scraping challenge for UC Davis bootcamp
# written by George Bigham

from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from splinter.exceptions import ElementDoesNotExist
import re

executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)

def news():
    # scrapes article titles and news from mars.nasa.gov
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    titles = []
    news = []

    for i in range(5):
         # Click the 'More' button five times
        try:
            browser.click_link_by_text('More')
        except:
            print("Scraping Complete")
        
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')   
    articles = soup.find_all('li', class_='slide')
    
    # Iterate through each book
    for article in articles:     
        news_title = article.find('div', class_="content_title").text.strip()
        news_p = article.find('div', class_="article_teaser_body").text.strip()
        titles.append(news_title)
        news.append(news_p)
       
    db = {"news_titles":titles, "news_p":news}

    return db


def featured_image():
    # scrapes featured space image url from jpl.nasa.gov
    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(featured_image_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image_url = soup.find('article', class_='carousel_item')['style']
    image_url = image_url.partition("'")[2].partition("'")[0]
    featured_image_url = 'https://www.jpl.nasa.gov' + image_url

    return featured_image_url


def weather():
    # scrapes latest weather info from nasa mars twitter
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    tweets = soup.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    latest_weather = ""
    for tweet in tweets:
        if tweet.text[0:7] == "InSight":
            latest_weather = tweet.text

    return latest_weather


def hemisphere_images():
    # scrapes high quality hemisphere image urls from USGS
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
    
    return hemisphere_image_urls