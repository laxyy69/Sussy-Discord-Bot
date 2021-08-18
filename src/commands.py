"""
This is not an script file, It's meant to be imported.

This is where all the bot commands are.


Author: SasumaTho
Discord: SasumaTho#9999

Status: Still in development.

"""


import asyncio
from datetime import datetime
from operator import add
from types import FunctionType
from typing import OrderedDict, Union
from asyncio.tasks import create_task
import discord
import inspect
import os
import random
from discord.ext.commands.core import command
from discord.ext.commands.errors import MemberNotFound
from copy_lib.googlesearch import search
from discord import colour
from bot import Bot # Importing Bot for type-checking
from discord.ext import commands
from tictactoe import TicTacToe
from var import MyJson


# This is used to @ decorate a functions

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



async def command_success(message: Union[discord.Message, commands.Context]) -> None:
    if isinstance(message, commands.Context):
        message: discord.Message = message.message

    await message.add_reaction('✅')




@add_class
class Owner(commands.Cog):
    def __init__(self, client: Bot) -> None:
        self.client = client


    @commands.command()
    @commands.is_owner()
    async def test(self, ctx: commands.Context, member: discord.Member):
        await ctx.send(embed=discord.Embed(title=member.name, colour=member.colour))


    @commands.command()
    @commands.is_owner()
    async def servers(self, ctx: commands.Context, _list: str=None) -> None:
        servers: discord.Guild = self.client.guilds

        if _list == 'list':
            return await ctx.send('\n'.join(['%s - %i members' % (server.name, len(server.members)) for server in servers]))
        elif _list is None:
            await ctx.send("I'm in **%i** servers." % len(servers))
        else:
            await ctx.reply("**%s**???" % _list)


@add_class
class Mod(commands.Cog):
    def __init__(self, client: Bot) -> None:
        self.client = client


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx: commands.Context, member: discord.Member, *, reason: str=None) -> None:
        await member.kick(reason=reason)


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx: commands.Context, member: discord.Member, *, reason: str=None) -> None:
        await member.ban(reason=reason)


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx: commands.Context, member_id: int, *, reason: str=None):
        guild: discord.Guild = ctx.guild

        user = self.client.get_user(member_id)

        await guild.unban(user, reason=reason)

        await ctx.reply("**%s** unban!" % user)


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def bans(self, ctx: commands.Context):
        embed = discord.Embed(title='Banned members', colour=discord.Colour.from_rgb(255, 0, 0))

        server: discord.Guild = ctx.guild

        banned_members: list[discord.guild.BanEntry] = await server.bans()

        embed.description = '\n'.join(
            ['%s ID: **%i**, reason: **%s**' % (ban_entry.user.mention, ban_entry.user.id, ban_entry.reason) for ban_entry in banned_members]
        ) if len(banned_members) != 0 else "**No banned members.**"

        await ctx.send(embed=embed)


    @commands.command()
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


    # Not a command, used for `code` command
    async def command_code(self, function_name: str) -> Union[discord.File, None]:
        """ | Get Command Source Code|

        Gets the source code of a function using `inspect.getsource`

        Paremters
        ----------
        function_name: :class:`str`
            The command name


        Returns
        --------
            Returns None if it didn't found the function

            But if it did found:
                file: :class:`discord.File` 
        
        """

        try:
            cmd_function: FunctionType = self.client.all_commands[function_name].callback
        except KeyError:
            return None
        else:
            source_code: str = inspect.getsource(cmd_function)
                
            with open('source_code.py', 'w') as f:
                f.write(source_code)

            file = discord.File('source_code.py')

            return file


    # Not a command, used for `code` command
    async def client_code(self, function_name: str) -> Union[discord.File, None]:
        """ | Get Bot Source Code |

        Gets the :class:`Bot` functions source code

        Paremters
        ----------
        function_name: :class:`str`
            The function name of :class:`Bot`


        Returns
        --------
        Returns None if there's no attribute `function_name` of :class:`Bot`

        file: :class:`discord.File`
        
        """
        
        try:
            func: FunctionType = self.client.__getattribute__(function_name)
        except AttributeError as e:
            return None
        else:
            source_code: str = inspect.getsource(func)

            with open('source_code.py', 'w') as f:
                f.write(source_code)

            file = discord.File('source_code.py')

            return file


    @commands.command()
    async def code(self, ctx: commands.Context, function_name: str) -> None:
        file: discord.File = await self.command_code(function_name) or await self.client_code(function_name)

        if file is None:
            return await ctx.send("**No function `%s` was found.**" % function_name)

        await ctx.send(
            file=file,
            embed=discord.Embed(
                description='**`%s`** source code:' % function_name,
                colour=discord.Colour.blue()
            )
        )

        with open('source_code.py', 'w'): pass # Empty source_code.py


    @commands.command()
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


    @commands.command(aliases=['r/', 'reddit'])
    async def r(self, ctx: commands.Context, sub_reddit: str, loop: int=1) -> None:
        await self.client.reddit(ctx, sub_reddit=sub_reddit, loop=loop)


    @commands.command()
    async def meme(self, ctx: commands.Context, loop: int=1):
        await self.client.reddit(ctx, 'meme', loop)


    @commands.command()
    async def memes(self, ctx: commands.Context, loop: int=1):
        await self.client.reddit(ctx, 'memes', loop)


    @commands.command()
    async def dankmemes(self, ctx: commands.Context, loop: int=1):
        await self.client.reddit(ctx, 'dankmemes', loop)


@add_class
class Nsfw(commands.Cog):
    def __init__(self, client: Bot) -> None:
        self.client = client


    @commands.is_nsfw()
    async def nsfw(self, ctx: commands.Bot) -> None:
        print('PORN YOU FUCKING HORNY BITCH')


@add_class
class User(commands.Cog):
    def __init__(self, client: Bot) -> None:
        self.client: Bot = client


    @commands.command(aliases=['av'], help='See avatar')
    async def pfp(self, ctx: commands.Context, member: discord.Member=None) -> None:
        """ | Profile Pic command |

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


    @commands.command()
    async def status(self, ctx: commands.Context, member: Union[discord.Member, str]=None, args=None) -> None:
        if isinstance(member, str):
            args = member
            member = ctx.author
        
        def get_nice_type(_type):
            return str(_type[0][0].upper() + _type[0][1:])


        status_icon = {
            'online': 'https://emoji.gg/assets/emoji/9166_online.png',
            'dnd': 'https://emoji.gg/assets/emoji/7907_DND.png',
            'offline': 'https://emoji.gg/assets/emoji/7445_status_offline.png',
            'idle': 'https://i.redd.it/kp69do60js151.png'
        }

        member = member or ctx.author
        _status = member.status

        status_platform = member._client_status.copy()

        del status_platform[None]

        if str(_status) == 'dnd':
            _status = 'Do Not Disturb'

        _status = '%s  -  %s' % (_status, ', '.join(list(status_platform)))

        activities = member.activities

        embed = discord.Embed(colour=discord.Colour.blue())
        embed.set_author(name=member, icon_url=member.avatar_url)
        embed.set_footer(text=_status, icon_url=status_icon[str(member.status)])

        if args == 'more':
            status = []

            for act in activities:
                # TODO: Clean up code

                if str(type(act)) == "<class 'discord.activity.Activity'>":
                    details = ''
                    if act.details is not None:
                        details = '\n> %s\n> %s\n%s' % (act.details, act.state, act.url or '')

                    status.append("%s **%s**%s" % (get_nice_type(act.type), act.name, details))
                elif str(type(act)) == "<class 'discord.activity.Spotify'>": # The user is playing spotify
                    embed.set_thumbnail(url=act.album_cover_url)
                    status.append("%s\n> **%s** - by __%s__\n> on __%s__" % ('%s To %s' % (get_nice_type(act.type), act), act.title, ', '.join(act.artists), act.album))
                else:
                    status.append('%s **%s**' % (get_nice_type(act.type), act))

            status = '\n'.join(status)

            embed.description = status
        elif args == '-d':
            embed.description = str(activities)
            embed.set_footer(text=str(member._client_status))
        else:
            if not len(activities) == 0:
                _type = get_nice_type(activities[0].type)
                _game = activities[0].name

                if not _type == "Playing":
                    if not activities[0].emoji is None:
                        _game = "%s %s" % (activities[0].emoji, _game)

                embed.description="%s **%s**" % (_type, _game)

        await ctx.send(embed=embed)


    @commands.command()
    async def forward(self, ctx: commands.Context, *members) -> None:
        if not members:
            members = (str(ctx.author.id),)

        try:
            rmsg = await self.client.reference(ctx.message)
        except self.client.reference.NoneReference as e:
            return await ctx.message.reply(e)
        else:
            link = rmsg.jump_url
            
            embed = discord.Embed(description=rmsg.content)
            embed.set_footer(text='Forwarded')
            embed.set_author(name='Message link', url=link, icon_url=rmsg.author.avatar_url)

            for member in members:
                await self.client.get_member(member).send('From **%s**' % ctx.author, embed=embed)
            else:
                await command_success(ctx)


    @commands.command()
    async def info(self, ctx: commands.Context, member: discord.Member=None) -> None:
        member: discord.Member = member or ctx.author

        member_created_at: datetime = member.created_at
        nick: str = member.nick

        created = member_created_at.strftime(f"%A, %B %d %Y @ %H:%M %p")
        joined = member.joined_at.strftime(f"%A, %B %d %Y @ %H:%M %p")

        embed = discord.Embed(
            title=member,
            description=str("Aka: **`%s`**" % nick if nick else '') + "\n%s" % member.mention,
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=member.avatar_url)

        embed.add_field(name='Account created at', value='> `%s`' % created, inline=False)
        embed.add_field(name='Joined this server at', value='> `%s`' % joined, inline=False)
        embed.add_field(name='Age of account', value='> `%s`' % (datetime.today() - member_created_at), inline=False)
        embed.add_field(name='Admin', value='`%s`' % member.guild_permissions.administrator)
        embed.add_field(name='Bot', value='`%s`' % member.bot)
        embed.add_field(name='ID', value='`%i`' % member.id)


        await ctx.send(embed=embed)


    @commands.command()
    async def kiss(self, ctx: commands.Context, member: discord.Member) -> None:
        author: discord.Member = ctx.author

        des = "**%s** gives **%s** a kiss. :kiss:" % (author.display_name, member.display_name) if member != author else "***Kissing yourself? Kinda sus, ngl***"

        msg: discord.Message = await ctx.send(
            embed=discord.Embed(
                description=des,
                colour=discord.Colour.from_rgb(255, 0, 0)
            )
        )

        if (random.randint(0, 1) == 1) and (member != author):
            await asyncio.sleep(random.randint(0, 2))

            await msg.reply(
                random.choice(
                    [
                        "WoW! So *Romantic* :heart:",
                        "Gay??",
                        "sus",
                        "Sussy!",
                        ":heart:",
                        ":heart: :heart:",
                        "Hmmm :unamused:",
                        ":unamused:",
                        "Hmmmm",
                        "Damn! That's *`real gay`*",
                        ":angry:",
                        ":zipper_mouth:",
                        ":rainbow_flag:",
                        ":flushed:"
                    ]
                )
            )


@add_class
class Fun(commands.Cog):
    def __init__(self, client: Bot) -> None:
        self.client: Bot = client


    @commands.command(name='8ball')
    async def _8ball(self, ctx: commands.Context, *, question: str):
        embed = discord.Embed(
            title=random.choice(self.client._8ball_says), 
            colour=discord.Colour.from_rgb(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )
        )

        await ctx.reply(embed=embed)


    @commands.command(aliases=['ttt', 'tic-tac-toe'])
    async def tictactoe(self, ctx: commands.Context, player1: Union[discord.Member, str], player2: discord.Member=None):
        player2: discord.Member = player2 or ctx.author

        if player1 == player2:
            return await ctx.reply("You can't play against yourself.")
        
        print(player1.name, 'vs.', player2.name)

        ttt_game = TicTacToe(player1, player2)
        await ttt_game.start(self.client, ctx)






@add_class
class Misc(commands.Cog):
    def __init__(self, client: Bot) -> None:
        self.client = client

    
    @commands.command()
    async def ping(self, ctx: commands.Context):
        await ctx.reply(
            embed=discord.Embed(
                description="**%i**ms" % round(self.client.latency * 1000),
                colour=discord.Colour.blue()
            )
        )


    @commands.command()
    async def invite(self, ctx: commands.Context) -> None:
        await ctx.send(
            embed=discord.Embed(
                title='CLICK HERE',
                description='**Add me to your server** :heart:',
                url='https://discord.com/api/oauth2/authorize?client_id=865258654692933652&permissions=8&scope=bot',
                colour=discord.Colour.blue()
            )
        )


    @commands.command()
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