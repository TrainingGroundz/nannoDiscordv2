import discord
from discord.ext import commands
from src.database.database import *
import asyncio
import random


class NumeroSecretoCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='n')
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def n(self, ctx):
        inicio = random.randint(50, 3500)
        intervalo = 1500
        fim = inicio + intervalo
        porao_channel = self.client.get_channel(1187065450459316364)
        vip = ctx.guild.get_role(983012540663599114)

        numero_secreto = random.randint(inicio, fim)
        print("numero secreto", numero_secreto)

        embed = discord.Embed(
            title="Descubra o número secreto e ganhe VIP",
            description=f"<:emoji_caio:1060460880162197546> Seu número secreto "
                        f"está entre **{inicio}** e **{fim}**\n"
                        f"Você tem 7 chances de acertá-lo em **2 minutos**\n\n\n"
                        f"Digite `!stop` para terminar o jogo a qualquer momento",
        )

        await porao_channel.send(embed=embed)

        def dicas(arg):
            if int(arg) < numero_secreto:
                return " ⬅️ é menor que o número secreto!"
            else:
                return " ⬅️ é maior que o número secreto!"

        async def calcular_proximidade(numero_secreto, resposta_user):
            diferenca = abs(numero_secreto - resposta_user)

            if diferenca <= 10:
                return discord.Color.dark_red(), (
                    f"**Muito quente** 🔥!!!\n{resposta.author.mention} está muito"
                    f" perto do número secreto, "
                    f"á uma diferença de apenas **10** números no máximo! 🌞"
                )

            elif 10 < diferenca <= 50:
                return discord.Color.red(), (
                    f"**Quente** ☀️!!\n{resposta.author.mention} está se "
                    f"aproximando do número secreto! 🔥"
                )

            elif 50 < diferenca <= 500:
                return (
                    discord.Color.from_rgb(255, 105, 97),
                    (
                        f"**Morno** 😎!\n{resposta.author.mention} ainda "
                        f"falta um pouco, confia! 🌡️"
                    ),
                )

            elif 500 < diferenca <= 800:
                return (
                    discord.Color.from_rgb(0, 255, 255),
                    (
                        f"❄️‍🦰 **Uh, está frio aqui né?** ❄️\n"
                        f"{resposta.author.mention} melhor ir buscar um agasalho"
                        f" pra gente não morrer de frio por aqui! 🧥"
                    ),
                )

            elif 800 < diferenca <= 1000:
                return (
                    discord.Color.blue(),
                    (
                        f"👩‍🦰 **Brrr... está congelando!** ❄️\n"
                        f"{resposta.author.mention} <= Se dependermos dessa "
                        f"pessoa aqui estaremos todos mortos de frio! 🥶"
                    ),
                )

            else:
                return (
                    discord.Color.dark_blue(),
                    (
                        f"🐻‍❄️ **Ops, parece que o {resposta.author.mention} gosta "
                        f"do Polo Norte!** ❄️\nA diferença é tão grande que até os "
                        f"**pinguins** estão surpresos! 🐧"
                    ),
                )

        tentativas_restantes = 7
        numero_invalido = 0

        try:
            while tentativas_restantes > 0:
                resposta = await self.client.wait_for(
                    "message",
                    check=lambda m: m.channel == porao_channel
                                    and m.author != self.client.user
                                    and not m.content.startswith("-n"),
                    timeout=120,
                )

                if "!stop" in resposta.content:
                    embed_stop = discord.Embed(
                        title="O jogo foi encerrado pelo comando `!stop`",
                        description=f"Agora ninguém vai ganhar as recompensas da"
                                    f" {self.client.user.mention} 😭\n"
                                    f"Graças ao {resposta.author.mention} que"
                                    f" encerrou o jogo 🥺",
                    )

                    await porao_channel.send(embed=embed_stop)
                    break

                try:
                    resposta_user = int(resposta.content)

                    if not inicio <= resposta_user <= fim:
                        embed_range = discord.Embed(
                            title=f"❌ {resposta.content} está fora do intervalo!\n"
                                  f"O número secreto deve estar entre {inicio} e "
                                  f"{fim}! Boa sorte 🫱🏻‍🫲🏾",
                            description=f"{resposta.author.mention} 😭 Não se "
                                        f"preocupe, você ainda tem "
                                        f"**{tentativas_restantes}** tentativas ✔️",
                        )

                        await porao_channel.send(embed=embed_range)
                        continue

                except ValueError:
                    numero_invalido += 1
                    if numero_invalido == 2:
                        await porao_channel.send(
                            f"{resposta.author.mention} **Você precisa se "
                            f"concentrar mais!** 🙏🏻\n**{resposta.content}** `"
                            f"<= Em que universo isso aqui é um número pra você"
                            f" meu querido ?!🤬`"
                        )

                    else:
                        if tentativas_restantes == 0:
                            break
                        await porao_channel.send(
                            f"Por favor, digite um número válido.\n"
                            f"Não se preocupe, você ainda tem "
                            f"**{tentativas_restantes}** tentativas ✔️"
                        )

                    continue

                saldo_vip = await checar_vips(ctx.author)
                cor_embed, mensagem = await calcular_proximidade(
                    numero_secreto, resposta_user
                )
                if resposta_user != numero_secreto:
                    tentativas_restantes -= 1
                    if resposta_user != numero_secreto:
                        hints = dicas(resposta_user)
                        if tentativas_restantes:
                            embed_tentativa = discord.Embed(
                                title=f"{resposta_user} {hints}",
                                description=f"{mensagem}\n\n"
                                            f"✔️ {tentativas_restantes} "
                                            f"tentativas restantes",
                                color=cor_embed,
                            )

                            await porao_channel.send(embed=embed_tentativa)

                else:
                    com_vip = "já está registrado"
                    sem_vip = "foi registrado"
                    tem_vip = vip in ctx.author.roles
                    mensagem_registro = (
                        (
                            f"🌟 {ctx.author.mention} {com_vip} no "
                            f"<@&983012540663599114> "
                            f"<:anime_popo_face:1013232728545697802>"
                            f"\nForam adicionadas 5000 **pikas** "
                            f":moneybag: no seu saldo"
                        )
                        if tem_vip
                        else (
                            f"{ctx.author.mention} {sem_vip} no <@&983012540663599114>"
                            f" <:anime_popo_face:1013232728545697802>\n Foram "
                            f"adicionadas 5000 **pikas** :moneybag: no seu saldo"
                        )
                    )

                    embed_acerto = discord.Embed(
                        description=f"# Parabéns 👻!\n O número secreto era "
                                    f"**{numero_secreto}**\n{mensagem_registro}"
                                    f"\nVocê ganhou **1 VIP** e agora possui "
                                    f"{saldo_vip + 1} VIPs\nUse o comando "
                                    f"`-topvip` para ver sua posição!",
                        color=discord.Color.light_grey(),
                    )

                    embed_acerto.set_image(
                        url="https://media1.tenor.com/m/W7g4Ay3jTCAAAAAd/nanno.gif"
                    )

                    if tem_vip:
                        await alterar_saldo(ctx.author, 5000)
                    else:
                        await ctx.author.add_roles(vip)
                        await alterar_saldo(ctx.author, 5000)

                    await porao_channel.send(embed=embed_acerto)
                    await incrementar_vitorias(ctx.author)
                    break

                await asyncio.sleep(0.5)

                if tentativas_restantes % 5 == 0:
                    await asyncio.sleep(0.5)

            else:
                embed_game_over = discord.Embed(
                    title="Game Over",
                    description=f"☠️ É meu puto, pensei que você fosse um "
                                f"verdadeiro **transudo**, mas me enganei!\nO "
                                f"número secreto era **{numero_secreto}**\n"
                                f"Você não tem mais tentativas! 😵",
                    color=discord.Color.red(),
                )

                await porao_channel.send(embed=embed_game_over)
        except asyncio.TimeoutError:
            embed_timeout = discord.Embed(
                title="Game Over",
                description=f"☠️ **Tempo esgotado!** ☠️\nO número secreto "
                            f"era **{numero_secreto}**",
                color=discord.Color.red(),
            )

            await porao_channel.send(embed=embed_timeout)

    @n.error
    async def n_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f"**💕{ctx.author.mention} Descanse um pouquinho enquanto recarrego "
                f"minhas energias! ✨\n⏳ Próximo jogo liberado em "
                f"{round(error.retry_after)} segundos**!"
            )


async def setup(client):
    await client.add_cog(NumeroSecretoCog(client))
