import discord
from discord.ext import commands
import json
from Modules.date_converter import date_hour
from Modules.date_converter import date_min
class profile(commands.Cog):

    #@commands.Cog.listener() [EVENT]
    #@commands.command() [COMMAND]
    def init(self, bot):
        self.bot = bot

    @commands.command()
    async def profile(self,ctx,user:discord.Member = None):
        with open('Config/data.json','r') as f:
            data = json.load(f)

        if user == None:
            author = str(ctx.author.id)
            url = ctx.author.avatar_url
            joined = ctx.author.joined_at.strftime("%A, %B %d %Y @ %H:%M:%S %p")
            fs = ctx.author
        else:
            author = str(user.id)
            if not author in data:
                await ctx.send(f"<:info:833301110835249163> **{user.name}** Hasn't created the account yet.")
                return
            elif not data[author]['items']['Profile Privacy'] == '0':
                await ctx.send(f'`{user.name}` Profile is :lock: Privacy Protected.')
                return
            else:
                url = user.avatar_url
                joined = user.joined_at.strftime("%A, %B %d %Y @ %H:%M:%S %p")
                fs = user


        rank = data[author]['rank']
        level = data[author]['level']
        exp = data[author]['experience']
        cash = data[author]['money']
        bank = data[author]['bank']
        cmd = data[author]['command']        
        prime = 'N/A'
        buffs = data[author]['buffs']
        num = 0
        num += data[author]['items']['Gift Box'] 
        num += data[author]['items']['Rose'] 
        num += data[author]['items']['Bomb'] 
        num += data[author]['items']['Undo Card'] 
        if level == 0:
            level_end = 520
        elif level== 1:
            level_end = 910
        elif level== 2:
            level_end = 1110
        elif level == 3:
            level_end = 1350
        elif level == 4:
            level_end = 1500
        elif level == 5:
            level_end = 1790
        elif level == 6:
            level_end = 1800
        elif level == 7:
            level_end = 1850
        elif level == 8:
            level_end = 1900
        elif level == 9:
            level_end = 1950
        elif level == 10:
            level_end = 2000
        else:
            level_end = 2500
        with open('Config/winning_percentage.json','r') as f:
            win_p = json.load(f)
        
        try:

            a  = 0
            a += win_p[author]['Bet'] 
            a += win_p[author]['Baccarat']
            a += win_p[author]['Roulette'] 
            a += win_p[author]['Russian_Roulette']
            a += win_p[author]['Bet'] 
            a += win_p[author]['Duelbet']
            a += win_p[author]['Race']
            a += win_p[author]['Keno']
            a += win_p[author]['Slots']
            a += win_p[author]['Highlow'] 
            win_percent = a / 1000 * 100

        except KeyError:
            win_percent = 100


        embed=discord.Embed(color=0x9257ff)
        embed.set_author(name=f"{fs}",icon_url=url)
        embed.add_field(name="> <:owner:690956629432205392> Rank:", value=f"> **{rank}**", inline=True)
        embed.add_field(name="> :1234: Level:", value=f"> **{level}**", inline=True)
        embed.add_field(name="> <a:UpgradeWheel:678608354582593546> Experience:", value=f"> **{exp}/{level_end}**", inline=True)
        embed.add_field(name="> :moneybag: Cash:", value=f"> **${cash}**", inline=True)
        embed.add_field(name="> :money_with_wings: Bank:", value=f"> **${bank}**", inline=True)
        embed.add_field(name="> <a:blobhearts:676691258059522068> Commands:", value=f"> **{cmd}**", inline=True)
        embed.add_field(name="> <:defloot:691164712540438559> Inventory", value=f"> **{num} Items**", inline=True)
        embed.add_field(name="> 🎲 Win Rate", value=f"> **{win_percent} %**", inline=True)
        embed.add_field(name="> <:witch:707823149647003649> Active Buffs:", value=f"> **{buffs}**", inline=True)
        embed.set_thumbnail(url = url)
        with open('Config/donators.json','r') as f:
            donators = json.load(f)
        
        if author in donators:
            if date_hour(data[author]['Prime']) <= 0:
                remaining = f"{date_min(data[author]['Prime'])} Minutes"
            else:
                remaining = f"{date_hour(data[author]['Prime'])} Hours"
            embed.set_footer(text = f'Prime Perks Ends in: {remaining}',icon_url= 'https://i.imgur.com/VCvf1ND.gif')
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(profile(bot))