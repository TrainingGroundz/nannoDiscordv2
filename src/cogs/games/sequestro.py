import discord
from discord.ext import commands
import asyncio
from src.database.database import *


class SequestroCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='s')
    async def s(self, ctx, membro: discord.Member):
        channel_commands = self.client.get_channel(982805491732320336)
        channel_porao = self.client.get_channel(1060307386889408564)
        sequestrador = ctx.author.guild.get_role(1060327608530776125)
        sequestrado = ctx.author.guild.get_role(1148067988470239252)

        permanent_roles = [
            1047588622603407501,
            982821606961344543,
            1172200597647269989,
        ]

        saldo = await checar_saldo(ctx.author)
        vips = await checar_vips2(ctx.author)

        if saldo < 7000:
            await channel_commands.send(
                f"O dotado {ctx.author.mention} não conseguiu "
                f"sequestrar a passiva **{membro.global_name}** "
                "por ter pikas insuficientes💰\nPara verificar "
                "suas pikas, use o comando `-pikas`"
            )
            return

        if not vips:
            await channel_commands.send(
                f"O dotado {ctx.author.mention} não conseguiu sequestrar "
                f"a passiva **{membro.global_name}** "
                f"por ter **VIPS** insuficientes💰 "
                f"verifique seu saldo com `-vips` "
            )
            return
        else:
            if not any(role.id in permanent_roles for role in ctx.author.roles):
                custo_pikas = 7000
            else:
                custo_pikas = 3000

            await alterar_saldo(ctx.author, -custo_pikas)
            await ctx.author.add_roles(sequestrador)
            await membro.add_roles(sequestrado)

            await channel_porao.send(
                f"O dotado {ctx.author.mention} pagou **{custo_pikas} "
                f"pikas** + **1 VIP** e sequestrou a passiva "
                f"{membro.mention} <:emoji_caio:1060460880162197546> "
                f"`verifique seu saldo com -vips`"
            )
            await channel_commands.send(
                f"O dotado {ctx.author.mention} pagou **{custo_pikas} "
                f"pikas** + **1 VIP** e sequestrou a passiva "
                f"{membro.mention} <:emoji_caio:1060460880162197546> "
                f"`verifique seu saldo com -vips`"
            )

            await decrementar_vitorias(ctx.author)

            await asyncio.sleep(300)

            await ctx.author.remove_roles(sequestrador)
            await membro.remove_roles(sequestrado)

            await channel_commands.send(
                f"Tempo esgotado! {membro.mention} foi liberado")

    @s.error
    async def s_error(self, ctx, error):
        error_messages = {
            commands.MissingRequiredArgument: lambda
                e: "Opaaa, algo deu errado. Use o comando corretamente "
                   "mencionando o membro que deseja **sequestrar** !",
            commands.BadArgument: lambda
                e: "Hmmm, eu não consegui encontrar esse membro. "
                   "Certifique-se de mencionar um membro válido !",
        }

        for error_type, message_func in error_messages.items():
            if isinstance(error, error_type):
                await ctx.send(
                    message_func(error),
                    allowed_mentions=discord.AllowedMentions(roles=False),
                )
                break


async def setup(client):
    await client.add_cog(SequestroCog(client))
