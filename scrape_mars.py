from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager

#JSON viewer URL http://jsonviewer.stack.hu/

RED_PLANET_URL       =  "https://redplanetscience.com/"
MARS_IMAGES_URL      =  "https://spaceimages-mars.com/"
GALAXY_FACTS_URL     =  "https://galaxyfacts-mars.com/"
MARS_HEMISPHERES_URL =  "https://marshemispheres.com/"

mars_facts={}

#Sergeant Function
def scrape() -> dict:
    scrape_red_planet()
    scrape_mars_images()
    scrape_galaxy_facts()
    scrape_mars_hemispheres()
    return mars_facts
    #print(mars_facts)

def scrape_red_planet():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser         = Browser('chrome', **executable_path, headless=False)    

    url = RED_PLANET_URL
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    news_items = soup.find_all('div', class_='list_text')
    news_hash = {}

    news_title = None
    news_body  = None
  
    for news_item in news_items:
        news_title = news_item.find('div',class_='content_title').text
        news_body = news_item.find('div',class_="article_teaser_body").text

        news_hash.update({news_title:news_body})
        mars_facts.update({"latest_mars_news":news_hash})
        break #only take first news item

def scrape_mars_images():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser         = Browser('chrome', **executable_path, headless=False)  
    featured_image_hash = {}

    browser.visit(MARS_IMAGES_URL)
    html = browser.html
    soup = bs(html, 'html.parser')

    mars_images_url     = browser.url
    mars_image_wrapper  = soup.find_all('div', class_='floating_text_area')[0]
    img_target_url      = mars_image_wrapper.find('a')['href']
    featured_image_url  = mars_images_url + img_target_url
    featured_image_hash = {"featured_image":featured_image_url}
    mars_facts.update({"featured_image":featured_image_hash})

def scrape_galaxy_facts():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser         = Browser('chrome', **executable_path, headless=False)    

    url = GALAXY_FACTS_URL
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")    

    equitorial_diameter = "Equatorial Diameter"
    polar_diameter      = "Polar Diameter"
    mass                = "Mass"
    moon                = "Moons"
    orbit_distance      = "Orbit Distance"
    orbit_period        = "Orbit Period"
    surface_temperature = "Surface Temperature"
    first_record        = "First Record"
    recorded_by         = "Recorded By"

    mars_fact_hash = {
                        equitorial_diameter:None,
                        polar_diameter:None,
                        mass:None,
                        moon:None,
                        orbit_distance:None,
                        orbit_period:None,
                        surface_temperature:None,
                        first_record:None,
                        recorded_by:None
                    }

    mars_facts_wrapper = soup.find('table', class_='table-striped')
    body = mars_facts_wrapper.find('tbody')
    table_rows = body.find_all('tr')

    for table_row in table_rows:
        measurement_key   = table_row.find('th').text.replace(':','')
        measurement_value = table_row.find('td').text.replace(':','')
        mars_fact_hash.update({measurement_key:measurement_value})
    
    mars_facts.update({"mars_facts":mars_fact_hash})

def scrape_mars_hemispheres():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser         = Browser('chrome', **executable_path, headless=False)    

    browser.visit(MARS_HEMISPHERES_URL)
    html = browser.html
    soup = bs(html, 'html.parser')
    
    hemisphere_image_urls = []

    time.sleep(1)

    mars_hemispheres_wrapper = soup.find('div', class_='collapsible results')
    hemispheres              = mars_hemispheres_wrapper.find_all('div', class_='item')
    mars_hemispheres_url     = browser.url

    for hemisphere in hemispheres:
        title               = hemisphere.find('h3').text.replace('Enhanced','')
        large_image_nav_url = mars_hemispheres_url + hemisphere.find('a')['href']

        browser.visit(large_image_nav_url)
        html = browser.html
        soup = bs(html, 'html.parser')

        mars_large_image_wrapper = soup.find('div', class_='downloads')
        image_container = mars_large_image_wrapper.find('ul')
        image_items = image_container.find_all('li')

        for image_item in image_items:
            image_pict_desc = image_item.find('a').text

            if 'Sample' == image_pict_desc:
                img_url = mars_hemispheres_url + image_item.find('a')['href']
                hemisphere_image_urls.append({title:img_url})
                break

    mars_facts.update({'hemisphere_image_urls' : hemisphere_image_urls})

#My function to call scrape as a test
#scrape()