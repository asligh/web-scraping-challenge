from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager

mars_facts={}

RED_PLANET_URL       =  "https://redplanetscience.com/"
MARS_IMAGES_URL      =  "https://spaceimages-mars.com/"
GALAXY_FACTS_URL     =  "https://galaxyfacts-mars.com/"
MARS_HEMISPHERES_URL =  "https://marshemispheres.com/"

#Sergeant Function
def scrape() -> dict:

    scrape_red_planet()
    scrape_mars_images()
    scrape_galaxy_facts()
    scrape_mars_hemispheres()

def scrape_red_planet():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit visitcostarica.herokuapp.com
    url = RED_PLANET_URL
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the average temps
    avg_temps = soup.find('div', id='weather')

    # Get the min avg temp
    min_temp = avg_temps.find_all('strong')[0].text

    # Get the max avg temp
    max_temp = avg_temps.find_all('strong')[1].text

    # BONUS: Find the src for the sloth image
    relative_image_path = soup.find_all('img')[2]["src"]
    sloth_img = url + relative_image_path

    # Store data in a dictionary
    costa_data = {
        "sloth_img": sloth_img,
        "min_temp": min_temp,
        "max_temp": max_temp
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return costa_data


def scrape_mars_images():
    None

def scrape_galaxy_facts():
    None

def scrape_mars_hemispheres():
    None