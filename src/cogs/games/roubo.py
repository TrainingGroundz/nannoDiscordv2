import asyncio
import discord
from discord.ext import commands, tasks
from src.database.database import *
import random
import datetime
import pytz


class RouboCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.my_loop.start()

    @tasks.loop(seconds=30)
    async def my_loop(self):
        agora_gmt = datetime.datetime.now(pytz.timezone('GMT'))
        meia_noite_gmt = (agora_gmt.replace(hour=0,
                                            minute=0,
                                            second=0,
                                            microsecond=0) + datetime.timedelta(days=1))

        if agora_gmt >= meia_noite_gmt:
            await zerar_roubos()

    @commands.command(name='roubar')
    @commands.has_role(983012540663599114)
    @commands.cooldown(1, 180, commands.BucketType.member)
    async def roubar(self, ctx, member: discord.Member):
        member_balance = await checar_saldo(member)
        author_balance = await checar_saldo(ctx.author)
        roubos = await checar_roubos(ctx.author)

        chance_roubo = 0.5

        if ctx.author.id == member.id:
            await ctx.send(f'{ctx.author.mention} Tá doido maluco? Roubar '
                           f'apenas os outros coleguinhas!')
            return

        if member_balance < 1:
            await ctx.send(f'Parece que {member.mention} é tipo o Tio Patinhas,'
                           f' tá mais seco que deserto! 😅 {ctx.author.mention},'
                           f' melhor dar uma olhada em outras pikas, porque '
                           f'esse alguém ja passou a mão. 💸')
            return

        if roubos >= 2:
            await ctx.send(f'{ctx.author.mention} Ladrãozinho safado, '
                           f'tente roubar novamante amanhã!')
            return

        embed_progress = discord.Embed(
            title='Roubo em andamento <a:doge_legal:1058817762262257754>',
            description='O roubo está sendo realizado hehehe.'
                        ' Volte daqui há 3min para saber o resultado',
            color=discord.Colour.from_rgb(0, 191, 255)
        )
        embed_progress.set_thumbnail(
            url='https://tenor.com/view/ladr%C3%A3o-gif-22153661.gif')

        msg = await ctx.send(embed=embed_progress)

        if random.random() < chance_roubo:
            max_roubo = 10000
            quantia_roubo = random.randint(1,
                                           min(author_balance,
                                               member_balance,
                                               max_roubo)
                                           )

            embed_sucess = discord.Embed(
                title="157 bem sucedido <:urso_rico:983160080474202204> ",
                description=f'{ctx.author.mention} fez umas trambicagens, tipo '
                            f'roubar pikas, e conseguiu **{quantia_roubo} '
                            f'pikas** de {member.mention}! 💰🔫 Parece que '
                            f'ninguém tava vigiando e ele vazou de fininho.'
                            f' Haja ousadia e pika na conta!',
                color=discord.Colour.green()
            )
            embed_sucess.set_thumbnail(
                url='https://media1.tenor.com/m/Zx-xrB_RkOEAAAAC/nanno-nanno-laugh.gif')

            await asyncio.sleep(180)
            await msg.delete()
            await ctx.send(f'{ctx.author.mention} {member.mention}',
                           embed=embed_sucess
                           )

            await adicionar_roubo(ctx.author)
            await alterar_saldo(ctx.author, quantia_roubo)
            await alterar_saldo(member, -quantia_roubo)
        else:
            max_roubo = 10000
            quantia_roubo = random.randint(1,
                                           min(author_balance,
                                               member_balance,
                                               max_roubo)
                                           )

            embed_failure = discord.Embed(
                title="<a:colorido_sirene:1013521589221994608> "
                      "PEGO EM FLAGRANTE!",
                description=f"{ctx.author.mention}, meu chapa, você tentou "
                            f"roubar as pikas do {member.mention}, mas a coisa "
                            f"não rolou muito bem, não é mesmo? 😅\nAgora, além"
                            f" de não levar nenhuma pika você ainda foi roubado"
                            f" pela própria vítima e perdeu **{quantia_roubo} "
                            f"pikas**. Não desista, a prática leva a perfeição!",
                color=discord.Colour.red()
            )
            embed_failure.set_thumbnail(
                url="https://media1.tenor.com/m/QgTx6fv4IpAAAAAd/el-risitas-juan-joya-borja.gif")

            await asyncio.sleep(180)
            await msg.delete()
            await ctx.send(f'{ctx.author.mention} {member.mention}',
                           embed=embed_failure
                           )

            await alterar_saldo(ctx.author, -quantia_roubo)
            await alterar_saldo(member, quantia_roubo)

    @roubar.error
    async def roubo_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send(f'{ctx.author.mention} Ei espertinho, mesmo sendo um'
                           f' ladrão, você precisa ser **VIP**!')
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'{ctx.author.mention} Calma lá amigão, você só pode'
                           f' fazer um roubo de pikas por vez!')


async def setup(client):
    await client.add_cog(RouboCog(client))