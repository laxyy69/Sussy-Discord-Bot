import discord
from discord.ext import commands


commands_classes: list[commands.Cog] = []

def add_class(cls):
    commands_classes.append(cls)

    return cls


@add_class
class Misc(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    
    @commands.command(help='Ping!!')
    async def ping(self, ctx: commands.Context):
        await ctx.reply(
            embed=discord.Embed(
                description="**%i**ms" % round(self.client.latency * 1000),
                colour=discord.Colour.blue()
            )
        )


@add_class
class Test(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client


    @commands.command()
    async def test(self, ctx: commands.Context):
        await ctx.send("Test")



def setup(client: commands.Bot) -> None:
    for cmd_cls in commands_classes:
        print('Adding', cmd_cls.__name__)
        client.add_cog(cmd_cls(client))