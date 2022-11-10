import discord
from discord.ext import commands
import json

class suggestion(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def suggestion(self,ctx,*,value:str = None):
        with open('Config/guildlogs.json','r') as f:
            data = json.load(f)
        
        guild = str(ctx.guild.id)

        if value == None:
            await ctx.send('<:info:722088058521911296> **Usage:** suggestion `text`')
            return
        
        else:
            def check(message):
                return message.author == ctx.author
            try:
                    
                if not 'Suggestion' in data[guild]:
                    if not ctx.message.author.guild_permissions.administrator:
                        await ctx.send('<a:alert_1:677763786664312860> This command requires a Setup, Contact the `Guild Administrator.`')
                        return
                    else:
                        print('tested')
                        await ctx.send('<:info:722088058521911296> This is one time process, Please enter the Channel ID you would like to pass the Suggestions to in the future: `(reply in the chat)`')
                        
                        msg = await self.bot.wait_for('message',check = check)
                        if msg.content.startswith('<#'):
                            a = msg.content
                            a = a.replace("<","")
                            a = a.replace(">","")
                            a = a.replace("#","")
                        else:
                            a = int(msg.content)
                        await ctx.send(f"<a:ln:678647491624960000> Suggestion Command settings have been Saved.")
                        data[guild]['Suggestion'] = a
                        data[guild]['Suggestion Num'] = 1
                        with open('Config/guildlogs.json','w') as f:
                            json.dump(data,f,indent = 4)
                
                else:
                    channel = self.bot.get_channel(int(data[guild]['Suggestion']))
                    embed=discord.Embed(description = value,color=0x5dfe78)
                    embed.set_author(name = f"{ctx.author} | Suggestion: #{data[guild]['Suggestion Num']}",icon_url= ctx.author.avatar_url)
                    em = await channel.send(embed=embed)
                    await em.add_reaction('👍')
                    await em.add_reaction('👎')
                    data[guild]['Suggestion Num'] += 1
                    with open('Config/guildlogs','w') as f:
                        json.dump(data,f,indent = 3)
            except Exception as e:
                print(e)

def setup(bot):
    bot.add_cog(suggestion(bot))



