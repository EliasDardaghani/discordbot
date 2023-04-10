from discord.ext import tasks, commands
import asyncio
import logging
from scrapers import Scrapers

class DealsCog(commands.Cog):
    def __init__(self, bot):
        self.logger = logging.getLogger('discord')
        self.bot = bot
        self.scrapers = Scrapers()
        self.scrape.start()

    def cog_unload(self):
        self.logger.info('DealsCog unloading')
        self.scrape.cancel()

    @tasks.loop(seconds=10.0)
    async def scrape(self):
        self.logger.info('DealsCog started')
        # adealsweden = self.scrapers.scrape_adealsweden()
        swedroid = self.scrapers.scrape_swedroid()
        # scrape websites for deals below
        # for channel in self.bot.allowed_channels:
        #     for adeal in adealsweden:
        #         await channel.send(content=f'@everyone new deal from adealsweden.com\n{adeal.name}\n{adeal.price}\n{adeal.url}')
                # await asyncio.sleep(1)

    @scrape.before_loop
    async def before_printer(self):
        self.logger.info('DealsCog waiting...')
        await self.bot.wait_until_ready()