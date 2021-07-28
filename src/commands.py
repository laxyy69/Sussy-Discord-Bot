import asyncio
import discord
import inspect
from bot import Bot # Importing Bot for type-checking
from discord.ext import commands


COMMAND = commands.command
OWNER = commands.is_owner
NSFW = commands.is_nsfw


commands_classes: list[commands.Cog] = []

def add_class(cls: commands.Cog) -> commands.Cog:
    commands_classes.append(cls)

    return cls


@add_class
class Owner(commands.Cog):
    def __init__(self, client: Bot) -> None:
        self.client = client


    @COMMAND()
    @OWNER()
    async def test(self, ctx: commands.Context):
        pass


@add_class
class Mod(commands.Cog):
    def __init__(self, client: Bot) -> None:
        self.client = client


    @COMMAND()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx: commands.Context, member: discord.Member, *, reason: str=None) -> None:
        await member.kick(reason=reason)


    @COMMAND()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx: commands.Context, member: discord.Member, *, reason: str=None) -> None:
        await member.ban(reason=reason)


    @COMMAND()
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx: commands.Context, member_id: int, *, reason: str=None):
        guild: discord.Guild = ctx.guild

        user = self.client.get_user(member_id)

        await guild.unban(user, reason=reason)

        await ctx.reply("**%s** unban!" % user)


    @COMMAND()
    @commands.has_permissions(administrator=True)
    async def bans(self, ctx: commands.Context):
        embed = discord.Embed(title='Banned members', colour=discord.Colour.from_rgb(255, 0, 0))

        server: discord.Guild = ctx.guild

        banned_members: list[discord.guild.BanEntry] = await server.bans()

        embed.description = '\n'.join(
            ['%s ID: **%i**, reason: **%s**' % (ban_entry.user.mention, ban_entry.user.id, ban_entry.reason) for ban_entry in banned_members]
        ) if len(banned_members) != 0 else "**No banned members.**"

        await ctx.send(embed=embed)


@add_class
class Nerd(commands.Cog):
    def __init__(self, client: Bot) -> None:
        self.client = client


    @COMMAND()
    async def command_code(self, ctx: commands.Context, function_name: str) -> None:
        for cmd in self.client.commands:
            if str(cmd) == function_name:
                source_code: str = inspect.getsource(cmd.callback)

                return await ctx.send('```py\n%s```' % source_code)

        await ctx.reply(
            embed=discord.Embed(
                description='Command **%s** not found.' % function_name,
                colour=discord.Colour.from_rgb(255, 0, 0)
            )
        )


    @COMMAND()
    async def client_code(self, ctx: commands.Context, function_name: str) -> None:
        try:
            print(self.client.__dir__())
            func = self.client.__getattribute__(function_name)
        except Exception as e:
            await ctx.send('`' + str(e) + '`')
        else:
            source_code: str = inspect.getsource(func)

            await ctx.send('```py\n%s```' % source_code)


@add_class
class Reddit(commands.Cog):
    def __init__(self, client: Bot) -> None:
        self.client = client


    @COMMAND(aliases=['r/', 'reddit'])
    async def r(self, ctx: commands.Context, sub_reddit: str, loop: int=1) -> None:
        await self.client.reddit(ctx, sub_reddit=sub_reddit, loop=loop)


    @COMMAND()
    async def meme(self, ctx: commands.Context, loop: int=1):
        await self.client.reddit(ctx, 'meme', loop)


    @COMMAND()
    async def memes(self, ctx: commands.Context, loop: int=1):
        await self.client.reddit(ctx, 'memes', loop)


    @COMMAND()
    async def dankmemes(self, ctx: commands.Context, loop: int=1):
        await self.client.reddit(ctx, 'dankmemes', loop)


@add_class
class Nsfw(commands.Cog):
    def __init__(self, client: Bot) -> None:
        self.client = client


    @NSFW()
    async def nsfw(self, ctx: commands.Bot) -> None:
        print('PORN YOU FUCKING HORNY BITCH')


@add_class
class Misc(commands.Cog):
    def __init__(self, client: Bot) -> None:
        self.client = client

    
    @COMMAND()
    async def ping(self, ctx: commands.Context):
        await ctx.reply(
            embed=discord.Embed(
                description="**%i**ms" % round(self.client.latency * 1000),
                colour=discord.Colour.blue()
            )
        )


    @COMMAND()
    async def invite(self, ctx: commands.Context) -> None:
        await ctx.send(
            embed=discord.Embed(
                title='CLICK HERE',
                description='**Add me to your server** :heart:',
                url='https://discord.com/api/oauth2/authorize?client_id=865258654692933652&permissions=8&scope=bot',
                colour=discord.Colour.blue()
            )
        )


def setup(client: commands.Bot) -> None:
    for cmd_cls in commands_classes:
        client.add_cog(cmd_cls(client))
        print('Added:', cmd_cls.__name__)