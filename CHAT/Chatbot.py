import discord
from discord.ext import commands
from discord.ext.commands.core import check
import smtplib
bot = commands.Bot(command_prefix = '=',intents= discord.Intents.all())

@bot.event
async def on_ready():
    print('-------------- SERVER HAS STARTED -----------')

@bot.event
async def on_member_join(member):
    print(member)

    def check(msg):
        return msg.author == member and msg.channel.type == discord.ChannelType.private
    
    def order_check(reaction,user):
        return str(reaction.emoji) in ('➡️','1️⃣','2️⃣') and user == member
    
    await member.send('https://www.youtube.com/watch?v=K3P1Gg6c5uE')

    
    description = "Here you will receive access to our Full Signals group + BONUS\n50+ Videos -MASTERY COURSE\nA step by step guide on how we trade our exact strategy!\n\n**__Do you want to get started?__**"
    embed = discord.Embed(title = 'WELCOME TRADER Join 32,000 other successful members!',color = discord.Color.blurple(),description = description)
    msg = await member.send(embed = embed)
    await msg.add_reaction('➡️')
    reaction,user = await bot.wait_for('reaction_add',check = order_check,timeout = 300)
    
    message = "**__Step 1- Enter your name__**"
    embed = discord.Embed(title = "Here's how exactly, how to get started for FREE!",color = discord.Color.blurple(),description = message)
    await member.send(embed = embed)
    name  = await bot.wait_for('message',check = check,timeout = 300)
    name = name.content

    message = "**__Step 2- Enter your phone__**"
    embed = discord.Embed(color = discord.Color.blurple(),description = message)
    await member.send(embed = embed)
    phone  = await bot.wait_for('message',check = check,timeout = 300)
    phone = phone.content

    message = "**__Step 3- Enter your email__**"
    embed = discord.Embed(color = discord.Color.blurple(),description = message)
    await member.send(embed = embed)
    email  = await bot.wait_for('message',check = check,timeout = 300)
    email = email.content

    message = "**__Step 4- Who referred you?__** `(NO if None)`"
    embed = discord.Embed(color = discord.Color.blurple(),description = message)
    await member.send(embed = embed)
    ref  = await bot.wait_for('message',check = check,timeout = 300)
    ref = ref.content
    if ref.lower() in ('no','none','no one','no-one'):
        ref = 'NONE'

    await member.send('https://www.youtube.com/watch?v=OzSINgZLi30')
    message = '''
    Step 2: You will need to register to the brokers account (every trader needs one)

**:one: __DO IT NOW__**\n**:two: __DO IT AFTER__**

    '''
    embed = discord.Embed(color = discord.Color.blurple(),description = message)
    msg = await member.send(embed = embed)
    await msg.add_reaction('1️⃣')
    await msg.add_reaction('2️⃣')
    reaction,user = await bot.wait_for('reaction_add',check = order_check,timeout = 900)
    if reaction.emoji == '1️⃣':
        embed = discord.Embed(color = discord.Color.blurple(),description = 'https://ca.puprime.com/?cxd=35263_357166&affid')
        msg = await member.send(embed = embed)
        await msg.add_reaction('➡️')
        reaction,user = await bot.wait_for('reaction_add',check = order_check,timeout = 900)
    
    elif reaction.emoji == '2️⃣':
        pass

    await member.send('https://www.youtube.com/watch?v=IwptZdItoAE')
    message = '''
    Step 3: You will need to go through all our discord channels, step by step to ensure your taking the trades we properly and making sure you will have the best success rate like the others! (If we profit so do you!)
    '''

    embed = discord.Embed(color = discord.Color.blurple(),description = message)
    msg = await member.send(embed = embed)
    await msg.add_reaction('➡️')
    reaction,user = await bot.wait_for('reaction_add',check = order_check,timeout = 900)

    message = '''
    Now You’re in our Free members discord where we give daily trades we take! Once you’re all setup and registered on our Website Piptraders.ca as a member you will immediately gain access to our 💠platinum trades💠 where you will receive more trades we post!

__We will contact you with the next steps on how you can take advantage to our 💠Platinum trades💠 completely for FREE__!

**:point_right: [Join the Free Signal group!](https://discord.gg/NtAUfDnwAX)**
    '''
    file = discord.File("Final.jpg")
    embed = discord.Embed(title = 'Welcome :tada:', color = discord.Color.blurple(),description = message)
    embed.set_image(url="attachment://Final.jpg")
    msg = await member.send(embed = embed,file = file)

    # Python code to illustrate Sending mail from 
    # your Gmail account 
    
    
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    
    # start TLS for security
    s.starttls()
    
    # Authentication
    s.login("support@piptraders.ca", "hervy9988")
    
    # message to be sent
    if not ref == 'NONE':
        msg = f"Name: {name}\nEmail: {email}\nPhone Number: {phone}\nReferred By: {ref}"
    else:
        msg = f"Name: {name}\nEmail: {email}\nPhone Number: {phone}"

    message = 'Subject: {}\n\n{}'.format(f'{member} has filled the FORM', msg)
    
    # sending the mail
    s.sendmail("support@piptraders.ca", "support@piptraders.ca", message)
    
    # terminating the session
    s.quit()

    embed = discord.Embed(title = f"{member} Has filled the form",color = discord.Color.blurple())
    embed.add_field(name = 'Name',value = name,inline = False)
    embed.add_field(name = 'Email',value = email,inline = False)
    embed.add_field(name = 'Phone',value = phone,inline = False)
    if not ref == 'NONE':
        embed.add_field(name = 'Referred By',value = ref,inline = False)

    
    channel = await bot.fetch_channel(868351693505585172)
    await channel.send(embed = embed)

TOKEN = ''

bot.load_extension('Cog')
bot.run('ODI1MjA5MzU5MDQ2MTQ4MTM2.YF6mGg.3BmBB87r-f5CUzLY6eh7CmcE6SE')

