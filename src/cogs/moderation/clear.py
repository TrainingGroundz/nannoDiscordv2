import asyncio
import discord
import pytz
from discord.ext import commands
import datetime
from datetime import timedelta


class ClearCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='clear')
    @commands.has_guild_permissions(manage_messages=True)
    async def _purgemsg(self, ctx, value: commands.Range[int, 2, 1000]):
        await ctx.message.delete()
        gmt = pytz.timezone('America/Sao_Paulo')
        now = datetime.datetime.now(tz=gmt)
        log_channel = self.client.get_channel(983234083918344222)

        fourteendays = now - timedelta(days=14)

        messages = [message async for message in
                    ctx.channel.history(limit=value,
                                        after=fourteendays,
                                        oldest_first=False)
                    ]

        messages_ignored = [message async for message in
                            ctx.channel.history(limit=value,
                                                before=now,
                                                oldest_first=False)
                            ]

        await ctx.channel.delete_messages(messages)

        result = len(messages_ignored) - len(messages)
        msg = (
                  f'**✅ Foram apagadas {len(messages)} mensagem(s).**\n\n'
                  if len(messages) > 0 else ''
              ) + (
                  f'**{result} mensagem(s)** não foram apagadas devido a '
                  f'limitações do Discord\n`mais antigas que 14 dias`\n'
                  if result != 0 else ''
              )

        embed = discord.Embed(description=f'{msg}Clear feito em <#{ctx.channel.id}>'
                                          f' por: {ctx.author.mention}')

        await log_channel.send(embed=embed,
                               allowed_mentions=discord.AllowedMentions(users=False))

    @_purgemsg.error
    async def msg_error(self, ctx, error):
        if isinstance(error, commands.RangeError):
            await ctx.send(f'Olá {ctx.author.mention} insira um numero de '
                           f'mensagens válido para apagar `2 a 1000`')
        elif isinstance(error, commands.MissingPermissions):
            return


async def setup(client):
    await client.add_cog(ClearCog(client))
