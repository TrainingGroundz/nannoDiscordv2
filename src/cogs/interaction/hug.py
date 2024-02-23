import discord
from discord.ext import commands


class HugCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hug')
    async def hug_command(self, ctx, member: discord.Member):
        pass


async def setup(bot):
    await bot.add_cog(HugCog(bot))
