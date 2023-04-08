import discord

# https://discordpy.readthedocs.io/en/stable/api.html

class DealsBot(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')
        for guild in client.guilds:
            print(f'Connected to server: {guild}')

    # async def on_message(self, message):
    #     print(f'Message from {message.author}: {message.content}')
    #     if message.author == self.user:
    #         return
    #     await message.channel.send('Hello World!')

# Not needed for now
# intents = discord.Intents.default()
# intents.message_content = True

client = DealsBot(intents=None)
client.run('')