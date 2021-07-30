"""
This is not an script file, It's meant to be imported.

This is where all the bot commands are.


Author: SasumaTho
Discord: SasumaTho#9999

Status: Still in development.

"""



import asyncio
import discord
import inspect
import os
import random
from googlesearch import search
from discord import colour
from bot import Bot # Importing Bot for type-checking
from discord.ext import commands
from var import MyJson


# This is used to @ decorate a functions
COMMAND = commands.command
OWNER = commands.is_owner
NSFW = commands.is_nsfw


commands_classes: list[commands.Cog] = []

def add_class(cls: commands.Cog) -> commands.Cog:
    """ | Decorator for classes |

    Appends :parm:`cls` to :var:`commands_classes`
    
    Parmaters
    ----------
        cls: :class:`discord.ext.commands.Cog`
            The class be a subclass of `discord.ext.commands.Cog`

    Returns
    --------
        :parm:`cls`
    
    """

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


    @COMMAND()
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx: commands.Context, new_prefix: str) -> None:
        guild_id: str = str(ctx.guild.id)

        with MyJson.readwrite('prefixes.json') as p:
            p[guild_id] = new_prefix

        await ctx.reply("New prefix is: **%s**" % await self.client.get_prefix(ctx.message))


@add_class
class Nerd(commands.Cog):
    def __init__(self, client: Bot) -> None:
        self.client = client


    @COMMAND(aliases=['commandcode', 'commandc'])
    async def command_code(self, ctx: commands.Context, function_name: str) -> None:
        embed = discord.Embed(colour=discord.Colour.blue())
        file = None
        
        try:
            cmd_function = self.client.all_commands[function_name].callback
        except KeyError:
            embed.description = 'Command **%s** not found.' % function_name
            embed.colour = discord.Colour.from_rgb(255, 0, 0)
        else:
            source_code: str = inspect.getsource(cmd_function)
                
            with open('source_code.py', 'w') as f:
                f.write(source_code)

            file = discord.File('source_code.py')

            embed.description = '**%s** source code:' % function_name
        finally:        
            await ctx.send(embed=embed, file=file)

            with open('source_code.py', 'w'): pass # empting source_code.py


    @COMMAND(aliases=['clientcode', 'clientc'])
    async def client_code(self, ctx: commands.Context, function_name: str) -> None:
        try:
            func = self.client.__getattribute__(function_name)
        except AttributeError as e:
            await ctx.send(
                embed=discord.Embed(
                    description='`%s`' % e,
                    colour=discord.Colour.from_rgb(255, 0, 0)
                )
            )
        else:
            source_code: str = inspect.getsource(func)

            with open('source_code.py', 'w') as f:
                f.write(source_code)

            file = discord.File('source_code.py')

            await ctx.send(
                file=file, 
                embed=discord.Embed(
                    description='**%s** source code:' % str(function_name)
                )
            )
            
            with open('source_code.py', 'w'): pass


    @COMMAND()
    async def lines(self, ctx: commands.Context) -> None:
        """ | lines command |
        
        This will say how much lines of code in the 'src' dir

        Paremters
        ----------
            ctx: :class:`commands.Conext`
                Context
        
        """

        lines_of_code: int = 0

        for file in os.scandir('src/'):
            if file.name.endswith('.py'):
                with open(file) as f:
                    lines_of_code += len(f.readlines())

        await ctx.send(
            embed=discord.Embed(
                description='I have **%i** lines of code.' % lines_of_code,
                colour=discord.Colour.blue()
            )
        )


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
class User(commands.Cog):
    def __init__(self, client: Bot) -> None:
        self.client: Bot = client


    @COMMAND(aliases=['av'])
    async def pfp(self, ctx: commands.Context, member: discord.Member=None) -> None:
        """ | Profile Pic comand |

        Shows the Profile Pic of a user

        Paremters
        ----------
        ctx: :class:`discord.ext.commands.Context`
            Context

        member: Optional[:class:`discord.Member`] 
            If you wanna see other member's profile pic


        Returns
        --------
        None: :class:`NoneType`
        
        """

        # If no member was passed in, then make it who ever sent the message
        member: discord.Member = member or ctx.author

        avatar_url = member.avatar_url

        embed = discord.Embed(colour=discord.Colour.blue(), description='Profile Pic :heart:')
        embed.set_image(url=avatar_url)
        embed.set_author(name=member.display_name, icon_url=avatar_url)

        msg: discord.Message = await ctx.send(embed=embed)

        # There's a chance that the bot will give It's "opinion"
        if random.randint(0, 1) == 1:
            await asyncio.sleep(random.randint(0, 2))

            await msg.reply(
                random.choice([
                    'Cool!', 
                    "It's OK", 
                    "WTF???", 
                    "Who this?", 
                    "Hmmm", 
                    "Interesting profile pic", 
                    "Damn! One ugly avatar!", 
                    "I rate it: **%i** out of 10" % random.randint(0, 10)
                ])
            )


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


    @COMMAND()
    async def google(self, ctx: commands.Context, *, google_search: str) -> None:
        """ | google command |

        Gets links using googlesearch module

        Paremters
        ----------
            ctx: :class:`discord.ext.commands.Context`
                Conext

            google_search: :class:`str`
                What ever you want to search using google

        Returns
        --------
            None: :class:`NoneType`
        
        """

        await ctx.send(
            random.choice(
                [link for link in search(google_search, stop=3, pause=0)]
            )
        )



def setup(client: commands.Bot) -> None:
    """ | Add each cog |
    
    Paremters
    ----------
        client: :class:`discord.ext.commands.Bot`
            Or a subclass of `discord.ext.commands.Bot`

    Returns
    --------
        NoneType: `None`
    
    """

    for cmd_cls in commands_classes:
        client.add_cog(cmd_cls(client))
        print('Added:', cmd_cls.__name__)