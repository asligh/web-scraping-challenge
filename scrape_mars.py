import pandas as pd
import time
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager

#JSON viewer URL http://jsonviewer.stack.hu/

RED_PLANET_URL       =  "https://redplanetscience.com/"
MARS_IMAGES_URL      =  "https://spaceimages-mars.com/"
PLANET_FACTS_URL     =  "https://galaxyfacts-mars.com/"
MARS_HEMISPHERES_URL =  "https://marshemispheres.com/"

mars_facts={}

#Sergeant Function
def scrape() -> dict:
    scrape_red_planet()
    scrape_mars_images()
    scrape_planet_facts()
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

    news_title = None
    news_body  = None
    featured_news = []

    for news_item in news_items:
        
        news_title = news_item.find('div',class_='content_title').text
        news_body = news_item.find('div',class_="article_teaser_body").text
        
        featured_news.append({"news_title"     : news_title, "news_paragraph" : news_body}) 
        
        mars_facts["featured_news"]=featured_news
        
        break #only take first news item

    browser.quit()

def scrape_mars_images():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser         = Browser('chrome', **executable_path, headless=False)  

    browser.visit(MARS_IMAGES_URL)
    time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')
    mars_images_url = browser.url
    mars_image_wrapper = soup.find_all('div', class_='floating_text_area')[0]
    img_target_url = mars_image_wrapper.find('a')['href']
    featured_image_url = [mars_images_url + img_target_url]

    mars_facts["featured_image"] = featured_image_url    

    browser.quit()


def scrape_planet_facts():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser         = Browser('chrome', **executable_path, headless=False)    

    url = PLANET_FACTS_URL
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")    

    df_column_1_name = "Description"
    df_column_2_name = "Mars"
    df_column_3_name = "Earth"

    descriptions = []
    mars_fcts   = []
    earth_fcts  = []

    mars_idx  = 0
    earth_idx = 1

    planet_facts_wrapper = soup.find('div', class_='diagram')
    planet_fact_table    = planet_facts_wrapper.find('table', class_="table")
    planet_fact_rows     = planet_fact_table.find_all('tr')

    for planet_fact_row in planet_fact_rows:
        row_desc = planet_fact_row.find('th').text.strip()
        descriptions.append(row_desc)
        
        facts = planet_fact_row.find_all('td')
        
        mars_fact  = facts[mars_idx].text.strip()
        earth_fact = facts[earth_idx].text.strip()
        
        mars_fcts.append(mars_fact)
        earth_fcts.append(earth_fact)

    planet_facts_df = pd.DataFrame({
                                        df_column_1_name: descriptions, 
                                        df_column_2_name: mars_fcts,
                                        df_column_3_name: earth_fcts,
                                })
    
    planet_facts_df.set_index(df_column_1_name,inplace=True)
    
    planet_facts_html = planet_facts_df.to_html(buf=None, 
                                                columns=None, 
                                                header=True, 
                                                index=True, 
                                                na_rep='NaN', 
                                                formatters=None, 
                                                float_format=None, 
                                                sparsify=None, 
                                                index_names=True, 
                                                justify=None, 
                                                bold_rows=True, 
                                                classes=None, 
                                                escape=True, 
                                                max_rows=None,
                                                max_cols=None, 
                                                show_dimensions=False, 
                                                notebook=False )

    planet_facts_html = planet_facts_html.replace("right","left")
    
    mars_facts["planet_facts"] = [planet_facts_html]  

    browser.quit()    

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
                image_dict = {"title":title,"img_url":img_url}
                hemisphere_image_urls.append(image_dict)
                break

    mars_facts["mars_images"] = hemisphere_image_urls

    browser.quit()    

#Test
#scrape()