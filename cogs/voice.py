from imports import *


class VOICE(commands.Cog):
    def __init__(self, dottie):
        self.dottie = dottie


    @commands.command(aliases=["espacito"], pass_context=True)
    async def despacito(self, ctx):
        try:
            channel = ctx.message.author.voice.channel
            await channel.connect()
            for vc in self.dottie.voice_clients:
                if vc.guild == ctx.guild:
                    vc.play(discord.FFmpegOpusAudio("misc/assets/misc_audio_assets/Normal_Despacito.ogg"))
                    await ctx.send("***```css\n🥁 Embrace my [DESPACITO!]```***")
                    return
        except:
            await ctx.send("How are you meant to hear my *100% normal Despacito* from outside of a Voice Channel? Hop in one first!")


def setup(dottie):
    dottie.add_cog(VOICE(dottie))
