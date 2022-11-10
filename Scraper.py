from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

driver = webdriver.Chrome('chromedriver')
driver.get('https://www.pimkie.fr/c-accessoires-mode')
sleep(2)
last_height = driver.execute_script("return document.body.scrollHeight")


while True:
    # Scroll down to the bottom.
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load the page.
    sleep(2)

    # Calculate new scroll height and compare with last scroll height.
    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        break
    last_height = new_height

response = driver.execute_script("return document.documentElement.outerHTML")
soup = BeautifulSoup(response,'lxml')
app = soup.find_all('a',class_ = 'thumb-link')
for x in app:
    for y in app.find_all('div',class_ = 'product-name'):
        print(y)
        
