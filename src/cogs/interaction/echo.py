import asyncio
import discord
from discord.ext import commands


class EchoCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="r")
    @commands.has_permissions(send_tts_messages=True)
    async def r(self, ctx, *, message: commands.clean_content = None):
        if message is not None:
            await ctx.message.delete()
            async with ctx.typing():
                await asyncio.sleep(1)
                await ctx.send(message)

        await ctx.message.delete()

        async with ctx.typing():
            await asyncio.sleep(1)
            await ctx.send(
                f"Ei {ctx.author.mention} amiguinho, é pra repetir uma mensagem "
                "e você não deixou mensagem alguma, cabeça de vento"
            )

    @r.error
    async def repeat_message_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                "Você não tem a tag <@&983012540663599114> para utilizar " "esse comando",
                allowed_mentions=discord.AllowedMentions(roles=False,
                                                         everyone=False),
            )


async def setup(client):
    await client.add_cog(EchoCog(client))
