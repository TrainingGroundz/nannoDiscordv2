import asyncio
import discord
from discord.ext import commands

id_cargo_atendente = 983142362698092555


class Dropdown(discord.ui.Select):
    def __init__(self):
        self.mensagens = {
            "1": "Para tirar dúvidas sobre o servidor, envie nesse ticket!",
            "2": "Para denunciar um membro é __indispensável__ as seguintes informações:\n\n> 1. Motivo da denúncia\n> 2. Nick do denunciado (de preferência o ID)\n> 3. Provas\n\nNa falta de alguma das informações acima é **inviável** realizar qualquer punição!",
            "3": "Para apelar uma advertência é __obrigatório__  as seguintes informações:\n\n> 1. Motivo do aviso\n> 2. Nick do punido (de preferência o ID)\n> 3. Motivos para retirarmos o aviso\n\nNa falta de alguma das informações acima é **inviável** realizar qualquer apelação!",
            "4": "Existem 3 verificações na Elite, sendo elas, Verificar Pack, Verificar Idade e Verificar Interação!\nEscolha uma delas em https://discord.com/channels/982795400798937128/982811153753341952 e abra o Ticket da verificação desejada.",
            "5": "O EDP+ Elite é uma assinatura mensal e pode ser adquirido por pikas, sonhos ou PIX.\n\n> __Pikas__: 50.000 \n> __Sonhos__: 50.000\n> __Pix__: R$5 \n\n> Para pikas, use o comando `-pagar @staff_atendente 50000` \n> Para sonhos, use o comando `+pagar @staff_atendente 50000` \n> Para PIX, envie o valor na chave:\n```00c72e9d-9db8-41a2-aa2d-7b0ec27e4447``` ou pelo QR [Code](https://media.discordapp.net/attachments/1124725730807394317/1187450957114638356/Screenshot_20231221_144430_Chrome.jpg?ex=6596eee1&is=658479e1&hm=7091c13aefaeaa74c799c71a2c332c2752e401adc98525eaed00b80095683d6a&)\nFavor enviar o comprovante do PIX!!!",
            "6": "Você ganhou um sorteio ou evento? Parabéns!!!\nInforme o nome do sorteio/evento e o prêmio",
            "7": "As parcerias do Elite são feitas através de **sorteios**. Para patrocinar um sorteio, você deve pagar o valor do prêmio, como PIX, Nitro ou Sonhos.\n\nCom isso, terá direito a mencionar o ping de sorteios e enviar o link do seu servidor.",
            "8": "Para fazer parte da __Staff EDP__, responda as perguntas abaixo:\n\n> Qual o seu nick e ID?\n> Qual a sua idade?\n> Qual a sua ocupação atual?\n> Quanto tempo faz parte da EDP?\n> Qual a sua disponibilidade?\n> Tem um bom microfone?\n> Se considera um membro ativo no servidor?\n> Já fez parte de alguma Staff? Se sim, qual?\n> Está ciente de todas as suas funções como staff previstas em https://discord.com/channels/982795400798937128/1056017474623131749 ?\n> Faça um breve resumo das regras da Elite.",
            "9": "Para reportar um **Bug** no servidor, informe:\n\n> 1. Contexto para ter encontrado o bug\n> 2. Explicação do bug\n> 3. Print ou gravação da tela mostrando o bug",
            "10": "A sua opção não está aqui?\nSem problemas, conte todos os detalhes aqui!",
        }
        options = [
            discord.SelectOption(
                value="duvidas",
                label="Tirar Dúvidas",
                emoji="<:anime_pensando:984217711708110948>",
            ),
            discord.SelectOption(
                value="denuncia",
                label="Denunciar Membro",
                emoji="<:frase_ban:1143185480557547581>",
            ),
            discord.SelectOption(
                value="apelo",
                label="Apelar Punição",
                emoji="<:pepe_ban:983158328295305227>",
            ),
            discord.SelectOption(
                value="verificaçao",
                label="Solicitar Verificação",
                emoji="<:colorido_sim:1013521308497215651>",
            ),
            discord.SelectOption(
                value="comprar edp+",
                label="Comprar EDP+",
                emoji="<:diamante_azul:1058813444704448633>",
            ),
            discord.SelectOption(
                value="resgatar prêmio",
                label="Resgatar Prêmio",
                emoji="<:colorido_festa:1013536095717298186>",
            ),
            discord.SelectOption(
                value="parceria",
                label="Fazer Parceria",
                emoji="<:dinheiro:1058813330531291236>",
            ),
            discord.SelectOption(
                value="form staff",
                label="Form Staff",
                emoji="<:emoji_bdsm:1132367626115489852>",
            ),
            discord.SelectOption(
                value="report bug",
                label="Reportar Bug",
                emoji="<:urso_besta:983194182585823263>",
            ),
            discord.SelectOption(
                value="outra",
                label="Outra Opção",
                emoji="<:emoji_caio:1060460880162197546>",
            ),
        ]
        super().__init__(
            placeholder="Selecione uma opção...",
            options=options,
            custom_id="persistent_view:dropdown_help",
        )

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "duvidas":
            await interaction.response.send_message(
                f'{self.mensagens["1"]}',
                ephemeral=True,
                view=CreateTicket(self.mensagens["1"]),
            )
        elif self.values[0] == "denuncia":
            await interaction.response.send_message(
                f'{self.mensagens["2"]}',
                ephemeral=True,
                view=CreateTicket(self.mensagens["2"]),
            )
        elif self.values[0] == "apelo":
            await interaction.response.send_message(
                f'{self.mensagens["3"]}',
                ephemeral=True,
                view=CreateTicket(self.mensagens["3"]),
            )
        elif self.values[0] == "verificaçao":
            await interaction.response.send_message(
                f'{self.mensagens["4"]}', ephemeral=True, view=Verificacao()
            )
        elif self.values[0] == "comprar edp+":
            await interaction.response.send_message(
                f'{self.mensagens["5"]}',
                ephemeral=True,
                view=CreateTicket(self.mensagens["5"]),
            )
        elif self.values[0] == "resgatar prêmio":
            await interaction.response.send_message(
                f'{self.mensagens["6"]}',
                ephemeral=True,
                view=CreateTicket(self.mensagens["6"]),
            )
        elif self.values[0] == "parceria":
            await interaction.response.send_message(
                f'{self.mensagens["7"]}',
                ephemeral=True,
                view=CreateTicket(self.mensagens["7"]),
            )
        elif self.values[0] == "form staff":
            await interaction.response.send_message(
                f'{self.mensagens["8"]}',
                ephemeral=True,
                view=CreateTicket(self.mensagens["8"]),
            )
        elif self.values[0] == "report bug":
            await interaction.response.send_message(
                f'{self.mensagens["9"]}',
                ephemeral=True,
                view=CreateTicket(self.mensagens["9"]),
            )
        elif self.values[0] == "outra":
            await interaction.response.send_message(
                f'{self.mensagens["10"]}',
                ephemeral=True,
                view=CreateTicket(self.mensagens["10"]),
            )


class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Dropdown())


class CreateTicket(discord.ui.View):
    def __init__(self, msg):
        super().__init__(timeout=300)
        self.value = None
        self.msg = msg

    @discord.ui.button(
        label="Abrir Ticket", style=discord.ButtonStyle.blurple, emoji="➕"
    )
    async def confirm(
            self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.value = True
        self.stop()
        mod = interaction.guild.get_role(id_cargo_atendente)

        ticket = None
        for thread in interaction.channel.threads:
            if f"{interaction.user.id}" in thread.name:
                if thread.archived:
                    ticket = thread
                else:
                    await interaction.response.send_message(
                        "Você já tem um atendimento em andamento!",
                        ephemeral=True
                    )
                    return

        async for thread in interaction.channel.archived_threads(private=True):
            if f"{interaction.user.id}" in thread.name:
                if thread.archived:
                    ticket = thread
                else:
                    await interaction.response.send_message(
                        "Você já tem um atendimento em andamento!", view=None
                    )
                    return

        if ticket is not None:
            await ticket.edit(archived=False, locked=False)
            await ticket.edit(
                name=f"{interaction.user.name} ({interaction.user.id})",
                auto_archive_duration=10080,
                invitable=False,
            )
        else:
            ticket = await interaction.channel.create_thread(
                name=f"{interaction.user.name} ({interaction.user.id})",
                auto_archive_duration=10080,
            )
            await ticket.edit(invitable=False)

        await interaction.response.send_message(
            f"Criei um ticket para você! {ticket.mention}", ephemeral=True
        )
        await ticket.send(f"Mencionando staff: {mod.mention}")
        await asyncio.sleep(5)
        await ticket.purge(limit=1)
        await ticket.send(
            f"📩  **|** {interaction.user.mention} ticket criado!"
            f"\n{self.msg}\nApós a sua questão ser sanada, use `-fecharticket` "
            f"para encerrar o atendimento!"
        )


class Verificacao(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        self.value = None
        self.msg = {
            "1": 'Para se verificar como **Vendedor(a) Oficial** e poder anunciar venda de conteúdo +18, você pode escolher uma forma:\n\n- __Plaquinha__: Uma foto NSFW (parte íntima) com uma plaquinha escrito "EDP"!\n\n- __Call__: Uma call (15s) com a câmera aberta mostrando o rosto e acenando!\n\nApós realizar a verificação, você deve pagar pelo cargo, possuindo duas opções:\n\n**R$15/mês** para poder anunciar venda de pack no <#1093456891889336370>, <#1158729581956698114> e/ou privado dos membros.\n\n**R$25/mês** você adquire, além do benefício a cima, um canal exclusivo para postar seus conteúdos, com permissão de mencionar o ping de pack e enviar o link do seu servidor quantas vezes desejar.\n\nRealize o PIX nessa chave:\n```00c72e9d-9db8-41a2-aa2d-7b0ec27e4447``` ou pelo QR [Code](https://media.discordapp.net/attachments/1124725730807394317/1187450957114638356/Screenshot_20231221_144430_Chrome.jpg?ex=6596eee1&is=658479e1&hm=7091c13aefaeaa74c799c71a2c332c2752e401adc98525eaed00b80095683d6a&)\nFavor enviar o comprovante do PIX!!!',
            "2": 'Para se verificar para poder postar nos canais de **nudes**, você pode escolher uma forma:\n\n- __Selfie__: Envie uma foto sua segurando uma plaquinha escrito "EDP" + sua data de nascimento. Com isso, analisaremos se você possui +18 anos para liberar a permissão.\n\n- __RG__: Envie uma foto do seu RG ou outro documento oficial, mostrando seu nome e data de nascimento. Demais informações, se quiser, pode censurar.',
            "3": 'A verificação de interação é para liberar a permissão de postar no <#982805582924886056> e/ou <#982805666420887602>. Veja a instrução de cada canal:\n\n- __Fotinha__: Envie um vídeo de 5 segundos acenando para câmera e falando seu nick no Discord.\n\n- __Instagram__: Envie uma foto sua segurando uma plaquinha escrito "@seu_user_do_instagram" + print do seu perfil no Instagram.',
        }

    @discord.ui.button(
        label="Verificar Pack", style=discord.ButtonStyle.red, emoji="➕", row=1
    )
    async def confirm_pack(
            self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.value = True
        self.stop()
        mod = interaction.guild.get_role(id_cargo_atendente)

        ticket = None
        for thread in interaction.channel.threads:
            if f"{interaction.user.id}" in thread.name:
                if thread.archived:
                    ticket = thread
                else:
                    await interaction.response.send_message(
                        "Você já tem um atendimento em andamento!",
                        ephemeral=True
                    )
                    return

        async for thread in interaction.channel.archived_threads(private=True):
            if f"{interaction.user.id}" in thread.name:
                if thread.archived:
                    ticket = thread
                else:
                    await interaction.response.send_message(
                        "Você já tem um atendimento em andamento!", view=None
                    )
                    return

        if ticket is not None:
            await ticket.edit(archived=False, locked=False)
            await ticket.edit(
                name=f"{interaction.user.name} ({interaction.user.id})",
                auto_archive_duration=10080,
                invitable=False,
            )
        else:
            ticket = await interaction.channel.create_thread(
                name=f"{interaction.user.name} ({interaction.user.id})",
                auto_archive_duration=10080,
            )
            await ticket.edit(invitable=False)

        await interaction.response.send_message(
            f"Criei um ticket para você! {ticket.mention}",
            ephemeral=True,
        )
        await ticket.send(f"Mencionando staff: {mod.mention}")
        await asyncio.sleep(5)
        await ticket.purge(limit=1)
        await ticket.send(
            f"📩  **|** {interaction.user.mention} ticket criado!"
            f'\n\n\n{self.msg["1"]}\nApós a sua questão ser sanada, você pode '
            f"usar `-fecharticket` para encerrar o atendimento!"
        )

    @discord.ui.button(
        label="Verificar Idade", style=discord.ButtonStyle.green, emoji="➕",
        row=2
    )
    async def confirm_idade(
            self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.value = True
        self.stop()
        mod = interaction.guild.get_role(id_cargo_atendente)

        ticket = None
        for thread in interaction.channel.threads:
            if f"{interaction.user.id}" in thread.name:
                if thread.archived:
                    ticket = thread
                else:
                    await interaction.response.send_message(
                        "Você já tem um atendimento em andamento!",
                        ephemeral=True
                    )
                    return

        async for thread in interaction.channel.archived_threads(private=True):
            if f"{interaction.user.id}" in thread.name:
                if thread.archived:
                    ticket = thread
                else:
                    await interaction.response.send_message(
                        "Você já tem um atendimento em andamento!", view=None
                    )
                    return

        if ticket is not None:
            await ticket.edit(archived=False, locked=False)
            await ticket.edit(
                name=f"{interaction.user.name} ({interaction.user.id})",
                auto_archive_duration=10080,
                invitable=False,
            )
        else:
            ticket = await interaction.channel.create_thread(
                name=f"{interaction.user.name} ({interaction.user.id})",
                auto_archive_duration=10080,
            )
            await ticket.edit(invitable=False)

        await interaction.response.send_message(
            f"Criei um ticket para você! {ticket.mention}", ephemeral=True
        )
        await ticket.send(f"Mencionando staff: {mod.mention}")
        await asyncio.sleep(5)
        await ticket.purge(limit=1)
        await ticket.send(
            f"📩  **|** {interaction.user.mention} ticket criado!"
            f'\n{self.msg["2"]}\nApós a sua questão ser sanada, você pode usar '
            f"`-fecharticket` para encerrar o atendimento!"
        )

    @discord.ui.button(
        label="Verificar Interação", style=discord.ButtonStyle.gray, emoji="➕",
        row=3
    )
    async def confirm_interacao(
            self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.value = True
        self.stop()
        mod = interaction.guild.get_role(id_cargo_atendente)

        ticket = None
        for thread in interaction.channel.threads:
            if f"{interaction.user.id}" in thread.name:
                if thread.archived:
                    ticket = thread
                else:
                    await interaction.response.send_message(
                        "Você já tem um atendimento em andamento!",
                        ephemeral=True
                    )
                    return

        async for thread in interaction.channel.archived_threads(private=True):
            if f"{interaction.user.id}" in thread.name:
                if thread.archived:
                    ticket = thread
                else:
                    await interaction.response.send_message(
                        "Você já tem um atendimento em andamento!", view=None
                    )
                    return

        if ticket is not None:
            await ticket.edit(archived=False, locked=False)
            await ticket.edit(
                name=f"{interaction.user.name} ({interaction.user.id})",
                auto_archive_duration=10080,
                invitable=False,
            )
        else:
            ticket = await interaction.channel.create_thread(
                name=f"{interaction.user.name} ({interaction.user.id})",
                auto_archive_duration=10080,
            )
            await ticket.edit(invitable=False)
        await interaction.response.send_message(
            f"Criei um ticket para você! {ticket.mention}", ephemeral=True
        )
        await ticket.send(f"Mencionando staff: {mod.mention}")
        await asyncio.sleep(5)
        await ticket.purge(limit=1)

        await ticket.send(
            f"📩  **|** {interaction.user.mention} ticket criado!"
            f'\n{self.msg["3"]}\nApós a sua questão ser sanada, você pode usar '
            f"`-fecharticket` para encerrar o atendimento!"
        )


class AtendimentoCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='setup')
    @commands.has_permissions(manage_guild=True)
    async def setup(self, ctx):
        embed = discord.Embed(
            title="Central de Atendimento EDP ☎️",
            description="Nesse menu, você pode entrar em contato com a nossa "
                        "equipe de atendimento da Elite!\n\nPara evitar problemas, "
                        "leia as opções com atenção e lembre-se que ao criar um "
                        "Ticket fora do horário abaixo, é provável que demore "
                        "mais para ser atendido.\n\n**Horário de atendimento:**"
                        "\n- Segunda a sexta-feira: 08h às 22h\n- Final de semana"
                        " e feriado: 10h às 20h",
            color=discord.Color.red(),
        )

        embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/1100253073596764190/1179374529173270589/Screenshot_20231129_075105_Photos.jpg"
        )
        embed.set_image(
            url="https://media.discordapp.net/attachments/1124725730807394318/1187122761118777434/standard_8.gif"
        )

        await ctx.send(embed=embed, view=DropdownView())

    @commands.command(name="fecharticket")
    async def _fecharticket(self, ctx):
        mod = ctx.guild.get_role(id_cargo_atendente)

        if str(ctx.author.id) in ctx.channel.name or mod in ctx.author.roles:
            await ctx.send(
                f"O ticket foi arquivado por {ctx.author.mention}, "
                f"obrigado por entrar em contato!"
            )

            await ctx.channel.edit(locked=True)
            await asyncio.sleep(1)

            reacoes = ["😡", "😤", "🙂", "😄"]
            msg = await ctx.send(
                "Por favor, avalie seu atendimento\n"
                "😡 Experiência frustrante, atendimento precisa melhorar urgentemente.\n"
                "😤 Não muito satisfeito com o serviço prestado, há espaço para melhorias.\n"
                "🙂 Atendimento razoável, mas poderia ser mais eficiente.\n"
                "😄 Excelente atendimento! Satisfeito com a experiência proporcionada."
            )

            for reacao in reacoes:
                await msg.add_reaction(reacao)

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in reacoes

            try:
                reaction, _ = await client.wait_for(
                    "reaction_add", timeout=60.0, check=check
                )

                canal_avaliacoes = ctx.guild.get_channel(1195429851943948399)
                await canal_avaliacoes.send(
                    f"Avaliação de {ctx.author.mention}: {str(reaction.emoji)}"
                )
            except asyncio.TimeoutError:
                pass
            await ctx.channel.edit(archived=True)

        else:
            await ctx.send("Isso não pode ser feito aqui...")


async def setup(client):
    await client.add_cog(AtendimentoCog(client))
