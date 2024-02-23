import discord
from discord.ext import commands


class RolesManagement(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="addedp")
    @commands.has_guild_permissions(ban_members=True)
    async def addedp(self, ctx, membro: discord.Member):
        edp = ctx.guild.get_role(983142637492137985)
        if edp not in membro.roles:
            await membro.add_roles(edp)
            await ctx.send("Cargo setado em " + membro.mention)
        else:
            await ctx.send(f"{membro.mention} já tem esse cargo")

    @addedp.error
    async def addedp_error(self, ctx, error):
        error_messages = {
            commands.MissingPermissions: lambda
                e: "Você não tem permissão para usar este comando!",
            commands.MissingRequiredArgument: lambda
                e: "Opaaa, algo deu errado. Use o comando corretamente "
                   "`-addedp @membro`",
            commands.BadArgument: lambda
                e: "Hmmm, eu não consegui encontrar esse membro!",
        }

        for error_type, message_func in error_messages.items():
            if isinstance(error, error_type):
                await ctx.send(message_func(error) + " " + ctx.author.mention)
                break

    @commands.command(name="removeedp")
    @commands.has_guild_permissions(ban_members=True)
    async def removeedp(self, ctx, membro: discord.Member):
        edp = ctx.guild.get_role(983142637492137985)
        if edp in membro.roles:
            await membro.remove_roles(edp)
            await ctx.send(f"Cargo removido de {membro.mention}")
        else:
            await ctx.send(
                f"Ei meu chapa {ctx.author.mention}, esse carinha não tem a tag "
                f"edp, favor prestar mais atenção diabo"
            )

    @removeedp.error
    async def removeedp_error(self, ctx, error):
        error_messages = {
            commands.MissingPermissions: lambda
                e: "Você não tem permissão para usar este comando!",
            commands.MissingRequiredArgument: lambda
                e: "Opaaa, algo deu errado. Use o comando corretamente "
                   "`-removeedp @membro`",
            commands.BadArgument: lambda
                e: "Hmmm, eu não consegui encontrar esse membro!",
        }

        for error_type, message_func in error_messages.items():
            if isinstance(error, error_type):
                await ctx.send(message_func(error) + " " + ctx.author.mention)
                break


async def setup(client):
    await client.add_cog(RolesManagement(client))
