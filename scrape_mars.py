# CONVERT JUPYTER NOTEBOOK TO PYTHON SCRIPT.

# Import dependencies
import pandas as pd
import json
import requests
from bs4 import BeautifulSoup as bs
import splinter
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import time

# Set executable path and initialize chrome browser.


def initialize_browser():
    # For MAC users:
    # executable_path = {'executable path': '../Missions_to_Mars/chromedriver'}
    # return Browser('chrome', **executable_path, headless=False)

    # For Windows users:
    executable_path = {
        'executable path': '../Missions_to_Mars/chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


# Create global dictionary to be loaded in MongoDB.
Mars_Info = {}


################
# NASA MARS NEWS
################

# Create function to scrape latest NASA Mars news.
def scrape_news():

    try:

        # Initialize browser
        browser = initialize_browser()
        #browser.is_element_present_by_css("img.jpg", wait_time=1)

        # View NASA news website using splinter.
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        # Define html object and parse using BeautifulSoup.
        html = browser.html
        soup = bs(html, 'html.parser')
        print(soup.prettify())

        # Specify target webpage element:
        slide_element = soup.select_one("ul.item_list li.slide")

        # Retrieve most recent news title and corresponding paragraph text:
        news_title = slide_element.find(
            'div', class_='content_title').get_text()
        news_p = slide_element.find(
            'div', class_='article_teaser_body').get_text()

        # Display results:
        print(news_title)
        print('---------------')
        print(news_p)

        # Incorporate results into dictionary:
        Mars_Info['news_title'] = news_title
        Mars_Info['news_p'] = news_p

        return Mars_Info

    finally:

        # Quit browser:
        browser.quit()

################
# FEATURED JPL MARS SPACE IMAGE
################


def scrape_featured_image():

    try:

        # Initialize browser
        browser = initialize_browser()
        #browser.is_element_present_by_css("img.jpg", wait_time=1)

        # View JPL website using the splinter module:
        init_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(init_url)

        # Define html object and parse using BeautifulSoup.
        html = browser.html
        soup = bs(html, 'html.parser')
        print(soup.prettify())

        # Specify target webpage element:
        full_image_button = soup.find(class_="button fancybox")

        # Instruct splinter to click on 'FULL IMAGE' button:
        browser.click_link_by_id('full_image')
        time.sleep(2)

        # Instruct splinter to click on 'more info' button:
        browser.click_link_by_partial_text('more info')

        # Parse resulting html page:
        html = browser.html
        image_soup = bs(html, "html.parser")

        # Incorporate results into dictionary:
        Mars_Info['news_title'] = news_title
        Mars_Info['news_p'] = news_p

        return Mars_Info

    finally:

        # Quit browser:
        browser.quit()
