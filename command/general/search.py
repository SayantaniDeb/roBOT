import json
import discord
from discord.ext import commands
from duckduckgo_search import ddg


class Search(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def search(self, ctx, *, query):

        results = ddg(query, region="in-en", safesearch="Off", time="y", max_results=1)[
            0
        ]
        data = json.loads(str(results).replace("'", '"'))

        embed = discord.Embed(
            title=data["title"],
            color=discord.Color.blue(),
            description=data["body"],
            url=data["href"],
        )

        await ctx.send(embed=embed)
        await ctx.message.add_reaction("\U0001f44d")


def setup(client):
    client.add_cog(Search(client))
