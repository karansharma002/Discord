 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import asyncio
import discord
from selenium.common.exceptions import NoSuchElementException

from discord.ext import commands,tasks
import json
import os
import sys
bot = commands.Bot(command_prefix= '$')

@bot.event
async def on_ready():
    print('-------------- INTITATED THE BOT ----------')


import chat_exporter
@bot.command()
async def save(ctx):
    file = await chat_exporter.quick_export(ctx)
    await ctx.channel.delete()
    channel = await bot.fetch_channel(865905245975740417)
    await channel.send(file = file)


@tasks.loop(minutes = 12)
async def get_data():
    with open('Settings.json') as f:
        settings = json.load(f)
    
    with open('Sent.json') as f:
        sent = json.load(f)

    
    channel = await bot.fetch_channel(863366350964654090)#settings['Channel'])

    profile = webdriver.FirefoxProfile() 
    profile.add_extension(extension='adblock.xpi')
    driver = webdriver.Firefox(firefox_profile=profile) 
    from os.path import abspath
    pt = abspath('adblock.xpi')
    driver.install_addon(pt, temporary=True)
    driver.get('https://wadeingames.com/')
    await asyncio.sleep(2)
    league_num = 1
    match_num = 1

    while True:
        try:
            league_link = driver.find_element_by_xpath(f'//*[@id="example"]/tbody/tr[{league_num}]/td[1]/a')
            title = league_link.text
            league_status = driver.find_element_by_xpath(f'//*[@id="example"]/tbody/tr[{league_num}]/td[5]/span')
            type_ = driver.find_element_by_xpath(f'//*[@id="example"]/tbody/tr[{league_num}]/td[2]/span').text
        
        except NoSuchElementException:
            driver.close()
            driver.quit()
            
        league_link.click()
        await asyncio.sleep(5)
        embed = discord.Embed(color = discord.Color.green(),title = f'{title} | Match DETAILS')
        link = ''
        msg = ''
        while True:
            if type_ == 'Rounds':
                try:
                    await asyncio.sleep(1)
                    score = driver.find_element_by_xpath(f'//*[@id="tablink1"]/table/tbody/tr[{match_num}]/td[2]/a')
                    link = score.get_attribute('href')
                    if link in sent:
                        match_num += 1
                        continue

                    scr = score.text.replace(' ','')
                    scr = scr.split('-')
                    if not score.text.lower() == 'vs':
                        player_1 = driver.find_element_by_xpath(f'//*[@id="tablink1"]/table/tbody/tr[{match_num}]/td[1]/span').text
                        player_2 = driver.find_element_by_xpath(f'//*[@id="tablink1"]/table/tbody/tr[{match_num}]/td[3]/span').text
                        
                        if int(scr[0]) > int(scr[1]):
                            embed.add_field(name = f'{player_1} has won against {player_2}',value = f"[Match Link Here]({link})")
                        else:
                            embed.add_field(name = f'{player_2} has won against {player_1}',value = f"[Match Link Here]({link})")
                        
                        msg += 'SNT'
                        sent[link] = 'SENT'
                        with open('Sent.json','w') as f:
                            json.dump(sent,f,indent = 3)
                    
                    match_num += 1
                    continue

                except NoSuchElementException as e:
                    if not msg == '':
                        await channel.send(embed = embed)
                    match_num = 1
                    msg = ''
                    break

                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    print(e)
                    match_num = 1
                    break
                
            else:
                try:
                    await asyncio.sleep(1)
                    score = driver.find_element_by_xpath(f'//*[@id="main"]/div[3]/div[1]/table/tbody/tr[{match_num}]/td[2]/a')
                    link = score.get_attribute('href')
                    if link in sent:
                        match_num += 1
                        continue
                    scr = score.text.replace(' ','')
                    scr = scr.split('-')
                    if not score.text == 'VS':
                        player_1 = driver.find_element_by_xpath(f'//*[@id="main"]/div[3]/div[1]/table/tbody/tr[{match_num}]/td[1]/span').text
                        player_2 = driver.find_element_by_xpath(f'//*[@id="main"]/div[3]/div[1]/table/tbody/tr[{match_num}]/td[3]/span').text
                        
                        if int(scr[0]) > int(scr[1]):
                            embed.add_field(name = f'{player_1} has won against {player_2}',value = f"[Match Link Here]({link})")
                        else:
                            embed.add_field(name = f'{player_2} has won against {player_1}',value = f"[Match Link Here]({link})")
                        sent[link] = 'SENT'
                        msg = 'TNA'
                        with open('Sent.json','w') as f:
                            json.dump(sent,f,indent = 3)
                        
                    match_num += 1
                    continue

                except NoSuchElementException as e:
                    if not msg == '':
                        await channel.send(embed = embed)
                    msg = ''
                    match_num = 1
                    break

                except Exception as e:
                    print(e)
                    match_num = 1
                    break
                
            await asyncio.sleep(1)
        
        league_num += 1
        driver.back()
            

TOKEN = 'ODIwODg3OTU1MjUyOTY5NDg0.YE7tew.0FxVEpkQgl_3P2tAozUA5nilUH4'
bot.run(TOKEN)