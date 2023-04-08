from discord.ext import tasks, commands
import logging

class DealsScraperCog(commands.Cog):
    def __init__(self, bot, channel):
        self.logger = logging.getLogger('discord')
        self.bot = bot
        self.channel = channel
        self.scrape.start()

    def cog_unload(self):
        self.logger.info('DealsScraperCog unloading')
        self.printer.cancel()

    @tasks.loop(minutes=1)
    async def scrape(self):
        self.logger.info('DealsScraperCog started')
        await self.channel.send('Testing background task')

    @scrape.before_loop
    async def before_printer(self):
        self.logger.info('DealsScraperCog waiting...')
        await self.bot.wait_until_ready()