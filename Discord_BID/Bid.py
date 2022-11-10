import discord
from discord.ext import commands

bids = {}
bot = commands.Bot(command_prefix = '!')

@bot.event
async def on_ready():
    print('----- BIDDING BOT HAS STARTED -----')

@bot.command()
async def pledge(ctx, amount = None, *, item = None):
    if not item or not amount:
        await ctx.send(':information_source: Command Usage: !pledge `<AMOUNT TO BID>` `<ITEM NAME>`')
        return

    global bids
    try:
        msg = await ctx.channel.fetch_message(int(list(bids)[0]))
        if not item.lower() == bids[str(msg.id)]['Item']:
            await ctx.send(':warning: Invalid Item Name')
            return
        
        if ctx.author.id in bids[str(msg.id)]['Participants']:
            await ctx.send(':warning: You have already Placed your BID for this ITEM.')
            return
        

        embed = msg.embeds[0].to_dict()
        desc = bids[list(bids)[0]]['MSG']
        desc += f"• {ctx.author} - __${amount}__\n"
        bids[list(bids)[0]]['MSG'] = desc
        for x in list(embed):
            if x == 'description':
                embed[x] = desc
        
        embed = discord.Embed.from_dict(embed)
        await msg.edit(embed = embed)
        bids[str(msg.id)]['Participants'].append(ctx.author.id)

    except Exception as e:
        print(e)
        await ctx.send(':warning: No Bid is current running in this CHANNEL!!')
        return

@bot.command()
async def startbid(ctx, *, item = None):
    if not item:
        await ctx.send(':information_source: Command Usage: !startbid `<ITEM NAME>`')
        return

    global bids
    await ctx.message.delete()

    desc = '__**Participants**__\n'
    embed = discord.Embed(color = discord.Color.green(), description = desc)
    embed.set_author(name = f'{item} | BIDDING')
    embed.set_footer(text = 'Use: {!pledge to BID}')
    msg = await ctx.send(embed = embed)
    bids[str(msg.id)] = {}
    bids[str(msg.id)]['MSG'] = desc
    bids[str(msg.id)]['Participants'] = []
    bids[str(msg.id)]['Item'] = item.lower()

bot.run('ODc0NTU4MDExNjEwMzcwMDU4.YRItng.DFjlf7SwyHF3OWeAQMv3-jVJmgA')