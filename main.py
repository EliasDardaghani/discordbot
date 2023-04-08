import discord
import logging

# https://discordpy.readthedocs.io/en/stable/api.html

class DealsBot(discord.Client):
    async def on_ready(self):
        logger.info(f'Logged in as {self.user}')
        for guild in client.guilds:
            logger.info(f'Connected to server: {guild}')
            for channel in guild.channels:
                if 'annons' in channel.name and 'text' == channel.type.name:
                    logger.info(f'Found channel for posting ads: {channel.name}')
                    await channel.send('Testing annons channel')

intents = discord.Intents.default()
intents.message_content = True

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
logger = logging.getLogger('discord')
client = DealsBot(intents=None)
client.run('', log_handler=handler, log_level=logging.INFO)