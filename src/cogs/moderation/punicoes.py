import asyncio
from datetime import timedelta
import discord
from discord.ext import commands
from src.database.database import *


class Punicoes(discord.ui.Select):
    def __init__(
            self, punicao: str,
            membro: discord.User,
            tempo_mute: int,
            id_user_interaction,
            client):

        self.msg = {
            "verificacao": "Venda sem verificação",
            "idade": "Idade mínima é 16",
            "privado": "Explanar privado",
            "avatar": "Avatar impróprio",
            "offtopic": "Atrapalhar chat",
            "scam": "Venda fake",
            "calls": "Atrapalhar calls",
            "exposed": "Exposed de terceiros",
            "flood": "Flood/Spam",
            "fake": "Membro Fake",
            "14anos": "Idade insuficiente",
            "divulgacao": "Divulgação não autorizada",
            "discriminacao": "Discriminação/Assédio",
            "perseguicao": "Perseguição de membros",
            "rato": "Rato",
        }

        self.punicao = punicao
        self.membro = membro
        self.tempo = tempo_mute
        self.id_author = id_user_interaction
        self.client = client

        options = [
            discord.SelectOption(
                value="verificacao",
                label=self.msg["verificacao"],
                emoji="<a:colorido_sim:1013521308497215651>",
            ),
            discord.SelectOption(value="idade", label=self.msg["idade"],
                                 emoji="🔞"),
            discord.SelectOption(
                value="privado",
                label=self.msg["privado"],
                emoji="<a:pepe_ban:983158328295305227>",
            ),
            discord.SelectOption(
                value="avatar",
                label=self.msg["avatar"],
                emoji="<:anime_vaca:1014871141426409574>",
            ),
            discord.SelectOption(
                value="offtopic",
                label=self.msg["offtopic"],
                emoji="<:anime_deitado:1058642904458989638>",
            ),
            discord.SelectOption(
                value="scam",
                label=self.msg["scam"],
                emoji="<:urso_besta:983194182585823263>",
            ),
            discord.SelectOption(
                value="calls",
                label=self.msg["calls"],
                emoji="<:anime_agua:983202199477817364>",
            ),
            discord.SelectOption(
                value="exposed",
                label=self.msg["exposed"],
                emoji="<:emoji_bdsm:1132367626115489852>",
            ),
            discord.SelectOption(
                value="flood",
                label=self.msg["flood"],
                emoji="<a:frase_ban:1143185480557547581>",
            ),
            discord.SelectOption(
                value="fake",
                label=self.msg["fake"],
                emoji="<:urso_pateta:1056764624457957407>",
            ),
            discord.SelectOption(
                value="14anos",
                label=self.msg["14anos"],
                emoji="<:urso_edu:983160043702722580>",
            ),
            discord.SelectOption(
                value="divulgacao",
                label=self.msg["divulgacao"],
                emoji="<:anime_pensando:984217711708110948>",
            ),
            discord.SelectOption(
                value="discriminacao",
                label=self.msg["discriminacao"],
                emoji="<:pica_pau:1130570834243747941>",
            ),
            discord.SelectOption(
                value="perseguicao",
                label=self.msg["perseguicao"],
                emoji="<:anime_omg:984217742120992769>",
            ),
            discord.SelectOption(
                value="rato",
                label=self.msg["rato"],
                emoji="<:emoji_caio:1060460880162197546>",
            ),
        ]
        super().__init__(placeholder="Selecione o motivo...", options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        membro = self.membro
        reason = self.msg[self.values[0]]
        punicao = self.punicao
        tempo = self.tempo
        author_id = self.id_author

        guild = interaction.guild
        member = await self.client.fetch_user(membro.id)
        membro_fora = await self.client.fetch_user(membro.id)
        author_member = guild.get_member(author_id)
        duracao = timedelta(minutes=tempo)
        canal_punicoes = self.client.get_channel(983234083918344222)

        if interaction.user.id == author_member.id:
            if member or membro_fora:
                if punicao == "aviso" and member:
                    contagem_mutes = await checar_mutes(member)
                    contagem_avisos = await checar_avisos(member)
                    if contagem_avisos < 3 or contagem_avisos % 3 != 0:
                        await canal_punicoes.send(
                            f"O membro **{member.mention}** recebeu uma punição do "
                            f"servidor 😈 EDP 😈 aplicada por {interaction.user.mention}"
                            f"\n\n__Motivo:__  **{reason}**\n\n__Punição:__  "
                            f"**[{self.punicao.capitalize()}]\n\n**O membro "
                            f"{member.mention} já tem {contagem_avisos} Avisos "
                            f"e {contagem_mutes} Mutes"
                        )
                        await member.send(
                            f"⚠️ Você recebeu uma punição do servidor 😈 EDP 😈"
                            f"\n\n__Motivo:__  **{reason}**  \n\n__Punição:__  "
                            f"**[{self.punicao.capitalize()}]**\n\nReceber múltiplas"
                            f" punições pode acarretar em mute eterno ou banimento!"
                            f"\n\nO que fazer agora?\nQueremos ajudar você a continuar"
                            f" no servidor. Para isso, é importante:\n> 1. Conhecer "
                            f"as <#982810991194689546> da Elite e não violá-las;\n> 2."
                            f" Apelar a punição em <#1077273053806997554> caso "
                            f"acredite que cometemos um erro."
                        )
                    elif contagem_avisos == 3:
                        await canal_punicoes.send(
                            f"**O membro {member.mention} recebeu {contagem_avisos} "
                            f"avisos e ganhou uma punição mais severa de 24 horas"
                            f" aplicada por {interaction.user.mention}**"
                        )
                        await member.timeout(
                            timedelta(hours=24),
                            reason=f"**O membro {member.display_name} recebeu "
                                   f"{contagem_avisos} avisos e ganhou uma punição"
                                   f" mais severa de 24 horas**",
                        )
                        await member.send(
                            f"⚠️ Você recebeu uma punição do servidor 😈 EDP 😈"
                            f"\n\n__Motivo:__  **{reason}**  \n\n__Punição:__  "
                            f"**[Mute : 24 horas || Esse é o seu {contagem_avisos}º "
                            f"Aviso]**\n\nReceber múltiplas punições pode acarretar"
                            f" em mute eterno ou banimento!\n\nO que fazer agora?"
                            f"\nQueremos ajudar você a continuar no servidor. Para"
                            f" isso, é importante:\n> 1. Conhecer as "
                            f"<#982810991194689546> da Elite e não violá-las;\n> 2."
                            f" Apelar a punição em https://discord.gg/4sdVrdVjbr caso "
                            f"acredite que cometemos um erro."
                        )
                    elif contagem_avisos == 6:
                        await canal_punicoes.send(
                            f"**O membro {member.mention} recebeu {contagem_avisos} "
                            f"avisos e ganhou uma punição mais severa de 24 horas"
                            f" aplicada por {interaction.user.mention}**"
                        )
                        await member.timeout(
                            timedelta(hours=24),
                            reason=f"O membro {member.display_name} recebeu "
                                   f"{contagem_avisos} e recebeu uma punição mais"
                                   f" severa de 24 horas",
                        )
                        await member.send(
                            f"⚠️ Você recebeu uma punição do servidor 😈 EDP 😈"
                            f"\n\n__Motivo:__  **{reason}**  \n\n__Punição:__  "
                            f"**[Mute : 24 horas || Esse é o seu {contagem_avisos}º "
                            f"Aviso]**\n\nReceber múltiplas punições pode acarretar"
                            f" em mute eterno ou banimento!\n\nO que fazer agora?"
                            f"\nQueremos ajudar você a continuar no servidor. Para"
                            f" isso, é importante:\n> 1. Conhecer as "
                            f"<#982810991194689546> da Elite e não violá-las;\n> 2. "
                            f"Apelar a punição em https://discord.gg/4sdVrdVjbr caso "
                            f"acredite que cometemos um erro."
                        )
                    elif contagem_avisos == 9:
                        await canal_punicoes.send(
                            f"**O membro {member.mention} recebeu {contagem_avisos}"
                            f" avisos e recebeu uma punição mais severa de 24 horas"
                            f" aplicada por {interaction.user.mention}**"
                        )
                        await member.timeout(
                            timedelta(hours=24),
                            reason=f"O membro {member.display_name} recebeu"
                                   f" {contagem_avisos} e recebeu uma punição "
                                   f"mais severa de 24 horas",
                        )
                        await member.send(
                            f"⚠️ Você recebeu uma punição do servidor 😈 EDP 😈"
                            f"\n\n__Motivo:__  **{reason}**  \n\n__Punição:__  "
                            f"**[Mute : 24 horas || Esse é o seu {contagem_avisos}º "
                            f"Aviso]**\n\nReceber múltiplas punições pode acarretar "
                            f"em mute eterno ou banimento!\n\nO que fazer agora?"
                            f"\nQueremos ajudar você a continuar no servidor. Para"
                            f" isso, é importante:\n> 1. Conhecer as "
                            f"<#982810991194689546> da Elite e não violá-las;\n> 2."
                            f" Apelar a punição em https://discord.gg/4sdVrdVjbr caso "
                            f"acredite que cometemos um erro."
                        )
                    elif contagem_avisos >= 12:
                        await canal_punicoes.send(
                            f"**O membro {member.mention} recebeu um aviso aplicado por "
                            f"{interaction.user.mention} e como ele tem {contagem_avisos}"
                            f" avisos o meliante foi contemplado com um banimento!**"
                            f"*Os avisos de {member.mention} foram zerados "
                            f"devido ao __banimento__*"
                        )
                        await remover_aviso(member, 12)
                        await member.send(
                            f"⚠️ Você recebeu uma punição do servidor 😈 EDP 😈"
                            f"\n\n__Motivo:__  **{reason}**  \n\n__Punição:__  "
                            f"**[Banimento]**\n\nO que fazer agora?"
                            f" 1. Apelar a punição em https://discord.gg/4sdVrdVjbr caso "
                            f" acredite que cometemos um erro.\n 2. Aguardar até o Natal para poder"
                            f" entrar novamente em https://discord.gg/edp2"
                        )
                        await guild.ban(membro_fora)
                    await interaction.followup.send(
                        f"Aviso enviado para **{member.display_name}**: {reason}",
                        ephemeral=True,
                    )

                elif punicao == "ban":
                    await canal_punicoes.send(
                        f"O membro **{member.mention}** recebeu uma punição do "
                        f"servidor 😈 EDP 😈 aplicada por {interaction.user.mention}"
                        f"\n\n__Motivo:__  **{reason}**\n\n__Punição:__  "
                        f"**[{self.punicao.capitalize()}]**"
                    )
                    await interaction.followup.send(
                        f"Aviso enviado para **{member.display_name}**: "
                        f"{reason}\n\n*Banimento aplicado*",
                        ephemeral=True,
                    )

                    membros = self.client.get_all_members()
                    if member in membros:
                        await member.send(
                            f"⚠️ Você recebeu uma punição do servidor 😈 EDP 😈"
                            f"\n\n__Motivo:__  **{reason}**  \n\n__Punição:__  "
                            f"**[{self.punicao.capitalize()}]**\n\nO que fazer agora?"
                            f" 1. Apelar a punição em https://discord.gg/4sdVrdVjbr caso"
                            f" acredite que cometemos um erro.\n 2. Aguardar até o Natal para poder"
                            f" entrar novamente em https://discord.gg/edp2"
                        )
                    await guild.ban(membro_fora)

                elif punicao == "mute":
                    contagem_mutes = await checar_mutes(member)
                    if contagem_mutes == 3:
                        await canal_punicoes.send(
                            f"**O membro {member.mention} recebeu {contagem_mutes}"
                            f" e foi contemplado com um banimento!"
                            f" aplicado por {interaction.user.mention}**"
                        )
                        await interaction.followup.send(
                            f"Aviso enviado para **{member.display_name}**: "
                            f"{reason}\n\n*Banimento aplicado*\n\n*",
                            ephemeral=True,
                        )
                        await member.send(
                            f"⚠️ Você recebeu uma punição do servidor 😈 EDP 😈"
                            f"\n\n__Motivo:__  **{reason}**  \n\n__Punição:__  "
                            f"**[Banido]**\n\nO que fazer agora?\n"
                            f" 1. Apelar a punição em https://discord.gg/4sdVrdVjbr caso"
                            f" acredite que cometemos um erro.\n 2. Aguardar até o Natal para poder"
                            f" entrar novamente em https://discord.gg/edp2"
                        )
                        await remover_mute(member, 3)
                        await guild.ban(membro_fora)
                    else:
                        await member.timeout(duracao, reason=reason)
                        await interaction.followup.send(
                            f"Aviso enviado para **{member.display_name}**: "
                            f"{reason}\n\n*Mute aplicado*",
                            ephemeral=True,
                        )
                        await canal_punicoes.send(
                            f"O membro **{member.mention}** recebeu uma punição do "
                            f"servidor 😈 EDP 😈 aplicada por {interaction.user.mention}"
                            f"\n\n__Motivo:__  **{reason}**\n\n__Punição:__  "
                            f"**[{self.punicao.capitalize()}] : {self.tempo} minutos"
                            f"\n\n**O membro {member.mention} já tem {contagem_avisos}"
                            f" Avisos e {contagem_mutes} Mutes"
                        )
                        await member.send(
                            f"⚠️ Você recebeu uma punição do servidor 😈 EDP 😈"
                            f"\n\n__Motivo:__  **{reason}**  \n\n__Punição:__  "
                            f"**[{punicao.capitalize()} : {self.tempo} minutos || "
                            f"Esse é o seu {mutes}º Mute]**\n\nReceber múltiplas "
                            f"punições pode acarretar em mute eterno ou banimento!"
                            f"\n\nO que fazer agora?\nQueremos ajudar você a "
                            f"continuar no servidor. Para isso, é importante:\n> 1. "
                            f"Conhecer as <#982810991194689546> da Elite e não "
                            f"violá-las;\n> 2. Apelar a punição em "
                            f"https://discord.gg/4sdVrdVjbr caso acredite que cometemos"
                            f" um erro."
                        )
            else:
                await interaction.followup.send("Membro não encontrado",
                                                ephemeral=True)
        else:
            await interaction.followup.send(
                f"{interaction.user.display_name} Você não tem permissão para "
                f"usar este Menu, somente o Moderador "
                f"{author_member.display_name} pode fazer isso!",
                ephemeral=True,
            )


class PunicoesView(discord.ui.View):
    def __init__(self, punicao: str,
                 membro: discord.User,
                 tempo_mute: int,
                 interacao,
                 client):
        super().__init__(timeout=None)
        self.add_item(
            Punicoes(
                punicao=punicao,
                membro=membro,
                tempo_mute=tempo_mute,
                id_user_interaction=interacao,
                client=client
            )
        )


class PunicoesCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="mod")
    @commands.has_permissions(ban_members=True)
    async def _punicao(self, ctx,
                       punicao: str,
                       member: discord.User,
                       mute: int = None):

        id_author = ctx.author.id
        if mute is None:
            mute = 40320
        await novo_usuario(member)
        await adicionar_chaves(member)
        if punicao == "ban":
            await ctx.send(
                f"Selecione um motivo para aplicar o **banimento em "
                f"{member.display_name}.**\n*Essa mensagem será apagada "
                f"automaticamente em 30 segundos*",
                view=PunicoesView(
                    punicao=punicao, membro=member, tempo_mute=mute,
                    interacao=id_author, client=self.client
                ),
                delete_after=30,
            )
            await asyncio.sleep(5)
            await ctx.message.delete()

        elif punicao == "mute":
            await adicionar_mute(member)
            await ctx.send(
                f"Selecione um motivo para aplicar o **mute de {mute} minutos "
                f"em {member.display_name}.**\n*Essa mensagem será apagada "
                f"automaticamente em 30 segundos*",
                view=PunicoesView(
                    punicao=punicao, membro=member, tempo_mute=mute,
                    interacao=id_author, client=self.client
                ),
                delete_after=30,
            )
            await asyncio.sleep(5)
            await ctx.message.delete()

        elif punicao == "aviso":
            await adicionar_aviso(member)
            await ctx.send(
                f"Selecione um motivo para aplicar **um aviso para "
                f"{member.display_name}.**\n*Essa mensagem será apagada "
                f"automaticamente em 30 segundos*",
                view=PunicoesView(
                    punicao=punicao,
                    membro=member,
                    tempo_mute=mute,
                    interacao=id_author,
                    client=self.client
                ),
                delete_after=30,
            )
            await asyncio.sleep(5)
            await ctx.message.delete()
        else:
            await novo_usuario(member)
            await adicionar_chaves(member)

            if punicao == "ban":
                await ctx.send(
                    f"Selecione um motivo para aplicar o **banimento em "
                    f"{member.display_name}.**\n*Essa mensagem será apagada "
                    f"automaticamente em 30 segundos*",
                    view=PunicoesView(
                        punicao=punicao, membro=member, tempo_mute=mute,
                        interacao=id_author, client=self.client
                    ),
                    delete_after=30,
                )
                await asyncio.sleep(5)
                await ctx.message.delete()

            elif punicao == "mute":
                await adicionar_mute(member)
                await ctx.send(
                    f"Selecione um motivo para aplicar o **mute de {mute} "
                    f"minutos em {member.display_name}.**\n*Essa mensagem será"
                    f" apagada automaticamente em 30 segundos*",
                    view=PunicoesView(
                        punicao=punicao,
                        membro=member,
                        tempo_mute=mute,
                        interacao=id_author,
                        client=self.client
                    ),
                    delete_after=30,
                )
                await asyncio.sleep(5)
                await ctx.message.delete()

            elif punicao == "aviso":
                await adicionar_aviso(member)
                await ctx.send(
                    f"Selecione um motivo para aplicar um **aviso para "
                    f"{member.display_name}.**\n*Essa mensagem será apagada "
                    f"automaticamente em 30 segundos*",
                    view=PunicoesView(
                        punicao=punicao,
                        membro=member,
                        tempo_mute=mute,
                        interacao=id_author,
                        client=self.client
                    ),
                    delete_after=30,
                )
                await asyncio.sleep(5)
                await ctx.message.delete()

    @_punicao.error
    async def _punicao_error(self, ctx, error):
        canal = self.client.get_channel(983234083918344222)
        if isinstance(error, commands.MissingPermissions):
            await canal.send(
                f"{ctx.author.mention} Olá pessoa, parece que você não tem "
                "privilégios suficientes para executar esse comando 😞"
            )
        elif isinstance(error, commands.UserNotFound):
            await canal.send(
                f"{ctx.author.mention} Olá pessoa, parece que o usuário não"
                f" foi encontrado 😞")

    @commands.command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx,
                    user_id: int):

        canal = self.client.get_channel(983234083918344222)
        try:
            user = await self.client.fetch_user(user_id)
            await ctx.guild.unban(user, reason=None)
            embed_user = discord.Embed(
                title="Membro desbanido!",
                description=f"{user_id} já pode entrar novamente no servidor!",
                color=0x00FF00,
            )
            await canal.send(embed=embed_user)
        except discord.NotFound:
            embed = discord.Embed(
                title="Erro",
                description=f"O id do usuário {user_id} não foi encontrado.",
                color=0xFF0000,
            )
            await canal.send(embed=embed)

    @unban.error
    async def _unban_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            canal = self.client.get_channel(983234083918344222)
            await canal.send(
                f"{ctx.author.mention} Certifique-se de fornecer um `ID` **válido**")

    @commands.command(name="unmute")
    @commands.has_permissions(ban_members=True)
    async def _unmute(self, member: discord.Member):
        mutado = member.is_timed_out()
        canal = self.client.get_channel(983234083918344222)

        if mutado:
            await member.edit(timed_out_until=None)
            await asyncio.sleep(1)
            await canal.send(
                f"**A punição mute foi removida de {member.display_name}**")
            await member.send("Sua punição de **mute** foi removida!")
        else:
            await canal.send(
                f"Oppss! parece que o {member.display_name} não está mutado!")

    @_unmute.error
    async def _unmute_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            canal = self.client.get_channel(983234083918344222)
            await canal.send(
                f"{ctx.author.mention} Certifique-se de mencionar um membro válido")

    @commands.command(name="removeravisos")
    @commands.has_permissions(ban_members=True)
    async def _removeravisos(self, ctx,
                             member: discord.Member,
                             quantidade: int = None):
        avisos = await checar_avisos(member)
        canal = self.client.get_channel(983234083918344222)

        if quantidade is None or quantidade > avisos:
            await canal.send(
                f"{ctx.author.mention} Por favor insira quantos avisos deseja"
                f" remover de {member.display_name}\n\n"
                f"Atualmente o membro possui `{avisos}` **Aviso(s)**"
            )
        if avisos > 0 and quantidade <= avisos:
            await remover_aviso(member, quantidade)
            await member.send(f"Você teve **{quantidade} aviso(s)** removido(s)!")
            await canal.send(
                f"**{quantidade} aviso(s)** removido(s) de " f"{member.display_name}"
            )
        else:
            return

    @_removeravisos.error
    async def _removeravisos_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            canal = self.client.get_channel(983234083918344222)
            await canal.send(
                f"{ctx.author.mention} Certifique-se de mencionar um membro válido")

    @commands.command(name="removermutes")
    @commands.has_permissions(ban_members=True)
    async def _removermutes(self, ctx,
                            member: discord.Member,
                            quantidade: int = None):

        canal = self.client.get_channel(983234083918344222)
        mutes = await checar_mutes(member)

        if quantidade is None or quantidade > mutes:
            await canal.send(
                f"{ctx.author.mention} Por favor insira quantos mutes deseja"
                f" remover de {member.display_name}\n\n"
                f"Atualmente o membro possui `{mutes}` **Mute(s)**"
            )

        if mutes > 0 and quantidade <= mutes:
            await remover_mute(member, quantidade)
            await member.send(f"Você teve **{quantidade} mute(s)** removido(s)!")
            await canal.send(
                f"**{quantidade} mute(s)** removido de " f"{member.display_name}")

    @_removermutes.error
    async def _removermutes_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            canal = self.client.get_channel(983234083918344222)
            await canal.send(
                f"{ctx.author.mention} Certifique-se de mencionar um membro válido")


async def setup(client):
    await client.add_cog(PunicoesCog(client))
