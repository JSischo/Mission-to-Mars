# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': 'C:\\Users\\drjef\\chromedriver\\chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemisphere(browser),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):

    # Scrape Mars News    
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    
    except AttributeError:
        return None, None

    return news_title, news_p

def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None
    
    # Use the base URL to create an absolute URL
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    
    return img_url

def mars_facts():
    try:
        # Use "read.html" to scrape the facts table into a dataframe.
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe    
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, ad bootstrap
    return df.to_html()

def hemisphere(browser):
    # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []
    hemispheres = {'title':[], 'img_url':[]}
    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    # Retrieve Cerberus data
    page_link = browser.links.find_by_partial_text('Cerberus')
    page_link.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # find the image url
    img_data_c = img_soup.find('li')
    img_url_c = img_data_c.find('a').get('href')

    # find the image title
    img_title_c = img_soup.find('h2', class_='title').get_text()

    # create dict
    cDict = {}
    cDict['img_url'] = img_url_c
    cDict['title'] = img_title_c
    
    # append to list
    hemisphere_image_urls.append(cDict)
    # append to dictionary
    hemispheres['title'].append(img_title_c)
    hemispheres['img_url'].append(img_url_c)
    
    browser.back()

    # Retrieve Schiaparelli data
    page_link = browser.links.find_by_partial_text('Schiaparelli')
    page_link.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # find the image url
    img_data_s = img_soup.find('li')
    img_url_s = img_data_s.find('a').get('href')

    # find the image title
    img_title_s = img_soup.find('h2', class_='title').get_text()

    # create dict
    sDict = {}
    sDict['img_url'] = img_url_s
    sDict['title'] = img_title_s

    # append to list
    hemisphere_image_urls.append(sDict)
    # append to dictionary
    hemispheres['title'].append(img_title_s)
    hemispheres['img_url'].append(img_url_s)
    
    browser.back()

    # Retrieve Syrtis Major info
    page_link = browser.links.find_by_partial_text('Syrtis')
    page_link.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # find the image url
    img_data_sm = img_soup.find('li')
    img_url_sm = img_data_sm.find('a').get('href')

    # find the image title
    img_title_sm = img_soup.find('h2', class_='title').get_text()

    # create the dict
    smDict = {}
    smDict['img_url'] = img_url_sm
    smDict['title'] = img_title_sm

    # append to list
    hemisphere_image_urls.append(smDict)
    # append to dictionary
    hemispheres['title'].append(img_title_sm)
    hemispheres['img_url'].append(img_url_sm)
    
    browser.back()
    
    # Retrieve Valles Marineris info
    page_link = browser.links.find_by_partial_text('Valles')
    page_link.click()
    
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    # find the image url
    img_data_v = img_soup.find('li')
    img_url_v = img_data_v.find('a').get('href')
    
    # find the image title
    img_title_v = img_soup.find('h2', class_='title').get_text()

    # create the dict
    vDict = {}
    vDict['img_url'] = img_url_v
    vDict['title'] = img_title_v
    
    # append to list
    hemisphere_image_urls.append(vDict)
    # append to dictionary
    hemispheres['title'].append(img_title_v)
    hemispheres['img_url'].append(img_url_v)
    
    return hemisphere_image_urls
    
    
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())


