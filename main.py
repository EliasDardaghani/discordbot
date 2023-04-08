import discord
import logging
from deals import DealsScraperCog
from discord.ext import commands

# https://discordpy.readthedocs.io/en/stable/api.html

class DealsBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger('discord')

    async def on_ready(self):
        self.logger.info(f'Logged in as {self.user}')
        for guild in self.guilds:
            self.logger.info(f'Connected to server: {guild}')
            for channel in guild.channels:
                if 'annons' in channel.name and 'text' == channel.type.name:
                    self.logger.info(f'Found channel for posting ads: {channel.name}')
                    # await channel.send('Testing annons channel')
                    await self.add_cog(DealsScraperCog(self, channel))

def main ():
    intents = discord.Intents.default()
    intents.message_content = True
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    client = DealsBot(intents=None, command_prefix='!')    
    client.run('', log_handler=handler, log_level=logging.INFO)

if __name__ == "__main__":
    main()