from discord.ext.commands import Cog
from discord import Embed, Colour

from bot import Bot

from datetime import datetime

class NewPatch(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_connect(self) -> None:
        await self.check()
    
    @Cog.listener()
    async def on_resumed(self) -> None:
        await self.check()

    async def check(self) -> None:
        current_version = await self.bot.database.load("VERSION")
        system_version = self.bot.config.version

        if current_version != system_version:
            await self.push_version_change(current_version, system_version)
            await self.bot.database.dump("VERSION", system_version)
    
    async def push_version_change(self, old_version: int, new_version: int) -> None:
        embed = Embed(
            title = "Version Change Detected",
            colour = Colour.teal(),
            timestamp = datetime.utcnow()
        )
        embed.description = "Version **{}** → **{}**".format(old_version, new_version)
        embed.add_field(name = "Patch Note:", value="\n".join(self.bot.config.note))

        await self.bot.get_channel(797479575944167444).send(embed=embed)

def setup(bot: Bot) -> None:
    bot.add_cog(NewPatch(bot))