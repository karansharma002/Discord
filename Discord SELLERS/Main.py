import discord
from discord.ext import commands,tasks
import json
import datetime

bot = commands.Bot(command_prefix = '!',intents = discord.Intents.all())

@bot.event
async def on_ready():
    print('------------- SERVER HAS STARTED ------------')

@bot.command()
async def rental(ctx,action:str = None,rental_type:str = None):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    if not action or not rental_type:
        await ctx.send(':information_source: Usage: !rental `<ACTION>` `<RENTAL TYPE>` ')
        return
    
    with open('Config/Rentals.json') as f:
        rentals = json.load(f)
    
    action = action.lower()

    if action == 'delete':
        if not rental_type.lower() in rentals:
            await ctx.send(f':warning: There is no active {rental_type} Rental.')
            return

        rentals[rental_type.lower()].pop('Duration')
        with open('Config/Rentals.json','w') as f:
            json.dump(rentals,f,indent = 2)
        
        await ctx.send(':white_check_mark: Duration has been DELETED.')


    elif action == 'update':
        if not rental_type.lower() in rentals:
            await ctx.send(f':warning: There is no active {rental_type} Rental.')
            return

        await ctx.send(f':arrow_double_down: Please enter the Duration for the {rental_type.upper()} RENTAL]\n`(Example: 04/01 - 04/30)`')
        duration = await bot.wait_for('message',check = check,timeout = 20)
        rentals[rental_type.lower()]['Duration'] = duration.content
        with open('Config/Rentals.json','w') as f:
            json.dump(rentals,f,indent = 2)
        
        await ctx.send(':white_check_mark: Duration for the rental has been UPDATED.')

    elif action == 'setup':
        if rental_type.lower() in rentals:
            await ctx.send(f':warning: {rental_type} Rental already exists. Please delete it or Modify if you want to update.')
            return

        await ctx.send(f':arrow_double_down: Please enter the Duration for the {rental_type.upper()} RENTAL]\n`(Example: 04/01 - 04/30)`')
        duration = await bot.wait_for('message',check = check,timeout = 20)
        rentals[rental_type.lower()] = {}
        rentals[rental_type.lower()]['Duration'] = duration.content
        with open('Config/Rentals.json','w') as f:
            json.dump(rentals,f,indent = 2)
        
        await ctx.send(':white_check_mark: Duration for the rental has been SET.')

    else:
        await ctx.send(':warning: Invalid Action Type `(ALLOWED - Setup / Update / Delete)`')
        return

@bot.command()
async def price(ctx,action:str = None,rental_type:str = None):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    if not action or not rental_type:
        await ctx.send(':information_source: Usage: !price `<ACTION>` `<RENTAL TYPE>` ')
        return
    
    with open('Config/Rentals.json') as f:
        rentals = json.load(f)
    
    action = action.lower()

    if action == 'delete':
        if not rental_type.lower() in rentals:
            await ctx.send(f':warning: There is no active {rental_type} Rental.')
            return

        await ctx.send(f':arrow_double_down: Enter the Product Name you want to DELETE the price for')
        old_product = await bot.wait_for('message',check = check,timeout = 20)
        old_product = old_product.content.lower()

        if not old_product in rentals[rental_type.lower()]['Products']:
            await ctx.send(':warning: Product not found')
            return
        
        rentals[rental_type.lower()]['Products'][old_product].pop('Price')
        with open('Config/Rentals.json','w') as f:
            json.dump(rentals,f,indent = 2)
        
        await ctx.send(f':white_check_mark: {old_product} Price has been DELETED.')

    elif action == 'update':
        if not rental_type.lower() in rentals:
            await ctx.send(f':warning: There is no active {rental_type} Rental.')
            return
        
        await ctx.send(f':arrow_double_down: Enter the Product Name you want to MODIFY')
        old_product = await bot.wait_for('message',check = check,timeout = 20)
        old_product = old_product.content.lower()
        if not old_product.lower() in rentals[rental_type.lower()]['Products']:
            await ctx.send(':warning: Product not found')
            return

        await ctx.send(f':arrow_double_down: Enter the new Product Price')
        product_name = await bot.wait_for('message',check = check,timeout = 20)
        product_name = product_name.content.lower()
        rentals[rental_type.lower()]['Products'][old_product]['Price'] = int(product_name)
        with open('Config/Rentals.json','w') as f:
            json.dump(rentals,f,indent = 2)
        
        await ctx.send(':white_check_mark: Product Price has been UPDATED.')
        return

    elif action == 'setup':
        if not rental_type.lower() in rentals:
            await ctx.send(f':warning: There is no active {rental_type} Rental.')
            return
        
        await ctx.send(f':arrow_double_down: Enter the Product Name to add the price to')
        product_name = await bot.wait_for('message',check = check,timeout = 20)
        product_name = product_name.content.lower()
        if not product_name in rentals[rental_type.lower()]['Products']:
            await ctx.send(':warning: Product not found!')
            return
        
        await ctx.send(f':arrow_double_down: Enter the Product Price')
        product_price = await bot.wait_for('message',check = check,timeout = 20)
        product_price = product_price.content.lower()
        
        rentals[rental_type.lower()]['Products'][product_name]['Price'] = int(product_price)
        with open('Config/Rentals.json','w') as f:
            json.dump(rentals,f,indent = 2)
        
        await ctx.send(f':white_check_mark: {product_name} Price has been SET')
        return

    else:
        await ctx.send(':warning: Invalid Action Type `(ALLOWED - Setup / Update / Delete)`')
        return
    


@bot.command()
async def product(ctx,action:str = None,rental_type:str = None):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    if not action or not rental_type:
        await ctx.send(':information_source: Usage: !product `<ACTION>` `<RENTAL TYPE>` ')
        return
    
    with open('Config/Rentals.json') as f:
        rentals = json.load(f)
    
    action = action.lower()

    if action == 'delete':
        if not rental_type.lower() in rentals:
            await ctx.send(f':warning: There is no active {rental_type} Rental.')
            return

        await ctx.send(f':arrow_double_down: Enter the Product Name you want to DELETE')
        old_product = await bot.wait_for('message',check = check,timeout = 20)
        old_product = old_product.content.lower()

        if not old_product in rentals[rental_type.lower()]['Products']:
            await ctx.send(':warning: Product not found')
            return
        
        rentals[rental_type.lower()]['Products'].pop(old_product)
        with open('Config/Rentals.json','w') as f:
            json.dump(rentals,f,indent = 2)
        
        await ctx.send(f':white_check_mark: {old_product} Product has been DELETED.')

    elif action == 'update':
        if not rental_type.lower() in rentals:
            await ctx.send(f':warning: There is no active {rental_type} Rental.')
            return
        
        await ctx.send(f':arrow_double_down: Enter the Product Name you want to MODIFY')
        old_product = await bot.wait_for('message',check = check,timeout = 20)
        old_product = old_product.content.lower()
        if not old_product.lower() in rentals[rental_type.lower()]['Products']:
            await ctx.send(':warning: Product not found')
            return

        await ctx.send(f':arrow_double_down: Enter the new Product Name')
        product_name = await bot.wait_for('message',check = check,timeout = 20)
        product_name = product_name.content.lower()
        rentals[rental_type.lower()][product_name] = {}
        if 'Price' in rentals[rental_type.lower()][old_product]:
            rentals[rental_type.lower()]['Products'][product_name]['Price'] = rentals[rental_type.lower()]['Products'][old_product]['Price']
        
        if 'Emoji' in rentals[rental_type.lower()][old_product]:
            rentals[rental_type.lower()]['Products'][product_name]['Emoji'] = rentals[rental_type.lower()]['Products'][old_product]['Emoji']

        rentals[rental_type.lower()]['Products'].pop(old_product)
        with open('Config/Rentals.json','w') as f:
            json.dump(rentals,f,indent = 2)
        
        await ctx.send(':white_check_mark: Product name has been UPDATED.')

    elif action == 'setup':
        if not rental_type.lower() in rentals:
            await ctx.send(f':warning: There is no active {rental_type} Rental.')
            return
        
        await ctx.send(f':arrow_double_down: Enter the Product Name you want to add')
        product_name = await bot.wait_for('message',check = check,timeout = 20)
        product_name = product_name.content.lower()
        if 'Products' in rentals[rental_type.lower()]:
            if product_name in rentals[rental_type.lower()]['Products']:
                await ctx.send(':warning: Product already exists')
                return

        await ctx.send(f':arrow_double_down: Enter the EMOJI for the {product_name}')
        emoji = await bot.wait_for('message',check = check,timeout = 20)
        emoji = emoji.content
        rentals[rental_type.lower()]['Products'] = {}
        rentals[rental_type.lower()]['Products'][product_name] = {}
        rentals[rental_type.lower()]['Products'][product_name]['Emoji'] = emoji
        with open('Config/Rentals.json','w') as f:
            json.dump(rentals,f,indent = 2)
        
        await ctx.send(f':white_check_mark: {product_name} has been ADDED in the Products.')


    else:
        await ctx.send(':warning: Invalid Action Type `(ALLOWED - Setup / Update / Delete)`')
        return


@bot.command()
async def post(ctx,rental_type:str = None):
    if not rental_type:
        await ctx.send(':information_source: Usage: !post `<rental_type>` `<#channel>`')
        return

    with open('Config/Rentals.json') as f:
        rentals = json.load(f)
    
    msg = f"**__Duration__**: {rentals[rental_type.lower()]['Duration']}\n\n**__Pricing for available bots:__**\n\n"
    for x in rentals[rental_type.lower()]['Products']:
        msg += f"{rentals[rental_type.lower()]['Products'][x]['Emoji']} "
        msg += f" {x} - "
        msg += f" $ {rentals[rental_type.lower()]['Products'][x]['Price']}\n"
    
    msg += "\n**__How to rent a bot?__**\nAll information on how to rent a bot through our service are available in #order-here.\n\n"
    msg += "**:sos:__Still confused?__**\n*If you have any further questions regarding renting a bot through our service, feel free to get in touch with one of our many qualified support members by opening a ticket in ##support-ticket*"
    embed = discord.Embed(title = rental_type.upper(),description = msg,color = discord.Color.dark_green())
    embed.set_footer(text = 'Sofio Rentals',icon_url = bot.user.avatar_url)
    embed.set_thumbnail(url = bot.user.avatar_url)
    await ctx.send(embed = embed)
        
@bot.command()
async def setup(ctx):
    msg = '''
    __Please read carefully before you proceed!__

    Thank you for choosing Soflo Rentals as your trusted rental provider. Down below we summarized some important points which you should check out before renting a bot.

    **__Renting Process__**
    1. Open a ticket in #order-here.
    2. Go to your ticket channel.
    3. Type in the bot's name & duration for the rental.
    4. Wait until one of our staff or providers will assist you.

    **__Renting Prices__**
    Please check our respective rental prices in the specific release day channel or in:
    :small_orange_diamond: #weekly-rentals
    :small_orange_diamond: #monthly-rentals

    **__Accepted Payment Methods__**
    :small_orange_diamond: Cashapp
    :small_orange_diamond: Zelle
    :small_orange_diamond: Paypal

    **React with :envelope: to create a ticket.**

    :sos: **__Still confused?__**
    If you have any further questions regarding renting a bot through our service, feel free to get in touch with one of our many qualified support members by opening a ticket in #support-ticket.
    '''
    embed = discord.Embed(color = discord.Color.blue(),title = 'Welcome to the Soflo Rental Store',description = msg,color = discord.Color.dark_green())
    embed.set_footer(text = 'Sofio Rentals',icon_url = bot.user.avatar_url)
    embed.set_thumbnail(url = bot.user.avatar_url)
    sent_ = await ctx.send(embed = embed)
    await sent_.add_reaction('✉️')
    with open('Config/Settings.json') as f:
        settings = json.load(f)
    
    settings['Order_MSG'] = sent_.id
    settings['Emoji'] = '✉️'
    with open('Config/Settings.json','w') as f:
        json.dump(settings,f,indent = 3)

@bot.event
async def on_raw_reaction_add(payload):
    
    msg_id = payload.message_id
    guild = await bot.fetch_guild(int(payload.guild_id))
    channel = await bot.fetch_channel(payload.channel_id)
    guild = channel.guilda
    member = channel.guild.get_member(int(payload.user_id))
    if member == bot.user:
        return

    emoji = payload.emoji
    emoji = str(emoji)
    print(guild)
    with open('Config/Settings.json') as f:
        settings= json.load(f)
    
    if emoji == settings['Emoji'] and msg_id == settings['Order_MSG']:
        def check(m):
            return m.author == member and m.channel == channel

        print('HERE')
        message = await channel.fetch_message(settings['Order_MSG'])
        await message.remove_reaction(settings['Emoji'],member)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        channel = await guild.create_text_channel(f'rental-{member.name}', overwrites=overwrites)
        description = '''
        Congratulations! :tada:
        Your ticket got assigned!

        Thank you for your patience.
        Our @Rental Staff and Provider will assist you now.
        '''
        embed = discord.Embed(title = 'Congratulations! :tada:',description = description,color = discord.Color.dark_green())
        embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/807202256080076800/862343155981746186/Soflo_rentals.png')
        embed.set_footer(text = 'Sofio Rentals',icon_url = 'https://cdn.discordapp.com/attachments/807202256080076800/862343155981746186/Soflo_rentals.png')
        await channel.send(embed = embed)

        with open('Config/Rentals.json') as f:
            rentals = json.load(f)
        
        await channel.send(':arrow_double_down: Enter the Duration: `(MONTHLY / WEEKLY OR CUSTOM)`')
        duration = await bot.wait_for('message',check = check)
        duration = duration.content.upper()
        embed = discord.Embed(description = f'Selected duration: `{duration}`',color = discord.Color.dark_green())
        await channel.send(embed = embed)
        products = []
        number = 0
        msg = ''
        for x in rentals:
            for y in rentals[x]['Products']:
                msg += f"{number + 1}: {rentals[x]['Products'][y]['Emoji']} - {y} - ${rentals[x]['Products'][y]['Price']}\n"
                number += 1
                products.append(y)

        msg += f"\n**Type the Product Number in the chat to SELECT the product**"    

        embed = discord.Embed(color = discord.Color.dark_green(),title = 'Choose the PRODUCT',description = msg)
        await channel.send(embed = embed)

        while True:
            choice = await bot.wait_for('message',check = check)
            choice = int(choice.content)
            try:
                embed = discord.Embed(description = f'Selected Bot: {products[choice - 1].upper()}',color = discord.Color.dark_green())
                await channel.send(embed = embed)
                await channel.send(f":arrow_double_down: Type: `CONFIRM` to Confirm the ORDER or `RETRY` to retry'")
                msg = await bot.wait_for('message',check = check)
                if msg.content.lower() == 'confirm':
                    break
                else:
                    await channel.send('Enter the product number')
                    continue

            except IndexError:
                await channel.send(':warning: Invalid Product Number, RETRY!')
                continue
        
        description = f'''
        Thank you for submitting your order details {member.mention}
        Our @Rental Support & @Rental Providers will be with your shortly!

        **__Your order details are:__**

        **Selected Bot**
        {products[number - 1].upper()}

        **Price**
        $TBD

        **Rental Duration**
        {duration.upper()}

        *If you have a valid discount code please send them into this channel
        before your order is completed. Feel free to get in touch with our
        qualified staff team if you have questions moving forward.*

        '''
        embed = discord.Embed(title = 'Your order details are ready!',description = description,color = discord.Color.dark_green())
        embed.set_footer(text = 'Sofio Rentals',icon_url = bot.user.avatar_url)
        embed.set_thumbnail(url = bot.user.avatar_url)
        await channel.send(embed = embed)
        with open('Config/Cache.json') as f:
            cache = json.load(f)

        cache[channel.id] = {}
        cache[channel.id]['Buyer'] = member.id
        cache[channel.id]['Seler'] = 'NONE'

        with open('Config/Cache.json','w') as f:
            json.dump(cache,f,indent = 3)
        
        with open('Config/Sales.json') as f:
            sales = json.load(f)
        
        sales[str(member.id)] = {}
        sales[str(member.id)]['Product'] = products[number - 1]
        sales[str(member.id)]['Amount'] = 0
        sales[str(member.id)]['Status'] = 'PENDING'
        sales[str(member.id)]['Discount'] = '0'
        sales[str(member.id)]['Duration'] = duration
        sales[str(member.id)]['Method'] = 'None'
        sales[str(member.id)]['Price'] = 'None'

        with open('Config/Sales.json','w') as f:
            json.dump(sales,f,indent  = 3)

@bot.command()
async def claim(ctx):
    channel = str(ctx.channel.id)
    with open('Config/Cache.json') as f:
        cache = json.load(f)
    
    if not channel in cache:
        await ctx.send(':warning: Invalid channel or Not available for the claim yet.')
        return
    
    cache[channel]['Seller'] = ctx.author.id
    await ctx.author.send(':white_check_mark: Ticket has been CLAIMED by you.')

    with open('Config/Cache.json', 'w') as f:
        json.dump(cache,f,indent = 3)
    
    await ctx.message.delete()

@bot.command()
async def payment(ctx):
    with open('Config/Cache.json', 'r') as f:
        cache = json.load(f)
    
    with open('Config/Sellers.json') as f:
        sl = json.load(f)

    if str(ctx.channel.id) in cache:
        if ctx.author.id == cache[str(ctx.channel.id)]['Seller']:
            sellr = str(ctx.author.id)
            cashapp = sl[sellr]['Cashapp']
            paypal = sl[sellr]['Paypal']
            revolut = sl[sellr]['Revolut']
            venmo = sl[sellr]['Venmo']
            zelle = sl[sellr]['Zelle']
            buyer = await bot.fetch_user(int(cache[str(ctx.channel.id)]['Buyer']))

            description = f'''
            **__Important Payment Information__**

            > **Rentee:** {buyer}
            > **Discord ID:** {buyer.id}

            > :small_orange_diamond: Please send all payments as **Friends and Family**
            > :small_orange_diamond: Send payments **without** any notes
            > :small_orange_diamond: Please post a **screenshot of the payment confirmation**

            **__Please choose one of the payment methods down below!__**

            <:SofloRentalsCashApp:864534361238798366> **Cashapp:** {cashapp}

            <:SofloRentalsPaypal:864534470824296469> **Paypal:** {paypal}

            <:SofloRentalsRevolut:864534631965655060> **Revolut:** {revolut}

            <:SofloRentalsVenmo:864534707059163157> **Venmo:** {venmo}

            <:SofloRentalsZelle:864534791851737108> **Zelle:** {zelle}

            ***Once you have selected a payment method, please send the order amount to your preferred method and let our staff/provider know when the transaction is completed!***
            '''
            embed = discord.Embed(title = 'Sofio Rentals - Payment Methods',description = description,color = discord.Color.dark_green())
            embed.set_thumbnail(url = bot.user.avatar_url)
            embed.set_footer(text = 'Sofio Rentals',icon_url = bot.user.avatar_url)
            await ctx.send(embed = embed)
            
        
        else:
            await ctx.author.send(":warning: You don't have the perrmisions to access this TICKET")
    
    else:
        await ctx.send(':warning: Invalid Channel')

    await ctx.message.delete()


@bot.command()
async def log(ctx,method:str = None):    
    with open('Config/Cache.json') as f:
        cache = json.load(f)
    
    if not str(ctx.channel.id) in cache:
        await ctx.send(':warning: Invalid Channel (Please use the main ticket channel)')
        return
    
    if not int(ctx.author.id) == cache[str(ctx.channel.id)]['Seller']:
        await ctx.send(':warning: You dont have the permissions for this action.')
        return
    
    if not method:
        await ctx.send(':information_source: Usage: !log `<PAYMENT METHOD>` (From which the payment was DONE)')
        return
    
    channel = str(ctx.channel.id)

    dt = datetime.datetime.today().strftime('%m/%d/%y')
    buyer = await bot.fetch_user(cache[channel]['Buyer'])
    seller = await bot.fetch_user(cache[channel]['Seller'])
    
    with open('Config/Sales.json') as f:
        sales = json.load(f)
    
    discount = sales[str(buyer.id)]['Discount']
    duration = sales[str(buyer.id)]['Duration']
    price_ = sales[str(buyer.id)]['Price']
    message = f'''
    **__General Information:__**

    > **Date:** `{dt}`

    > **Rentee:** `{buyer}`
    > **Rentee ID:** `{buyer.id}`

    > **Renter:** `{seller}`
    > **Renter ID:** `{seller.id}`

    **__Financial Information:__**

    > **Sale amount:** `{price_}$`
    > **Discount:** `{discount}`
    > **Duration:** `{duration}`

    > **Payment Method:** `{method.upper()}`
    '''
    embed = discord.Embed(color = discord.Color.dark_green(),title = 'A new sale was successfully logged!',description = message)
    embed.set_thumbnail(url = bot.user.avatar_url)
    embed.set_footer(text = 'Soflo Rentals',icon_url= bot.user.avatar_url)
    await ctx.send(embed = embed)

@bot.command()
async def seller(ctx,action:str = None):
    if not action:
        await ctx.send(':information_source: Usage: !seller `<ACTION>`  `(ALLOWED - Update / Delete / Create)`')
        return
    
    with open('Config/Sellers.json') as f:
        sl = json.load(f)
    
    action = action.lower()
    
    if action == 'create':
        discord_name = str(ctx.author)
        discord_id = str(ctx.author.id)
        if discord_id in sl:
            await ctx.send(':warning: Profile already exists. For modifying, Please use `!seller update`')
            return

        num = 0
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        await ctx.send(':arrow_double_down: **Enter your <:SofloRentalsCashApp:864534361238798366> Cashapp Details:** `(Type None if None)`')
        cashapp = await bot.wait_for('message',check = check)
        await ctx.send(':arrow_double_down: **Enter your <:SofloRentalsPaypal:864534470824296469> Paypal Details:** `(Type None if None)`')
        paypal = await bot.wait_for('message',check = check)
        await ctx.send(':arrow_double_down: **Enter your <:SofloRentalsRevolut:864534631965655060> Revolut Details:** `(Type None if None)`')
        revolut = await bot.wait_for('message',check = check)
        await ctx.send(':arrow_double_down: **Enter your <:SofloRentalsVenmo:864534707059163157> Venmo Details:** `(Type None if None)`')
        venmo = await bot.wait_for('message',check = check)
        await ctx.send(':arrow_double_down: **Enter your <:SofloRentalsZelle:864534791851737108> Zelle Details:** `(Type None if None)`')
        zelle = await bot.wait_for('message',check = check)
        cashapp = cashapp.content
        paypal = paypal.content
        revolut = revolut.content
        venmo = venmo.content
        zelle = zelle.content

        sl[discord_id] = {}
        sl[discord_id]['Discord_Name'] = discord_name
        sl[discord_id]['Cashapp'] = cashapp if not cashapp.lower() == 'none' else 'Not Available'
        sl[discord_id]['Paypal'] = paypal if not paypal.lower() == 'none' else 'Not Available'
        sl[discord_id]['Revolut'] = revolut if not revolut.lower() == 'none' else 'Not Available'
        sl[discord_id]['Venmo'] = venmo if not venmo.lower() == 'none' else 'Not Available'
        sl[discord_id]['Zelle'] = zelle if not zelle.lower() == 'none' else 'Not Available'
        with open('Config/Sellers.json','w') as f:
            json.dump(sl,f,indent= 3)
        
        await ctx.send(':white_check_mark: Your profile has been created.')

    elif action == 'update':
        pass

    elif action == 'delete':
        discord_id = str(ctx.author.id)
        if not discord_id in sl:
            await ctx.send(':warning: Profile not found.')
            return   
        
        sl.pop(discord_id)
        with open('Config/Sellers.json','w') as f:
            json.dump(sl,f,indent = 3)
        
        await ctx.send(':white_check_mark: Profile has been deleted.')
    


@bot.command()
async def deliver(ctx,*,key:str = None):
    if not key:
        await ctx.send(':information_source: Command Usage: !deliver `<YOUR KEY>`')
        return
    
    with open('Config/Cache.json') as f:
        cache = json.load(f)
    
    if not str(ctx.channel.id) in cache:
        await ctx.send(':warning: Invalid Channel (Please use the main ticket channel)')
        return
    
    if not int(ctx.author.id) == cache[str(ctx.channel.id)]['Seller']:
        await ctx.send(':warning: You dont have the permissions for this action.')
        return


    message = '''
    Please check your DM to access your @productname key.

    **__Setup Process:__**
    **1)** Download the software located in #kodai-download.
    **2)** Insert the license key from above into the bot.
    **3)** The corresponding bot guide is available via #kodai-guide

    **_Please visit:**
    :small_orange_diamond: #kodai-updates for any bot updates
    :small_orange_diamond: #kodai-release-guides for additional setup information

    ***Once you have received your key, please activate your key immediately to prevent any last-minute problems before the drop! Make sure to setup in a timely manner!***

    :sos: **__Still confused?__**
    *If you have any further questions regarding your setup, feel free to get in touch with one of our many qualified support members by opening a ticket in #support-ticket.*
    '''


    embed = discord.Embed(color = discord.Color.dark_green(),title = 'You are ready to roll!',description = message)
    embed.set_thumbnail(url = bot.user.avatar_url)
    embed.set_footer(text = 'Soflo Rentals',icon_url= bot.user.avatar_url)
    await ctx.send(embed = embed)
    with open('Config/Sales.json') as f:
        sales = json.load(f)
    

    
    buyer = await bot.fetch_user(int(cache[str(ctx.channel.id)]['Buyer']))
    product_name = sales[str(buyer.id)]['Product']

    message = f'''
    Your @{product_name} key got delivered.

    **Key:** {key}

    > **Rentee:** {buyer}
    > **Discord ID:** {buyer.id}

    **__Setup Process:__**
    **1)** Download the software located in #kodai-download.
    **2)** Insert the license key from above into the bot.
    **3)** The corresponding bot guide is available via #kodai-guide

    **__Please visit:__**
    :small_orange_diamond: #kodai-updates for any bot updates
    :small_orange_diamond: #kodai-release-guides for additional setup information

    ***Once you have received your key, please activate your key immediately to prevent any last-minute problems before the drop! Make sure to setup in a timely manner!***

    :sos: **__Still confused?__**
    *If you have any further questions regarding your setup, feel free to get in touch with one of our many qualified support members by opening a ticket in #support-ticket*

    '''
    embed = discord.Embed(color = discord.Color.dark_green(),title = 'Thank you for your purchase!',description = message)
    embed.set_thumbnail(url = bot.user.avatar_url)
    embed.set_footer(text = 'Soflo Rentals',icon_url= bot.user.avatar_url)
    await buyer.send(embed = embed)
    await ctx.message.delete()

TOKEN = 'ODY1NDY3NzA4MzAzNDc0Njk5.YPEbnQ.6lka1tA8IvicxkTpnuEMarJObz4'
bot.run(TOKEN)