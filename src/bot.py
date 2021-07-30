"""
This is not an script file, It's meant to be imported.


Author: SasumaTho
Discord: SasumaTho#9999

Status: Still in development

"""

import discord
from var import MyJson
from reddit import Reddit
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


    async def get_prefix(self, message: discord.Message) -> str:
        """ |Get prefix per server|

        Gets called when processing command.

        Parameters
        -----------
            message (discord.Message)
        
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

        print(self.user, 'online!')

    # event
    async def on_message(self, message: discord.Message) -> None:
        """|on message sent event|

        1: It's going to count each message sent.
        2: Checks for bad words
        3: And process commands

        Parameters
        -----------
            message (discord.Message)

        Returns
        --------
            None
        """

        if not message.content: 
            return

        # TODO: Add stuff: e.g: Bad works, Leveling, etc

        await self.process_commands(message)
