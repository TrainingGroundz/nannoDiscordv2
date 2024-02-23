import discord
from discord.ext import commands


class AvatarCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="av")
    async def __avatar(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(
            title=f"Avatar de {member.display_name} 😎",
            color=0xFF0703,
        )
        embed.set_image(url=member.avatar.url)

        await ctx.send(embed=embed)

    @commands.command(name="bot_avatar")
    @commands.has_guild_permissions(administrator=True)
    async def addavatar(self, ctx: commands.Context,
                        attachment: discord.Attachment):

        data = await attachment.read()
        await self.client.user.edit(avatar=data)
        await ctx.send(f"Avatar atualizado\nenviado por {ctx.author.mention}!")

    @addavatar.error
    async def addavatar(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Parece que você não tem permissões suficientes!")
        elif isinstance(error, commands.MissingRequiredAttachment):
            await ctx.send(
                f"Olá {ctx.author.mention}, por favor envie o avatar "
                f"que deseja usar!")


async def setup(client):
    await client.add_cog(AvatarCog(client))
