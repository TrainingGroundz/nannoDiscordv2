import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

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

    # async def setup_hook(self):
    #     self.add_view(DropdownView()


client = Client()

cogs_list = [
    'games.numero',
    'games.sequestro'
]


async def load_cogs():
    loaded_cogs = []
    for cog in cogs_list:
        await client.load_extension(f'cogs.{cog}')
        cog_name = cog.split('.')[-1]
        loaded_cogs.append(f'{cog_name.capitalize()} ✅')
    loaded_cogs_str = '\n'.join(loaded_cogs)
    print(f'Os seguintes comandos foram carregados:\n{loaded_cogs_str}')



client.run(os.getenv('TOKEN_BOT'))
