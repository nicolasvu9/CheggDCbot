import discord
import os
import chegg_grab
from discord.ext import commands
from pathlib import Path
import config
parentdir = Path(__file__).parent.absolute()

client = commands.Bot(command_prefix='-')

# def in_channel(channel_id):
#     def predicate(ctx):
#         return ctx.message.channel.id == channel_id
#     return commands.check(predicate)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.command()
async def getlink(ctx, link):
    if not chegg_grab.validate_url(link):
        await ctx.send("invalid url")
        return 1

    name = chegg_grab.get_answer(link)

    if name !=1:
        print('--------------------------------------------------------------------------\nSending PDF: ' + name)    
        await ctx.send(file=discord.File(os.path.join(parentdir.parent,'data', name)))

        print('--------------------------------------------------------------------------\nPDF SENT: ' + name)
        os.remove(os.path.join(parentdir.parent,'data', name))
        print('--------------------------------------------------------------------------\n Done')
    else:
        await ctx.send("Error")



client.run(config.config_token)

