import discord
from discord.ext import commands
import json

class Queue(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def clearqueue(self,ctx):
        role1 = discord.utils.get(ctx.guild.roles,name = 'Admin')
        role2 = discord.utils.get(ctx.guild.roles,name = 'Moderator')

        if role1 in ctx.author.roles:
            pass
        elif role2 in ctx.author.roles:
            pass
        else:
            await ctx.send(":tools: You don't have the sufficient permissions for using this command.")
            return

        with open('Config/Queue.json') as f:
            queue = json.load(f)
        
        if len(queue) == 0:
            await ctx.send(':warning: There are no active queues.')
            return
            
        queue = {}
        with open('Config/Queue.json','w') as f:
            json.dump(queue,f,indent = 3 )
        
        await ctx.send(':white_check_mark: All queues have been Cleared')
    
    @commands.command()
    async def endseason(self,ctx,channel:discord.TextChannel = None):
        role1 = discord.utils.get(ctx.guild.roles,name = 'Admin')

        if role1 in ctx.author.roles:
            pass
        else:
            await ctx.send(":tools: You don't have the sufficient permissions for using this command.")
            return

        with open('Config/Data.json') as f:
            data = json.load(f)
        def check(m):
            return m.author == ctx.author

        await ctx.send('Are you sure about it? Reply with yes/no')
        confirmation = await self.bot.wait_for('message',check = check)
        if confirmation.content.lower() in ('yes','y'):
            for x in data:
                data[x]['Points'] = 0
                data[x]['Wins'] = 0
                data[x]['Loss'] = 0 
                data[x]['Best_Maps'] = 'NONE'
                user = ctx.guild.get_member(int(data[x]['ID']))
                try:
                    await user.edit(nick = f"[0] {data[x]['Username']} ({data[x]['Region']})")
                except:
                    pass
                with open('Config/Data.json','w') as f:
                    json.dump(data,f,indent = 3)
                
                
            
            await ctx.send(':white_check_mark: Points Resetted')
            return

        else:
            await ctx.send('---- ACTION REVERTED ----')
            return

    @commands.command(aliases = ['q'])
    async def queue(self,ctx):
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
        with open('Config/Queue.json') as f:
            queue = json.load(f)
        
        with open('Config/Settings.json') as f:
            settings = json.load(f)
        
        with open('Config/Cache.json') as f:
            cache = json.load(f)

        if 'Max_Players' in settings:
            max_players = settings['Max_Players']
        else:
            max_players = 1

        msg = ''
        
        current_game = str(cache['Game_Num'])
        if not current_game in queue:
            await ctx.send(':warning: There is no active QUEUE')
            return
            
        for num,x in enumerate(queue[current_game]):
            user = await self.bot.fetch_user(x)
            total_players = len(queue[current_game])
            msg += f'**{num+1}** - {user.mention}\n'
        
        if not msg == '':
            embed = discord.Embed(title = f"{total_players}/{max_players} Players JOINED",color = discord.Color.dark_orange(),description = msg)
            await ctx.send(embed = embed)
        
        else:
            await ctx.send(':warning: No queue is active.')
    

    @commands.command()
    async def replace(self,ctx,user:discord.User = None):
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
            
        if not user:
            await ctx.send(':information_source: Usage: =replace `<@user>` (REPLACES THE USER IN THE GAME)')
            return
        
        with open('Config/Queue.json') as f:
            queue = json.load(f)
        
        with open('Config/Cache.json') as f:
            cache = json.load(f)
        
        if not str(ctx.author.id) in cache:
            await ctx.send(':warning: You are not registered currently. Please register using `=register`')
            return

        with open('Config/Games.json') as f:
            games = json.load(f)

        current_game = str(cache['Game_Num'])
        if not games[current_game]['Status'] in ('REPORTED','CANCELLED'):
            if ctx.author.id in games[current_game]['EDEN'] or ctx.author.id in games[current_game]['NAF'] or ctx.author.id == games[current_game]['Captain1'] or ctx.author.id == games[current_game]['Captain2'] or ctx.author.id in games[current_game]['Players']:
                await ctx.send(':warning: You are already a part of this GAME.')
                return
            if user.id in games[current_game]['EDEN']:
                games[current_game]['EDEN'].remove(user.id)
                games[current_game]['EDEN'].append(ctx.author.id)
            
            elif user.id in games[current_game]['NAF']:
                games[current_game]['NAF'].remove(user.id)
                games[current_game]['NAF'].append(ctx.author.id)

            elif user.id == games[current_game]['Captain1']:
                games[current_game]['Captain1'] = ctx.author.id

            elif user.id == games[current_game]['Captain2']:
                games[current_game]['Captain2'] = ctx.author.id
            
            elif user.id in games[current_game]['Players']:
                games[current_game]['Players'].remove(user.id)
                games[current_game]['Players'].append(ctx.author.id)
            else:
                await ctx.send(':warning: Mentioned user is not a part of active game')
                return

            with open('Config/Games.json','w') as f:
                json.dump(games,f,indent = 3)
            
            await ctx.send(f':information_source: {ctx.author.mention} has replaced with {user.mention}')
            return
            
        else:
            await ctx.send(':warning: The current game is not eligible for this feature.')
            return


    @commands.command()
    async def forceremove(self,ctx,user:discord.User = None):
        role1 = discord.utils.get(ctx.guild.roles,name = 'Admin')
        role2 = discord.utils.get(ctx.guild.roles,name = 'Moderator')

        if role1 in ctx.author.roles:
            pass
        elif role2 in ctx.author.roles:
            pass
        else:
            await ctx.send(":tools: You don't have the sufficient permissions for using this command.")
            return

        if not user:
            await ctx.send(':information_source: Usage: =forceremove `<@user>` (REMOVES THE USER FROM THE QUEUE)')
            return
        
        with open('Config/Queue.json') as f:
            queue = json.load(f)
        
        with open('Config/Cache.json') as f:
            cache = json.load(f)
        

        with open('Config/Games.json') as f:
            games = json.load(f)

        current_game = str(cache['Game_Num'])
        if not len(queue) == 0:
            if user.id in queue[current_game]:
                queue[current_game].remove(user.id)
                with open('Config/Queue.json','w') as f:
                    json.dump(queue,f,indent = 3)
                
                await ctx.send(f':information_source: {user.mention} has been removed from the QUEUE.')
                return
            
            else:
                await ctx.send(':warning: Mentioned user is not a part of active queue')
                return
        else:
            await ctx.send(':warning: The queue is empty')
            return

def setup(bot):
    bot.add_cog(Queue(bot))