# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import csv
import re

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_main():
    # Scrape location, location_url (for location report), wave height range
    
    # Initialize browser
    browser = init_browser()

    # Initialize website we want to scrape
    url = 'https://www.surfline.com/surf-reports-forecasts-cams/costa-rica/3624060'
    browser.visit(url)

    # Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Initialize lists for main page data
    location_url = []
    smallest = []
    biggest = []
    locations = []

    # url prefix
    link_prefix = "https://www.surfline.com"

    ## Loop through html elements and add to appropriate list
    for link in soup.find_all('a',class_ = 'sl-cam-list-link'):
        # Add location url to location_url list
        location_url.append((f"{link_prefix}"f"{link['href']}"))
        for location in link.find_all('div', class_ = 'sl-spot-details'):
            for x in location.find_all('h3', class_ = 'sl-spot-details__name'):
                locations.append(x.get_text()) 
        for height in link.find_all('span', class_ = 'quiver-surf-height'):
            # Add smallest and biggest waves to corresponding list
            h = height.get_text()
            pos = h.find('-')
            smallest.append(f"{h[:pos]}{'FT'}")
            biggest.append (f"{h[pos+1:]}")

    if browser is not None:
        # Minimize open browser windows
        browser.quit()

    return (locations, location_url, smallest, biggest)

def scrape_reports():
    # Scrape water and air temperature per location

    # Initialize temperature variables
    water = "Water Temp"
    air = "Wind & Weather"
    # initiate temperature lists 
    water_temp = []
    air_temp = []

    # Initialize browser
    browser = init_browser()

    # Loop through location report sites
    for url in scrape_main()[1]:
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        for item in soup.find_all('div',class_ = 'sl-wetsuit-recommender__weather'):
            for x in item.find_all('div'):
                img = x.find('img', alt=True)
                m = (img['alt'])
                # Grab water temperature
                if re.search(water,m):
                    water_temp.append(x.get_text())
                # Grab air temperature
                if re.search(air,m):
                    air_temp.append(x.get_text())

    if browser is not None:
        # Minimize open browser windows
        browser.quit()

    return (water_temp, air_temp)
    
def zip_lists():
        
    surf_data = [
            list(i) for i in zip(scrape_main()[0], scrape_main()[1],scrape_main()[2],scrape_main()[3],
            scrape_reports()[0], scrape_reports()[1])    
            ]

    return surf_data

    """Export data

    In case you want to save the data in a csv file, use this code:

    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        [writer.writerows([i]) for i in data]"""

    """Import data

    In case you saved the data in a csv file and would like to import, use this code:

    #data = []
    with open('output.csv') as csvfile:
        reader  = csv.reader(csvfile)
        data = [row for row in csv.reader(csvfile)]"""