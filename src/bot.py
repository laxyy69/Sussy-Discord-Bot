"""
This is not an script file, It's meant to be imported.


Author: SasumaTho
Discord: SasumaTho#9999

Status: Still in development

"""

import discord
from discord.ext.commands.errors import MemberNotFound
from var import MyJson
from reddit import Reddit
from reference import Reference
from discord.ext import commands


class Bot(commands.Bot):
    """| Represents a discord bot.|
    
    This class is a subclass of :class:`discord.ext.commands.Bot`

    Attributes
    ------------
    Private:
        
        __args: :class:`list[str]`
            It's from `sys.argv`
            So any args when excuteing the script from the command line

        _default_prefix: :class:`str` 
            The bot default command prefix

    Public:

        Reddit: :class:`Reddit`
            Reddit object from reddit.py
            Is used to get reddit post using aiohttp


    Mehods
    ------------
    ...
    """

    def __init__(self, command_prefix: str, args: list[str]=None, **options):
        """
        Parameters
        -----------
        command_prefix: :class:`str`
        
        args: Optional[:class:`list[str]`]
            This should be `sys.argv`

        """
        
        super().__init__(command_prefix=command_prefix, **options) # init commands.Bot

        self.__args: list[str] = args or None
        self._default_prefix: str = command_prefix
        
        
        self.reddit: Reddit = Reddit()
        self.reference: Reference = None

        self._8ball_says: list[str] = [ # TODO: Put it in a json file, and not hard coded
            'no.', 
            'no???', 
            'Hell NO!', 
            'Bruh, you know its a NO', 
            'yes.', 
            'Yes??', 
            'ok, yea', 
            'Ugg, yes...', 
            'Tbh, no.', 
            'Tbh, yes', 
            'can you not', 
            "ask again later when I'm less busy with ur daddy", 
            'sure, why not', 
            "heck off, you know that's a no"
        ]


    async def get_prefix(self, message: discord.Message) -> str:
        """ |Get prefix per server|

        Gets called when processing command.

        Parameters
        -----------
            message: :class:`discord.Message`
        
        Returns
        --------
            str: prefix
        
        """

        prefix = self._default_prefix

        with MyJson.read('prefixes.json') as p:
            if str(message.guild.id) in p:
                prefix = p[str(message.guild.id)]
        
        return prefix


    # event
    async def on_ready(self):
        """ This saying when It's ready. """

        self.reference = Reference(self)
        

        print(self.user, 'online!')

    # event
    async def on_message(self, message: discord.Message) -> None:
        """ | on message event |

        Parameters
        -----------
            message: :class:`discord.Message`

        Returns
        --------
            None
        """

        if not message.content: 
            return

        # TODO: Add stuff: e.g: Bad works, Leveling, etc

        await self.process_commands(message)



    def get_member(self, member: str) -> discord.Member:
        try:
            return self.get_user(int(member)) # Checks if member is an ID
        except ValueError:
            if member.startswith('<@!'): # Its a member
                return self.get_user(int(member[3:-1]))
            else:
                raise MemberNotFound('**%s**' % member)

