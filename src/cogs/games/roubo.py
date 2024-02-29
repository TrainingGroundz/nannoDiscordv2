import asyncio
import discord
from discord.ext import commands
from src.database.database import *
import random


class RouboCog(commands.Cog):
    members_in_theft = set()

    def __init__(self, client):
        self.client = client

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
            ctx.command.reset_cooldown(ctx)
            return

        if member_balance < 1:
            await ctx.send(f'Parece que {member.mention} é tipo o Tio Patinhas,'
                           f' tá mais seco que deserto! 😅 {ctx.author.mention},'
                           f' melhor dar uma olhada em outras pikas, porque '
                           f'esse alguém ja passou a mão. 💸')
            ctx.command.reset_cooldown(ctx)
            return

        if author_balance < 1:
            await ctx.send(f'{ctx.author.mention}Você precisa de pikas pra '
                           f'poder roubar, ganhe em <#1187065450459316364>')
            ctx.command.reset_cooldown(ctx)
            return

        if roubos >= 2:
            await ctx.send(f'{ctx.author.mention} Ladrãozinho safado, '
                           f'tente roubar novamante amanhã!')
            ctx.command.reset_cooldown(ctx)
            return

        if ctx.author.id in self.members_in_theft or member.id in self.members_in_theft:
            await ctx.send(
                "Desculpe, mas um dos membros está atualmente ocupado em uma "
                "`operação de roubo` 🕵️‍♂️💰.\nFique ligado o roubo pode acabar "
                "a qualquer momento! 🕒😄")
            ctx.command.reset_cooldown(ctx)
            return

        try:
            self.members_in_theft.add(ctx.author.id)
            self.members_in_theft.add(member.id)

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
                max_roubo = 1000
                quantia_roubo = random.randint(1,
                                               min(author_balance,
                                                   member_balance,
                                                   max_roubo)
                                               )
                if member_balance < quantia_roubo:
                    quantia_roubo = member_balance

                embed_sucess = discord.Embed(
                    title="157 BEM SUCEDIDO <:urso_rico:983160080474202204> ",
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
                max_roubo = 1000
                quantia_roubo = random.randint(1,
                                               min(author_balance,
                                                   member_balance,
                                                   max_roubo)
                                               )

                if author_balance < quantia_roubo:
                    quantia_roubo = author_balance

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

        finally:
            self.members_in_theft.remove(ctx.author.id)
            self.members_in_theft.remove(member.id)

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
