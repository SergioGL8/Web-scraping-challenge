# Import Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import time


def init_browser():
    # Capture path to Chrome Driver & Initialize browser
    executable_path = {'executable_path':"chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_facts_data = {}

    # Visit web page
    nasa = "https://mars.nasa.gov/news/"
    browser.visit(nasa)
    time.sleep(2)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html,"html.parser")

    # Scrapping latest news about mars from nasa
    slide_element = soup.select_one("ul.item_list li.slide")
    news_title = slide_element.find("div",class_="content_title").get_text()
    news_paragraph = slide_element.find("div", class_="article_teaser_body").get_text()
    # Close the browser after scraping
    #browser.quit()
    
    # Mars Featured Image
    browser = init_browser()
    JPL_Mars = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    img_base_url = 'https://www.jpl.nasa.gov'
    browser.visit(JPL_Mars)
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    results = soup.select('a',class_="button fancybox")
    link_list=[]
    for result in results:
    # Error handling
      try:
        img_list = result.get('data-fancybox-href')
               
        if img_list:
          link_list.append(img_list)
           
         
      except Exception as e:
        print(e)
    featured_image_url = img_base_url + link_list[0]
    
    #browser.quit()

    
    # Mars Weather
    # Get Mars weather's latest tweet from the website
    browser = init_browser()
    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)
    html_weather = browser.html
    soup = BeautifulSoup(html_weather, "html.parser")
    mars_weather = soup.find("div", class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0").text
    mars_facts_data["mars_weather"] = mars_weather

    # #### Mars Facts
    browser = init_browser()
    url_facts = "https://space-facts.com/mars/"
    time.sleep(2)
    table = pd.read_html(url_facts)
    table[0]

    df_mars_facts = table[0]
    df_mars_facts.columns = ["Parameter", "Values"]
    clean_table = df_mars_facts.set_index(["Parameter"])
    mars_html_table = clean_table.to_html()
    mars_html_table = mars_html_table.replace("\n", "")
    mars_facts_data["mars_facts_table"] = mars_html_table



    # Mars Hemispheres Web Scraper
def hemisphere(browser):
    # Visit the USGS Astrogeology Science Center Site
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    hemisphere_image_urls = []

    # Get a List of All the Hemisphere
    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}
        
        # Find Element on Each Loop to Avoid a Stale Element Exception
        browser.find_by_css("a.product-item h3")[item].click()
        
        # Find Sample Image Anchor Tag & Extract <href>
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
        
        # Get Hemisphere Title
        hemisphere["title"] = browser.find_by_css("h2.title").text
        
        # Append Hemisphere Object to List
        hemisphere_image_urls.append(hemisphere)
        
        # Navigate Backwards
        browser.back()
    return hemisphere_image_urls

# Helper Function
def scrape_hemisphere(html_text):
    hemisphere_soup = BeautifulSoup(html_text, "html.parser")
    try: 
        title_element = hemisphere_soup.find("h2", class_="title").get_text()
        sample_element = hemisphere_soup.find("a", text="Sample").get("href")
    except AttributeError:
        title_element = None
        sample_element = None 
    hemisphere = {
        "title": title_element,
        "img_url": sample_element
    }
    return hemisphere

# Main Web Scraping Bot
def scrape_all():
    executable_path = {"executable_path": "chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)
    news_title, news_paragraph = (browser)
    img_url = nasa_image(browser)
    mars_weather = twitter_weather(browser)
    facts = mars_facts()
    hemisphere_image_urls = hemisphere(browser)
    timestamp = dt.datetime.now()

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image_url,
        "weather": mars_weather,
        "facts": mars_html_table,
        "hemispheres": hemisphere_image_urls,
        "last_modified": timestamp
    }
    browser.quit()
    return data  

​# Define Main Behavior
if __name__ == "__main__":
    app.run(debug=True)
    
