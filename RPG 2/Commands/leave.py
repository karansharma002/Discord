import discord
from discord.ext import commands
import json

class Leave(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command(aliases = ['l'])
    async def leave(self,ctx):     
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
        with open('Config/Cache.json') as f:
            cache = json.load(f)
        
        with open('Config/Queue.json') as f:
            queue = json.load(f)
        
        with open('Config/Settings.json') as f:
            settings = json.load(f)

        if 'Max_Players' in settings:
            max_players = settings['Max_Players']
        else:
            max_players = 1
        
        id_ = ctx.author.id

        if not str(id_) in cache:
            await ctx.send(':warning: You are not registered currently. Please register using =register')
            return      
        
        for x in queue:
            if id_ in queue[x]:
                total_players = len(queue[x]) - 1
                queue[x].remove(id_)
                msg = f'{total_players}/{max_players} - {ctx.author.mention} LEFT THE QUEUE'
                embed = discord.Embed(color = discord.Color.dark_orange(),description = msg)
                await ctx.send(embed = embed)   
                with open('Config/Queue.json','w') as f:
                    json.dump(queue,f,indent = 3)    

                return

        await ctx.send(":warning: You haven't joined the QUEUE.") 

def setup(bot):
    bot.add_cog(Leave(bot))