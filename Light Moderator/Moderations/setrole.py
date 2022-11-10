import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

class setrole(commands.Cog):
    #@commands.Cog.listener() [EVENT]
    #@commands.command() [COMMAND]
	def init(self, bot):
		self.bot = bot
	
	@has_permissions(manage_roles = True)
	@commands.command()
	async def setrole(self,ctx,user: discord.User = None,*,role:str = None):
		if role == None or user == None:
			embed=discord.Embed(description="Usage: setrole `<@user` `<Role Name>`",color=0xff8083)
			embed.set_author(name="Setrole Help", icon_url="https://i.imgur.com/wHD6EKK.jpg")
			embed.set_footer(text="Set the Given role to an user")
			await ctx.send(embed = embed)
			return
		
		else:
			try:
				author = user.name
				role = discord.utils.get(ctx.guild.roles, name=role)
				member = ctx.guild.get_member(user.id)
				await member.add_roles(role)
				await ctx.send(f'<a:ln:678647491624960000> {user.mention} has received the `{role}` Role.')

			except Exception as e:
				await ctx.send(f"<a:alert_1:677763786664312860> An Error Occured.\n:information_source: Make sure **SIVA ROLE** is higher than the given **ROLE**\n:information_source: Make sure the given  **ROLE** Exists.")
				return

	@setrole.error
	async def setrole_error(self,ctx,error):
		if isinstance(error, commands.CheckFailure):
			await ctx.send('<a:alert_1:677763786664312860> You are missing the: `Manage Roles` Permission.')

def setup(bot):
    bot.add_cog(setrole(bot))	
