from io import BytesIO
import discord
import requests
from PIL import ImageFont, Image, ImageDraw
from discord.ext import commands
import random
from src.database.database import *


class EconomyCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="pikas")
    async def _saldo(self, ctx, user: discord.User = None):
        if user:
            moedas_user = await checar_saldo(user)
            await ctx.send(f"{user.mention} tem **{moedas_user} pikas** "
                           f"<:emoji_pica:1014864321349681232>")
            return

        moedas_author = await checar_saldo(ctx.author)
        await ctx.send(
            f"{ctx.author.mention} possui **{moedas_author} "
            "pikas** <:emoji_pica:1014864321349681232>"
        )

    @_saldo.error
    async def saldo_error(self, ctx, error):
        if isinstance(error, commands.UserNotFound):
            await ctx.send(
                "😹 Todos podem usar para ver as pikas do coleguinha, mas é "
                "complicado encontrar um coleguinha que não tem **pikas** 🤡 "
                "\n\nTente novamente, mas lembre-se de verificar saldo de alguém"
                " com **pikas**"
            )

    @commands.command(name="addpikas")
    @commands.has_guild_permissions(administrator=True)
    async def _addpikas(self, ctx: commands.Context,
                        user: discord.User = None,
                        quantidade: int = None):

        if not user or not quantidade:
            await ctx.send(
                f"{ctx.author.mention} O comando deve ser usado da seguinte "
                "forma `-addpikas @membro quantidade`"
            )

            return
        else:
            await alterar_saldo(user, quantidade)
            await ctx.send(
                f"{ctx.author.mention} O valor de **{quantidade} pikas** "
                f":moneybag: foi enviado com sucesso para **{user.global_name}**"
            )

    @_addpikas.error
    async def addpikas_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                f"{ctx.author.mention} Olá pessoa, parece que você não tem "
                "privilégios suficientes para executar esse comando 😞"
            )
        elif isinstance(error, commands.UserNotFound):
            await ctx.send(
                f"{ctx.author.mention} Olá pessoa, parece que o usuário não "
                "foi encontrado 😞"
            )

    @commands.command(name="removepikas")
    @commands.has_guild_permissions(administrator=True)
    async def _removepikas(self, ctx: commands.Context,
                           user: discord.User = None,
                           quantidade: int = None):

        if not user or not quantidade:
            await ctx.send(
                f"{ctx.author.mention} O comando deve ser usado da seguinte "
                "forma `-removepikas @membro quantidade`"
            )

            return

        moedas = await checar_saldo(user)

        if moedas > quantidade:
            await alterar_saldo(user, -quantidade)
            await ctx.send(
                f"{ctx.author.mention} O valor de **{quantidade} pikas** "
                f":moneybag: foi removido de **{user.global_name}**"
            )

        else:
            await ctx.send(
                f"{ctx.author.mention}\n\n🗶Ei coleguinha, {user.mention} tem "
                f"apenas **{moedas} pikas**\nA quantidade a ser removida deve ser "
                "menor que o saldo atual do membro😋"
            )

    @_removepikas.error
    async def removepikas_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                f"{ctx.author.mention} Olá pessoa, parece que você não tem "
                "privilégios suficientes para executar esse comando 😞"
            )
        elif isinstance(error, commands.UserNotFound):
            await ctx.send(
                f"{ctx.author.mention} Olá pessoa, parece que o usuário não foi "
                "encontrado 😞"
            )

    @commands.command(name="daily")
    async def _daily(self, ctx):
        await novo_usuario(ctx.author)
        resultado, tempo_restante, timestamp = await checar_cooldown(ctx.author)
        cargo_2x = [1047588622603407501]
        valor = random.randint(1000, 5000)
        valor_2x = random.randint(2000, 10000)
        msg_semvip = f"{ctx.author.mention} ganhou **{valor} pikas** hoje <:diabinha_pica:1132367768835076176>\nSabia que você poderia receber **2x mais pikas** com o <@&1047588622603407501>?\nAdquira agora em <#1047577913995829380>!"
        msg_vip = f"{ctx.author.mention} ganhou **{valor_2x} pikas** hoje <:diabinha_pica:1132367768835076176>\nVocê ganhou **2x mais pikas** por ter <@&1047588622603407501>"

        if not resultado:
            if any(role.id in cargo_2x for role in ctx.author.roles):
                await ctx.send(
                    msg_vip, allowed_mentions=discord.AllowedMentions(roles=False)
                )
                await alterar_saldo(ctx.author, valor_2x)
                await add_cooldown(ctx.author)
            else:
                await ctx.send(
                    msg_semvip,
                    allowed_mentions=discord.AllowedMentions(roles=False)
                )

                await alterar_saldo(ctx.author, valor)
                await add_cooldown(ctx.author)
        else:
            embed_daily = discord.Embed(
                title="❌ Desculpe, você só pode usar o comando `daily` "
                      "uma vez por dia! :moneybag:",
                description=f"\nAinda faltam **{tempo_restante}** :alarm_clock:"
                            f" para coletar o prêmio diário de **pikas** "
                            f"novamente\nEspero você {ctx.author.mention} "
                            f"às `{timestamp}` 💕\n||Compreendo sua "
                            f"necessidade de pegar **pikas**, mas regras são regras 😏||",
                color=discord.Color.from_rgb(255, 255, 255),
            )

            await ctx.send(embed=embed_daily)

    @commands.command(name="pagar")
    async def pagamento(self, ctx, usuario: discord.User, valor: int):
        moedas = await checar_saldo(ctx.author)
        if ctx.author.id == usuario.id:
            await ctx.send(f'Você não pode fazer uma transferência para si '
                           f'mesmo!')
            return
        if moedas >= valor:
            await alterar_saldo(ctx.author, -valor)
            await alterar_saldo(usuario, valor)
            await ctx.send(
                f"{ctx.author.mention} enviou {valor} pikas com sucesso "
                f"para **{usuario.display_name}** "
                f"<:pica_olhos:1182843924990144602>"
            )
        else:
            await ctx.send(
                "**Você não tem pikas o suficiente para fazer esse pagamento!**"
                "\nUse o comando `-pikas` para verificar quantas pikas você tem!"
            )

    @pagamento.error
    async def erro_pagamento(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.author.mention} parece que você esqueceu de'
                           f' colocar a quantia a ser paga!')

    @commands.command(name="toppikas")
    async def mostrar_rank(self, ctx, pagina=1, ordenar_por="moedas"):
        skip = (pagina - 1) * 5

        campo_ordenacao = ordenar_por if ordenar_por in ['moedas', 'vitorias'] else 'moedas'

        membros_servidor = [membro.id for membro in ctx.guild.members]

        pipeline = [
            {'$match': {'discord_id': {'$in': membros_servidor}}},
            {'$sort': {campo_ordenacao: -1}},
            {'$project': {'discord_id': 1, 'moedas': 1, 'vitorias': 1, '_id': 0}},
            {'$skip': skip},
            {'$limit': 5}
        ]

        resultado = usuarios.aggregate(pipeline)

        rank = []
        posicao = 1 + skip

        for usuario in usuarios.find():
            discord_id = usuario['discord_id']
            membro = ctx.guild.get_member(discord_id)

            if membro is None:
                usuarios.delete_one({'discord_id': discord_id})
                continue

        for usuario in resultado:
            discord_id = usuario['discord_id']
            moedas = usuario['moedas']
            vitorias = usuario.get('vitorias', 0)

            rank.append({
                'posicao': posicao,
                'discord_id': discord_id,
                'moedas': moedas,
                'vitorias': vitorias
            })

            posicao += 1

        if not rank:
            await ctx.send(f"**Não existem membros na página {pagina}!**")
            return

        largura_imagem = 600
        altura_imagem = 675

        script_dir = os.path.dirname(os.path.abspath(__file__))

        font_path = os.path.join(script_dir,
                                 "../../assets/fonts/JetBrainsMono-Bold.ttf")
        image_path = os.path.join(script_dir,
                                  "../../assets/images/background.png")

        fonte_nome = ImageFont.truetype(font_path, 35)
        fonte_moedas = ImageFont.truetype(font_path, 25)

        imagem_fundo = Image.open(image_path)
        imagem_base = Image.new("RGB", (largura_imagem, altura_imagem),
                                (40, 40, 40))
        imagem_base.paste(imagem_fundo.resize((largura_imagem, altura_imagem)),
                          (0, 0))
        desenho = ImageDraw.Draw(imagem_base)

        y_pos = 40
        for index, usuario in enumerate(rank):
            posicao = usuario["posicao"]
            nome = usuario["discord_id"]
            moedas = usuario["moedas"]
            membro = ctx.guild.get_member(nome)

            avatar_url = membro.display_avatar
            avatar = Image.open(BytesIO(requests.get(avatar_url.__str__()).content))
            avatar = avatar.resize((110, 110))

            cor_fundo_avatar = (60, 60, 60)
            desenho.rectangle([10, y_pos, 10 + 110, y_pos + 110],
                              fill=cor_fundo_avatar)

            imagem_base.paste(avatar, (10, y_pos))

            cor_texto = (255, 255, 255)

            if index == 0:
                cor_destaque = (255, 255, 0)
            elif index == 1:
                cor_destaque = (220, 220, 220)
            elif index == 2:
                cor_destaque = (255, 140, 0)
            else:
                cor_destaque = cor_texto

            desenho.text(
                (130, y_pos + 10),
                f"{posicao}. {membro.name}",
                font=fonte_nome,
                fill=cor_destaque,
            )
            desenho.text(
                (130, y_pos + 50), f"Pikas: {moedas}", font=fonte_moedas,
                fill=cor_destaque
            )
            y_pos += 120

        buffer = BytesIO()
        imagem_base.save(buffer, format="PNG")
        buffer.seek(0)

        await ctx.send(file=discord.File(buffer, filename="rank.png"))

    @commands.command(name="topvip")
    async def rank_porao(self, ctx, pagina=1, ordenar_por='vitorias'):
        skip = (pagina - 1) * 5

        campo_ordenacao = ordenar_por if ordenar_por in ['moedas',
                                                         'vitorias'] else 'moedas'

        membros_servidor = [membro.id for membro in ctx.guild.members]

        pipeline = [
            {'$match': {'discord_id': {'$in': membros_servidor}}},
            {'$sort': {campo_ordenacao: -1}},
            {'$project': {'discord_id': 1, 'moedas': 1, 'vitorias': 1,
                          '_id': 0}},
            {'$skip': skip},
            {'$limit': 5}
        ]

        resultado = usuarios.aggregate(pipeline)

        rank = []
        posicao = 1 + skip

        for usuario in usuarios.find():
            discord_id = usuario['discord_id']
            membro = ctx.guild.get_member(discord_id)

            if membro is None:
                usuarios.delete_one({'discord_id': discord_id})
                continue

        for usuario in resultado:
            discord_id = usuario['discord_id']
            moedas = usuario['moedas']
            vitorias = usuario.get('vitorias', 0)

            rank.append({
                'posicao': posicao,
                'discord_id': discord_id,
                'moedas': moedas,
                'vitorias': vitorias
            })

            posicao += 1

        if not rank:
            await ctx.send(f"**Não existem membros na página {pagina}!**")
            return

        largura_imagem = 600
        altura_imagem = 675

        script_dir = os.path.dirname(os.path.abspath(__file__))

        font_path = os.path.join(script_dir,
                                 "../../assets/fonts/JetBrainsMono-Bold.ttf")
        image_path = os.path.join(script_dir,
                                  "../../assets/images/background.png")

        fonte_nome = ImageFont.truetype(font_path, 35)
        fonte_vitorias = ImageFont.truetype(font_path, 25)

        imagem_fundo = Image.open(image_path)
        imagem_base = Image.new("RGB", (largura_imagem, altura_imagem),
                                (40, 40, 40))
        imagem_base.paste(imagem_fundo.resize((largura_imagem, altura_imagem)),
                          (0, 0))
        desenho = ImageDraw.Draw(imagem_base)

        y_pos = 40
        for index, usuario in enumerate(rank):
            posicao = usuario["posicao"]
            nome = usuario["discord_id"]
            vitorias = usuario["vitorias"]
            membro = self.client.get_user(nome)

            avatar_url = membro.display_avatar
            avatar = Image.open(
                BytesIO(requests.get(avatar_url.__str__()).content))
            avatar = avatar.resize((110, 110))

            cor_fundo_avatar = (60, 60, 60)
            desenho.rectangle([10, y_pos, 10 + 110, y_pos + 110],
                              fill=cor_fundo_avatar)

            imagem_base.paste(avatar, (10, y_pos))

            cor_texto = (255, 255, 255)

            if index == 0:
                cor_destaque = (255, 255, 0)
            elif index == 1:
                cor_destaque = (220, 220, 220)
            elif index == 2:
                cor_destaque = (255, 140, 0)
            else:
                cor_destaque = cor_texto

            desenho.text(
                (130, y_pos + 10),
                f"{posicao}. {membro.name}",
                font=fonte_nome,
                fill=cor_destaque,
            )
            desenho.text(
                (130, y_pos + 50),
                f"VIP: {vitorias}",
                font=fonte_vitorias,
                fill=cor_destaque,
            )
            y_pos += 120

        buffer = BytesIO()
        imagem_base.save(buffer, format="PNG")
        buffer.seek(0)

        await ctx.send(file=discord.File(buffer, filename="rank.png"))

    @commands.command(name="vips")
    async def __saldo(self, ctx, membro: discord.User = None):
        if membro is None:
            saldo_author = await checar_vips(ctx.author)
            await ctx.send(
                f"{ctx.author.mention} Você possui um saldo de **{saldo_author}"
                f" VIPS <:emoji_pica:1014864321349681232>**"
            )

        else:
            saldo = await checar_vips(membro)
            await ctx.send(f"{membro.mention} tem um saldo de **{saldo} VIPS**")

    @__saldo.error
    async def saldo_error(self, ctx, error):
        if isinstance(error, commands.UserNotFound):
            await ctx.send(
                "😹Todos podem usar consultar o saldo de **VIPS** do coleguinha, "
                "mas é complicado encontrar o saldo de alguém que não **existe**"
                "🤡\n\nTente novamente, mas lembre-se de mencionar um membro existente!"
            )

    @commands.command(name="addvip")
    @commands.has_guild_permissions(ban_members=True)
    async def addvip(self, ctx, membro: discord.Member, quantidade: int):
        if not membro or not quantidade:
            await ctx.send(
                f"{ctx.author.mention} O comando deve ser usado da seguinte "
                "forma `-addvip @membro quantidade`"
            )

            return
        else:
            await add_vip(membro, quantidade)
            await ctx.send(
                f"{ctx.author.mention} O valor de **{quantidade} VIPS** "
                f":moneybag: foi enviado com sucesso para **{membro.global_name}**"
            )

    @addvip.error
    async def addvip_error(self, ctx, error):
        error_messages = {
            commands.MissingPermissions: lambda
                e: "Você não tem permissão para usar este comando!",
            commands.MissingRequiredArgument: lambda
                e: "Opaaa, algo deu errado. Use o comando corretamente "
                   "`-addvip @membro quantia`",
            commands.BadArgument: lambda
                e: "Hmmm, eu não consegui encontrar esse membro!",
        }

        for error_type, message_func in error_messages.items():
            if isinstance(error, error_type):
                await ctx.send(message_func(error) + " " + ctx.author.mention)
                break

    @commands.command(name="removevip")
    @commands.has_guild_permissions(ban_members=True)
    async def removevip(self, ctx, membro: discord.Member, quantidade: int):
        check = await checar_vips(membro)
        if not membro or not quantidade:
            await ctx.send(
                f"{ctx.author.mention} O comando deve ser usado da seguinte forma "
                "`-removevip @membro quantidade`\n\nLembrando que a quantidade deve ser "
                "menor/igual o saldo atual de **{membro.global_name}**\nVocê pode "
                "verificar o saldo com o comando `-vips @membro`"
            )

            return
        else:
            if check >= quantidade:
                await remove_vip(membro, quantidade)
                await ctx.send(
                    f"{ctx.author.mention} O valor de **{quantidade} VIPS** "
                    f":moneybag: foi removido com sucesso de **{membro.name}**"
                )
            else:
                await ctx.send(
                    f"{ctx.author.mention} Você não pode remover **{quantidade} VIPS** "
                    f":moneybag: pois **{membro.name}** tem um saldo de **{check} VIP**"
                )

    @removevip.error
    async def removevip_error(self, ctx, error):
        error_messages = {
            commands.MissingPermissions: lambda
                e: "Você não tem permissão para usar este comando!",
            commands.MissingRequiredArgument: lambda
                e: "Opaaa, algo deu errado. Use o comando corretamente "
                   "`-removevip @membro quantia`",
            commands.BadArgument: lambda
                e: "Hmmm, eu não consegui encontrar esse membro!",
        }

        for error_type, message_func in error_messages.items():
            if isinstance(error, error_type):
                await ctx.send(message_func(error) + " " + ctx.author.mention)
                break


async def setup(client):
    await client.add_cog(EconomyCog(client))
