 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from discord import Webhook, RequestsWebhookAdapter
import discord
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException,TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC 





driver = webdriver.Firefox() 


driver.get('https://bitcointreasuryreserve.com/')
sleep(5)
pt = driver.find_element_by_xpath('//*[@id="post-4767"]/div/div/div/div/div/div/section/div/div/div/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]')
print(pt.text)
input()










def scraper():
    page = 1

    raffles = []
    profile = webdriver.FirefoxProfile() 
    profile.add_extension(extension='adblock.xpi')
    extensions = ['uBlock0@raymondhill.net.xpi',]
    driver = webdriver.Firefox(firefox_profile=profile) 

    driver.install_addon('C:\\Users\\Sofia\\Desktop\\Discord Sneaker Raffles\\adblock.xpi', temporary=True)
    
    driver.get('https://www.soleretriever.com/raffles')
    sleep(2)
    x = 1
    while True:
        sleep(2)
        y = 1
        try:
            item = driver.find_element_by_xpath(f'//*[@id="__next"]/div[2]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/a[{x}]/div/div[2]/div[3]/div/div/a')
            item.click()
        
        except NoSuchElementException:
            try:
                if page == 4:
                    return

                x = 1
                page += 1
                driver.get(f'https://www.soleretriever.com/raffles?page={page}')
                sleep(3)
                item = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,f'//*[@id="__next"]/div[2]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/a[{x}]/div/div[2]/div[3]/div/div/a')))
                item.click()
            
            except TimeoutException:
                continue

        
        sleep(2)
        
        while True:
            try:
                image_url = WebDriverWait(driver,9).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[2]/div[1]/div[2]/div[1]/div/div[1]/div[2]/img')))
            
            except NoSuchElementException:
                driver.back()
                break
            
            except Exception as e:
                driver.back()
                break

            image_url = image_url.get_attribute('src')
            sleep(0.9)

            try:
                closed = WebDriverWait(driver,9).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="__next"]/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]/div[{y}]/a[2]/div[1]/h2')))

            except NoSuchElementException:
                driver.back()
                break

            except Exception as e:
                driver.back()
                break

            t = str(closed.text)

            if 'Closed' in t:
                print('NOT')
                driver.back()
                break

            sleep(2)
            try:
                raffle = WebDriverWait(driver,9).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="__next"]/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]/div[{y}]/div/div/a')))
            except Exception as e:
                print('4',e)
                y += 1
                #driver.back()
                sleep(2)
                continue

            raffle.click()
            sleep(2)
            try:

                a = driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div[1]/div[2]/div[1]/div[3]/div[1]/div[2]')
            
            except NoSuchElementException:
                driver.refresh()
                sleep(2)
                a = driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div[1]/div[2]/div[1]/div[3]/div[1]/div[2]')
            
            sleep(0.9)
            b = driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div[1]/div[2]/div[1]/div[3]/div[3]/div[2]')
            sleep(0.9)
            c = driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div[1]/div[2]/div[1]/div[3]/div[9]/div[2]')
            sleep(0.9)
            d = driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div[1]/div[2]/div[1]/div[3]/div[7]/div[2]')     
            sleep(0.9)
            e = driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div[1]/div[2]/div[1]/div[3]/div[12]/div/a')
            enter_at = e.text
            titles = driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/h2')
            titles = titles.text
            link = e.get_attribute('href')
            sleep(0.9)
            f = driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div[1]/div[2]/div[1]/div[3]/div[9]/div[2]')
            msg = f"A New raffle for the {titles} is Live!"
            embed=discord.Embed(title = titles,description = msg, color=0xff8800)
            embed.add_field(name="Region:", value=f"{d.text}", inline=True)
            embed.add_field(name="Type:", value=f"{c.text}", inline=True)
            embed.add_field(name="Delivery:", value=f"{f.text}", inline=True)
            embed.add_field(name="Open:", value=f"{a.text}", inline=True)
            embed.add_field(name="Close:", value=f"{b.text}", inline=True)
            embed.add_field(name="Entry:", value=f"[{enter_at}]({link})", inline=True)
            embed.set_image(url = image_url)

            if not t in raffles: 
                if str(d.text) in ('United States','Europe','Worldwide'):
                    webhook = Webhook.from_url("https://discord.com/api/webhooks/826508313188499486/3Xc4I0ebK_JHj6wQt7TeV3tCUU-pavYNDfzxccV6ipfBGV5WkoXw2QyS55adqusexy93", adapter=RequestsWebhookAdapter())
                    webhook.send(embed = embed)
                    raffles.append(t)

            y += 1
            driver.back()
            sleep(2)
        
        x += 1
        sleep(2)

