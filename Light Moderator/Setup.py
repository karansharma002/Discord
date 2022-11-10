
#MODULES LOADING
import random
import discord
from discord import embeds
#from random import sample
from discord.ext import commands,tasks
from discord.utils import get
from discord.ext.commands import has_permissions, MissingPermissions
import json
import os
import datetime
#!-------------------------------------------------------------------------------------------------------------------------------------								
#*-------------------------------------------------------------------------------------------------------------------------------------
												# --------------------------------------------- #
												#? 			VERSION:  1.5 BETA                  #
												#!		 ----------- FILLORY -----------        #
												#*		 Last Updated on [06/22/2020]           #
												#TODO: 		Project By: Sofia  ;)               #
												# --------------------------------------------- #
#*-------------------------------------------------------------------------------------------------------------------------------------
#!-------------------------------------------------------------------------------------------------------------------------------------

#BOT DEFINE
bot = commands.Bot(command_prefix = '=',case_insensitive=True,intents = discord.Intents.all())

bot.remove_command('help')

#Ready Event
@bot.event
async def on_ready():
	try:
		await bot.change_presence(status=discord.Status.online,activity=discord.Game(f'Watching Members'))
	except Exception as e:
		print(e)
	
	print (F" // ------------------------- LOGGED IN FOR {len(bot.guilds)} GUILDS --------------------------- //")


#ON GUILD JOIN EVENT
@bot.event
async def on_guild_join(guild):
	with open('Config/prefixes.json','r') as f:
		rv = json.load(f)	
	
	with open('Config/guildlogs.json','r') as f:
		data = json.load(f)

	guild = str(guild.id)
	if not guild in rv:
		rv[guild] = {}
		rv[guild]['Prefix'] = 'f.'
		rv[guild]['Join_Message'] = 'Disabled'
		rv[guild]['Leave_Message'] = 'Disabled'
		rv[guild]['Join ID'] = 0
		rv[guild]['Leave ID'] = 0
		rv[guild]['Autorole'] = 'Disabled'
		with open('Config/prefixes.json','w') as f:
			json.dump(rv,f,indent = 3)

	if not guild in data:
		data[guild] = {}
		data[guild]["Channel Logs"] = "Disabled"
		data[guild]["User Logs"] = "Disabled"
		data[guild]["Role Logs"] = "Disabled"
		data[guild]["User ID"]  = "Disabled"
		data[guild]["Role ID"] = "Disabled"
		data[guild]["Channel ID"] = "Disabled"
		with open('Config/guildlogs.json','w') as f:
			json.dump(data,f,indent = 3)


#ON COMMAND EVENT

#JOIN MEMBER EVENT
@bot.event
async def on_member_join(member):
	guild = str(member.guild.id)
	with open('Config/prefixes.json','r') as f:
		data = json.load(f)
	try:
		if data[guild]['Join_Message'] == 'Enabled':
			url = member.avatar_url
			embed=discord.Embed(color=0x00ffff)
			embed.set_author(name="Member Joined",icon_url=url)
			embed.add_field(name="> 📝 **Member Name:**", value=f"> {member.mention}", inline=False)
			embed.add_field(name="> 📝 **Member ID:** ", value=f"> {member.id}", inline=False)
			embed.set_footer(text=f"🆆🅴🅻🅲🅾🅼🅴 🆃🅾 🆃🅷🅴 ({member.guild}).",icon_url = member.avatar_url)
			embed.set_thumbnail(url = url)
			channel = bot.get_channel(int(data[guild]['Join ID']))
			await channel.send(embed = embed)

		if not data[guild]['Autorole'] == 'Disabled':
			role = discord.utils.get(member.guild.roles, name=data[str(member.guild.id)]['Autorole'])
			await member.add_roles(role)

	except Exception:
		pass

#REMOVE MEMBER EVENT
@bot.event
async def on_member_remove(member):
	guild = str(member.guild.id)
	with open('Config/prefixes.json','r') as f:
		data = json.load(f)
	try:
		if data[guild]['Leave_Message'] == 'Enabled':
			url = member.avatar_url
			embed=discord.Embed(color=0xff0000)
			embed.set_author(name="Member Left", icon_url=url)
			embed.add_field(name="> 📝 Member Name:", value=f"> {member.mention}", inline=False)
			embed.add_field(name="> 📝 Member ID: ", value=f"> {member.id}", inline=False)
			embed.set_footer(text="🅷🅾🅿🅴 🆃🅾 🆂🅴🅴 🆈🅾🆄 🆂🅾🅾🅽!")
			embed.set_thumbnail(url = url)
			channel = bot.get_channel(int(data[guild]['Leave ID']))
			await channel.send(embed = embed)
	except Exception:
		pass

#GUILD CHANNEL DELETE EVENT
@bot.event
async def on_guild_channel_delete(channel):
	with open('Config/guildlogs.json','r') as f:
		data = json.load(f)
	
	if data[str(channel.guild.id)]['Channel Logs'] == 'Enabled':
		date = datetime.datetime.now().strftime("%A, %B %d %Y @ %H:%M:%S %p")
		key = data[str(channel.guild.id)]["Channel ID"]
		a = bot.get_channel(int(key))
        #"Role ID": "721994479715876865",
        #"Channel ID": "721994479715876865"
		
		embed=discord.Embed(title=f"Channel Deleted",color=0xfc0303)
		embed.add_field(name="Channel Name:", value=f"{channel.name}", inline=False)
		embed.add_field(name="Channel ID:", value=f"{channel.id}", inline=False)
		embed.set_footer(text=f"{date}")
		await a.send(embed = embed)

#GUILD CHANNEL CREATE EVENT
@bot.event
async def on_guild_channel_create(channel):
	with open('Config/guildlogs.json','r') as f:
		data = json.load(f)
	
	if data[str(channel.guild.id)]['Channel Logs'] == 'Enabled':
		key = data[str(channel.guild.id)]["Channel ID"]
		a = bot.get_channel(int(key))
		date = datetime.datetime.now().strftime("%A, %B %d %Y @ %H:%M:%S %p")
		embed=discord.Embed(title=f"Channel Created", color=0x3dff6e)
		embed.add_field(name="Channel Name:", value=f"{channel.mention}", inline=False)
		embed.add_field(name="Channel ID:", value=f"{channel.id}", inline=False)
		embed.set_footer(text=f"{date}")
		await a.send(embed = embed)

#MEMBER BAN EVENT
@bot.event
async def on_member_ban(guild, user):
	with open('Config/guildlogs.json','r') as f:
		data = json.load(f)
	
	if data[str(guild.id)]['User Logs'] == 'Enabled':
		date = datetime.datetime.now().strftime("%A, %B %d %Y @ %H:%M:%S %p")
		key = data[str(guild.id)]["User ID"]
		a = bot.get_channel(int(key))
		embed=discord.Embed(title=f"Member Banned",color=0xfc0303)
		embed.add_field(name="Member Name", value=f"{user}", inline=False)
		embed.add_field(name="Member ID", value=f"{user.id}", inline=False)
		embed.set_footer(text=f"{date}")
		await a.send(embed = embed)

#MEMBER UNBAN EVENT
@bot.event
async def on_member_unban(guild, user):
	with open('Config/guildlogs.json','r') as f:
		data = json.load(f)
	
	if data[str(guild.id)]['User Logs'] == 'Enabled':
		date = datetime.datetime.now().strftime("%A, %B %d %Y @ %H:%M:%S %p")
		key = data[str(guild.id)]["User ID"]
		a = bot.get_channel(int(key))
		embed=discord.Embed(title=f"Member UnBanned",color=0x3dff6e)
		embed.add_field(name="Member Name", value=f"{user}", inline=False)
		embed.add_field(name="Member ID", value=f"{user.id}", inline=False)
		embed.set_footer(text=f"{date}")
		await a.send(embed = embed)
	
#ROLE CREATE EVENT
@bot.event
async def on_guild_role_create(role):
	with open('Config/guildlogs.json','r') as f:
		data = json.load(f)
	
	if data[str(role.guild.id)]['Role Logs'] == 'Enabled':

		date = datetime.datetime.now().strftime("%A, %B %d %Y @ %H:%M:%S %p")
		key = data[str(role.guild.id)]["User ID"]
		a = bot.get_channel(int(key))
		embed=discord.Embed(title=f"Role Created ",color=0x3dff6e)
		embed.add_field(name="Role Name", value=f"{role.mention}", inline=False)
		embed.add_field(name="Role ID:", value=f"{role.id}", inline=False)
		embed.add_field(name="Position:", value=f"{role.position}", inline=False)
		embed.set_footer(text=f"{date}")
		await a.send(embed = embed)

#ROLE DELETE EVENT
@bot.event
async def on_guild_role_delete(role):
	with open('Config/guildlogs.json','r') as f:
		data = json.load(f)
	
	if data[str(role.guild.id)]['Role Logs'] == 'Enabled':
		date = datetime.datetime.now().strftime("%A, %B %d %Y @ %H:%M:%S %p")
		key = data[str(role.guild.id)]["User ID"]
		a = bot.get_channel(int(key))
		embed=discord.Embed(title=f"Role Deleted",color=0xfc0303)
		embed.add_field(name="Role Name:", value=f"{role}", inline=False)
		embed.add_field(name="Role ID:", value=f"{role.id}", inline=False)
		embed.set_footer(text=f"{date}")
		await a.send(embed = embed)


#MESSAGE DELETE EVENT
@bot.event
async def on_message_delete(message):
	with open('Config/guildlogs.json','r') as f:
		data = json.load(f)
	
	try:
		if data[str(message.guild.id)]['Message Delete'] == 'Enabled':
			date = datetime.datetime.now().strftime("%A, %B %d %Y @ %H:%M:%S %p")
			key = data[str(message.guild.id)]["Message Delete ID"]
			channel = bot.get_channel(int(key))
			embed=discord.Embed(color=0xff292c)
			embed.set_author(name=f"Message Deleted by {message.author}",icon_url= message.author.avatar_url)
			embed.add_field(name="Channel", value=f"{message.channel.mention}", inline=False)
			embed.add_field(name="Message:", value=f"{message.content}", inline=False)
			embed.set_footer(text = f'{date}')
			await channel.send(embed = embed)

	except Exception:
		pass

#MESSAGE CREATE EVENT

@bot.event
async def on_message_edit(before,after):
	with open('Config/guildlogs.json','r') as f:
		data = json.load(f)
	try:
		if data[str(before.guild.id)]['Message Edit'] == 'Enabled':
			date = datetime.datetime.now().strftime("%A, %B %d %Y @ %H:%M:%S %p")
			key = data[str(before.guild.id)]["Message Edit ID"]
			channel = bot.get_channel(int(key))
			embed=discord.Embed(color=0x386aff)
			embed.set_author(name=f"Message Edited by {before.author}",icon_url= before.author.avatar_url)
			embed.add_field(name="Channel:", value=f"{before.channel.mention}", inline=False)
			embed.add_field(name="Message Before:", value=f"{before.content}", inline=False)
			embed.add_field(name="Message After:", value=f"{after.content}", inline=False)
			embed.set_footer(text = f'{date}')
			await channel.send(embed = embed)

	except Exception:
		pass

# *-------------------------------------------------- ADDITIONAL TESTING PHASE -----------------------------------------

### NOTHING HERE <23

# *------------------------------------------------- > ENDING OF THE TESTING < -----------------------------------------

# A GOOD COMMAND FOR SAVING MY IDIOTIC TIME



#COGS / Command LOADING
for filename in os.listdir('./Moderations'):
	if filename.endswith('.py'):
		bot.load_extension(f'Moderations.{filename[:-3]}')

@bot.event
async def on_raw_reaction_add(payload):
	with open('Config/guildlogs.json') as f:
		r = json.load(f)

	guild = str(payload.guild_id)
	channel = await bot.fetch_channel(payload.channel_id)
	user = channel.guild.get_member(payload.user_id)
	emoji = payload.emoji
	emoji = str(emoji)
	if channel.id == r[guild]['Verify_Channel'] and emoji == '✅':
		role = discord.utils.get(channel.guild.roles, name = 'Member')
		await user.add_roles(role)

bot.run('ODU1Mzk2MDk4MzIyNDY0Nzg5.YMx3sg.Wgf-KbCEqa6WvI0uIjdUGod01xU')