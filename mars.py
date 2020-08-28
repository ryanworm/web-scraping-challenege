from splinter import Browser
from bs4 import BeautifulSoup as bs
import time

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")
    parent_headline = soup.find_one("div", "content_title") 
    latest_headline = parent_headline.find("_self")
    mars_data = {
    "latest_headline":latest_headline
}
    browser.quit()
    return mars_data