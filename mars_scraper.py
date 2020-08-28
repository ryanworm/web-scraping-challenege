from splinter import Browser
from bs4 import BeautifulSoup as bs
import datetime as dt
import pandas as pd
import time 

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path)

def scrape_mars():
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    mars_list = {}

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")
    print(soup)

    #getting the first header
    mars_div = soup.find("div", class_="content_title")
    mars_title = mars_div.find_all("a").text
    
    #getting out the picture content
    mars_text_div = soup.find("div", class_="article_teaser_body")
    mars_ptext = mars_text_div.find_all("p").text

    return mars_list

print(scrape_mars())