import asyncio
import discord
from discord.ext import commands
import json
bot = commands.Bot(command_prefix= '%',intents = discord.Intents.all())

@bot.event
async def on_ready():
    print('Server has Started')

@bot.command()
async def setup(ctx,channel:discord.TextChannel = None):
    embed = discord.Embed(title = 'Disclaimer ',color = discord.Color.green())

    field1 = """
    Welcome to Catalyst Trading. Catalyst Trading is offered to you conditioned on your acceptance without modification of the terms, conditions and notices contained herein (the “Terms”). Your use of Catalyst Trading constitutes to that you agree to all such Terms. Please read these terms, carefully, and keep a copy of them for your reference. 

    Catalyst Trading is a Forum/Online discussion Site. Conquered Catalyst Trading LLC is for informational and entertainment purposes only. Catalyst Trading LLC moderators, administrators, and employees are not investment advisers.

    """
    embed.add_field(name = 'Agreement between User and Catalyst Trading',value = field1,inline = False)

    field2 = """
    Trading Catalyst may contain links to other websites ("Linked Sites"). The Linked Sites are not under the control of Trading Catalyst and Trading Catalyst is not responsible for the contents of any Linked Site, including without limitation any link contained in a Linked Site, or any changes or updates to a Linked Site. Trading Catalyst is providing these links to you only as a convenience, and the inclusion of any link does not imply endorsement by Catalyst Trading of the site or any association with its operators. 

    Certain services made available via Catalyst Trading are delivered by third party sites and organizations. By using any product, service, or functionality originating from the Trading Catalyst domain, you hereby acknowledge and consent that Trading Catalyst may share such information and data with any third party with whom Trading Catalyst has a contractual relationship to provide the requested product, service or functionality on behalf of Catalyst Trading users and customers. 

    """
    embed.add_field(name = 'Links to Third Party Sites/Third Party Services',value = field2,inline =False)

    field3 = """
    Trading Catalyst does not knowingly collect, either online or offline, personal information from users. You must be 18 years of age to be a part of the discord server.
    """

    embed.add_field(name = 'Users Under Eighteen',value = field3,inline = False)

    field4 = """
    You are granted a non-exclusive, non-transferable, revocable license to access and use Trading Catalyst strictly in accordance with these terms of use. 

    You warrant to Trading Catalyst that you will not use the Site for any purpose that is unlawful or prohibited by these Terms. You may not use the Site in any manner which could damage, disable, overburden, or impair the Site or interfere with any other party's use and enjoyment of the Site. You may not obtain or attempt to obtain any materials or information through any means not intentionally made available or provided for through the Site.

    All content included as part of the Service, such as text, graphics, logos, images, as well as the compilation thereof, and any software used on the Site, is the property of Trading Catalyst or its suppliers and protected by copyright and other laws that protect intellectual property and proprietary rights. You agree to observe and abide by all copyright and other proprietary notices, legends, or other restrictions contained in any such content and will not make any changes thereto.

    You will not modify, publish, transmit, reverse engineer, participate in the transfer or sale, create derivative works, or in any way exploit any of the content, in whole or in part, found on the Site. Catalyst Trading content is not for resale. Your use of the Site does not entitle you to make any unauthorized use of any protected content, and in particular, you will not delete or alter any proprietary rights or attribution notices in any content. You will use protected content solely for your personal use and will make no other use of the content without the express written permission of Catalyst Trading and the copyright owner. You agree that you do not acquire any ownership rights in any protected content. We do not grant you any licenses, express or implied, to the intellectual property of Catalyst Trading or our licensors except as expressly authorized by these Terms.

    """

    await channel.send(embed = embed)
 
    field5 = """
    **No Unlawful or Prohibited Use/Intellectual Property **\n
    You are granted a non-exclusive, non-transferable, revocable license to access and use Trading Catalyst strictly in accordance with these terms of use. 

    You warrant to Trading Catalyst that you will not use the Site for any purpose that is unlawful or prohibited by these Terms. You may not use the Site in any manner which could damage, disable, overburden, or impair the Site or interfere with any other party's use and enjoyment of the Site. You may not obtain or attempt to obtain any materials or information through any means not intentionally made available or provided for through the Site.

    All content included as part of the Service, such as text, graphics, logos, images, as well as the compilation thereof, and any software used on the Site, is the property of Trading Catalyst or its suppliers and protected by copyright and other laws that protect intellectual property and proprietary rights. You agree to observe and abide by all copyright and other proprietary notices, legends, or other restrictions contained in any such content and will not make any changes thereto.
    """
    embed = discord.Embed(color = discord.Color.green(),description = field5)
    await channel.send(embed = embed)

    field5 = """
    You will not modify, publish, transmit, reverse engineer, participate in the transfer or sale, create derivative works, or in any way exploit any of the content, in whole or in part, found on the Site. Catalyst Trading content is not for resale. Your use of the Site does not entitle you to make any unauthorized use of any protected content, and in particular, you will not delete or alter any proprietary rights or attribution notices in any content. You will use protected content solely for your personal use and will make no other use of the content without the express written permission of Catalyst Trading and the copyright owner. You agree that you do not acquire any ownership rights in any protected content. We do not grant you any licenses, express or implied, to the intellectual property of Catalyst Trading or our licensors except as expressly authorized by these Terms.
    """
    embed = discord.Embed(color = discord.Color.green(),description = field5)
    await channel.send(embed = embed)

    field5 = """
    **Use of Communication Services **\n
    You are granted a non-exclusive, non-transferable, revocable license to access and use Trading Catalyst strictly in accordance with these terms of use. 

    You warrant to Trading Catalyst that you will not use the Site for any purpose that is unlawful or prohibited by these Terms. You may not use the Site in any manner which could damage, disable, overburden, or impair the Site or interfere with any other party's use and enjoyment of the Site. You may not obtain or attempt to obtain any materials or information through any means not intentionally made available or provided for through the Site.

    All content included as part of the Service, such as text, graphics, logos, images, as well as the compilation thereof, and any software used on the Site, is the property of Trading Catalyst or its suppliers and protected by copyright and other laws that protect intellectual property and proprietary rights. You agree to observe and abide by all copyright and other proprietary notices, legends, or other restrictions contained in any such content and will not make any changes thereto.
    """
    embed = discord.Embed(color = discord.Color.green(),description = field5)
    await channel.send(embed = embed)

    field5 = """
    The Site may contain bulletin board services, chat areas, news groups, forums, communities, personal web pages, calendars, and/or other message or communication facilities designed to enable you to communicate with the public at large or with a group (collectively, "Communication Services"). You agree to use the Communication Services only to post, send and receive messages and material that are proper and related to the particular Communication Service.
    """
    embed = discord.Embed(color = discord.Color.green(),description = field5)
    await channel.send(embed = embed)

    field5 = """
    By way of example, and not as a limitation, you agree that when using a Communication Service, you will not: defame, abuse, harass, stalk, threaten or otherwise violate the legal rights (such as rights of privacy and publicity) of others; publish, post, upload, distribute or disseminate any inappropriate, profane, defamatory, infringing, obscene, indecent or unlawful topic, name, material or information; upload files that contain software or other material protected by intellectual property laws (or by rights of privacy of publicity) unless you own or control the rights thereto or have received all necessary consents; upload files that contain viruses, corrupted files, or any other similar software or programs that may damage the operation of another's computer; advertise or offer to sell or buy any goods or services for any business purpose, unless such Communication Service specifically allows such messages; conduct or forward surveys, contests, pyramid schemes or chain letters; download any file posted by another user of a Communication Service that you know, or reasonably should know, cannot be legally distributed in such manner; falsify or delete any author attributions, legal or other proper notices or proprietary designations or labels of the origin or source of software or other material contained in a file that is uploaded; restrict or inhibit any other user from using and enjoying the Communication Services; violate any code of conduct or other guidelines which may be applicable for any particular Communication Service; harvest or otherwise collect information about others, including e-mail addresses, without their consent; violate any applicable laws or regulations.
    """
    embed = discord.Embed(color = discord.Color.green(),description = field5)
    await channel.send(embed = embed)

    field5 = """
    Catalyst Trading has no obligation to monitor the Communication Services. However, Catalyst Trading reserves the right to review materials posted to a Communication Service and to remove any materials at its sole discretion. Catalyst Trading reserves the right to terminate your access to any or all of the Communication Services at any time without notice for any reason whatsoever. Catalyst Trading reserves the right at all times to disclose any information as necessary to satisfy any applicable law, regulation, legal process, or governmental request, or to edit, refuse to post, or to remove any information or materials, in whole or in part, in Catalyst Trading sole discretion. Always use caution when giving out any personally identifying information about yourself or your children in any Communication Service. Catalyst Trading does not control or endorse the content, messages, or information found in any Communication Service and, therefore, Catalyst Trading specifically disclaims any liability with regard to the Communication Services and any actions resulting from your participation in any Communication Service. Managers and hosts are not authorized Catalyst Trading spokespersons, and their views do not necessarily reflect those of Catalyst Trading.
    """
    embed = discord.Embed(color = discord.Color.green(),description = field5)
    await channel.send(embed = embed)

    field5 = """
    **Materials uploaded to a Communication**\n
    Service may be subject to posted limitations on usage, reproduction, and/or dissemination. You are responsible for adhering to such limitations if you upload the materials. 
    """
    embed = discord.Embed(color = discord.Color.green(),description = field5)
    await channel.send(embed = embed)

    field5 = """
    **Materials Provided to Catalyst Trading**\n
    Catalyst Trading does not claim ownership of the materials you provide to Catalyst Trading (including feedback and suggestions) or post, upload, input or submit to any Catalyst Trading or our associated services (collectively "Submissions"). However, by posting, uploading, inputting, providing, or submitting your Submission you are granting Catalyst Trading, our affiliated companies, and necessary sublicensees permission to use your Submission in connection with the operation of their Internet businesses including, without limitation, the rights to copy, distribute, transmit, publicly display, publicly perform, reproduce, edit, translate and reformat your Submission; and to publish your name in connection with your Submission. 

    No compensation will be paid with respect to the use of your Submission, as provided herein. Catalyst Trading is under no obligation to post or use any Submission you may provide and may remove any Submission at any time at Stacked Up's sole discretion. 

    By posting, uploading, inputting, providing, or submitting your Submission you warrant and represent that you own or otherwise control all of the rights to your Submission as described in this section including, without limitation, all the rights necessary for you to provide, post, upload, input or submit the Submissions.

    """

    embed = discord.Embed(color = discord.Color.green(),description = field5)
    await channel.send(embed = embed)
    field5 = """
    **International Users**\n
    The Service is controlled, operated, and administered by Catalyst Trading from our offices within Cyprus. If you access the Service from a location outside Cyprus, you are responsible for compliance with all local laws. You agree that you will not use the Catalyst Trading Content accessed through Catalyst Trading in any country or in any manner prohibited by any applicable laws, restrictions, or regulations. 
    """
    embed = discord.Embed(color = discord.Color.green(),description = field5)
    await channel.send(embed = embed)
    field5 = """
    **Indemnification**\n
    You agree to indemnify, defend and hold harmless Catalyst Trading, its officers, directors, employees, agents, and third parties, for any losses, costs, liabilities, and expenses (including reasonable attorney's fees) relating to or arising out of your use of or inability to use the Site or services, any user postings made by you, your violation of any terms of this Agreement or your violation of any rights of a third party, or your violation of any applicable laws, rules or regulations. 

    Catalyst Trading reserves the right, at its own cost, to assume the exclusive defense and control of any matter otherwise subject to indemnification by you, in which event you will fully cooperate with Catalyst Trading in asserting any available defenses.
    """
    embed = discord.Embed(color = discord.Color.green(),description = field5)
    await channel.send(embed = embed)
    field5 = """
    **Arbitration**\n 
    In the event the parties are not able to resolve any dispute between them arising out of or concerning these Terms and Conditions, or any provisions hereof, whether in contract, tort, or otherwise at law or in equity for damages or any other relief, then such dispute shall be resolved only by final and binding arbitration pursuant to the Federal Arbitration Act, conducted by a single neutral arbitrator and administered by the American Arbitration Association, or a similar arbitration service selected by the parties, in a location mutually agreed upon by the parties. The arbitrator's award shall be final, and judgment may be entered upon it in any court having jurisdiction. In the event that any legal or equitable action, proceeding, or arbitration arises out of or concerns these Terms and Conditions, the prevailing party shall be entitled to recover its costs and reasonable attorney's fees. 

    The parties agree to arbitrate all disputes and claims in regards to these Terms and Conditions or any disputes arising as a result of these Terms and Conditions, whether directly or indirectly, including Tort claims that are a result of these Terms and Conditions. The parties agree that the Federal Arbitration Act governs the interpretation and enforcement of this provision. The entire dispute, including the scope and enforceability of this arbitration provision, shall be determined by the Arbitrator. This arbitration provision shall survive the termination of these Terms and Conditions.
    """
    embed = discord.Embed(color = discord.Color.green(),description = field5)
    await channel.send(embed = embed)

    field5 = """
    **Class Action Waiver**\n
    Any arbitration under these Terms and Conditions will take place on an individual basis; class arbitrations and class/representative/collective actions are not permitted. 

    The parties agree that a party may bring claims against the other only in each’s individual capacity, and not as a plaintiff or class member in any putative class, collective, and/or representative proceeding, such as a form of a private attorney general action against the other. 

    Further, unless both you and Catalyst Trading agree otherwise, the arbitrator may not consolidate more than one person's claims, and may not otherwise preside over any form of a representative or class proceeding. 
    """
    embed = discord.Embed(color = discord.Color.green(),description = field5)
    await channel.send(embed = embed)
    
    field5 = """
    **Liability Disclaimer**\n 
    The information, software, products, and services included in or available through the Server may include inaccuracies or typographical errors. Changes are periodically added to the information herein. Catalyst Trading and/or its suppliers may make improvements and/or changes in the Server at any time. 

    Catalyst Trading and/or its suppliers make no representations about the suitability, reliability, availability, timeliness, and accuracy of the information, software, products, services, and related graphics contained on the Server for any purpose. To the maximum extent permitted by applicable law, all such information, software, products, services, and related graphics are provided “as is” without warranty or condition of any kind. 

    Catalyst Trading and/or its suppliers hereby disclaim all warranties and conditions with regard to this information, software, products, services, and related graphics, including all implied warranties or conditions of merchantability, fitness for a particular purpose, title, and non-infringement.
    """
    embed = discord.Embed(color = discord.Color.green(),description = field5)
    await channel.send(embed = embed)
    field5 = """
    To the maximum extent permitted by applicable law, in no event shall Catalyst Trading and/or its suppliers be liable for any direct, indirect, punitive, incidental, special, or consequential damages or any damages whatsoever including, without limitation, damages for loss of use, data or profits, arising out of or in any way connected with the use or performance of the Server, with the delay or inability to use the Server or related Services, the provision of or failure to provide Services, or for any information, software, products, services and related graphics obtained through the Server, or otherwise arising out of the use of the Server, whether based on contract, tort, negligence, strict liability or otherwise, even if Catalyst Trading or any of its suppliers has been advised of the possibility of damages.
    """
    embed = discord.Embed(color = discord.Color.green(),description = field5)
    await channel.send(embed = embed)
    field5 = """
    Because some states/jurisdictions do not allow the exclusion or limitation of liability for consequential or incidental damages, the above limitation may not apply to you. If you are dissatisfied with any portion of the Server, or with any of these Terms of Use, your sole and exclusive remedy is to discontinue using the Server. Termination/Access Restriction Catalyst Trading reserves the right, in its sole discretion, to terminate your access to the Server and the related services or any portion thereof at any time, without notice. To the maximum extent permitted by law, this agreement is governed by the laws of the State of Michigan and you hereby consent to the exclusive jurisdiction and venue of courts in Michigan in all disputes arising out of or relating to the use of the Site. Use of the Site is unauthorized in any jurisdiction that does not give effect to all provisions of these Terms, including, without limitation, this section.
    """
    embed = discord.Embed(color = discord.Color.green(),description = field5)
    await channel.send(embed = embed)
    field5 = """
    You agree that no joint venture, partnership, employment, or agency relationship exists between you and Catalyst Trading as a result of this agreement or use of the Site. Catalyst Trading`s performance of this agreement is subject to existing laws and legal process, and nothing contained in this agreement is in derogation of Catalyst Trading’s right to comply with governmental, court, and law enforcement requests or requirements relating to your use of the Site or information provided to or gathered by Catalyst Trading with respect to such use. If any part of this agreement is determined to be invalid or unenforceable pursuant to applicable law including, but not limited to, the warranty disclaimers and liability limitations set forth above, then the invalid or unenforceable provision will be deemed superseded by a valid, enforceable provision that most closely matches the intent of the original provision and the remainder of the agreement shall continue in effect.
    """
    embed = discord.Embed(color = discord.Color.green(),description = field5)
    await channel.send(embed = embed)
    field5 = """
    Unless otherwise specified herein, this agreement constitutes the entire agreement between the user and Catalyst Trading with respect to the Server and it supersedes all prior or contemporaneous communications and proposals, whether electronic, oral, or written, between the user and Catalyst Trading with respect to the Site. A printed version of this agreement and of any notice given in electronic form shall be admissible in judicial or administrative proceedings based upon or relating to this agreement to the same extent and subject to the same conditions as other business documents and records originally generated and maintained in printed form. It is the express wish of the parties that this agreement and all related documents be written in English.
    """
    embed = discord.Embed(color = discord.Color.green(),description = field5)
    await channel.send(embed = embed)

    field5 = """
    **Changes to Terms**\n
    Catalyst Trading reserves the right, in its sole discretion, to change the Terms under which Catalyst Trading is offered. The most current version of the Terms will supersede all previous versions. Catalyst Trading encourages you to periodically review the Terms to stay informed of our updates. 
    """
    embed = discord.Embed(color = discord.Color.green(),description = field5)
    await channel.send(embed = embed)
    field5 = """
    **Contact Us**\n
    Catalyst Trading welcomes your questions or comments regarding the Terms: 

    Email Address: admin@catalyst.trading.com
    """
    embed = discord.Embed(color = discord.Color.green(),description = field5)
    await channel.send(embed = embed)
    field5 = """
    This is not an investment advisory and should not be used to make investment decisions. Information provided by Catalyst Trading. Should only be considered for informational purposes. Catalyst Trading accepts no liability for any direct or consequential loss arising from any use of information found within this document or any other forms of communication. The reader bears responsibility for his/her own investment research and decisions. Information found here is not intended to be used as the sole basis of any investment decision, nor should it be construed as advice designed to meet the investment needs of any particular investor. Catalyst Trading is not registered as a security broker-dealer or an investment advisor. No information is intended, as securities brokerage, investment, tax, accounting, or legal advice, as an offer or solicitation of an offer to buy or sell, or as an endorsement, recommendation, or sponsorship of any company, security, or fund. Catalyst Trading cannot and does not assess, verify or guarantee the adequacy, accuracy, or completeness of any information, the suitability or profitability of any particular investment, or the potential value of an investment or information source. Please be aware when trading stocks, options, ETF’s and futures you can suffer a loss greater than your total account balance. 
    """
    embed = discord.Embed(color = discord.Color.green(),description = field5)
    await channel.send(embed = embed)

    field5 = """
    **By reading this document, you are agreeing to waive all liability of losses you may suffer; additionally, hereby acknowledge and agree to the terms and conditions provided in this disclaimer. If you do not agree to any portion of this disclaimer, you are not to scan/proceed forward with Catalyst Trading.**
    """

    embed = discord.Embed(color = discord.Color.green(),description = field5)
    msg = await channel.send(embed = embed)
    with open('DT.json') as f:
        data = json.load(f)
    
    data['MSG'] = msg.id
    with open('DT.json','w') as f:
        json.dump(data,f,indent = 3)
    
    await msg.add_reaction('✅')
    await ctx.send(':white_check_mark: Dispatched')

@bot.event
async def on_raw_reaction_add(payload):
    with open('DT.json') as f:
        data = json.load(f)
     
    guild = str(payload.guild_id)
    channel = await bot.fetch_channel(payload.channel_id)
    user = channel.guild.get_member(payload.user_id)
    msg = payload.message_id
    emoji = payload.emoji
    emoji = str(emoji)
    if emoji == '✅' and msg == data['MSG']:
        role = discord.utils.get(channel.guild.roles,name = 'Potential Catalyst')
        if role in user.roles:
            return
        def check(m):
            return m.author == user and m.channel.type == discord.ChannelType.private
        await user.send(f':closed_lock_with_key: {user.mention}, Type Your Name To Confirm the Verification! `(Timeout in 20 Seconds)`')
        try:
            msg = await bot.wait_for('message',check = check,timeout = 20)
            content = str(msg.content)
            if content.lower() == str(user.name).lower():
                await user.send(':white_check_mark: Verified Successfully!')
                await user.add_roles(role)
                return
            else:
                await user.send(":warning: Name didn't matched. Restart the Verification by reacting to the Disclaimer.")
                message = await channel.fetch_message(payload.message_id)
                reaction = discord.utils.get(message.reactions, emoji='✅')
                await reaction.remove(user)
        except asyncio.TimeoutError:
            await user.send(':warning: You failed to enter the name in the Given TIME. Restart the Verification by reacting to the Disclaimer.')
            message = await channel.fetch_message(payload.message_id)
            reaction = discord.utils.get(message.reactions, emoji='✅')
            await reaction.remove(user)
            
bot.run('ODQyNDU1NzY1MDExNjYwODAx.YJ1kEg.iC_C7mX4EBZLdLwLHfRA8D2y-As')