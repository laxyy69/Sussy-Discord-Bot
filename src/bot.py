import discord
from reddit import Reddit
from discord.ext import commands


class Evets(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client



class Bot(commands.Bot):
    def __init__(self, command_prefix: str, args: list[str], **options):

        super().__init__(command_prefix=command_prefix, **options) # init commands.Bot

        self.args: list[str] = args
        self.reddit: Reddit = Reddit()

    # event
    async def on_ready(self):
        print(self.user, 'online!')

    # event
    async def on_message(self, message: discord.Message) -> None:
        if not message.content: 
            return

        # print(message.author.display_name + ": " + message.content)

        await self.process_commands(message)
