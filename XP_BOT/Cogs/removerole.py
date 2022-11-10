import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

class removerole(commands.Cog):
    #@commands.Cog.listener() [EVENT]
	#@commands.command() [COMMAND]
	def init(self, bot):
		self.bot = bot
	
	@has_permissions(manage_roles = True)
	@commands.command()
	async def removerole(self,ctx,user: discord.User =None,*,role:str = None):
		if role == None or user == None:
			embed=discord.Embed(description="Usage: removerole `<@user` `<Role Name>`",color=0xff8083)
			embed.set_author(name="Removerole Help", icon_url="https://i.imgur.com/wHD6EKK.jpg")
			embed.set_footer(text="Removes the Given role from user")
			await ctx.send(embed = embed)
			return
			
		else:
			try:
				role = discord.utils.get(ctx.guild.roles, name=role)
				member = ctx.guild.get_member(user.id)
				await member.remove_roles(role)
				await ctx.send(f'<a:ln:678647491624960000> {user.mention} has been removed from the `{role}` Role.')
				
			except Exception :
				await ctx.send(f"<a:alert_1:677763786664312860> Either the User has no Role Or the Role given is invalid.")
				return

	@removerole.error
	async def removerole_error(self,ctx,error):
		if isinstance(error, commands.CheckFailure):
			await ctx.send('<a:alert_1:677763786664312860> You are missing the: `Manage Roles` Permission.')

def setup(bot):
    bot.add_cog(removerole(bot))
