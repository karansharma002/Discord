import discord
from discord.ext import commands
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow
from discord_slash.utils.manage_components import create_actionrow, create_button, wait_for_component
from discord_slash import SlashCommand, SlashContext
from discord_slash.context import ComponentContext
import asyncio
import datetime

bot = commands.Bot(command_prefix = '??', intents = discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)

@bot.event
async def on_ready():
    print('------ READY -------')
    await bot.wait_until_ready()


@slash.slash(name="request", description = 'Protocol Coverage Request', guild_ids=[886983311002591293])
async def request(ctx):
    creator = ctx.author
    answers = {}

    def check(m):
        return m.author.id == creator.id and m.channel == ctx.channel

    def check2(m):
        return m.author.id == creator.id and m.channel == ctx.channel and m.attachments

    from discord_slash.utils.manage_components import create_button, create_actionrow
    from discord_slash.model import ButtonStyle

    embed = discord.Embed(color = discord.Color.blue(), description = '1: __Are you a team member of the protocol ?__')
    buttons = [
        create_button(style=ButtonStyle.green, label="YES"),
        create_button(style=ButtonStyle.red, label="NO")
    ]

    action_row = create_actionrow(*buttons)

    msg = await ctx.send(embed = embed, components=[action_row])

    answers[str(creator.id)] = []

    action_row = create_actionrow(*buttons)

    interaction = await ctx.send(embed = embed, components=[action_row])

    try:
        button_ctx: ComponentContext = await wait_for_component(bot,components=action_row, timeout = 60)
    except asyncio.TimeoutError:
        await ctx.send(':warning: Request TimedOut!!', hidden =True)
        return

    item = button_ctx.component['label']
    answers[str(creator.id)].append(item)
    await interaction.delete()
    
    if item == 'NO':
        msg = await ctx.send('2: __Name of the protocol__')
        msg2 = await bot.wait_for('message', check = check)
        answers[str(creator.id)].append(msg2.content)
        await msg.delete()
        await msg2.delete()

        msg = await ctx.send('3: __Please provide a brief introduction of the protocol.__')
        msg2 = await bot.wait_for('message', check = check)
        answers[str(creator.id)].append(msg2.content)
        await msg.delete()

        msg = await ctx.send("4: __What is the address of the project's website?__")
        msg2 = await bot.wait_for('message', check = check)
        answers[str(creator.id)].append(msg2.content)
        await msg.delete()

        msg = await ctx.send("5: __Please provide the name and email address which we can follow up if the requested protocol gets listed__")
        msg2 = await bot.wait_for('message', check = check)
        answers[str(creator.id)].append(msg2.content)
        await msg.delete()

        msg = await ctx.send("6: __Any further information you would like to share with us regarding the protocol or this request__")
        msg2 = await bot.wait_for('message', check = check)
        answers[str(creator.id)].append(msg2.content)
        await msg.delete()

        QNA = ['1: Are you a team member of the protocol ?', '2: Name of the protocol', "3: Please provide a brief introduction of the protocol",
        "4: What is the address of the project's website?", "5: Please provide the name and email address which we can follow up if the requested protocol gets listed",
        "6: Any further information you would like to share with us regarding the protocol or this request"]

        msg = ''

        for x,y in zip(QNA, answers[str(creator.id)]):
            msg += f"**{x}**\n> {y}\n\n"

        embed = discord.Embed(color = discord.Color.dark_orange(), description = msg)
        embed.set_author(name = f"{ctx.author} | PROTOCOL REQUEST", icon_url=ctx.author.avatar_url)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed = embed)
        await ctx.send(f':white_check_mark: {ctx.author.mention}, Your Protocol Request has been Submitted.', hidden = True)

    else:
        msg = await ctx.send('2: __Name of the protocol__')
        msg2 = await bot.wait_for('message', check = check)
        answers[str(creator.id)].append(msg2.content)
        await msg.delete()
        await msg2.delete()

        msg = await ctx.send('3: __Please provide a brief introduction of the protocol.__')
        msg2 = await bot.wait_for('message', check = check)
        answers[str(creator.id)].append(msg2.content)
        await msg.delete()

        msg = await ctx.send("4: __What types of risk you wish to be covered for the protocol?__\
            \n*Please illustrate on risk you wish to be covered by Unore, which will help us understand better how to be more valuable to the protocol.*")

        msg2 = await bot.wait_for('message', check = check)
        answers[str(creator.id)].append(msg2.content)
        await msg.delete()

        tvl = ["$10,000,000 - $25,000,000","$25,000,000 - $100,000,000","$100,000,000 - $500,000,000","> $500,000,000"]

        options = []
        for x in tvl:
            options.append(create_select_option(x,value=x))
        
        select = create_select(
            options=options,
            placeholder="5: What is the protocol's current TVL?",
            min_values=1, # the minimum number of options a user must select
            max_values=1, # the maximum number of options a user can select
            custom_id="tvl"
        )

        action_row = create_actionrow(select)

        interaction = await ctx.send(components=[action_row])

        try:
            button_ctx: ComponentContext = await wait_for_component(bot,components=action_row, timeout = 60)
        except asyncio.TimeoutError:
            await ctx.send(':warning: Request TimedOut!!', hidden =True)
            return

        await interaction.delete()

        item = button_ctx.values[0]
        answers[str(creator.id)].append(item)

        types_ = ["DEX", "Lending", "Token/Bridge", "Smart Wallet", "Asset management(Farms/Vaults)", "Derivatives", "Coverage Market", "Multiple Services"]

        options = []
        for x in types_:
            options.append(create_select_option(x,value=x))
        
        select = create_select(
            options=options,
            placeholder="6: What type of application is the protocol?",
            min_values=1, # the minimum number of options a user must select
            max_values=1, # the maximum number of options a user can select
            custom_id="type"
        )

        action_row = create_actionrow(select)

        interaction = await ctx.send(components=[action_row])

        try:
            button_ctx: ComponentContext = await wait_for_component(bot,components=action_row, timeout = 60)
        except asyncio.TimeoutError:
            await ctx.send(':warning: Request TimedOut!!', hidden =True)
            return

        await interaction.delete()

        item = button_ctx.values[0]
        answers[str(creator.id)].append(item)

        age_ = ["Not Launched Yet", "Recent - 1 Month", "1 Month - 3 Months", "3 Months - 6 Months", "6 Months - 1 Year", "> 1 Year"]

        options = []
        for x in age_:
            options.append(create_select_option(x,value=x))
        
        select = create_select(
            options=options,
            placeholder="7: What is the project's mainnet age?",
            min_values=1, # the minimum number of options a user must select
            max_values=1, # the maximum number of options a user can select
            custom_id="age"
        )

        action_row = create_actionrow(select)

        interaction = await ctx.send(components=[action_row])

        try:
            button_ctx: ComponentContext = await wait_for_component(bot,components=action_row, timeout = 60)
        except asyncio.TimeoutError:
            await ctx.send(':warning: Request TimedOut!!')
            return

        await interaction.delete()

        item = button_ctx.values[0]
        answers[str(creator.id)].append(item)

        msg = await ctx.send("8: __What is the address of the project's website?__")
        msg2 = await bot.wait_for('message', check = check)
        answers[str(creator.id)].append(msg2.content)
        await msg.delete()

        msg = await ctx.send("9: __Link to White Paper or Docs__")
        msg2 = await bot.wait_for('message', check = check)
        answers[str(creator.id)].append(msg2.content)
        await msg.delete()

        embed = discord.Embed(color = discord.Color.blue(), description = '10: __Have the smart contracts been audited?__')
        buttons = [
            create_button(style=ButtonStyle.green, label="YES"),
            create_button(style=ButtonStyle.red, label="NO")
        ]

        action_row = create_actionrow(*buttons)

        msg = await ctx.send(embed = embed, components=[action_row])

        action_row = create_actionrow(*buttons)

        interaction = await ctx.send(embed = embed, components=[action_row])

        try:
            button_ctx: ComponentContext = await wait_for_component(bot,components=action_row, timeout = 60)
        except asyncio.TimeoutError:
            await ctx.send(':warning: Request TimedOut!!', hidden =True)
            return

        item = button_ctx.component['label']
        answers[str(creator.id)].append(item)
        await interaction.delete()


        msg = await ctx.send("11: __Please provide the link of your audit report(s)__")
        msg2 = await bot.wait_for('message', check = check)
        answers[str(creator.id)].append(msg2.content)
        await msg.delete()

        msg = await ctx.send("12: __Would you like be a partnership with Unore officially__")
        msg2 = await bot.wait_for('message', check = check)
        answers[str(creator.id)].append(msg2.content)
        await msg.delete()

        QNA = ['1: Are you a team member of the protocol ?', '2: Name of the protocol', "3: Please provide a brief introduction of the protocol",
        "4: What types of risk you wish to be covered for the protocol?", "5: What is the protocol's current TVL?","6: What type of application is the protocol?",
        "7: What is the project's mainnet age?", "8: What is the address of the project's website?",  "9: Link to White Paper or Docs", "10: Have the smart contracts been audited?",
        "11: Please provide the link of your audit report(s)", "12: Would you like be a partnership with Unore officially"]

        await ctx.send(f':white_check_mark: {ctx.author.mention}, Your Protocol Request has been Submitted.', hidden = True)

        msg = ''

        for x,y in zip(QNA, answers[str(creator.id)]):
            msg += f"**{x}**\n> {y}\n\n"

        embed = discord.Embed(color = discord.Color.dark_orange(), description = msg)
        embed.set_author(name = f"{ctx.author} | PROTOCOL REQUEST", icon_url=ctx.author.avatar_url)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed = embed)

bot.run('ODQyNDU1NzY1MDExNjYwODAx.G80Kzi._oFHxAYMACr0HXST8AJn5ab0xwr6Q5J2aIaVUc')