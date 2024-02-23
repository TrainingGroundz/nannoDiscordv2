import asyncio
import difflib
import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
from src.cogs.moderation import atendimento

DropdownView = atendimento.DropdownView
load_dotenv()


class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='-', intents=discord.Intents.all())

    async def on_ready(self):
        activity = discord.Game(name="com ELITE DAS PUTARIAS", type=3)
        await self.change_presence(status=discord.Status.online,
                                   activity=activity)
        await load_cogs()
        print(f'(＾◡＾)っ Sou o {self.user.name} e acabei de me conectar')

    async def setup_hook(self):
        self.add_view(DropdownView())

    async def on_command_error(self, ctx, error):
        try:
            await ctx.message.delete()
        except discord.errors.NotFound:
            pass

        def similar(a, b):
            return difflib.SequenceMatcher(None, a, b).ratio()

        command_parts = ctx.message.content.split()
        cmd = command_parts[0][1:]

        if len(command_parts) > 1:
            full_command = ' '.join(command_parts[1:])
        else:
            full_command = cmd

        command_list = [command.name for command in self.commands]

        similar_commands = difflib.get_close_matches(full_command, command_list,
                                                     cutoff=0.5)

        manual_similar_commands = [command for command in command_list if
                                   similar(full_command, command) > 0.5]

        all_similar_commands = set(similar_commands + manual_similar_commands)

        if all_similar_commands:
            suggestions = '`\n➡️ `'.join(all_similar_commands)
            embed = discord.Embed(
                title='Erro ❌',
                description=f'Comando não encontrado. Você quis dizer:\n'
                            f'\n➡️ `{suggestions}`',
                color=discord.Colour.red()
            )
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            try:
                await msg.delete()
            except discord.errors.NotFound:
                pass
        else:
            pass

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.channel.id == 1093456891889336370:
            if message.mentions:
                await message.delete()
                return

            if message.reference:
                await message.delete()
                return

        if isinstance(message.author, discord.Member):
            cargo_id = 983012540663599114
            messages_list_a = [
                'Ei, parece que encontrei um chifrudo <:anime_apontando:1058639652581539880> ',
                'Esse daí já levou mais de um chifre <:palavra_corno:1013521829916332092> ',
                'Desça daí seu corno, desça daí <:frase_gado_dms:983202218285101106>'
            ]
            messages_list_b = [
                'Ei, parece que encontrei uma chifruda <:anime_apontando:1058639652581539880> ',
                'Essa daí já levou mais de um chifre <:palavra_corno:1013521829916332092> ',
                'Desça daí sua corna, desça daí <:frase_gado_dms:983202218285101106>'
            ]
            messages_list_c = [
                'Essa coca aí é fanta, hein 🏳️‍🌈 ',
                'Gosta de dar a bundinha pro amigo <:palavra_gay:983202213717495869>',
                'Paga de hétero, mas adora uma brotheragem <a:palavra_gay:1058816734196416532>'
            ]

            if isinstance(message.author.roles, list):
                if any(role.id == cargo_id for role in message.author.roles):
                    if 'corno' in message.content.lower() and message.mentions:
                        mentioned_member = message.mentions[0]
                        await message.channel.send(
                            f'{random.choice(messages_list_a)}'
                            f' {mentioned_member.mention}')
                        return
                    elif 'corna' in message.content.lower() and message.mentions:
                        mentioned_member = message.mentions[0]
                        await message.channel.send(
                            f'{random.choice(messages_list_b)}'
                            f' {mentioned_member.mention}')
                        return
                    elif 'gay' in message.content.lower() and message.mentions:
                        mentioned_member = message.mentions[0]
                        await message.channel.send(
                            f'{random.choice(messages_list_c)}'
                            f' {mentioned_member.mention}')
                        return
                    else:
                        await self.process_commands(message)
                        return

        await self.process_commands(message)


client = Client()

cogs_list = [
    'games.numero',
    'games.sequestro',
    'moderation.atendimento',
    'moderation.punicoes',
    'moderation.clear',
    'moderation.roles',
    'economy.economia',
    'util.avatar',
    'interaction.echo'
]


async def load_cogs():
    loaded_cogs = []
    for cog in cogs_list:
        await client.load_extension(f'src.cogs.{cog}')
        cog_name = cog.split('.')[-1]
        loaded_cogs.append(f'{cog_name.capitalize()} ✅')
    loaded_cogs_str = '\n'.join(loaded_cogs)
    print(f'Foram carregados:\n{loaded_cogs_str}')


client.run(os.getenv('TOKEN_BOT'))
