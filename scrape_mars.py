# CONVERT JUPYTER NOTEBOOK TO PYTHON SCRIPT.

def scrape():

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

    # For MAC users:
    # executable_path = {'executable path': '../Missions_to_Mars/chromedriver'}
    # return Browser('chrome', **executable_path, headless=False)

    # For Windows users:
    executable_path = {
        'executable path': '../Missions_to_Mars/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    ################
    # NASA MARS NEWS
    ################

    # View NASA news website using splinter.
    url = 'https://mars.nasa.gov/news/'
    browser = Browser('chrome', **executable_path, headless=False)
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

    # Quit browser:
    browser.quit()

    ################
    # FEATURED JPL MARS SPACE IMAGE
    ################

    init_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser = Browser('chrome', **executable_path, headless=False)
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

    # Retrieve relevant url for full-size featured image:
    img_url = image_soup.select_one("figure.lede a img").get("src")
    img_url

    # Using the initial url, build the complete url for the full-sized featured image:
    featured_image_url = f"https://www.jpl.nasa.gov{img_url}"

    # Quit browser:
    browser.quit()

    ###########
    # MARS FACTS
    ###########

    # View Mars Facts website using the splinter module:
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)

    # Using Pandas, scrape facts table:
    mars_facts = pd.read_html(facts_url)

    # Assign Mars facts dataframe to 'mars_facts':
    mars_facts = mars_facts[0]

    # Set index and display facts table:
    mars_facts = mars_facts.rename(
        columns={0: 'Mars Planet Profile', 1: ''})
    mars_facts.set_index('Mars Planet Profile')

    # Convert the data to a HTML table string:
    mars_html = mars_facts.to_html(index=False, table_id='fact_table')
    mars_html

    # Quit browser:
    browser.quit()

    ####################
    # MARS HEMISPHERES
    ####################

   # View USGS Astrogeology website using splinter module:
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser = Browser("chrome", **executable_path)
    browser.visit(hemisphere_url)

    # Build a for loop to retrieve a list of the hemisphere image urls:
    hemisphere_image_urls = []

    url = browser.find_by_css("a.product-item h3")
    for i in range(len(url)):
        hemisphere = {}

        # Find element on each loop:
        browser.find_by_css("a.product-item h3")[i].click()

        # Find sample image anchor tag & extract <href> portion:
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]

        # Get hemisphere name(title):
        hemisphere["title"] = browser.find_by_css("h2.title").text

        # Append to list:
        hemisphere_image_urls.append(hemisphere)

        # Navigate backwards:
        browser.back()

        # Display list:
        hemisphere_image_urls

    ################
    # SUMMARIZE INFO
    ################
    Mars_Info = {'headline': news_title,
                 'paragraph': news_p,
                 'featured_image': featured_image_url,
                 'facts': mars_html,
                 'hemispheres': hemisphere_image_urls}

    return Mars_Info
