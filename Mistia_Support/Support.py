

import discord
from discord.ext import commands, tasks
#from discord_slash import SlashCommand, SlashContext
import json
import datetime
import asyncio

'''
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow
from discord_slash.utils.manage_components import create_actionrow, create_button, wait_for_component

from discord_slash.context import ComponentContext
'''

bot = commands.Bot(command_prefix = 'ms.', intents = discord.Intents.all())
#slash = SlashCommand(bot, sync_commands=True)

partner_responses = {}


@bot.event
async def on_ready():
    print('----- PROTECTION BOT HAS STARTED -----')
    await bot.wait_until_ready()

COLOR = discord.Color.from_rgb(34,34,34)

@commands.has_permissions(administrator = True)
@bot.command()
async def support(ctx):
    msg = '''
Vous avez besoin d'aide, signaler quelqu'un, ou faire une demande de partenariat ?

Merci d'effectuer la commande correspondante :
> • Faire un signalement : /report et suivez la procédure.
> • Faire une demande de partenaire : /partenaire et suivez la procédure.
    '''
    embed = discord.Embed(color = COLOR, title = 'SUPPORT ET PARTENARIAT :', description = msg)
    embed.set_image(url = 'https://zupimages.net/up/22/08/5dpp.gif')
    await ctx.send(embed = embed)

@bot.command()
async def report(ctx):
    await ctx.message.delete()
    def message_check(msg):
        return msg.author == ctx.author and msg.guild == None

    report_type = {'Spam' : '1️⃣','Publicité en message privé' : '2️⃣','Insulte(s)' : '3️⃣','Troll' : '4️⃣','Autre' : '5️⃣'}
    responses = {}


    msg = '''
Voulez-vous lancer la procédure de plainte ?

↳ Oui [<a:Pour:955064316598550549>]
↳ Non [<a:Contre:955064316594368532>]
'''
    embed = discord.Embed(title = 'CONFIRMATION :', description = msg)
    confirm = await ctx.send(embed = embed)
    for x in bot.emojis:
        if str(x) in ('<a:Pour:955064316598550549>', '<a:Contre:955064316594368532>'):
            await confirm.add_reaction(x)

    def check(reaction, user):
        return user == ctx.message.author

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=300, check=check)
        await reaction.message.delete()

        if str(reaction.emoji) == '<a:Pour:955064316598550549>':
            msg = '''
Quelle est la raison du report :
↳ Spam : 1️⃣
↳ Publicité en message privé : 2️⃣
↳ Insulte(s) : 3️⃣
↳ Troll : 4️⃣
↳ Autre : 5️⃣
            '''

            embed = discord.Embed(title=  'ETAPE 1/3 :', description = msg)
            try:
                msg = await ctx.author.send(embed = embed)

            except discord.Forbidden:
                msg = '''
    Une erreur est survenue : vos messages privés sont fermés

    Pour les ouvrir :
    ↳ Paramètres [<:MC_Serveur:906936886960984144>]
    ↳ Confidentialité & Sécurité
    ↳ Autoriser les messages privés venant des membres du serveur

    Et retentez la commande /report)
                '''
                embed = discord.Embed(title=  'ERREUR', description = msg)
                await ctx.author.send(embed = embed)
                return
            
            for x in ('1️⃣', '2️⃣', '3️⃣','4️⃣', '5️⃣'):
                await msg.add_reaction(x)

            reaction, user = await bot.wait_for('reaction_add', timeout=300, check=check)
            emoji = str(reaction.emoji)

            if reaction.emoji == '<a:Contre:955064316594368532>':
                await ctx.author.send("<a:Contre:955064316594368532> ︙Vous avez annulé la plainte.")
                return

            author = str(ctx.author.id)
            responses[author] = []
            responses[author].append(emoji)

            while True:
                msg = '''
    Quel est l'identifiant du membre que vous souhaitez report :

    *Vous ne savez pas comment trouver l'identifiant ?[Cliquez ici](https://support.discord.com/hc/fr/articles/206346498-Où-trouver-l-ID-de-mon-compte-utilisateur-serveur-message-)*      
    '''     
                embed = discord.Embed(description = msg, title = 'ETAPE 2/3 :')
                msg1 = await ctx.author.send(embed = embed)
                msg = await bot.wait_for('message',timeout=300,  check = message_check)
                content = msg.content

                try:
                    user = await bot.fetch_user(int(content))
                    break

                except:
                    continue

            id_ = user.id
            responses[author].append(id_)
            msg = f'''
Est-ce la personne que vous souhaitez report :
{user} | `{id_}`

↳ Oui [<a:Pour:955064316598550549>]
↳ Non [<a:Contre:955064316594368532>]
            '''
            embed = discord.Embed(description = msg, title = 'CONFIRMATION ETAPE 2/3 :')
            confirm = await ctx.author.send(embed = embed)
            for x in bot.emojis:
                if str(x) in ('<a:Pour:955064316598550549>', '<a:Contre:955064316594368532>'):
                    await confirm.add_reaction(x)
            
            reaction, user = await bot.wait_for('reaction_add', timeout=300, check=check)

            if reaction.emoji == '<a:Contre:955064316594368532>':
                await ctx.author.send("<a:Contre:955064316594368532> ︙Vous avez annulé la plainte.")
                return
            
            msg = '''
Expliquez-nous ce que la personne a fait :
            '''
            embed = discord.Embed(description = msg, title = 'ETAPE 3/3 :')
            await ctx.author.send(embed = embed)

            msg = await bot.wait_for('message',timeout=300,  check = message_check)

            content = msg.content
            responses[author].append(content)

            msg = f'''
Confirmez-vous les faits suivants :
{content}
↳ Oui [<a:Pour:955064316598550549>]
↳ Non [<a:Contre:955064316594368532>]
'''
            embed = discord.Embed(description = msg, title = 'CONFIRMATION ETAPE 3/3 :')
            confirm = await ctx.author.send(embed = embed)
            for x in bot.emojis:
                if str(x) in ('<a:Pour:955064316598550549>', '<a:Contre:955064316594368532>'):
                    await confirm.add_reaction(x)

            reaction, user = await bot.wait_for('reaction_add', timeout=300, check=check)
            if reaction.emoji == '<a:Contre:955064316594368532>':
                await ctx.author.send("<a:Contre:955064316594368532> ︙Vous avez annulé la plainte.")
                return

            embed = discord.Embed(description = "Envoyez un capture d'écran de votre preuve pouvant confirmer vos dires", title = 'PREUVE:')
            await ctx.author.send(embed  = embed)
            
            msg = await bot.wait_for('message', timeout=300, check = message_check)
            content = msg.content
            
            url = ''
            try:
                attachment = msg.attachments[0]
                url = attachment.url
            except:
                url = content

            responses[author].append(url)

            tt = ''
            for key, value in report_type.items():
                if value in responses[author]:
                    tt = key
            
            demander = await bot.fetch_user(responses[author][1])

            msg = f"> <:MC_Personne:906936886755491870> ︙**DEMANDEUR :**\n\n↳ {user} `{user.id}`\
            \n\n> <:MC_Idee:906936886415753290> ︙**TYPE DE PLAINTE :**\n\n↳ `{tt}`\
            \n\n> <:MC_Actualit:906936886600302602>︙**ACCUSE :**\n\n↳ {demander} `{demander.id}`\
            \n\n> <:MC_PartPub:924476801273700403>︙**EXPLICATIONS :**\n\n```{responses[author][2]}\n```\
            \n\n> <:MC_MAJNotif:907018309172613150> ︙**PREUVE :**\n\n↳ [Cliquez-ici]({responses[author][3]})\
            \n\n> **RECAPITULATIF:**\n\n↳ Cliquez sur l'emoji pour confirmer ou non votre demande :"

            embed = discord.Embed(description = msg , title = 'RECAPITULATIF :')
            confirm = await ctx.author.send(embed = embed)
            for x in bot.emojis:
                if str(x) in ('<a:Pour:955064316598550549>', '<a:Contre:955064316594368532>'):
                    await confirm.add_reaction(x)

            reaction, user = await bot.wait_for('reaction_add', timeout=300, check=check)
            if emoji == '<a:Contre:955064316594368532':
                msg = '''Vous n'avez pas confirmé l'étape, la demande a été annulée, pour recommencer, veuillez effectuer à nouveau la commande /report sur le serveur MISTIA Conceptions | Graphismes & Serveurs.                   '''
                embed = discord.Embed(title = 'ANNULATION DE LA DEMANDE :', description = msg)
                await ctx.author.send(embed = embed)
                return
            
            demander = await bot.fetch_user(responses[author][1])

            msg = f"> <:MC_Personne:906936886755491870> ︙**DEMANDEUR :**\n\n↳ {user} `{user.id}`\
                \n\n> <:MC_Idee:906936886415753290> ︙**TYPE DE PLAINTE :**\n\n↳ `{tt}`\
                \n\n> <:MC_Actualit:906936886600302602>︙**ACCUSE :**\n\n↳ {demander} `{demander.id}`\
                \n\n> <:MC_PartPub:924476801273700403>︙**EXPLICATIONS :**\n\n```{responses[author][2]}\n```\
                \n\n> <:MC_MAJNotif:907018309172613150> ︙**PREUVE :**\n\n↳ [Cliquez-ici]({responses[author][3]})"

            embed = discord.Embed(description = msg , title = 'RECAPITULATIF :')
            embed.set_image(url = 'https://images-ext-2.discordapp.net/external/I5RPtPiQb61b6-mBJJv-hZYSjv3Vwe4jLDWgo4gpCIo/https/zupimages.net/up/22/04/b758.png')

            channel = await bot.fetch_channel(943986649254227978)
            await channel.send(embed = embed)
            return

        elif str(reaction.emoji) == '<a:Contre:955064316594368532>':
            await ctx.author.send("<a:Contre:955064316594368532> ︙Vous avez annulé la plainte.")
            return
    
    except asyncio.TimeoutError:
        await ctx.author.send("<a:Loading:907074827184140308> ︙5 minutes sont passées et vous n'avez pas répondu. Votre plainte a été annulée.")
        await confirm.delete()
        return
    
    except:
        import traceback
        traceback.print_exc()


#! -----------------------------------------------------------------------------

#@slash.slash(name="partenaire", guild_ids=[941324732119285771])
@bot.command()
async def partenaire(ctx):
    global partner_responses

    author = str(ctx.author.id)

    await ctx.message.delete()
    def message_check(msg):
        return msg.author == ctx.author and isinstance(msg.channel, discord.DMChannel)

    report_type = {'Spam' : '1️⃣','Publicité en message privé' : '2️⃣','Insulte(s)' : '3️⃣','Troll' : '4️⃣','Autre' : '5️⃣'}
    responses = {}

    msg = '''
Voulez-vous lancer la procédure de partenariat ?

↳ Oui [<a:Pour:955064316598550549>]
↳ Non [<a:Contre:955064316594368532>]
'''
    embed = discord.Embed(title = 'CONFIRMATION :', description = msg)
    confirm = await ctx.send(embed = embed)
    for x in bot.emojis:
        if str(x) in ('<a:Pour:955064316598550549>', '<a:Contre:955064316594368532>'):
            await confirm.add_reaction(x)

    def check(reaction, user):
        return user == ctx.message.author

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=300, check=check)
        await reaction.message.delete()

        if str(reaction.emoji) == '<a:Pour:955064316598550549>':
            partner_responses[author] = []

            embed = discord.Embed(title=  'ETAPE 1/6 :', description = 'Quel est le nom du serveur ?')
            try:
                msg = await ctx.author.send(embed = embed)
            except discord.Forbidden:
                msg = '''
    Une erreur est survenue : vos messages privés sont fermés

    Pour les ouvrir :
    ↳ Paramètres [<:MC_Serveur:906936886960984144>]
    ↳ Confidentialité & Sécurité
    ↳ Autoriser les messages privés venant des membres du serveur

    Et retentez la commande /report)
                '''
                embed = discord.Embed(title=  'ERREUR', description = msg)
                await ctx.author.send(embed = embed)
                return
            
            msg = await bot.wait_for('message',timeout=300,  check = message_check)
            content = msg.content


            msg = f'''
Confirmez-vous le nom :
`{content}`

↳ Oui [<a:Pour:955064316598550549>]
↳ Non [<a:Contre:955064316594368532>]
            '''
            embed = discord.Embed(title = 'CONFIRMATION ETAPE 1/6 :', description = msg)

            confirm = await ctx.author.send(embed = embed)
            for x in bot.emojis:
                if str(x) in ('<a:Pour:955064316598550549>', '<a:Contre:955064316594368532>'):
                    await confirm.add_reaction(x)

            reaction, user = await bot.wait_for('reaction_add', timeout=300, check=check)
            emoji = str(reaction.emoji)

            if reaction.emoji == '<a:Contre:955064316594368532>':
                await ctx.author.send("<a:Contre:955064316594368532> ︙Vous avez annulé la plainte.")
                return

            partner_responses[author].append(content)


            embed = discord.Embed(title = 'ETAPE 2/6 :', description = "Envoyez un lien d'invitation illimité de votre serveur :")
            msg1 = await ctx.author.send(embed = embed)
            msg = await bot.wait_for('message', timeout=300,check = message_check)
            content = msg.content

            try:
                await bot.fetch_invite(content)
                partner_responses[author].append(content)

            except:
                await ctx.send("<a:Contre:955064316594368532> ︙ Désolé, mais le lien est invalide ou est expiré !")
                return

            msg = f'''
Confirmez-vous le lien :
`{content}`

↳ Oui [<a:Pour:955064316598550549>]
↳ Non [<a:Contre:955064316594368532>]
            '''
            embed = discord.Embed(title = 'CONFIRMATION ETAPE 2/6 :', description = msg)

            confirm = await ctx.author.send(embed = embed)
            for x in bot.emojis:
                if str(x) in ('<a:Pour:955064316598550549>', '<a:Contre:955064316594368532>'):
                    await confirm.add_reaction(x)


            reaction, user = await bot.wait_for('reaction_add', timeout=300, check=check)
            emoji = str(reaction.emoji)

            if reaction.emoji == '<a:Contre:955064316594368532>':
                await ctx.author.send("<a:Contre:955064316594368532> ︙Vous avez annulé la plainte.")
                return
            

            msg = f'''
Quel est le thème du serveur :
↳ Communautaire : 1️⃣
↳ Gaming : 2️⃣
↳ Publicité : 3️⃣
↳ Artistique : 4️⃣
↳ Musical : 5️⃣
↳ Autre : 6️⃣
            '''
            embed = discord.Embed(title = 'ETAPE 3/6 :', description = msg)

            confirm = await ctx.author.send(embed = embed)
            for x in ('1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣'):
                await confirm.add_reaction(x)

            reaction, user = await bot.wait_for('reaction_add', timeout=300, check=check)
            emoji = str(reaction.emoji)

            report_type = {'Musical' : '5️⃣', 'Artistique' : '4️⃣', 'Publicité' : '3️⃣', 'Gaming' : '2️⃣', 'Communautaire' : '1️⃣', 'Autre' : '6️⃣'}

            tt = ''

            for key, value in report_type.items():
                print(value)
                if value == emoji:
                    tt = key

            partner_responses[author].append(tt + ' ' + emoji)


            msg = '''
Présentez-moi le mieux possible votre serveur, ce que vous faites, ce que vous proposez aux membres :
↳ Ne pas envoyer votre pub et ne pas mettre de caractères suivants : * _ ~
            '''
            embed = discord.Embed(title = 'ETAPE 4/6 :', description = msg)
            msg1 = await ctx.author.send(embed = embed)
            msg = await bot.wait_for('message', timeout=300, check = message_check)
            content = msg.content

            msg = f'''
Confirmez-vous votre présentation :
`{content}`

↳ Oui [<a:Pour:955064316598550549>]
↳ Non [<a:Contre:955064316594368532>]
            '''
            embed = discord.Embed(title = 'CONFIRMATION ETAPE 4/6 :', description = msg)

            confirm = await ctx.author.send(embed = embed)
            for x in bot.emojis:
                if str(x) in ('<a:Pour:955064316598550549>', '<a:Contre:955064316594368532>'):
                    await confirm.add_reaction(x)


            reaction, user = await bot.wait_for('reaction_add', timeout=300, check=check)
            emoji = str(reaction.emoji)

            if reaction.emoji == '<a:Contre:955064316594368532>':
                await ctx.author.send("<a:Contre:955064316594368532> ︙Vous avez annulé la plainte.")
                return

            partner_responses[author].append(content)

            msg = f'''
Quelle mention voulez-vous sur notre serveur :
↳ Aucune : 1️⃣
↳ Rôle partenaire : 2️⃣
↳ Here : 3️⃣
            '''

            embed = discord.Embed(title = 'ETAPE 5/6 :', description = msg)

            confirm = await ctx.author.send(embed = embed)
            for x in ('1️⃣', '2️⃣', '3️⃣'):
                await confirm.add_reaction(x)

            reaction, user = await bot.wait_for('reaction_add', timeout=300, check=check)
            emoji = str(reaction.emoji)

            report_type = {'Aucune' : '1️⃣', 'Rôle partenaire' : '2️⃣', 'Here' : '3️⃣'}

            tt = ''

            for key, value in report_type.items():
                print(value)
                if value == emoji:
                    tt = key

            partner_responses[author].append(tt)


            msg = f'''
ETAPE 6/6 :
Quelle mention proposez-vous sur votre serveur :
↳ Aucune : 1️⃣
↳ Rôle partenaire : 2️⃣
↳ Here : 3️⃣
            '''

            embed = discord.Embed(title = 'ETAPE 6/6 :', description = msg)

            confirm = await ctx.author.send(embed = embed)
            for x in ('1️⃣', '2️⃣', '3️⃣'):
                await confirm.add_reaction(x)

            reaction, user = await bot.wait_for('reaction_add', timeout=300, check=check)
            emoji = str(reaction.emoji)

            report_type = {'Aucune' : '1️⃣', 'Rôle partenaire' : '2️⃣', 'Here' : '3️⃣'}

            tt = ''

            for key, value in report_type.items():
                print(value)
                if value == emoji:
                    tt = key

            partner_responses[author].append(tt)
            print(partner_responses[author])
            print(len(partner_responses[author]))

            msg = f'''
> <:MC_Personne:906936886755491870> ︙**DEMANDEUR :**

↳ {user} `{user.id}`

> <:MC_Idee:906936886415753290> ︙**INFORMATIONS SERVEUR :**

↳ Nom du serveur : `{partner_responses[author][0]}`
↳ Lien du serveur : [Cliquez-ici]({partner_responses[author][1]})
↳ Thème du serveur : `{partner_responses[author][2]}`
↳ Présentation :
```
{partner_responses[author][3]}
```
<:MC_PartPub:924476801273700403>︙**NOTIFICATIONS :**

↳ Notification demandée : `{partner_responses[author][4]}`
↳ Notification proposée : `{partner_responses[author][5]}`
'''
            embed = discord.Embed(description = msg , title = 'RECAPITULATIF :')
            embed.set_footer(text = "Cliquez sur l'emoji pour confirmer ou non votre demande :")
            embed.set_image(url = 'https://images-ext-2.discordapp.net/external/I5RPtPiQb61b6-mBJJv-hZYSjv3Vwe4jLDWgo4gpCIo/https/zupimages.net/up/22/04/b758.png')
            confirm = await ctx.author.send(embed = embed)

            for x in bot.emojis:
                if str(x) in ('<a:Pour:955064316598550549>', '<a:Contre:955064316594368532>'):
                    await confirm.add_reaction(x)

            reaction, user = await bot.wait_for('reaction_add', timeout=300, check=check)
            if reaction.emoji == '<a:Contre:955064316594368532>':
                await ctx.author.send("<a:Contre:955064316594368532> ︙Vous avez annulé la plainte.")
                return

            msg = f'''
> <:MC_Personne:906936886755491870> ︙**DEMANDEUR :**
↳ {user} `{user.id}`

> <:MC_Idee:906936886415753290> ︙**INFORMATIONS SERVEUR :**

> Nom du serveur : `{partner_responses[author][0]}`
> Lien du serveur : [Cliquez-ici]({partner_responses[author][1]})
> Thème du serveur : `{partner_responses[author][2]}`
> Présentation :
```
{partner_responses[author][3]}
```
<:MC_PartPub:924476801273700403>︙**NOTIFICATIONS :**

> Notification demandée : `{partner_responses[author][4]}`
> Notification proposée : `{partner_responses[author][5]}`
'''

            embed = discord.Embed(description = msg , title = 'RECAPITULATIF :')
            embed.set_image(url = 'https://images-ext-2.discordapp.net/external/I5RPtPiQb61b6-mBJJv-hZYSjv3Vwe4jLDWgo4gpCIo/https/zupimages.net/up/22/04/b758.png')
            channel = await bot.fetch_channel(943986649254227978)
            await channel.send(embed = embed)
        
        else:
            await confirm.delete()

    except asyncio.TimeoutError:
        await ctx.author.send("<a:Loading:907074827184140308> ︙5 minutes sont passées et vous n'avez pas répondu. Votre plainte a été annulée.")
        await confirm.delete()
        return
        
    except:
        import traceback
        traceback.print_exc()


#! -----------------------------------------------------------------------------
@bot.command()
async def purge(ctx):
    await ctx.channel.purge()

bot.run('OTQzNTcxNjM0MTUxODgyODAz.Yg0_kA.0X-cxfHZ2mWR8-TGxIREBdhja7w')