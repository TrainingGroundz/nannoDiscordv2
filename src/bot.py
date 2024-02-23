import asyncio
import difflib
import os
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
        await ctx.message.delete()

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
            await msg.delete()
        else:
            embed = discord.Embed(
                title='Erro ❌',
                description=f'Comando não encontrado',
                color=discord.Color.red()
            )
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(2)
            await msg.delete()


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
        await client.load_extension(f'cogs.{cog}')
        cog_name = cog.split('.')[-1]
        loaded_cogs.append(f'{cog_name.capitalize()} ✅')
    loaded_cogs_str = '\n'.join(loaded_cogs)
    print(f'Foram carregados:\n{loaded_cogs_str}')


client.run(os.getenv('TOKEN_BOT'))
