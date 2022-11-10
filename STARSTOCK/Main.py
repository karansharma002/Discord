
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from discord import Webhook, RequestsWebhookAdapter
import discord
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException,TimeoutException

def scraper():
    raffles = []
    options = Options()
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-infobars')
    options.add_extension('adblock.crx')
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(20)
    driver.implicitly_wait(5)
    driver.get('https://www.soleretriever.com/raffles')
    sleep(2)
    last_height = driver.execute_script("return document.body.scrollHeight")
    num = 0
    while True:
        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
        sleep(2)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            sleep(1)

        last_height = new_height
        num += 1
        if num >= 3:
            break

    x = 7

    while True:
        if x == 7:
            x = 8
        
        sleep(1)
        y = 1
        try:

            item = driver.find_element_by_xpath(f'//*[@id="__next"]/div[2]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/a[{x}]/div/div[2]/div[3]/div/div/a')
            item.click()
        
        except NoSuchElementException:
            x = 1
            driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div[1]/div[2]/div[2]/div[2]/div[2]/div[2]/ul/li[5]/a').click()
            sleep(3)
            item = driver.find_element_by_xpath(f'//*[@id="__next"]/div[2]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/a[{x}]/div/div[2]/div[3]/div/div/a')
            item.click()
            
        sleep(1)
        while True:
            try:

                image_url = driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div[1]/div[2]/div[1]/div/div[1]/div[2]/img').get_attribute('src')
                sleep(0.5)
                closed = driver.find_element_by_xpath(f'//*[@id="__next"]/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]/div[{y}]/a[2]/div[1]/h2')
                t = closed.text
                print(t)
                if 'Closed' in t:
                    driver.back()
                    break

                else:
                    if t in raffles:
                        continue
                    else:
                        raffles.append(t)

                sleep(1)
                raffle = driver.find_element_by_xpath(f'//*[@id="__next"]/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]/div[{y}]/div/div/a')
                raffle.click()
                sleep(2)
                try:

                    a = driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div[1]/div[2]/div[1]/div[3]/div[1]/div[2]')
                
                except NoSuchElementException:
                    driver.refresh()
                    sleep(1)
                    a = driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div[1]/div[2]/div[1]/div[3]/div[1]/div[2]')
                
                sleep(0.5)
                b = driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div[1]/div[2]/div[1]/div[3]/div[3]/div[2]')
                sleep(0.5)
                c = driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div[1]/div[2]/div[1]/div[3]/div[5]/div[2]')
                sleep(0.5)
                d = driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div[1]/div[2]/div[1]/div[3]/div[7]/div[2]')     
                sleep(0.5)
                e = driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div[1]/div[2]/div[1]/div[3]/div[12]/div/a')
                enter_at = e.text
                link = e.get_attribute('href')
                sleep(0.5)
                f = driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div[1]/div[2]/div[1]/div[3]/div[9]/div[2]')
                embed=discord.Embed(title = 'Testing the elements',color=0xff8800)
                embed.add_field(name="Region:", value=f"{d.text}", inline=True)
                embed.add_field(name="Type:", value=f"{c.text}", inline=True)
                embed.add_field(name="Delivery:", value=f"{f.text}", inline=True)
                embed.add_field(name="Open:", value=f"{a.text}", inline=True)
                embed.add_field(name="Close:", value=f"{b.text}", inline=True)
                embed.add_field(name="Entry:", value=f"[{enter_at}]({link})", inline=True)
                embed.set_image(url = image_url)
                webhook = Webhook.from_url("https://discord.com/api/webhooks/827500121745784833/ymuzwbFh8sDUBvG2KRF04lauPNQ9QPaETitnsr1Es7GB8FEgsLxHpOxcc1nxnExSs2DW", adapter=RequestsWebhookAdapter())
                webhook.send(embed = embed)
                y += 1
                driver.back()
                sleep(1)
            
            except TimeoutException as e:
                print(e)
                y += 1
                driver.back()
                sleep(1)
                continue
        
        x += 1
        sleep(2)
        
scraper()
