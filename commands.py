import logging
from discord.ext import commands
import asyncio

class CommandsCog(commands.Cog):
    def __init__(self, bot):
        self.logger = logging.getLogger('discord')
        self.bot = bot

    def cog_unload(self):
        self.logger.info('DealsCog unloading')

    @commands.command()
    async def start(self, ctx):
        async with ctx.typing():
            await asyncio.sleep(2)
        if str(ctx.author.id) in self.bot.admins:
            await ctx.reply('Yas boss!')
        else:
            await ctx.reply('Yas!')

    @commands.command()
    async def stop(self, ctx):
        async with ctx.typing():
            await asyncio.sleep(2)
        if str(ctx.author.id) in self.bot.admins:
            await ctx.reply('Yas boss!')
        else:
            await ctx.reply('Yas!')

    @commands.command()
    async def logs(self, ctx):
        async with ctx.typing():
            await asyncio.sleep(2)
        if str(ctx.author.id) in self.bot.admins:
            log = ''
            with open('discord.log', 'r') as f:
                for line in (f.readlines() [-10:]):
                    log += line
            await ctx.reply(f'Yas boss!\n{log}')
        else:
            await ctx.reply('Yas!')
