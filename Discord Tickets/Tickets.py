import asyncio
import discord
from discord.ext import commands
import json
from discord_components import DiscordComponents, Button, ButtonStyle

bot = commands.Bot(command_prefix = 'dm!',intents = discord.Intents.all())

COLOR = discord.Color.from_rgb(80, 133, 81)

@bot.event
async def on_ready():
    DiscordComponents(bot)
    print('---------- SERVER HAS STARTED ---------')

@bot.event
async def on_button_click(interaction):
    with open('Tickets.json') as f:
        tickets = json.load(f)
    
    id = str(interaction.channel.id)
    
    if interaction.component.label.startswith("📌 Claim/Unclaim"):
        channel = interaction.channel
        if id in tickets:
            if tickets[id]['Owner'] == 'NONE':
                tickets[id]['Owner'] = interaction.author.id
                with open('Tickets.json','w') as f: 
                    json.dump(tickets,f,indent = 3)

                role = discord.utils.get(interaction.guild.roles,name = 'Admins')
                if interaction.author.guild_permissions.administrator:
                    pass

                elif not role in interaction.author.roles:
                    await interaction.respond(type = "4", content = ":warning: You don't have enough permissions to CLAIM this ticket.")
                    return

                overwrites = {
                    role:discord.PermissionOverwrite(read_messages = False,send_messages = False),
                    interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    interaction.guild.me: discord.PermissionOverwrite(read_messages=True,send_messages = True),
                    interaction.author: discord.PermissionOverwrite(read_messages=True,send_messages = True)
                }
                await interaction.channel.edit(overwrites = overwrites)
                msg = f'This ticket was claimed by {interaction.author.mention}'
                embed = discord.Embed(title = 'Ticket Claimed',color = COLOR,description = msg)
                embed.set_footer(text = 'Dodo Mail | ©️ 2021 | www.thelandofark.com',icon_url='https://i.imgur.com/hODYmHU.png')
                embed.set_thumbnail(url = 'https://i.imgur.com/ZovNveV.png')
                await interaction.channel.send(embed = embed)
                await interaction.respond(type='7')

            elif tickets[id]['Owner'] == interaction.author.id:
                await channel.send(':white_check_mark: You have left the TICKET.')
                role = discord.utils.get(interaction.guild.roles,name = 'Admins')
                overwrites = {
                    role:discord.PermissionOverwrite(read_messages = True,send_messages = True),
                    interaction.author: discord.PermissionOverwrite(read_messages=False,send_messages = False)
                }
                await interaction.channel.edit(overwrites = overwrites)
                tickets[id]['Owner'] = 'NONE'
                with open('Tickets.json','w') as f: 
                    json.dump(tickets,f,indent = 3)
                    
                msg = f'This ticket was unclaimed by {interaction.author.mention}'
                embed = discord.Embed(title = 'Ticket Unclaimed',color = 0xfcff57,description = msg)
                embed.set_footer(text = 'Dodo Mail | ©️ 2021 | www.thelandofark.com',icon_url='https://i.imgur.com/hODYmHU.png')
                embed.set_thumbnail(url = 'https://i.imgur.com/ZovNveV.png')
                await interaction.channel.send(embed = embed)
                await interaction.respond(type='7')

            else:
                await interaction.respond(type='4', content=':warning: This ticket is already claimed by someone else.')
            
    elif interaction.component.label.startswith("🔒 Close"):
        msg = f"{interaction.author.mention}, Are you sure you would like to close this ticket?"
        embed = discord.Embed(title = 'Close Ticket',color = COLOR,description = msg)
        embed.set_footer(text = 'Dodo Mail | ©️ 2021 | www.thelandofark.com',icon_url='https://i.imgur.com/hODYmHU.png')
        embed.set_thumbnail(url = 'https://i.imgur.com/ZovNveV.png')
        await interaction.respond(embed = embed, components = [[Button(style=ButtonStyle.red, label='Close'),Button(style=ButtonStyle.grey, label="Cancel", custom_id="button")]])
        try:
            
            res = await bot.wait_for("button_click",timeout = 20)
            if res.component.label == 'Close':
                await res.respond(type='7')
                author = await bot.fetch_user(int(tickets[id]['Creator']))

                import chat_exporter
                file = await chat_exporter.quick_export(interaction)
                await author.send(file = file)  
                for channels in interaction.channel.category.channels:
                    if 'transcript' in channels.name:
                        ch = channels
                        break

                embed = discord.Embed(color = COLOR,description = f'Transcript sent to {interaction.author.mention}')
                await interaction.channel.send(embed = embed)
                embed = discord.Embed(color = COLOR,description = f'Transcript sent to {ch.mention}')
                await interaction.channel.send(embed = embed)

                file = await chat_exporter.quick_export(interaction)
                await ch.send(file = file)

                embed = discord.Embed(color = COLOR,description = 'This ticket has been CLOSED.')
                embed.set_footer(text = 'Dodo Mail | ©️ 2021 | www.thelandofark.com',icon_url='https://i.imgur.com/hODYmHU.png')
                embed.set_thumbnail(url = 'https://i.imgur.com/ZovNveV.png')
                await interaction.channel.send(embed = embed)
                msg = f"{interaction.author.mention} I've really enjoyed talking with you. If you need support again feel free to open a new ticket."
                embed = discord.Embed(color = COLOR,title = 'Ticket Closed',description = msg)
                embed.set_footer(text = 'Dodo Mail | ©️ 2021 | www.thelandofark.com',icon_url='https://i.imgur.com/hODYmHU.png')
                embed.set_image(url = 'https://i.imgur.com/Wfsj20u.png')

                await author.send(embed = embed)      

            else:
                await res.respond(type='4', content = 'Request Cancelled!')
                return

        except asyncio.TimeoutError:
            await interaction.channel.send(type='4', content = ':warning: Request Timed-Out')

@bot.command(description = 'INFO: Setup the ticket in a channel.\n Takes a channel which is used to fetch the CATEGORY.')
async def setup(ctx,channel:discord.TextChannel = None):
    if not channel:
        await ctx.send(':information_source: Usage: !setupticket `<#CHANNEL>` (USED TO FETCH THE CATEGORY)')
        return

    with open('Database.json') as f:
        data = json.load(f)
    
    category = str(channel.category.id)
    data[category] = {}

    def check(m):
        return m.author == ctx.author and m.channel.id == ctx.channel.id
    
    await ctx.send('1: Enter the Ticket Title')
    name = await bot.wait_for('message',check = check, timeout = 40)
    name = name.content

    await ctx.send('2: Enter the Ticket Description')
    description = await bot.wait_for('message',check = check, timeout = 40)
    description = description.content

    await ctx.send('3: Enter the Ticket Emoji')
    emoji = await bot.wait_for('message',check = check, timeout = 40)
    emoji = emoji.content

    data[category]['Name'] = name
    data[category]['Description'] = description
    data[category]['Emoji'] = emoji

    with open('Database.json','w') as f:
        json.dump(data,f,indent = 3)

    embed = discord.Embed(title = name,color = COLOR,description = description)
    embed.set_thumbnail(url = 'https://i.imgur.com/ZovNveV.png')
    embed.set_footer(text = 'Dodo Mail | ©️ 2021 | www.thelandofark.com',icon_url='https://i.imgur.com/hODYmHU.png')
    msg = await ctx.send(embed = embed)
    await msg.add_reaction(emoji)
    await ctx.message.add_reaction('✅')

@bot.command(description = 'INFO: Add a user to a Ticket')
async def add(ctx,user:discord.Member = None):
    if not user:
        await ctx.send(':information_source: !add `<@user>`')
        return

    with open('Tickets.json') as f:
        tickets = json.load(f)
    
    id = str(ctx.channel.id)

    if id in tickets:
        if tickets[id]['Owner'] == ctx.author.id:
            await ctx.send(f':white_check_mark: You have added {user} in the Ticket.')
            overwrites = {
                user: discord.PermissionOverwrite(read_messages=True,send_messages = True)
            }
            await ctx.channel.edit(overwrites = overwrites)

        else:
            await ctx.send('This ticket is not claimed by you.')

    else:
        await ctx.send('Invalid Ticket Channel.')
    
    ctx.message.delete()

@bot.command(description = 'INFO: Removes the user from a Ticket')
async def remove(ctx,user:discord.Member = None):
    if not user:
        await ctx.send(':information_source: !remove `<@user>`')
        return

    with open('Tickets.json') as f:
        tickets = json.load(f)
    
    id = str(ctx.channel.id)

    if id in tickets:
        if tickets[id]['Owner'] == ctx.author.id:
            await ctx.send(f':white_check_mark: You have removed {user} from the Ticket.')
            overwrites = {
                user: discord.PermissionOverwrite(read_messages=False,send_messages = False)
            }
            await ctx.channel.edit(overwrites = overwrites)

        else:
            await ctx.send('This ticket is not claimed by you.')

    else:
        await ctx.send('Invalid Ticket Channel.')
    
    ctx.message.delete()

@bot.event
async def on_raw_reaction_add(payload):
    channel = await bot.fetch_channel(payload.channel_id)
    guild = channel.guild
    member = channel.guild.get_member(int(payload.user_id))
    if member == bot.user:
        return

    emoji = payload.emoji
    emoji = str(emoji)
    with open('Tickets.json') as f:
        tickets = json.load(f)
    
    with open('Database.json') as f:
        database = json.load(f)

    msg = await channel.fetch_message(payload.message_id)
    await msg.remove_reaction(emoji,member)

    id1 = str(channel.category.id)
    if id1 in database:
        if emoji == database[id1]['Emoji']:
            role = discord.utils.get(guild.roles,name = 'Admins')
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                role:discord.PermissionOverwrite(read_messages = True,send_messages = True),
                guild.me: discord.PermissionOverwrite(read_messages=True,send_messages = True),
                member: discord.PermissionOverwrite(read_messages=True,send_messages = True)
            }
            category = discord.utils.get(guild.categories,id = int(id1))
            print(category)
            channel = await guild.create_text_channel(f'ticket-{member.name}', overwrites=overwrites,category = category)
            
            msg = f"Hi there {member.mention} Our {role.mention} have been notified of this Ticket and will be with you as soon as they can.\n**__Want to the close the ticket??__**\nPress the :lock: emoji."
            embed = discord.Embed(title = "__GENERAL SUPPORT TICKET__",color = COLOR,description = msg)
            embed.set_footer(text = 'Dodo Mail | ©️ 2021 | www.thelandofark.com',icon_url='https://i.imgur.com/hODYmHU.png')
            embed.set_thumbnail(url = 'https://i.imgur.com/ZovNveV.png')
            await channel.send(embed = embed, components = [[Button(style=ButtonStyle.grey, label='📌 Claim/Unclaim'),Button(style=ButtonStyle.grey, label="🔒 Close", custom_id="button")]])
            tickets[str(channel.id)] = {}
            tickets[str(channel.id)]['Owner'] = 'NONE'
            tickets[str(channel.id)]['Creator'] = member.id
            with open('Tickets.json','w') as f:
                json.dump(tickets,f,indent = 3)
        
            msg = f"Hi there {member.mention}, a Ticket has been created in the {channel.mention} channel. Please visit the ticket and explain the reason for opening it."
            embed = discord.Embed(title = 'Ticket Created',description =  msg,color = COLOR)
            embed.set_footer(text = 'Dodo Mail | ©️ 2021 | www.thelandofark.com',icon_url='https://i.imgur.com/hODYmHU.png')
            embed.set_thumbnail(url = 'https://i.imgur.com/ZovNveV.png')
            await member.send(embed = embed)

bot.run('ODgxOTM0NTAxNjM3NDIzMTc0.YS0Dgg.6F3BSKqp7IXg4W92hOJY9m1m0Bs')
