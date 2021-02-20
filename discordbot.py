import discord, asyncio, random
from discord.ext import commands
from itertools import accumulate

import os
import traceback


client = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']


# on_ready
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    
    await client.change_presence(activity=discord.Game(name='/team'))
            

# on command
@client.command()
async def team(ctx, count):
    count = int(count)
    
    channel = ctx.author.voice.channel
    l = []
    for member in channel.members:
        l.append(member.name)
    
    n = len(l)
    g = count
    
    embed_body = discord.Embed(title=f"{n} 人を {g} チームにシャッフル", colour=0x00a381)
    
    def shuffle_groups():
        # Prepare group separators
        size = n // g
        rem = n % g
        separators = list(accumulate([0] + [size+1] * rem + [size] * (g - rem)))

        # Make raw data
        items = list(range(n))
        random.shuffle(items)

        # Iterate and print
        for i, s in enumerate(zip(separators, separators[1:])):
            group = items[slice(*s)]
            print(f'Group {i+1}: {group} (size {len(group)})')
            ul = []
            for u in group:
                ul.append(l[u])
            name = f"チーム {i+1}: {len(group)} 人\n"
            value = "\n".join(ul)
            embed_body.add_field(name=name, value=value, inline=True)
    
    shuffle_groups()
    
    msg = await ctx.send(embed=embed_body)

@client.command()
async def count(ctx):
    
    channel = ctx.author.voicechannel
    l = []
    for member in channel.members:
        l.append(member.name)
    
    n = len(l)
    
    embed_body = discord.Embed(title=f"{channel.name} には {n} 人 参加しています", description=f"{channel.members}", colour=0x00a381) 
    
    msg = await ctx.send(embed=embed_body)
    
# run the bot    
client.run(token)
