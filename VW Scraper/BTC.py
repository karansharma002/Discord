import requests
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import discord
from discord.ext import commands,tasks
import datetime
import json
import asyncio


bot = commands.Bot(command_prefix= '!',intents = discord.Intents.all())

with open('Data.json') as f:
    data = json.load(f)

driver = webdriver.Firefox()

code = 0

while True:

    driver.get('https://www.google.com')

    input()

    iframe = driver.find_element('xpath', '//*[@id="{733e4e96-de37-474d-9c2d-6ce5e2b14105}{1}"]')
    driver.switch_to.frame(iframe)

    input()

    driver.find_element('xpath', '//*[@id="splashIndustry"]').send_keys('Test')

    input()


    try:
    
        driver.get('https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjolfThk6_5AhXF6jgGHcLiD4AQFnoECAgQAQ&url=https%3A%2F%2Foffice.live.com%2Fstart%2Fword.aspx&usg=AOvVaw0kP4tmyfWWgfnfl_-mCXdY')

        input()

        driver.get('https://www.office.com/launch/word?ui=en-US&rs=US&auth=1#')
        input()
        
        x = driver.find_element('xpath','//*[@id="find_dealer"]/section/section/div/div[1]/div[1]/h5/span[2]/div/div/div/div[1]/p').click()

        time.sleep(2)

        b = driver.find_element('xpath','//*[@id="find_dealer"]/section/section/div/div[1]/div[1]/h5/span[2]/div/div/div/div[2]/div/div/ul/li[1]/a').click()

        time.sleep(2)

        c = driver.find_element('xpath','//*[@id="find_dealer"]/section/section/div/div[2]/div[2]/input')

        c.click()

        time.sleep(2)
    
    except Exception as e:
        print(e)
        continue
    

    while True:
        try:
            c.clear()
            c.send_keys('0900')

            time.sleep(2)

            b = driver.find_element('xpath','//*[@id="style-15"]/div/ul/li[1]').click()

            time.sleep(3)

            c = driver.find_element('xpath',f'//*[@id="find_dealer"]/section/div[2]/div/div/div[5]/div/div[1]/div[1]/div[1]')          
            break 

        except:
            code += 100
            continue
    
    code += 100

    num = 1

    time.sleep(2)

    while True:
        try:
            title = driver.find_element('xpath',f'//*[@id="find_dealer"]/section/div[2]/div/div/div[5]/div/div[1]/div[{num}]/div[1]').text
            
            address = driver.find_element('xpath',f'//*[@id="find_dealer"]/section/div[2]/div/div/div[5]/div/div[1]/div[{num}]/div[5]').text

            pin = address.split('\n')[1]
            pin = pin.split(' ')[1]

        except:
            try:
                address = driver.find_element('xpath',f'//*[@id="find_dealer"]/section/div[2]/div/div/div[5]/div/div[1]/div[{num}]/div[4]').text
                pin = address.split('\n')[1]
                pin = pin.split(' ')[1]
            except:
                break
        
        print(pin)

        num += 1

        if [pin,title,address] in data['Data']:
            continue

        data['Data'].append([pin,title,address])

        

    with open('Data.json', 'w') as f:
        json.dump(data,f,indent = 3)

    

with open('Languages.json','r') as f:
    data = json.load(f)

def language(value):
    return data[value]

sample = []
for x in range(20):
    url = driver.get(f'http://model-gan.com/?cat=10&paged={x+1}')
    lenf = driver.find_elements_by_tag_name('img')
    if lenf == [] or lenf == 'None':
        break
    
    for v in lenf:
        src = v.get_attribute("src")
        vv = v.get_attribute("alt")
        if vv in sample:
            continue
        else:
            sample.append(vv)

        a = translator.translate(str(vv), dest='en')
        filename = wget.download(src, 'kindergartens')
        filenames, file_extension = os.path.splitext(filename)
        os.rename(filename, f"kindergartens/{a.text}{file_extension}")

input()

@bot.event
async def on_ready():
    print('------ STARTED ---------')
    await bot.wait_until_ready()
    print(bot.user)
    scrape_data.start()

@tasks.loop(minutes = 48)
async def scrape_data():
    f = '%H:%M'
    nw = datetime.datetime.strftime(datetime.datetime.now(), f)
    nw = nw.split(':')
    print(nw)
    print(nw[0])

    '''
    if not str(nw[0]) == '04':
        return
    '''

    with open('Settings.json') as f:
        data = json.load(f)

    channel = await bot.fetch_channel(853838520912838678)#data['Channel'])
    channel2 = await bot.fetch_channel(853838520912838678)

    #! BITCOIN LEFT TO BE MINED
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-infobars')
    driver = webdriver.Chrome()#options=options)
    driver.get('https://www.buybitcoinworldwide.com/how-many-bitcoins-are-there/')
    await asyncio.sleep(2)
    left = driver.find_element('xpath','//*[@id="bitcoinsleft"]').text
    print(left)

    #!BIT COIN PRICE AND %CHANGE
    
    driver.get('https://www.coingecko.com/en')
    await asyncio.sleep(2)
    price = driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[7]/div[1]/div/table/tbody/tr[1]/td[4]/span').text
    print(price)
    percent_change = driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[7]/div[1]/div/table/tbody/tr[1]/td[6]/span').text
    print(percent_change)
    

    #! BITCOIN DOMINANCE CURRENT
    
    await asyncio.sleep(1)
    driver.get('https://www.tradingview.com/symbols/CRYPTOCAP-BTC.D/')
    await asyncio.sleep(2)
    num = driver.find_element_by_xpath('//*[@id="anchor-page-1"]/div/div[3]/div[1]/div/div/div/div[1]/div[1]').text
    print(num)
    percent = driver.find_element_by_xpath('//*[@id="anchor-page-1"]/div/div[3]/div[1]/div/div/div/div[1]/div[3]/span[2]').text
    print(percent)

    dt = str(datetime.date.today() - datetime.timedelta(days = 2))
    r = requests.get('https://www.lookintobitcoin.com/django_plotly_dash/app/unrealised_profit_loss/_dash-layout')
    content = json.loads(r.content)

    x = content['props']['children'][0]['props']['figure']['data'][0]['x']
    index_x = x.index(f'{dt}T00:00:00.000Z')
    y = content['props']['children'][0]['props']['figure']['data'][0]['y']
    y = "{:.2f}".format(y[index_x])
    y = y.split('.')
    unrealised_profit_loss = y[1]


    #! STOCK  TO FLOW MODEL BITCOIN EXPECT PRICE

    LINK = 'https://www.lookintobitcoin.com/django_plotly_dash/app/stock_flow/_dash-layout'
    dt = str(datetime.date.today() - datetime.timedelta(days = 1))
    r = requests.get(LINK)
    content = json.loads(r.content)


    #x = content['props']['children'][0]['props']['figure']['data'][0]['x']
    #index_x = x.index(f'{dt}')
    #y = content['props']['children'][0]['props']['figure']['data'][0]['y']
    #predicted_val = "{:.2f}".format(y[index_x])
    predicted_val = 'Not Available'
    embed=discord.Embed(color=0xfb8313)
    embed.set_author(name="Daily BTC Data",icon_url=bot.user.avatar_url)
    embed.add_field(name="Bitcoin Left To Be Mined:", value=f"{left}", inline=False)
    embed.add_field(name="Bitcoin Price", value=f"{price}", inline=False)
    embed.add_field(name="Bitcoin Percentage Change (past 24 hours)", value=f"{percent_change}", inline=False)
    embed.add_field(name="Current Bitcoin Dominance", value=f"{num} ({percent})", inline=False)
    embed.add_field(name = 'Stock to Flow Model Predicted Value',value = f'{predicted_val}',inline = False)
    embed.add_field(name = ' Current Unrealised Profit / Loss',value = f'{unrealised_profit_loss}%',inline = False)
    print('EROR')
    #embed.timestamp = datetime.utcnow()
    await channel.send(embed=embed)
    await channel2.send(embed = embed)

    driver.get('https://bitcointreasuryreserve.com/')
    await asyncio.sleep(5)

    btc_value = driver.find_element_by_xpath('//*[@id="post-4767"]/div/div/div/div/div/div/section/div/div/div/div/div/div[2]/div/div/table/tfoot/tr/td[3]').text
    btc_owned = driver.find_element_by_xpath('//*[@id="post-4767"]/div/div/div/div/div/div/section/div/div/div/div/div/div[2]/div/div/table/tfoot/tr/td[4]').text
    btc_percent = driver.find_element_by_xpath('//*[@id="post-4767"]/div/div/div/div/div/div/section/div/div/div/div/div/div[2]/div/div/table/tfoot/tr/td[5]').text
    embed=discord.Embed(color=0xfb8313)
    embed.set_author(name="COMPANIES BTC DATA",icon_url=bot.user.avatar_url)
    embed.add_field(name="Bitcoin Owned", value=f"{btc_owned}", inline=False)
    embed.add_field(name = 'Total Value of Bitcoin Held by Public Companies',value = btc_value,inline = False)
    embed.add_field(name = 'Percent of Bitcoin Supply Owned by Public Companies',value = f'{btc_percent}',inline = False)
    await channel.send(embed = embed)
    await channel2.send(embed = embed)
    
    driver.close()

@bot.command()
async def setchannel(ctx,channel:discord.TextChannel = None):
    if not channel:
        await ctx.send(':information_source: Usage: !setchannel `<#channel>`')
        return
    
    with open('Settings.json') as f:
        data = json.load(f)
    
    data['Channel'] = channel.id

    with open('Settings.json','w') as f:
        json.dump(data,f,indent = 3)
    
    await ctx.send(':white_check_mark: Channel has been SET!')
        
token = 'ODIwODkxMzg3MjE3MTgyNzQx.YE7wrg.tojF5VIEWKcssfqy0r_m66XLibI'

bot.run(token)
