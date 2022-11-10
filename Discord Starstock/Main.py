import discord
from discord.ext import commands,tasks
from discord.ext.commands import has_permissions
import json

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print('----------------- STARTED ----------------')

@bot.command()
async def setup(ctx,channel:discord.TextChannel = None):
    if not channel:
        await ctx.send(':warning: COMMAND USAGE: $setup `#channel`')
        return
    else:
        with open('Settings.json') as f:
            d = json.load(f)
        
        d['Channel'] = channel.id

        with open('Settings.json','w') as f:
            json.dump(d,f,indent = 3)
        
        await ctx.send('✓ Channel Updated')
        
@bot.command()
async def timeframe(ctx,amount:int = None):
    if not amount:
        return
    else:
        await ctx.send('✓ Timeframe Updated')
'''
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

driver = webdriver.Chrome('chromedriver')
driver.get('https://bitpay.com/insight/#/BCH/mainnet/address/qrfh5807ynvcpvm8ykatd4pmkel84e4jcv4l9z3ehm')
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
        x = driver.find_element_by_xpath('//*[@id="root"]/div/div/div[2]/div/div/div[2]/div[3]/div/div[2]/button')
        x.click()

    last_height = new_height
    num += 1
    if num >= 3:
        break

response = driver.execute_script("return document.documentElement.outerHTML")

soup = bs(response,'html.parser')
app = soup.find_all('div',class_ = 'col px-2 mb-2 mb-sm-3')

for x in app:
    print(x)
    print('------------------------')

    for y in x.find('div',class_ = 'sc-kfzAmx fcxxjR d-flex flex-column text-left text-nowrap mt-2'):
        print(y)
        print('-------------------------------------')

'''

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from time import sleep

driver = webdriver.Chrome('chromedriver')
driver.get('https://bitpay.com/insight/#/BCH/mainnet/address/qrfh5807ynvcpvm8ykatd4pmkel84e4jcv4l9z3ehm')
sleep(3)
num = 1
while True:
    try:
        pt = driver.find_element_by_xpath(f'/html/body/ion-app/ng-component/ion-nav/page-address/ion-content/div[2]/ion-grid/div/div/coin-list/div/ion-grid/ion-row[1]/ion-col/coin/ion-grid/ion-row/ion-col[1]/div/span/a').text
        print(pt)
        sleep(1)
        amount = driver.find_element_by_xpath(f'/html/body/ion-app/ng-component/ion-nav/page-address/ion-content/div[2]/ion-grid/div/div/coin-list/div/ion-grid/ion-row[1]/ion-col/coin/ion-grid/ion-row/ion-col[2]/ion-chip[2]/ion-label').text
        print(amount)
        num += 1
    except NoSuchElementException as e:
        print(e)
        input()
    

input()
