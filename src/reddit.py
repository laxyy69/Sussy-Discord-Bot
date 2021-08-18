"""
This is not an script file, It's meant to be imported.


Author: SasumaTho
Discord: SasumaTho#9999


Status: Still in development

"""



import asyncio
from asyncio.tasks import wait_for
import random
import aiohttp
import discord
from discord import colour
from discord.ext import commands


class Reddit(aiohttp.ClientSession):
    """ | To get posts from reddit |

    This class is a subclass of `aiohttp.ClientSession`
    
    
    """
    def __init__(self) -> None:
        super().__init__()
        
        self.types: list[str] = ['hot', 'top', 'new']
        self.max_loop: int = 5

        self.able_to_not_use: list[int] = []



    async def cooldown(self, id: int, wait_time: int) -> None:
        await asyncio.sleep(wait_time)

        self.able_to_not_use.remove(id)

    
    async def __call__(self, ctx: commands.Context, sub_reddit: str, loop: int=1) -> None:

        # TODO: Doc this code

        if ctx.author.id in self.able_to_not_use:
            return await ctx.reply("Chill down!")

        wait_time: int = loop * 5

        self.reddit_url: str = 'https://www.reddit.com/r/{}/%s.json?sort=%s' % (random.choice(self.types), random.choice(self.types))
        
        channel: discord.TextChannel = ctx.channel
        loop = self.max_loop if loop > self.max_loop else loop

        async with self.get(self.reddit_url.format(sub_reddit)) as r:
            _json = await r.json()
        
        children = _json['data']['children']
        
        if children[0]['data']['over_18']:
            if not channel.is_nsfw():
                return await ctx.reply(
                    embed=discord.Embed(
                        title=':underage: **This is not an NSFW text channel.**',
                        colour=discord.Colour.from_rgb(255, 0, 0)
                    )
                )
            loop = 1
            wait_time = wait_time * 2

        self.able_to_not_use.append(ctx.author.id)

        for i in range(loop):
            data = children[random.randint(0, len(children) - 1)]['data']

            url = data['url']

            # This checks if a dot is in the end of the url, if so it's probably an image link 
            if '.' in url[-4:]: 
                embed: discord.Embed = discord.Embed(colour=discord.Colour.blue(), title=data['title'], url=url)
                embed.set_image(url=url)
                embed.set_footer(text='%i/%i' % (i + 1, loop))
                
                await ctx.send(embed=embed)
            else:
                await ctx.send(url)

        asyncio.create_task(self.cooldown(ctx.author.id, wait_time=wait_time))