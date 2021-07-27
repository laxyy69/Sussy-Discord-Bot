import discord
import os
import sys
from dotenv import load_dotenv
from bot import Bot

PREFIX='.'


def main(args: list[str]) -> None:
    client = Bot(
        command_prefix=PREFIX,
        args=args,
        intents=discord.Intents().all()
    )
    
    client.load_extension('commands')

    load_dotenv()

    client.run(os.getenv('TOKEN'))


if __name__ == '__main__':
    main(sys.argv[1:])