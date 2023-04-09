from discord.ext import tasks, commands
import logging

class DealsScraperCog(commands.Cog):
    def __init__(self, bot, channels):
        self.logger = logging.getLogger('discord')
        self.bot = bot
        self.channels = channels
        self.scrape.start()

    def cog_unload(self):
        self.logger.info('DealsScraperCog unloading')
        self.scrape.cancel()

    @tasks.loop(minutes=1)
    async def scrape(self):
        self.logger.info('DealsScraperCog started')
        # scrape websites for deals below
        # for channel in self.channels:
            # await self.channel.send('NEW DEAL')

    @scrape.before_loop
    async def before_printer(self):
        self.logger.info('DealsScraperCog waiting...')
        await self.bot.wait_until_ready()