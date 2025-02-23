import discord
from discord.ext import commands

import setting

logger = setting.logging.getLogger("bot")


def run():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")

        for cog_file in setting.COGS_DIR.glob("*.py"):
            if cog_file != "__init__.py":
                await bot.load_extension(f"cogs.{cog_file.name[:-3]}")


    @bot.command(aliases=['quit','sd'])
    @commands.has_permissions(administrator=True)
    async def shutdown(ctx):
        await ctx.send("Bot Shutdown.")
        await bot.close()
        print("Bot Shutdown")

    bot.run(setting.DISCORD_BOT_TOKEN,root_logger=True)

if __name__ == '__main__':
    run()




