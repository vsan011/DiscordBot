import discord
from discord.ext import commands

import setting
from tts import TTS


class Voice(commands.Cog):
    vc = None
    """
        Voice Cog for turning your text to speech.
        :param bot: Discord bot
        """
    def __init__(self,bot):
        self.bot = bot


    @commands.command()
    async def join(self,ctx):
        channel = ctx.message.author.voice.channel
        if channel:
            self.vc = await channel.connect()
            await ctx.send(f"Joined {channel.name}")
            self.vc.play(discord.FFmpegPCMAudio(executable=setting.FFMPEG_EXE,
                                           source=f"{setting.AUDIO_DIR}/greeting/join.mp3"))
        else:
            await ctx.send(f"Please join a channel")

    @commands.command()
    async def play(self,ctx,*,text):
        vc = self.vc
        if vc is None:
            await ctx.send("Please join a channel")
            return
        if text:
            await ctx.message.delete()
            try:
                print(text)
                file_name =TTS.speak(text)
                vc.play(discord.FFmpegPCMAudio(executable=setting.FFMPEG_EXE,source=file_name))
            except Exception as e:
                print(f"Error occur : {e}")



async def setup(bot):
    await bot.add_cog(Voice(bot))


