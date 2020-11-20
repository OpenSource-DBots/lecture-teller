import discord
from discord.ext import commands
from logger import log


class Latency(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='ping')
    async def ping(self, ctx):
        embed = discord.Embed(description=f':ping_pong: Pong! with `{round(self.client.latency * 1000)}ms`!',
                              color=discord.Color.from_rgb(114, 137, 218))

        await ctx.send(embed=embed)
        log(f'{ctx.author} executed command \'ping\'')

def setup(client):
    client.add_cog(Latency(client))
