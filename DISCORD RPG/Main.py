import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import json
from PIL import Image, ImageDraw, ImageFont

bot = commands.Bot(command_prefix = '$')

Fight_Entries = []
match_queue = {}

@bot.event
async def on_ready():
    print('----------- == SERVER HAS STARTED == -------------')

@bot.command()
async def fight(ctx):
    #TODO PENDING MATCHUP
    
    global Fight_Entries   
    global match_queue

    with open('Data.json') as f:
        data = json.load(f)
     
    user = str(ctx.author.id)
    
    #! CREATE AN ACCOUNT IF USER IS NEW
    if not user in data:
        data[user] = 0
        with open('Data.json','w') as f:
            json.dump(data,f,indent = 3)
    
    #! CHECK IF USER is in the QUEUE
    if user in Fight_Entries:
        await ctx.send(':warning: You are already in the QUEUE')
        return
    
    #! If NO SAME RANK IN THE QUEUE or NO MATCHUP
    required = [5000,10000,20000,30000,35000,40000,50000,60000,70000,100000,125000,150000]
    for x in Fight_Entries:
        if x == user:
            continue
        author1 = str(ctx.author.id)
        author2 = str(x)
        RANK1 = data[user]
        RANK2 = data[x]
        max_rank1 = 0
        max_rank2 = 0
        for y in required:
            if data[user] <= y and max_rank1 == 0:
                print(data[user])
                max_rank1 = y
            
            if data[x] <= y and max_rank2 == 0:
                print(data[x])
                max_rank2 = y
            
            if not max_rank1 == 0 and not max_rank2 == 0:
                break
        
        print(max_rank1,max_rank2)
        if RANK1 == RANK2:
            match_queue[author1] = author2
            if not author1 in Fight_Entries:
                Fight_Entries.append(author1)
            
            if not author2 in Fight_Entries:
                Fight_Entries.append(author2)
            us = await bot.fetch_user(int(x))
            await ctx.send(f':crossed_swords: ({ctx.author.mention}) and ({us.mention}) :crossed_swords: will be facing off, watch the stream and wait until your fight is called in the `Announcements Channel`.')
            return

        elif RANK1 >= required[required.index(max_rank2)+1] and not RANK1 > required[required.index(max_rank2)+2]:
            print('TRIGGERED 1')
            match_queue[author1] = author2
            if not author1 in Fight_Entries:
                Fight_Entries.append(author1)
            
            if not author2 in Fight_Entries:
                Fight_Entries.append(author2)
            us = await bot.fetch_user(int(x))
            await ctx.send(f':crossed_swords: ({ctx.author.mention}) and ({us.mention}) :crossed_swords: will be facing off, watch the stream and wait until your fight is called in the `Announcements Channel`.')
            return

        elif RANK2 >= required[required.index(max_rank1)+1] and not RANK2 > required[required.index(max_rank1)+2]:
            print('TRIGGERED 2')
            match_queue[author1] = author2
            if not author1 in Fight_Entries:
                Fight_Entries.append(author1)
            
            if not author2 in Fight_Entries:
                Fight_Entries.append(author2)
            us = await bot.fetch_user(int(x))
            await ctx.send(f':crossed_swords: ({ctx.author.mention}) and ({us.mention}) :crossed_swords: will be facing off, watch the stream and wait until your fight is called in the `Announcements Channel`.')
            return
        try:
            if RANK1 <= required[required.index(max_rank2)-1] and not RANK1 < required[required.index(max_rank2)-2]:
                print('TRIGGERED 3')
                match_queue[author1] = author2
                if not author1 in Fight_Entries:
                    Fight_Entries.append(author1)
                
                if not author2 in Fight_Entries:
                    Fight_Entries.append(author2)
                us = await bot.fetch_user(int(x))
                await ctx.send(f':crossed_swords: ({ctx.author.mention}) and ({us.mention}) :crossed_swords: will be facing off, watch the stream and wait until your fight is called in the `Announcements Channel`.')
                return

            if RANK2 <= required[required.index(max_rank1)-1] and not RANK2 < required[required.index(max_rank1)-2]:
                print('TRIGGERED 4')
                match_queue[author1] = author2
                if not author1 in Fight_Entries:
                    Fight_Entries.append(author1)
                
                if not author2 in Fight_Entries:
                    Fight_Entries.append(author2)
                us = await bot.fetch_user(int(x))
                await ctx.send(f':crossed_swords: ({ctx.author.mention}) and ({us.mention}) :crossed_swords: will be facing off, watch the stream and wait until your fight is called in the `Announcements Channel`.')
                return
        
        except:
            break
    
    print(Fight_Entries)
    await ctx.send(':white_check_mark: Fight Entry Successful. Waiting to find an Opponent.')
    Fight_Entries.append(user)
    print(Fight_Entries)
    return

@bot.command()
async def challenge(ctx,user:discord.User = None):
    if not user:
        await ctx.send(':information_source: Command Usage: !challenge `<@player>`')
        return
    
    elif user == ctx.author:
        await ctx.send(':warning: You cannot challenge yourself.')
        return

    global Fight_Entries
    global match_queue

    with open('Data.json') as f:
        data = json.load(f)

    author1 = str(ctx.author.id)
    author2 = str(user.id)

    if not author1 in data:
        data[author1] = 0
        with open('Data.json','w') as f:
            json.dump(data,f,indent = 3)
    
    if not author2 in data:
        data[author2] = 0
        with open('Data.json','w') as f:
            json.dump(data,f,indent = 3) 

    if author1 in Fight_Entries:
        await ctx.send(':warning: You are already in the QUEUE')
        return
    
    if author2 in Fight_Entries:
        await ctx.send(':warning: The player is already in the QUEUE')
        return     
    
    else:
        def check(m):
            return m.author == user

        await ctx.send(f'{user.mention} Will you accept the Challenge:question: Reply with **`(Y/Yes - N/No)`** `(TIMEOUT IN 30 SECONDS)`')
        try:
            msg = await bot.wait_for('message',check = check,timeout = 30)
            if msg.content.lower() in ('yes','y'):
                match_queue[author1] = author2
                Fight_Entries.append(author1)
                Fight_Entries.append(author2)
                await ctx.send(f':crossed_swords: ({ctx.author.mention}) and ({user.mention}) :crossed_swords: will be facing off, watch the stream and wait until your fight is called in the `Announcements Channel`.')
                return

            else:
                await ctx.send(':warning: Invalid Choice or Player Declined the challenge')
                return

        except asyncio.TimeoutError:
            await ctx.send(':warning: The player failed to accept the challenge in the given time!')
            return

@bot.command()
async def rank(ctx):
    with open('Data.json') as f:
        data = json.load(f)

     
    user = str(ctx.author.id)
    
    #! CREATE AN ACCOUNT IF USER IS NEW
    if not user in data:
        data[user] = 0
        with open('Data.json','w') as f:
            json.dump(data,f,indent = 3)

    def human_format(num):
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0

        return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])
        
    def return_pic(user):
        with open('Data.json') as f:
            data = json.load(f)

        current_rank = data[user] 

        required = [5000,10000,20000,30000,35000,40000,50000,60000,70000,100000,125000,150000]
        for x in required:
            if current_rank <= x:
                percent = (current_rank/(x * 1.0))*100
                print(percent)
                if percent <= 30:
                    filename = 'Images/10.png'
                elif percent <= 50:
                    filename = 'Images/30.png'
                elif percent <= 70:
                    filename = 'Images/50.png'

                elif percent < 100:
                    filename = 'Images/70.png'
                    
                elif percent >= 100:
                    filename = 'Images/100.PNG'
            
                if x in (5000,10000,20000):
                    type_ = 'red'
                else:
                    type_ = 'others'
                
                y = current_rank
                filename = [filename,f'Images/{x}.png',type_,x,y]
                return filename
    
    if return_pic(user)[2] == 'red':
        print(return_pic(user)[4])
        if return_pic(user)[4] < 5000: 
            im = Image.open('Images/Unranked.jpg').convert("RGBA")
            region = im.resize((85, 80)).convert("RGBA")
            background = Image.open('Images/r.png').convert("RGBA")
            background.paste(region,(10,4),mask=region)
        else:
            im = Image.open(return_pic(user)[1]).convert("RGBA")
            region = im.resize((500, 210)).convert("RGBA")
            background = Image.open('Images/r.png').convert("RGBA")
            background.paste(region,(-188,-44),mask=region)
    
    else:
        print(return_pic(user)[4])
        if return_pic(user)[4] < 5000: 
            im = Image.open('Images/Unranked.jpg').convert("RGBA")
            region = im.resize((75, 100)).convert("RGBA")
            background = Image.open('Images/r.png').convert("RGBA")
            background.paste(region,(10,4),mask=region)
        else:
            im = Image.open(return_pic(user)[1]).convert("RGBA")
            region = im.resize((95, 95)).convert("RGBA")
            background = Image.open('Images/r.png').convert("RGBA")
            background.paste(region,(5,4),mask=region)

    d2 = Image.open(return_pic(user)[0])
    background.paste(d2,(115,50))
    background.save('Images/os.png')
    img = Image.open('Images/os.png')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("./l_10646.ttf", 14)
    draw.text((117,30),f"{ctx.author}",(255, 255, 255),font=font)
    font = ImageFont.truetype("./l_10646.ttf", 10)
    draw.text((244,2),f"{human_format(data[user])}/{human_format(return_pic(user)[3])} XP",(169,169,169),font=font)
    img.save('Images/sample-out.png')
    await ctx.send(file=discord.File('Images/sample-out.png'))


@bot.command()
async def queue(ctx):
    global match_queue

    msg = ''
    for num,x in enumerate(match_queue):
        num += 1
        user1 = await bot.fetch_user(int(x))
        user2 = await bot.fetch_user(int(match_queue[x]))
        msg += f"**{num}:** {user1.mention} **(VS)** {user2.mention}\n"
    
    embed = discord.Embed(description = msg,color = discord.Color.red())
    embed.set_author(name = 'Current Matchmaking',icon_url = bot.user.avatar_url)
    await ctx.send(embed = embed)

@has_permissions(administrator = True)
@bot.command(aliases = ['sw'])
async def select_winner(ctx,user:discord.User = None):
    with open('Data.json') as f:
        data = json.load(f)
    global match_queue
    global Fight_Entries
    print(Fight_Entries)
    if not user:
        await ctx.send(':information_source: Usage: !sw `<@user>` or `<USER ID>`')
        return
    else:
        if not str(user.id) in Fight_Entries:
            await ctx.send(':warning: Player has not participated in any FIGHT')
            return
        else:
            for x in match_queue:
                if x == str(user.id):
                    if data[str(x)] == data[str(match_queue[x])]:
                        win = 4000
                        loss = 5500

                    elif data[str(x)] < data[str(match_queue[x])]:
                        win = 4500
                        loss = 5000

                    elif data[str(x)] > data[str(match_queue[x])]:
                        win = 350
                        loss = 5000
                    
                    
                    author = await bot.fetch_user(int(match_queue[x]))
                    await ctx.send(f':tada: {user.mention} has won the FIGHT against {author.mention}')
                    data[x] += win
                    if data[str(author.id)] - loss < 0:
                        data[str(author.id)] = 0
                    else:
                        data[str(author.id)] -= loss

                    with open('Data.json','w') as f:
                        json.dump(data,f,indent = 3)
                    
                    match_queue.pop(str(x))
                    Fight_Entries.remove(str(user.id))
                    Fight_Entries.remove(str(author.id))
                    return

                elif match_queue[x] == str(user.id):
                    if data[str(x)] == data[str(match_queue[x])]:
                        win = 4000
                        loss = 5500

                    elif data[str(x)] > data[str(match_queue[x])]:
                        win = 4500
                        loss = 5000

                    elif data[str(x)] < data[str(match_queue[x])]:
                        win = 350
                        loss = 5000

                    author = await bot.fetch_user(int(x))
                    await ctx.send(f':tada: {user.mention} has won the FIGHT against {author.mention}')
                    data[str(user.id)] += win
                    if data[str(author.id)] - loss < 0:
                        data[str(author.id)] = 0
                    else:
                        data[str(author.id)] -= loss

                    with open('Data.json','w') as f:
                        json.dump(data,f,indent = 3)
                    
                    match_queue.pop(str(x))
                    Fight_Entries.remove(str(author.id))
                    print(Fight_Entries)
                    print(match_queue)
                    Fight_Entries.remove(str(user.id))
                    print(Fight_Entries)
                    print(match_queue)
                    return 


bot.run('ODQ2MDQ3NDcyMzA3Nzk4MDE3.YKp1HA.-GH_gRqk_0EqEqnJ86P4D4LOaCA')