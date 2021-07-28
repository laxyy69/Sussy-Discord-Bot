import discord
from var import MyJson
from reddit import Reddit
from discord.ext import commands


class Evets(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client



class Bot(commands.Bot):
    def __init__(self, command_prefix: str, args: list[str], **options):

        super().__init__(command_prefix=command_prefix, **options) # init commands.Bot

        self.command_prefix = command_prefix
        self.args: list[str] = args
        self.reddit: Reddit = Reddit()


    async def get_prefix(self, message: discord.Message) -> str:
        prefix = self.command_prefix

        with MyJson.read('prefixes.json') as p:
            if str(message.guild.id) in p:
                prefix = p[str(message.guild.id)]
        
        return prefix


    # event
    async def on_ready(self):
        print(self.user, 'online!')

    # event
    async def on_message(self, message: discord.Message) -> None:
        if not message.content: 
            return

        # TODO: Add stuff: e.g: Bad works, Leveling, etc

        await self.process_commands(message)
