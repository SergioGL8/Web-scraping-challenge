# Misson to Mars

# Step 1 - Scraping
# -----------------
# Get the latest  [NASA Mars News](https://mars.nasa.gov/news/) by scraping the website and collect the latest news title and paragragh text.

# Import Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import re


def init_browser():
    # Capture path to Chrome Driver & Initialize browser
    executable_path = {'executable_path':"chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
     # Create a dictionary for all of the scraped data
    mars_data = {}

    # Visit web page
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(2)

    # Scrape page into Soup
    html = browser.html
    new_soup = bs(html, 'html.parser')

    # Scrapping latest news about mars from nasa
    #slide_element = new_soup.select_one("ul.item_list li.slide")
    news_title = new_soup.find("div",class_="content_title").text
    news_p = new_soup.find("div", class_="article_teaser_body").text
    # Close the browser after scraping
    # browser.quit()

    # Add the news date, title and summary to the dictionary
    mars_data["news_title"] = news_title
    mars_data["summary"] = news_p
    
    
    # JPL Mars Space Images - Featured Image
    # --------------------------------------
    # - Visit the url for JPL's Featured Space [Image](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
    # - Use splinter to navigate the site and find the full size jpg image url for the current Featured Mars Image.
    # - Save a complete url string for this image

    # Mars Featured Image
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)
    time.sleep(2)

    # Ask Splinter to Go to Site and Click Button with Class Name full_image
    # <button class="full_image">Full Image</button>
    full_image_button = browser.find_by_id("full_image")
    full_image_button.click()

    # Find "More Info" Button and Click It
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()

    # Parse Results HTML with BeautifulSoup
    html = browser.html
    image_soup = bs(html, "html.parser")

    img = image_soup.select_one("figure.lede a img")
    try:
        img_url = img.get("src")
    except AttributeError:
        return None 

    # Use Base URL to Create Absolute URL
    img_url = f"https://www.jpl.nasa.gov{img_url}"
    
    # Close the browser after scraping
    # browser.quit()

     # Add the image to the dictionary
    mars_data["img_url"] = img_url


    # Mars Weather 
    # ------------
    # - From the [Mars Weather twitter](https://twitter.com/marswxreport?lang=en) account scrape the latest Mars weather tweet from the page.
    # - Save the tweet text for the weather report.

    # Mars weather's latest tweet from the website
    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)
    html_weather = browser.html
    soup = bs(html_weather, "html.parser")
    # Find a Tweet with the data-name `Mars Weather`
    mars_weather = soup.find("div", attrs={"class": "tweet", "data-name": "Mars Weather"})
    try:
        mars_weather = mars_weather.find("p", "tweet-text").get_text()
        mars_weather
    except AttributeError:
        pattern = re.compile(r'sol')
        mars_weather = soup.find('span', text=pattern).text

    # Close the browser after scraping
    # browser.quit()

     # Add the mars weather to the dictionary
    mars_data["mars_weather"] = mars_weather


    # Mars Facts
    # -----------
    # - Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.

    url_facts = "https://space-facts.com/mars/"
    time.sleep(2)
    table = pd.read_html(url_facts)
    table[0]

    df_mars_facts = table[0]
    df_mars_facts.columns = ["Parameter", "Values"]
    clean_table = df_mars_facts.set_index(["Parameter"])
    mars_html_table = clean_table.to_html()
    mars_html_table = mars_html_table.replace("\n", "")
    
    # Add the mars facts to the dictionary
    mars_data["mars_html_table"] = mars_html_table


    # Mars Hemispheres 
    # -----------------------------
    # - Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
    # - You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    # - Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name

    # Visit the USGS Astrogeology Science Center Site
    url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemisphere)
    html = browser.html
    soup = bs(html, 'html.parser')
    mars_hemis=[]

    for i in range (4):
        time.sleep(5)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = bs(html, 'html.parser')
        partial = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ partial
        dictionary={"title":img_title,"img_url":img_url}
        mars_hemis.append(dictionary)
        browser.back()

    mars_data['mars_hemis'] = mars_hemis
    
    # Return the dictionary
    return mars_data