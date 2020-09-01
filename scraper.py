from flask import Flask, Response
from splinter import Browser
from bs4 import BeautifulSoup as bs
import datetime as dt
import pandas as pd
import time
import requests


def scrape_all():
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    mars_title, mars_text_div = mars_news(browser)

    # mars_title, mars_text_div, featured_image_url, facts_df, mars_list_dict = scrape(browser)

    data_dict = {
        "news_title": mars_title,
        "news_paragraph": mars_text_div,
        "img": featured_img(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser)
        }

    browser.quit()
    return data_dict

def mars_news(browser):
    url = "https://mars.nasa.gov/news"
    browser.visit(url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    html = browser.html
    news_soup = bs(html, "html.parser")

    try:
        # getting the first header and description content
        mars_slide = news_soup.select_one("ul.item_list li.slide")
        mars_title = mars_slide.find("div", class_="content_title").get_text()
        mars_text_div = mars_slide.find(
            "div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return mars_title, mars_text_div

    # returning picture

def featured_img(browser):
    img_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(img_url)
    time.sleep(1)

    full_image_elem = browser.find_by_id("full_image")
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_elem = browser.find_link_by_partial_text("more info")
    more_info_elem.click()
    html = browser.html
    img_soup = bs(html, "html.parser")

    img = img_soup.select_one("figure.lede a img")
    try:
        rel_img_path = img.get('src')

    except AttributeError:
        return None

    mars_img_url = 'https://www.jpl.nasa.gov'+rel_img_path
    # featured_image_url="https://www.jpl.nasa.gov"+relative_image_path
    
    return mars_img_url

# getting mars facts

def mars_facts():
    facts_url = "https://space-facts.com/mars/"

    try:
        facts_table = pd.read_html(facts_url)[0]
    except AttributeError:
        return None

    facts_table.columns = ['Description', 'Value']
    facts_table.set_index('Description', inplace=True)
    facts_df = facts_table.to_html(classes="table table-striped")
    return facts_df

    # relative_fact_path = soup.find_all('a',class_='fancybox')[0]['data-fancybox-href']
    # featured_fact_url="https://www.jpl.nasa.gov"+relative_fact_path


# getting the pictures of mars hemispheres

def hemispheres(browser):
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)

    hemisphere_links = []

    for x in range(4):
        browser.find_by_css("a.product-item h3")[x].click()
        hemisphere_data = scrape_hemisphere(browser.html)
        hemisphere_links.append(hemisphere_data)
        browser.back()

    return hemisphere_links
    # response = requests.get(hemisphere_url)
    # soup = bs(response.text, 'lxml')

def scrape_hemisphere(html_text):
    hemisphere_soup = bs(html_text, "html.parser")

    try:
        hemi_title_rel = hemisphere_soup.find("h2", class_="title").get_text()
        hemi_img_par = hemisphere_soup.find("a", text="Sample").get("href")

    except AttributeError:
        return None, None

    hemisphere = {
        "title" : hemi_title_rel,
        "img_url" : hemi_img_par
    }
    return hemisphere

# print(img_titles)

if __name__ == "__main__":
    print(scrape_all())
    
