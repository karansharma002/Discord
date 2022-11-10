async def biggoose():

    global words1
    with open('Data.json') as f:
        data = json.load(f)
    
    ch = data['BG']

    ctx = await bot.fetch_channel(ch)
    try:
        stock = words1[0]
        url = f'https://api.tdameritrade.com/v1/marketdata/chains'
        dt = datetime.date.today()
        dt = str(dt.isoformat())
        params = {'apikey': KEY,'symbol':stock,'contractType': 'PUT','strategy': 'ANALYTICAL','strikeCount': 1,'fromDate':dt}
        r = requests.get(url,params = params)
        data = json.loads(r.content)
        for x in data['putExpDateMap']:
            for y in data['putExpDateMap'][x]:
                sorted_data = data['putExpDateMap'][x][y][0]
                stk = sorted_data['totalVolume']
                if stk >= 1000:
                    delta = sorted_data['delta']
                    theta = sorted_data['theta']
                    cost = sorted_data['mark']
                    interest = sorted_data['openInterest']
                    volume = sorted_data['totalVolume']
                    multiplier = sorted_data['multiplier']
                    last = sorted_data['last']
                    premium = volume * multiplier * cost
                    premium = round(premium,2)
                    description = sorted_data['description']
                    embed=discord.Embed(color=discord.Color.dark_blue())
                    embed.set_author(name = f'{stock} PUTS | BIGGOOSE',icon_url= bot.user.avatar_url)
                    embed.add_field(name = 'Sweep',value = stock,inline = False)
                    embed.add_field(name = 'Description',value = description,inline = False)
                    embed.add_field(name = 'Delta',value = delta,inline = False)
                    embed.add_field(name = 'Theta',value = theta,inline = False)
                    embed.add_field(name = 'Cost',value = cost,inline = False)
                    embed.add_field(name = 'Interest',value = interest,inline = False)
                    embed.add_field(name = 'Premium',value = premium,inline = False)
                    embed.add_field(name = 'Volume',value = volume,inline = False)
                    embed.timestamp = datetime.datetime.utcnow()
                    embed.set_footer(icon_url=bot.user.avatar_url)
                    await ctx.send(embed = embed)
                    break
                else:
                    break
            break

        params = {'apikey': KEY,'symbol':stock,'contractType': 'CALL','strategy': 'ANALYTICAL','strikeCount': 1,'fromDate':dt}
        r = requests.get(url,params = params)
        data = json.loads(r.content)
        for x in data['callExpDateMap']:
            for y in data['callExpDateMap'][x]:
                sorted_data = data['callExpDateMap'][x][y][0]
                stk = sorted_data['totalVolume']
                if stk >= 1000:
                    delta = sorted_data['delta']
                    theta = sorted_data['theta']
                    cost = sorted_data['mark']
                    interest = sorted_data['openInterest']
                    volume = sorted_data['totalVolume']
                    multiplier = sorted_data['multiplier']
                    last = sorted_data['last']
                    premium = volume * multiplier * cost
                    premium = round(premium,2)
                    description = sorted_data['description']
                    embed=discord.Embed(color=0xffff00)
                    embed.set_author(name = f'{stock} CALLS | BIGGOOSE',icon_url= bot.user.avatar_url)
                    embed.add_field(name = 'Sweep',value = stock,inline = False)
                    embed.add_field(name = 'Description',value = description,inline = False)
                    embed.add_field(name = 'Delta',value = delta,inline = False)
                    embed.add_field(name = 'Theta',value = theta,inline = False)
                    embed.add_field(name = 'Cost',value = cost,inline = False)
                    embed.add_field(name = 'Interest',value = interest,inline = False)
                    embed.add_field(name = 'Premium',value = premium,inline = False)
                    embed.add_field(name = 'Volume',value = volume,inline = False)
                    embed.timestamp = datetime.datetime.utcnow()
                    embed.set_footer(icon_url=bot.user.avatar_url)
                    await ctx.send(embed = embed)
                    words1.remove(stock)
                    return

                else:    
                    words1.remove(stock)
                    return
            return
    
    except:
        words1.remove(stock)
        import traceback
        print(traceback.print_exc())

async def goldengoose():
    global words2
    with open('Data.json') as f:
        data = json.load(f)
    
    ch = data['GG']

    ctx = await bot.fetch_channel(ch)
    stock = words2[0]

    try:
        url = f'https://api.tdameritrade.com/v1/marketdata/chains'
        dt = datetime.date.today()
        dt = str(dt.isoformat())
        params = {'apikey': KEY,'symbol':stock,'contractType': 'PUT','strategy': 'ANALYTICAL','strikeCount': 1,'fromDate':dt}
        r = requests.get(url,params = params)
        data = json.loads(r.content)
        for x in data['putExpDateMap']:
            for y in data['putExpDateMap'][x]:
                sorted_data = data['putExpDateMap'][x][y][0]
                bg = sorted_data['totalVolume']
                l = sorted_data['mark']
                m = sorted_data['multiplier']
                goose = bg * l * m
                if goose >= 1000000:
                    delta = sorted_data['delta']
                    theta = sorted_data['theta']
                    cost = sorted_data['mark']
                    description = sorted_data['description']
                    interest = sorted_data['openInterest']
                    volume = sorted_data['totalVolume']
                    multiplier = sorted_data['multiplier']
                    last = sorted_data['last']
                    premium = volume * multiplier * cost
                    premium = round(premium,2)
                    embed=discord.Embed(color=discord.Color.dark_blue())
                    embed.set_author(name = f'{stock} PUTS | GOLDENGOOSE',icon_url= bot.user.avatar_url)
                    embed.add_field(name = 'Sweep',value = stock,inline = False)
                    embed.add_field(name = 'Description',value = description,inline = False)
                    embed.add_field(name = 'Delta',value = delta,inline = False)
                    embed.add_field(name = 'Theta',value = theta,inline = False)
                    embed.add_field(name = 'Cost',value = cost,inline = False)
                    embed.add_field(name = 'Interest',value = interest,inline = False)
                    embed.add_field(name = 'Premium',value = premium,inline = False)
                    embed.add_field(name = 'Volume',value = volume,inline = False)
                    embed.timestamp = datetime.datetime.utcnow()
                    embed.set_footer(icon_url=bot.user.avatar_url)
                    await ctx.send(embed = embed)
                    break
                else:
                    break
            break

        params = {'apikey': KEY,'symbol':stock,'contractType': 'CALL','strategy': 'ANALYTICAL','strikeCount': 1,'fromDate':dt}
        r = requests.get(url,params = params)
        data = json.loads(r.content)
        for x in data['callExpDateMap']:
            for y in data['callExpDateMap'][x]:
                sorted_data = data['callExpDateMap'][x][y][0]
                bg = sorted_data['totalVolume']
                l = sorted_data['mark']
                m = sorted_data['multiplier']
                goose = bg * l * m
                if goose >= 1000000:
                    delta = sorted_data['delta']
                    theta = sorted_data['theta']
                    cost = sorted_data['mark']
                    description = sorted_data['description']
                    interest = sorted_data['openInterest']
                    volume = sorted_data['totalVolume']
                    multiplier = sorted_data['multiplier']
                    last = sorted_data['last']
                    premium = volume * multiplier * cost
                    premium = round(premium,2)
                    embed=discord.Embed(color=0xffff00)
                    embed.set_author(name = f'{stock} CALLS | GOLDENGOOSE',icon_url= bot.user.avatar_url)
                    embed.add_field(name = 'Sweep',value = stock,inline = False)
                    embed.add_field(name = 'Description',value = description,inline = False)
                    embed.add_field(name = 'Delta',value = delta,inline = False)
                    embed.add_field(name = 'Theta',value = theta,inline = False)
                    embed.add_field(name = 'Cost',value = cost,inline = False)
                    embed.add_field(name = 'Interest',value = interest,inline = False)
                    embed.add_field(name = 'Premium',value = premium,inline = False)
                    embed.add_field(name = 'Volume',value = volume,inline = False)
                    embed.timestamp = datetime.datetime.utcnow()
                    embed.set_footer(icon_url=bot.user.avatar_url)
                    await ctx.send(embed = embed)
                    
                    words2.remove(stock)
                    return
                else:
                    
                    words2.remove(stock)
                    return
            return
    
    except:
        words2.remove(stock)
        import traceback
        print(traceback.print_exc())

async def chilly():
    global words3
    with open('Data.json') as f:
        data = json.load(f)
    
    ch = data['CL']

    ctx = await bot.fetch_channel(ch)
    stock = words3[0]
    try:
        url = f'https://api.tdameritrade.com/v1/marketdata/chains'
        
        dt = datetime.date.today()
        dt = str(dt.isoformat())
        params = {'apikey': KEY,'symbol':stock,'contractType': 'CALL','strategy': 'ANALYTICAL','strikeCount': 1,'fromDate':dt}
        r = requests.get(url,params = params)
        data = json.loads(r.content)
        for x in data['callExpDateMap']:
            for y in data['callExpDateMap'][x]:
                data = web.get_data_yahoo(stock)
                data['new'] = data.index
                stock_df = Sdf.retype(data)
                data['rsi']=stock_df['rsi_14']
                data = data[data['new'] == str(datetime.date.today() - datetime.timedelta(days = 1))]
                rsi = data['rsi'].astype(str)  
                dt = datetime.date.today()
                dt = str(dt.isoformat())
                sorted_data = data['callExpDateMap'][x][y][0]
                delta = sorted_data['delta']
                theta = sorted_data['theta']
                cost = sorted_data['mark']
                interest = sorted_data['openInterest']
                volume = sorted_data['totalVolume']
                if float(rsi) >= 60 and interest + volume >= 750:
                    multiplier = sorted_data['multiplier']
                    last = sorted_data['last']
                    premium = volume * multiplier * cost
                    premium = round(premium,2)
                    description = sorted_data['description']
                    embed=discord.Embed(color=discord.Color.blue())
                    embed.set_author(name = f'{stock} | CALL | RSI: {float(rsi)}',icon_url= bot.user.avatar_url)
                    embed.add_field(name = 'Sweep',value = stock,inline = False)
                    embed.add_field(name = 'Description',value = description,inline = False)
                    embed.add_field(name = 'Delta',value = delta,inline = False)
                    embed.add_field(name = 'Theta',value = theta,inline = False)
                    embed.add_field(name = 'Cost',value = cost,inline = False)
                    embed.add_field(name = 'Interest',value = interest,inline = False)
                    embed.add_field(name = 'Premium',value = premium,inline = False)
                    embed.add_field(name = 'Volume',value = volume,inline = False)
                    embed.timestamp = datetime.datetime.utcnow()
                    embed.set_footer(icon_url=bot.user.avatar_url)
                    await ctx.send(embed = embed)

        params = {'apikey': KEY,'symbol':stock,'contractType': 'CALL','strategy': 'ANALYTICAL','strikeCount': 1,'fromDate':dt}
        r = requests.get(url,params = params)
        data = json.loads(r.content)
        for x in data['callExpDateMap']:
            for y in data['callExpDateMap'][x]:
                data = web.get_data_yahoo(stock)
                data['new'] = data.index
                stock_df = Sdf.retype(data)
                data['rsi']=stock_df['rsi_14']
                data = data[data['new'] == str(datetime.date.today() - datetime.timedelta(days = 1))]
                rsi = data['rsi'].astype(str)  
                dt = datetime.date.today()
                dt = str(dt.isoformat())
                url = f'https://api.tdameritrade.com/v1/marketdata/chains'
                sorted_data = data['callExpDateMap'][x][y][0]
                delta = sorted_data['delta']
                theta = sorted_data['theta']
                cost = sorted_data['mark']
                interest = sorted_data['openInterest']
                volume = sorted_data['totalVolume']
                if float(rsi) >= 60 and interest + volume >= 750:
                    multiplier = sorted_data['multiplier']
                    last = sorted_data['last']
                    premium = volume * multiplier * cost
                    premium = round(premium,2)
                    description = sorted_data['description']
                    embed=discord.Embed(color=discord.Color.purple())
                    embed.set_author(name = f'{stock} | CALL | RSI: {float(rsi)}',icon_url= bot.user.avatar_url)
                    embed.add_field(name = 'Sweep',value = stock,inline = False)
                    embed.add_field(name = 'Description',value = description,inline = False)
                    embed.add_field(name = 'Delta',value = delta,inline = False)
                    embed.add_field(name = 'Theta',value = theta,inline = False)
                    embed.add_field(name = 'Cost',value = cost,inline = False)
                    embed.add_field(name = 'Interest',value = interest,inline = False)
                    embed.add_field(name = 'Premium',value = premium,inline = False)
                    embed.add_field(name = 'Volume',value = volume,inline = False)
                    embed.timestamp = datetime.datetime.utcnow()
                    embed.set_footer(icon_url=bot.user.avatar_url)
                    await ctx.send(embed = embed)                     

        url = f'https://api.tdameritrade.com/v1/marketdata/chains'
        stock = words3[0]
        dt = datetime.date.today()
        dt = str(dt.isoformat())
        params = {'apikey': KEY,'symbol':stock,'contractType': 'PUT','strategy': 'ANALYTICAL','strikeCount': 1,'fromDate':dt}
        r = requests.get(url,params = params)
        data = json.loads(r.content)
        for x in data['putExpDateMap']:
            for y in data['putExpDateMap'][x]:
                data = web.get_data_yahoo(stock)
                data['new'] = data.index
                stock_df = Sdf.retype(data)
                data['rsi']=stock_df['rsi_14']
                data = data[data['new'] == str(datetime.date.today() - datetime.timedelta(days = 1))]
                rsi = data['rsi'].astype(str)  
                dt = datetime.date.today()
                dt = str(dt.isoformat())
                sorted_data = data['putExpDateMap'][x][y][0]
                delta = sorted_data['delta']
                theta = sorted_data['theta']
                cost = sorted_data['mark']
                interest = sorted_data['openInterest']
                volume = sorted_data['totalVolume']
                if float(rsi) >= 60 and interest + volume >= 750:
                    multiplier = sorted_data['multiplier']
                    last = sorted_data['last']
                    premium = volume * multiplier * cost
                    premium = round(premium,2)
                    description = sorted_data['description']
                    embed=discord.Embed(color=discord.Color.blue())
                    embed.set_author(name = f'{stock} | PUT | RSI: {float(rsi)}',icon_url= bot.user.avatar_url)
                    embed.add_field(name = 'Sweep',value = stock,inline = False)
                    embed.add_field(name = 'Description',value = description,inline = False)
                    embed.add_field(name = 'Delta',value = delta,inline = False)
                    embed.add_field(name = 'Theta',value = theta,inline = False)
                    embed.add_field(name = 'Cost',value = cost,inline = False)
                    embed.add_field(name = 'Interest',value = interest,inline = False)
                    embed.add_field(name = 'Premium',value = premium,inline = False)
                    embed.add_field(name = 'Volume',value = volume,inline = False)
                    embed.timestamp = datetime.datetime.utcnow()
                    embed.set_footer(icon_url=bot.user.avatar_url)
                    await ctx.send(embed = embed)
                    words3.pop(0)
                    return

        params = {'apikey': KEY,'symbol':stock,'contractType': 'PUT','strategy': 'ANALYTICAL','strikeCount': 1,'fromDate':dt}
        r = requests.get(url,params = params)
        data = json.loads(r.content)
        for x in data['putExpDateMap']:
            for y in data['putExpDateMap'][x]:
                data = web.get_data_yahoo(stock)
                data['new'] = data.index
                stock_df = Sdf.retype(data)
                data['rsi']=stock_df['rsi_14']
                data = data[data['new'] == str(datetime.date.today() - datetime.timedelta(days = 1))]
                rsi = data['rsi'].astype(str)  
                dt = datetime.date.today()
                dt = str(dt.isoformat())
                url = f'https://api.tdameritrade.com/v1/marketdata/chains'
                sorted_data = data['putExpDateMap'][x][y][0]
                delta = sorted_data['delta']
                theta = sorted_data['theta']
                cost = sorted_data['mark']
                interest = sorted_data['openInterest']
                volume = sorted_data['totalVolume']
                if float(rsi) >= 60 and interest + volume >= 750:
                    multiplier = sorted_data['multiplier']
                    last = sorted_data['last']
                    premium = volume * multiplier * cost
                    premium = round(premium,2)
                    description = sorted_data['description']
                    embed=discord.Embed(color=discord.Color.purple())
                    embed.set_author(name = f'{stock} | PUT | RSI: {float(rsi)}',icon_url= bot.user.avatar_url)
                    embed.add_field(name = 'Sweep',value = stock,inline = False)
                    embed.add_field(name = 'Description',value = description,inline = False)
                    embed.add_field(name = 'Delta',value = delta,inline = False)
                    embed.add_field(name = 'Theta',value = theta,inline = False)
                    embed.add_field(name = 'Cost',value = cost,inline = False)
                    embed.add_field(name = 'Interest',value = interest,inline = False)
                    embed.add_field(name = 'Premium',value = premium,inline = False)
                    embed.add_field(name = 'Volume',value = volume,inline = False)
                    embed.timestamp = datetime.datetime.utcnow()
                    embed.set_footer(icon_url=bot.user.avatar_url)
                    await ctx.send(embed = embed)  
                    words3.pop(0)
                    return

        words3.pop(0)

    except:
        words3.pop(0)
        import traceback
        print(traceback.print_exc())

async def squeezescan():
    global words4
    with open('Data.json') as f:
        data = json.load(f)
    
    ch = data['SC']

    ctx = await bot.fetch_channel(ch)
    stock = words4[0]
    try:
        
        print(stock)
        url = f'https://api.tdameritrade.com/v1/marketdata/{stock}/pricehistory'
        params = {'apikey': KEY}
        r = requests.get(url,params = params)
        data = json.loads(r.content)
        data = web.get_data_yahoo(stock)
        data['new'] = data.index
        stock_df = Sdf.retype(data)
        data['rsi']=stock_df['rsi_14']
        data['ma'] = stock_df['cr-ma2']
        data['ema'] = stock_df['dx_9_ema']
        data = data[data['new'] == str(datetime.date.today() - datetime.timedelta(days = 1))]
        ema = float(data['ema'].astype(str))
        ma = float(data['ma'].astype(str))
        price = stockquotes.Stock(stock)
        price = float(price.current_price)
        price_high = float(data['high'].astype(str))
        price_low = float(data['low'].astype(str))
        price_close = float(data['close'].astype(str))
        avg = float(data['10DR_Vol'].astype(str))
        volume = float(data['Volume'].astype(str))
        rel = avg * 0.25 

        if price >= ema and price >= ma and volume >= rel:
            embed = discord.Embed(color = discord.Colour.red())
            embed.set_author(name = f'{stock} | Technical Analysis',icon_url= bot.user.avatar_url)
            pivot = (price_high + price_low + price_close) / 3
            r1 = 2 * pivot - price_low
            s1 = 2 * pivot - price_high
            s2 = pivot - (r1 - s1)
            r2 = pivot + (r1 - s1)
            diff = price_high - price_low
            f1 = price_low + (diff * 0.618)
            f2 = price_low + (diff * 0.5)
            f3 = price_low + (diff * 0.382)
            r1 = round(r1,2)
            r2 = round(r2,2)
            s1 = round(s1,2)
            s2 = round(s2,2)
            f1 = round(f1,2)
            f2 = round(f2,2)
            f3 = round(f3,2)
            price = stockquotes.Stock(stock)
            price = float(price.current_price)
            last = round(float(data['adj close'].as_type(str)),2)
            embed.add_field(name = '1st Support Level',value = s1,inline = False)
            embed.add_field(name = '2nd Support Level',value = s2,inline = False)
            embed.add_field(name = 'Current Price',value = price,inline = False)
            embed.add_field(name = 'Last Price',value = last,inline = False)
            embed.add_field(name = '1st Resistance Point',value = r1,inline = False)
            embed.add_field(name = '2nd Resistance Point',value = r2,inline = False)
            embed.add_field(name = 'Fibonacci 61.8%',value = f1,inline = False)
            embed.add_field(name = 'Fibonacci 50%',value = f2,inline = False)
            await ctx.send(embed = embed)
            words4.pop(0)

        else:
            words4.pop(0)

    except:
        words4.pop(0)
        import traceback
        print(traceback.print_exc())

async def squeezescan():
    global words5
    with open('Data.json') as f:
        data = json.load(f)
    
    ch = data['SS']

    ctx = await bot.fetch_channel(ch)
    stock = words5[0]
    try:
        
        print('SQ',stock)
        url = f'https://api.tdameritrade.com/v1/instruments'
        params = {'apikey': KEY,"symbol":stock,"projection":"fundamental"}
        r = requests.get(url,params = params)
        data = json.loads(r.content)
        peg = float(data[stock]['fundamental']['pegRatio'])
        data = web.get_data_yahoo(stock)
        data['new'] = data.index
        stock_df = Sdf.retype(data)
        data['rsi']=stock_df['rsi_14']
        data['ma'] = stock_df['cr-ma3']
        data['ema'] = stock_df['dx_9_ema']
        data = data[data['new'] == str(datetime.date.today() - datetime.timedelta(days = 1))]
        ema = float(data['ema'].astype(str))
        chk = float(data['ma'].astype(str))
        price_high = float(data['high'].astype(str))
        price_low = float(data['low'].astype(str))
        price_close = float(data['close'].astype(str))
        m = stockquotes.Stock(stock)
        m = float(m.current_price)
        m = round(m,2)
        l = price_low
        V = float(data['1DR_Vol'].astype(str))
        avgv = float(data['10DR_Vol'].astype(str))
        diff = chk - l
        drk = chk - m
        t = diff - drk
        p = m * 0.0125
        w = avgv * 2.5
        if t >= 0.5 and V >= w:
            embed = discord.Embed(color = discord.Colour.red())
            embed.set_author(name = f'{stock} | Technical Analysis',icon_url= bot.user.avatar_url)
            pivot = (price_high + price_low + [price_close]) / 3
            r1 = 2 * pivot - price_low
            s1 = 2 * pivot - price_high
            s2 = pivot - (r1 - s1)
            r2 = pivot + (r1 - s1)
            diff = price_high - price_low
            f1 = price_low + (diff * 0.618)
            f2 = price_low + (diff * 0.5)
            f3 = price_low + (diff * 0.382)
            r1 = round(r1,2)
            r2 = round(r2,2)
            s1 = round(s1,2)
            s2 = round(s2,2)
            f1 = round(f1,2)
            f2 = round(f2,2)
            f3 = round(f3,2)
            price = stockquotes.Stock(stock)
            price = float(price.current_price)
            price = round(price,2)
            last = round(float(data['adj close'].as_type(str)),2)
            embed.add_field(name = '1st Support Level',value = s1,inline = False)
            embed.add_field(name = '2nd Support Level',value = s2,inline = False)
            embed.add_field(name = 'Current Price',value = price,inline = False)
            embed.add_field(name = 'Last Price',value = last,inline = False)
            embed.add_field(name = '1st Resistance Point',value = r1,inline = False)
            embed.add_field(name = '2nd Resistance Point',value = r2,inline = False)
            embed.add_field(name = 'Fibonacci 61.8%',value = f1,inline = False)
            embed.add_field(name = 'Fibonacci 50%',value = f2,inline = False)
            embed.add_field(name = 'Fibonacci 38.2%',value = f3,inline = False)
            await ctx.send(embed = embed)
            words5.pop(0)
        else:
            words5.pop(0)

    except:
        words5.pop(0)
        import traceback
        print(traceback.print_exc())