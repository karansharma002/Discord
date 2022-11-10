import discord
from discord.ext import commands
import json

class Points(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def addpoints(self,ctx,user:discord.User = None,pt:int = None):
        role1 = discord.utils.get(ctx.guild.roles,name = 'Admin')
        if role1 in ctx.author.roles:
            pass
        else:
            await ctx.send(":tools: You don't have the sufficient permissions for using this command.")
            return

        with open('Config/Data.json') as f:
            data = json.load(f)

        with open('Config/Cache.json') as f:
            cache = json.load(f)

        if not user and not pt:
            await ctx.send(':information_source: Usage: =addpoints `<@User>` `<Points>`')
            return
        
        id_ = str(user.id)
        if not id_ in cache:
            await ctx.send(':warning: User is not registered.')
            return
        
        username = id_
        data[username]['Points'] += pt
        
        with open('Config/Data.json','w') as f:
            json.dump(data,f,indent = 3)
        
        await ctx.send(f':white_check_mark: Added `{pt}` Points to {user} account.')
        
        with open('Config/Data.json') as f:
            data= json.load(f)
        
        pt = data[username]['Points']
        region = data[username]['Region']
        await user.edit(nick = f'[{pt}] {data[username]["Username"]} ({region})')


    @commands.command()
    async def delpoints(self,ctx,user:discord.User = None,pt:int = None):
        role1 = discord.utils.get(ctx.guild.roles,name = 'Admin')
        if role1 in ctx.author.roles:
            pass
        else:
            await ctx.send(":tools: You don't have the sufficient permissions for using this command.")
            return
        with open('Config/Data.json') as f:
            data = json.load(f)

        with open('Config/Cache.json') as f:
            cache = json.load(f)

        if not user and not pt:
            await ctx.send(':information_source: Usage: =removepoints `<@User>` `<Points>`')
            return

        id_ = str(user.id)
        if not id_ in cache:
            await ctx.send(':warning: User is not registered.')
            return
        
        username = id_
        data[username]['Points'] -= pt
        
        with open('Config/Data.json','w') as f:
            json.dump(data,f,indent = 3)
        
        await ctx.send(f':white_check_mark: Deleted `{pt}` Points from {user} account.')
        with open('Config/Data.json') as f:
            data= json.load(f)
        
        points = data[username]['Points']
        region = data[username]['Region']
        await user.edit(nick = f"[{points}] {data[username]['Username']} ({region})")

    @commands.command()
    async def setpoints(self,ctx,user:discord.User = None,pt:int = None):
        role1 = discord.utils.get(ctx.guild.roles,name = 'Admin')
        if role1 in ctx.author.roles:
            pass
        else:
            await ctx.send(":tools: You don't have the sufficient permissions for using this command.")
            return
        with open('Config/Data.json') as f:
            data = json.load(f)

        with open('Config/Cache.json') as f:
            cache = json.load(f)

        if not user and not pt:
            await ctx.send(':information_source: Usage: =setpoints `<@User>` `<Points>`')
            return

        id_ = str(user.id)
        if not id_ in cache:
            await ctx.send(':warning: User is not registered.')
            return

        username = id_
        data[username]['Points'] = pt
        
        with open('Config/Data.json','w') as f:
            json.dump(data,f,indent = 3)
        
        await ctx.send(f':white_check_mark: Successfully modified `{pt}` Points for {user} account.')
        with open('Config/Data.json') as f:
            data= json.load(f)
        
        points = pt
        region = data[username]['Region']
        await user.edit(nick = f'[{points}] {data[username]["Username"]} ({region})')
    
    @commands.command()
    async def win_pts(self,ctx,pts:int = None):
        role1 = discord.utils.get(ctx.guild.roles,name = 'Admin')
        if role1 in ctx.author.roles:
            pass
        else:
            await ctx.send(":tools: You don't have the sufficient permissions for using this command.")
            return
        with open('Config/Settings.json')  as f:
            settings = json.load(f)
        
        if not pts:
            await ctx.send(':information_source: Usage: =win_pts `<POINTS>`')
            return
        
        settings['Win_Points']=  pts

        with open('Config/Settings.json','w') as f:
            json.dump(settings,f,indent = 3)
        
        await ctx.send(f':white_check_mark: Winning Points have been Changed to {pts}')

    @commands.command()
    async def lose_pts(self,ctx,pts:int = None):
        role1 = discord.utils.get(ctx.guild.roles,name = 'Admin')
        if role1 in ctx.author.roles:
            pass
        else:
            await ctx.send(":tools: You don't have the sufficient permissions for using this command.")
            return
        with open('Config/Settings.json')  as f:
            settings = json.load(f)
        
        if not pts:
            await ctx.send(':information_source: Usage: =lose_pts `<POINTS>`')
            return
        
        settings['Lose_Points']=  pts

        with open('Config/Settings.json','w') as f:
            json.dump(settings,f,indent = 3)
        
        await ctx.send(f':white_check_mark: Losing Points have been Changed to {pts}')
    
    @commands.command()
    async def user(self,ctx,user2:discord.User = None):
        with open('Config/Settings.json') as f:
            settings = json.load(f)

        role1 = discord.utils.get(ctx.guild.roles,name = 'Admin')
        role2 = discord.utils.get(ctx.guild.roles,name = 'Moderator')
        if role1 in ctx.author.roles or role2 in ctx.author.roles:
            pass

        elif 'Bot_Channel' in settings:
            if not ctx.channel.id == settings['Bot_Channel']:
                return
        else:
            await ctx.channel.send(':warning: Default BOT channel is not SET.')
            return
            
        with open('Config/Bans.json') as f:
            bans = json.load(f)
        
        user = str(ctx.author.id)
        if user in bans:
            await ctx.send(f":warning: {ctx.author.mention} You don't have the access to use this command. **[BANNED]**")
            return
            
        with open('Config/Data.json') as f:
            data = json.load(f)
        
        with open('Config/Cache.json') as f:
            cache = json.load(f)
        
        if not user2:
            id_ = str(ctx.author.id)
            usr = ctx.author.name
        else:
            id_ = str(user2.id)
            usr = user2.name

        if id_ in cache:
            username = id_
        else:
            await ctx.send(':warning: Account is not registered. Pleaser register using ==register')
            return

        Points = data[username]['Points']
        Wins = data[username]['Wins']
        Loss = data[username]['Loss']
        Best_Map = data[username]['Best_Maps']
        
        if Loss == 0 and Wins == 0:
            KDA = '0%'
        else:
            total_games = int(Wins) + int(Loss)
            KDA = round(int(Wins) / int(total_games) * 100)
            KDA = str(KDA) + '%' 

        embed = discord.Embed(color = discord.Color.blue(),title = f"{usr} STATS")
        embed.add_field(name = 'Points',value = Points,inline = False)
        embed.add_field(name = 'Wins',value = Wins,inline = False)
        embed.add_field(name = 'Loss',value = Loss,inline = False)
        embed.add_field(name = 'Best Map',value = Best_Map,inline = False)
        embed.add_field(name = 'Win Rate',value = KDA,inline = False)
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Points(bot))