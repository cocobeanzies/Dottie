from imports import *
from bot import print2
from bot import log_update


# psutil.Process() is just Task Manager 2.0
TaskManager2 = psutil.Process()

def get_cpu_percent():
    futs = [create_future_ex(child.cpu_percent) for child in TaskManager2.children(True)]
    cpu = TaskManager2.cpu_percent()
    cpu += sum(fut.result() for fut in futs)
    return cpu

def get_memory_percent():
    futs = [create_future_ex(child.memory_percent) for child in TaskManager2.children(True)]
    cpu = TaskManager2.memory_percent()
    cpu += sum(fut.result() for fut in futs)
    return cpu

def get_code_length():
    total = 0
    for filename in os.listdir():
        if filename.endswith(".py"):
            with open(filename, "r", encoding="utf-8") as f:
                total += f.read().count("\n") + 1
    for filename in os.listdir("json/"):
        if filename.endswith(".json"):
            with open("json/" + filename, "r", encoding="utf-8") as f:
                total += f.read().count("\n") + 1
    for filename in os.listdir("cogs/"):
        if filename.endswith(".py"):
            with open("cogs/" + filename, "r", encoding="utf-8") as f:
                total += f.read().count("\n") + 1
        return total

def get_command_count():
    dottie_commands = len(set(dottie.all_commands.values()))
    return dottie_commands + 16

create_future_ex(get_cpu_percent)


class GENERAL(commands.Cog):
    def __init__(self, dottie):
        self.dottie = dottie


    @commands.command()
    async def help(self, ctx):
        home = discord.Embed(colour=discord.Colour(pink_embed), timestamp=ctx.message.created_at)
        home.set_author(name="🐾 Help List 🌨️", url="https://github.com/smudgedpasta/Dottie/wiki", icon_url=self.dottie.user.avatar_url_as(format="png", size=4096))
        home.description = "*I think I need heeelp, I'm drowning in myseeelf* 🎵"
        home.set_image(url="https://cdn.discordapp.com/attachments/683233571405561876/746281046231875594/image0.png")
        home.set_footer(icon_url=ctx.author.avatar_url_as(format="png", size=4096), text="Click the reactions to scroll through the pages!")

        info = discord.Embed(colour=discord.Colour(pink_embed), timestamp=ctx.message.created_at)
        info.set_author(name="🐾 First, a few things... 🌨️", url="https://github.com/smudgedpasta/Dottie/wiki", icon_url=self.dottie.user.avatar_url_as(format="png", size=4096))
        info.description = f"""```🔸 What permissions does {self.dottie.user.name} need?```\nReally the only additional permissions I need from the default are `Manage Messages` if you don't wish to use moderation commands. This is because commands such as `{PREFIX[0]}say` can delete the original message afterwards! But you can just give me admin if that's easier.\n
```🔸 Do I need to @ myself?```\nLets say you are using `{PREFIX[0]}info`. If you want to see your own, just send it by itself!\n
```🔸 Are commands case sensitive?```\nNope! Using `{PREFIX[0]}hElLo` would work just the same as `{PREFIX[0]}hello`.\n
```🔸 Does {PREFIX[0].upper()} work?```\nYep! Just like commands, the prefix is case insensitive!\n
```🔸 What permissions are required to use moderation commands?```\nAt the moment, you have to be an admin!\n
```🔸 How do I seperate my sentences?```\nLet's suppose you're using {PREFIX[0]}ship. Normally, I would work like this: `{PREFIX[0]}ship Smudge Txin`. If you want me to read the whole sentence, put quotes around it! For example: `{PREFIX[0]}ship \"My sleeping routine\" School`. These all go for any command!\n
```🔸 How do I search for users?```\nYou don't have to @ them! Lets say you are using {PREFIX[0]}info, you can write the command like this: `{PREFIX[0]}info smudge` and it'll still work to finding `smudgedpasta`, etc! If they are not in the server, you can use their user ID to still find them! If they are not in *this* server but *do* share another server with me, you can supply their full Discord tag! For example: `{PREFIX[0]}info smudgedpasta#6605`\n
```🔸 Do commands work in DM's?```\nSome do! Some may error, however.\n
```🔸 What's up with the changing statuses?```\nWhenever anyone uses my commands, I will change from idle to online for a few seconds!\n
```🔸 What do I do if I get an error?```\nFirstly, make sure you are using the command correctly. My lead programmer is <@530781444742578188>, and <@201548633244565504> wrote my more complicated features, so if you're having any issues, let either of them know and they'll get on it!\n
```🔸 What are "Cheesecake", "Kittens" and "Puppies" on {PREFIX[0]}info?```\nThese are prizes you can win on some of {self.dottie.user.name}'s \"fun\" commands! \"Cheesecake\" are won from `{PREFIX[0]}quiz`, \"Kittens\" are won from `{PREFIX[0]}snake` and \"Puppies\" are won from successfully filling the entire board in `{PREFIX[0]}snake`!
"""
        info.set_footer(icon_url=ctx.author.avatar_url_as(format="png", size=4096), text="Click 🔻 to see my commands!")
        
        moderation = discord.Embed(colour=discord.Colour(pink_embed))
        moderation.set_author(name="⚔️ MODERATION ⚔️", url="https://github.com/smudgedpasta/Dottie/wiki", icon_url=self.dottie.user.avatar_url_as(format="png", size=4096))
        moderation.set_footer(text="Click 🔺 to go back to info, click 🔻 to see GENERAL commands!")
        moderation.description = """***levels_remove***\n**```fix\nAliases: levels_d```**\n*```Prevents level-up embeds from posting in the server.```*
***levels_add***\n**```fix\nAliases: levels_e```**\n*```If level-up embeds were disabled, this re-enables them.```*
***topicloop_add***\n**```fix\nAliases: topicloop_e```**\n*```Enables the bot to ask a question or give a random fact every 3 hours to spice up your server activity a bit!```*
***topicloop_remove***\n**```Aliases: topicloop_d```**\n*```Disables the 3 hourly spam of questions or facts.```*
***purge***\n*```Clears inputted message count, not counting the command message.```*
***ban***\n*```Bans a user the same way as kick.```*
***unban***\n*```Unbans a user by typing their username and discriminator. (Example: Dottie#7157)```*
***kick***\n*```Kicks a user from the server, either by mentioning or stating their username.```*
"""

        general = discord.Embed(colour=discord.Colour(pink_embed))
        general.set_author(name="🤍 GENERAL 🤍", url="https://github.com/smudgedpasta/Dottie/wiki", icon_url=self.dottie.user.avatar_url_as(format="png", size=4096))
        general.set_footer(text="Click 🔺 to go back to MODERATION, click 🔻 to see FUN commands!")
        general.description = f"""***help***\n*```Legends say you've found this command already. 👀```*
***hello***\n**```fix\nAliases: "hemlo", "hoi"```**\n*```I will greet you back!```*
***profile***\n**```fix\nAliases: userinfo, info, stats, userstats```**\n*```Views the profile of a provided user!```*
***level***\n**```fix\nAliases: pokémon, pokemon```**\n*```Shows the current level and experience of a provided user!```*
***source***\n**```fix\nAliases: link, invite```**\n*```Sends a link to my source code and Discord invite!```*
***random***\n*```Takes all arguments you've provided and chooses one at random!```*
***note***\n*```Adds a note to your personal list of notes- helpful for a to-do list!```*
***view_notes***\n**```fix\nAliases: notes```**\n*```Views your list of notes! You cannot search for other's notes, so if you intend to keep them private, use the command in DM's!```*
***delete_note***\n**```fix\nAliases: trash```**\n*```Deletes a note from your list, specified by its number. Example: {PREFIX[0]}delete_note 5```*
***edit_note***\n**```fix\nAliases: edit```**\n*```Appends something new to a specified note number! Example: {PREFIX[0]}edit_note 5```*
***wordcount***\n**```fix\nAliases: charcount, charactercount, wc, cc```**\n*```I will ask for some text. Post it afterwards and I'll tell you the word and character count!```*
***loop***\n*```Repeats an inputted command a specified amount of times! Example: {PREFIX[0]}loop 5 {PREFIX[0]}hello```*
***nitro***\n*```My creator has been kind enough to bestow free Discord Nitro to whomever uses this command, RIP her credit card!```*
***ping***\n*```Returns some technical information.```*
***avatar***\n**```fix\nAliases: icon```**\n*```Sends an image of yours or someone else's Discord avatar!```*
***quote***\n*```Pulls a platonic-friendly quote regarding long-distance relationships with people.```*
"""

        fun = discord.Embed(colour=discord.Colour(pink_embed))
        fun.set_author(name="🥖 FUN 🥖", url="https://github.com/smudgedpasta/Dottie/wiki", icon_url=self.dottie.user.avatar_url_as(format="png", size=4096))
        fun.set_footer(text="Click 🔺 to go back to GENERAL, click 🔻 to see IMAGE commands!")
        fun.description = """***AskDottie***\n**```fix\nAliases: ask, 8ball```**\n*```Ask me anything, I'll give a random answer!```*
***rate***\n*```Give me anything and I'll give it a rating!```*
***topic***\n*```I will ask a random question or state a random fact- Like topicloop but less spammy!```*
***matchmaking***\n**```fix\nAliases: ship, love```**\n*```Ship two people/characters of your choosing!```*
***snake***\n**```fix\nAliases: snail```**\n*```Plays a real-time, in-Discord game of snake!```*
***numberguess***\n**```fix\nAliases: quiz```**\n*```A "guess-the-number" guessing game!```*
***rps***\n**```fix\nAliases: rockpaperscissors, rock_paper_scissors```**\n*```Plays the game "Rock Paper Scissors"!```*
***speak***\n**```fix\nAliases: say```**\n*```Make me say something, anything, and I'll repeat! Nobody will know it was you!```*
***heart***\n*```Use this with two emojis, and I'll make them a heart!```*
***pyramid***\n*```Tell me to build a pyramid with a height of your choosing!```*
***useless***\n**```fix\nAliases: annoying, name, myname```**\n*```Just a useless command, I'm sure it's nothing to worry about.```*
***cha_cha_slide***\n**```fix\nAliases: chachaslide, ccs```**\n*```This is something new, the Casper Slide part 2!```*
"""
        image = discord.Embed(colour=discord.Colour(pink_embed))
        image.set_author(name="🖼️ IMAGE 🖼️", url="https://github.com/smudgedpasta/Dottie/wiki", icon_url=self.dottie.user.avatar_url_as(format="png", size=4096))
        image.set_footer(text="Click 🔺 to go back to FUN, click 🔻 to see VOICE commands!")
        image.description = f"""***letmeoutroaring***\n**```fix\nAliases: lmor```**\n*```Allows you to select between various different types of content for {', '.join(str(dottie.get_user(u))[:-5] for u in OWNERS[:-1])}'s comic, Let Me Out Roaring!```*
***hug***\n**```fix\nAliases: nuzzle, cuddle```**\n*```Hugs you, another user, or a provided image!```*
***photo***\n*```Pulls a random image of me!```*
***nsfw_photo***\n**```css\n[NSFW CHANNEL ONLY]```**\n*```Pulls a random image of me, but be warned, they are gore.```*
***smudgin***\n**```fix\nAliases: smudge, txin, smudgetxin, txinsmudge, critter_cuddle, crittercuddle```**\n*```Pulls a random image of {', '.join(str(dottie.get_user(u))[:-5] for u in OWNERS[:-1])} and {str(dottie.get_user(OWNERS[-1]))[:-5]}!```*
***art***\n*```Takes the most recent image in a channel and only states the truth!```*
***http_cats***\n**```fix\nAliases: cats, http```**\n*```Pulls a HTTP status code with a funny cat picture and command_related caption!```*
***http_list***\n**```fix\nAliases: cats_list```**\n*```Want to see all the {PREFIX[0]}http_cats status codes? That's what this command is for!```*
***inspiro***\n**```css\n[NSFW CHANNEL ONLY]```**\n*```Some quotes contain references to sex; pulls a random funny quote from https://inspirobot.me/```*
***marble_fox***\n**```fix\nAliases: marble```**\n*```Sends a random image of a marble fox!```*
***seal***\n**```fix\nAliases: sea_doggo, seals```**\n*```Sends a random image of a seal!```*
***dog***\n**```fix\nAliases: og, doggo, puppo```**\n*```Sends a random image of a dog!```*
***fox***\n*```Sends a random image of any kind of fox!```*
***muffin***\n**```fix\nAliases: muffins```**\n*```Sends a random image of a muffin!```*
***ab***\n**```fix\nAliases: dab```**\n*```ab will spell out {PREFIX[0]}ab with my prefix, so I'll dab!```*
***how***\n*```How.gif, that is all.```*
"""

        voice = discord.Embed(colour=discord.Colour(pink_embed))
        try:
            voice.set_author(name="🎧 VOICE 🎧", url="https://github.com/thomas-xin/Miza/wiki/Commands", icon_url=self.dottie.get_user(668999031359537205).avatar_url_as(format="png", size=4096))
        except:
            voice.set_author(name="🎧 VOICE 🎧", url="https://github.com/thomas-xin/Miza/wiki/Commands", icon_url=self.dottie.user.avatar_url_as(format="png", size=4096))
        voice.set_footer(text="Click 🔺 to go back to IMAGE, click 🔻 to see more VOICE commands!")
        voice.description = """***queue***\n**```fix\nAliases: ▶️, p, q, play, enqueue```**\n*```Shows the music queue, or plays a song in voice.```*
***playlist***\n**```fix\nAliases: defaultplaylist, pl, playlist```**\n*```Shows, appends, or removes from the default playlist.```*
***connect***\n**```fix\nAliases: 📲, 🎤, 🎵, 🎶, 📴, 📛, summon, join, dc, disconnect, leave, move, reconnect```**\n*```Summons the bot into a voice channel.```*
***skip***\n**```fix\nAliases: ⏭, 🚫, s, sk, cq, remove, rem, clearqueue, clear```**\n*```Removes an entry or range of entries from the voice channel queue.```*
***pause***\n**```fix\nAliases: ⏸️, ⏯️, resume, unpause, stop```**\n*```Pauses, stops, or resumes audio playing.```*
***seek***\n**```fix\nAliases: ↔️, replay```**\n*```Seeks to a position in the current audio file.```*
***dump***\n**```fix\nAliases: save```**\n*```Saves or loads the currently playing audio queue state.```*
***audiosettings***\n**```fix\nAliases: volume, speed, pitch, pan, bassboost, reverb, compressor, chorus, nightcore, resample, bitrate, loopqueue, repeat, shufflequeue, quiet, stay, reset```**\n*```Changes the current audio settings for this server.```*
***rotate***\n**```fix\nAliases: 🔄, jump```**\n*```Rotates the queue to the left by a certain amount of steps.```*
"""

        voice2 = discord.Embed(colour=discord.Colour(pink_embed))
        voice2.set_author(name="🎧 VOICE 🎧", url="https://github.com/thomas-xin/Miza/wiki/Commands", icon_url=self.dottie.get_user(668999031359537205).avatar_url_as(format="png", size=4096))
        voice2.set_footer(text="Click 🔺 to go back to previous VOICE commands!")
        voice2.description = f"""***shuffle***\n**```fix\nAliases: 🔀```**\n*```Shuffles the audio queue.```*
***reverse***\n*```Reverses the audio queue direction.```*
***unmuteall***\n*```Disables server mute/deafen for all members.```*
***voicenuke***\n**```fix\nAliases: ☢️```**\n*```Removes all users from voice channels in the current server.```*
***radio***\n**```fix\nAliases: fm```**\n*```Searches for a radio station livestream on http://worldradiomap.com that can be played on {self.dottie.user.name}.```*
***player***\n**```fix\nAliases: np, nowplaying, playing```**\n*```Creates an auto-updating virtual audio player for the current server.```*
***lyrics***\n**```fix\nAliases: songlyrics```**\n*```Searches genius.com for lyrics of a song.```*
***download***\n**```fix\nAliases: 📥, search, ytdl, youtube_dl, af, audiofilter, trim, convertorg, org2xm, convert```**\n*```Searches and/or downloads a song from a YouTube/SoundCloud query or audio file link.```*
***despacito***\n**```fix\nAliases: espacito```**\n*```Plays a totally normal version of Despacito!```*
"""
        
        pages = [home, info, moderation, general, fun, image]
        if "MIZA" in GLOBALS:
            pages.extend((voice, voice2))
        message = await ctx.send(embed=home)

        await message.add_reaction("🔺")
        await message.add_reaction("🔻")

        def user_check(reaction, user):
            if reaction.message.id == message.id:
                if user.id == ctx.author.id or user.id in OWNERS:
                    return True
                if user.id != self.dottie.user.id:
                    guild = reaction.message.guild
                    if guild is not None:
                        member = guild.get_member(user.id)
                        if member is not None:
                            if member.guild_permissions.administrator:
                                return True
    
        async def page_reaction_listener(page, event_type="add"):
            while True:
                react = await self.dottie.wait_for(f"reaction_{event_type}", check=user_check)
                emoji = str(react[0])
                if emoji == "🔺" and page[0] > 0:
                    page[0] -= 1
                    await message.edit(embed=pages[page[0]])
                if emoji == "🔻" and page[0] < len(pages) - 1:
                    page[0] += 1
                    await message.edit(embed=pages[page[0]])
        page = [0]
        create_task(page_reaction_listener(page, "add"))
        create_task(page_reaction_listener(page, "remove"))


    @commands.command(aliases=["hi", "hemlo", "henlo", "hoi"])
    async def hello(self, ctx):
        await ctx.send(f"Hello, {ctx.author.display_name}! {get_random_emoji()}")


    @commands.command(aliases=["userinfo", "info", "stats", "userstats"])
    async def profile(self, ctx):
        spl = ctx.message.content.split(None, 1)
        if len(spl) > 1:
            try:
                member = await self.dottie.find_user(spl[-1], guild=ctx.guild)
            except:
                print(traceback.format_exc(), end="")
                return await ctx.send(f"I can't find the user \"{spl[-1]}\"! Please specify a more specific identifier such a username#discriminator, or a user ID.")
        else:
            member = ctx.author
        try:
            Roles = member.roles[1:]
        except AttributeError:
            Roles = None

        if not os.path.exists("database/prizes.json"):
            with open("database/prizes.json", "w") as f:
                f.write("{}")
                pass
        with open("database/prizes.json", "r") as f:
            prize_userbase = json.load(f)
            if member.id == self.dottie.user.id:
                cheesecake = "♾"
                kittens = "♾"
                puppies = "♾"
            else:
                try:
                    cheesecake = prize_userbase[str(member.id)][0]
                    kittens = prize_userbase[str(member.id)][2]
                    puppies = prize_userbase[str(member.id)][1]
                except:
                    cheesecake = 0
                    kittens = 0
                    puppies = 0
        
        sus = {"".join(c.upper() if 1 << i & z else c.lower() for i, c in enumerate(str(self.dottie.user.name))) for z in range(2 ** len(self.dottie.user.name))}

        embed = discord.Embed(colour=member.colour, timestamp=ctx.message.created_at)
        if member.id in OWNERS:
            embed.set_author(name=f"Hey there my owner, {member.name}! Let's see your info! 🤍", icon_url=member.avatar_url_as(format="png", size=4096))
        elif member.id == self.dottie.user.id:
            embed.set_author(name=f"Hey, isn't that me? {self.dottie.user.name}! 🎉", icon_url=member.avatar_url_as(format="png", size=4096))
        elif member.display_name in sus or any(role.name in sus for role in member.roles):
            embed.set_author(name=f"Oh, I see what you're trying to do, impostor... 👺", icon_url=member.avatar_url_as(format="png", size=4096))
        else:
            embed.set_author(name=f"Snap! Let's see your info, {member.name}! 👀", icon_url=member.avatar_url_as(format="png", size=4096))
        embed.set_thumbnail(url=member.avatar_url_as(format="png", size=4096))
        embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png", size=4096), text=f"Command run by {ctx.author.display_name}")

        if member.display_name in sus:
            embed.description = "```ini\n👺 Nobody is falling for your name being [" + member.display_name + "], sweetheart... 👺```"
        else:
            embed.description = "```ini\n🤍 Here they like to call you [" + member.display_name + "], what a nice nickname! 🤍```"

        embed.add_field(name="Cheesecake", value=f"x{str(cheesecake)} <:cheesecake:881133619983302718>")
        embed.add_field(name="Kittens", value=f"x{str(kittens)} <:kitten:881205443320479754>")
        embed.add_field(name="Puppies", value=f"x{str(puppies)} <:puppy:881202126070624286>")
        embed.add_field(name="Too lazy for developer mode? Here's the ID:", value=str(member.id) + " ✌️")
        embed.add_field(name="You fell into Discord addiction on:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M, %p UTC"))
        if member.bot == True:
            embed.add_field(name="CAPTCHA TEST, are you a robot?", value="True! You failed the test, you robot! 🤖")
        else:
            embed.add_field(name="CAPTCHA TEST, are you a robot?", value="False! I'll let this one slide, mortal. 🔪")
        if getattr(member, "joined_at", None):
            embed.add_field(name="You stumbled into this server on:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M, %p UTC"))
        if Roles is not None:
            if len(Roles) == 0:
                embed.add_field(name="Here you have earnt these ranks in 0 roles- wait a minute...", value="\u200b")
                embed.add_field(name="... Your highest rank being nothing, obviously. 😔", value="\u200b")
            else:
                if any(role.name in sus for role in member.roles):
                    embed.add_field(name=f"You know which of these {len(Roles)} roles is fake... 👺", value=" ".join([role.mention for role in Roles]))
                    embed.add_field(name="... With your highest rank being:", value="Obviously not the role with my name.")
                else:
                    embed.add_field(name=f"Here you have earnt these ranks in {len(Roles)} roles! ⚔️", value=" ".join([role.mention for role in Roles]))
                    embed.add_field(name="... With your highest rank being:", value=member.top_role.mention)

        await ctx.send(embed=embed)


    @commands.command(aliases=["link", "invite"])
    async def source(self, ctx):
        embed = discord.Embed(colour=discord.Colour(pink_embed))
        embed.description = f"[My GitHub](https://github.com/smudgedpasta/Dottie)\n[My Invite]({INVITE})"
        embed.set_author(name=self.dottie.user.name, icon_url=self.dottie.user.avatar_url_as(format="png", size=4096))
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/751513839169831083/793587710391746590/768px-Python-logo-notext.png")
        await ctx.send(embed=embed)


    @commands.command()
    async def random(self, ctx, *args):
        embed = discord.Embed(colour=discord.Colour(pink_embed), timestamp=ctx.message.created_at)
        embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png", size=4096), text=f"Randomized by {ctx.author.display_name}")
        embed.description = "```" + random.choice(["ini", "css"]) + f"\n🎉 [{random.choice(args)}] 🎉```"
        await ctx.send("🥁 ***Your random selection is...***", embed=embed)


    @commands.command()
    async def note(self, ctx, *args):
        note = ctx.message.content[7:]
        try:
            with open("database/notes.json", "rb") as f:
                note_userbase = json.load(f)
        except:
            note_userbase = {}
        try:
            note_userbase[f"{ctx.author.id}"].append(note)
        except KeyError:
            note_userbase[f"{ctx.author.id}"] = [note]
        with open("database/notes.json", "w") as f:
            json.dump(note_userbase, f, indent=4)
        await ctx.send(":white_heart: Note taken!")


    @commands.command(aliases=["notes"])
    async def view_notes(self, ctx):
        try:
            with open("database/notes.json", "r") as f:
                user_notes = json.load(f)[str(ctx.author.id)]
        except:
            user_notes = ["**No notes!**"]
        embed = discord.Embed(colour=ctx.author.colour, timestamp=ctx.message.created_at)
        embed.set_author(name=f"{ctx.author.display_name}'s notebook! 📖", icon_url=ctx.author.avatar_url_as(format="png", size=4096))
        embed.description = "\n".join(f"**{i + 1}.** {line}" for i, line in enumerate(user_notes))
        embed.set_footer(icon_url=self.dottie.user.avatar_url_as(format="png", size=4096), text="Be careful when using this command publicly!")
        await ctx.send(embed=embed)


    @commands.command(aliases=["trash"])
    async def delete_note(self, ctx, num):
        with open("database/notes.json", "r") as f:
            userbase = json.load(f)
        try:
            userbase[str(ctx.author.id)].pop(int(num)-1)
        except:
            return await ctx.send(f":upside_down: Hey, you don't have a note number {num}!")
        if not userbase[str(ctx.author.id)]:
            userbase.pop(str(ctx.author.id))
        with open("database/notes.json", "w") as f:
            json.dump(userbase, f, indent=4)
        await ctx.send(f":black_heart: Note number {num} has been removed!")


    @commands.command(aliases=["edit"])
    async def edit_note(self, ctx, num):
        with open("database/notes.json", "r") as f:
            userbase = json.load(f)
        temp = userbase[str(ctx.author.id)][int(num)-1]
        await ctx.send(f"Would you like to add something underneath or alongside note number {num}? (Reply \"**under**\" for underneath, or \"**side**\" for alongside!)")
        choice = await self.dottie.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
        await ctx.send(f"Now please reply with what you'd like to add to note number {num}!")
        edit = await self.dottie.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
        if choice.content.lower() == "under":
            userbase[str(ctx.author.id)][int(num)-1] = temp + "\n" + str(edit.content)
        elif choice.content.lower() == "side":
            userbase[str(ctx.author.id)][int(num)-1] = temp + ", " + str(edit.content)
        else:
            return await ctx.send("<a:THONKSUN:868210645672288286> Where the heck do I put this- Please follow the instructions!")
        with open("database/notes.json", "w") as f:
            json.dump(userbase, f, indent=4)
        await ctx.send("✏ Note successfully edited!")


    @commands.command(aliases=["charcount", "charactercount", "wc", "cc"])
    async def wordcount(self, ctx):
        await ctx.send("Please post the text you would like the word and character count for! :pen_fountain:")
        message = await self.dottie.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
        wc = message.content.split()
        cc = message.content.strip()
        embed = discord.Embed(colour=discord.Colour(pink_embed), timestamp=ctx.message.created_at)
        embed.description = "```" + random.choice(["ini", "css"]) + f"\n𝒲𝑜𝓇𝒹 𝒸𝑜𝓊𝓃𝓉 𝒾𝓈: [{len(wc)}]❕\n𝒞𝒽𝒶𝓇𝒶𝒸𝓉𝑒𝓇 𝒸𝑜𝓊𝓃𝓉 𝒾𝓈: [{len(cc)}]❕```"
        embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png", size=4096), text=f"Checked by {ctx.author.display_name}")
        await ctx.send(embed=embed)


    @commands.command()
    async def loop(self, ctx):
        message = ctx.message
        content = message.content
        _, count, command = content.split(None, 2)
        fake_message = copy.copy(message)
        fake_message.content = command
        for i in range(int(count)):
            if int(count) > 50:
                await ctx.send("Yeah no, let's not go *too* spammy! :sweat_drops:")
                break
            else:
                new_ctx = await self.dottie.get_context(fake_message)
                await self.dottie.invoke(new_ctx)

    
    @commands.command()
    async def nitro(self, ctx, pass_context=True):
        sliding_into_your_dms = ctx.author.dm_channel
        if sliding_into_your_dms is None:
            sliding_into_your_dms = await ctx.author.create_dm()
        if hasattr(ctx.channel, "guild"):
            await ctx.send(f"{ctx.author.mention}, I've sent you your DM! (If you haven't received it, make sure server member DM's are enabled! Your gift awaits!) 🥳")
        await sliding_into_your_dms.send(f"Hi, {ctx.author.name}! Thank you for destroying my creator's wallet. To get started, please watch the following tutorial and follow it carefully! :blush:\n\nhttps://cdn.discordapp.com/attachments/687567100767633432/886664366815068230/Dotties_Nitro_Tutorial.mp4")
        await self.dottie.wait_for("message", check=lambda m: m.channel.id == sliding_into_your_dms.id)
        await sliding_into_your_dms.send(random.choice(["😈", "😇", "😚"]))
        

    @commands.command()
    async def ping(self, ctx):
        cpu = await create_future(get_cpu_percent)
        memory = await create_future(get_memory_percent)
        TechyInfo = {
            "CPU": f"[{cpu / psutil.cpu_count()}%]",
            "Memory": f"[{round(memory, 2)}%]",
            "Ping": f"[{round(self.dottie.latency * 1000)}ms]",
            "Uptime": f"[{str(self.dottie.uptime)[:-7]}]",
            "Code Length": f"[{get_code_length()} lines]",
            "Command Count": f"[{get_command_count()} commands]"
        }
        
        embed = discord.Embed(colour=discord.Colour(pink_embed))
        embed.set_author(name=self.dottie.user.name, url="https://github.com/smudgedpasta/Dottie", icon_url=self.dottie.user.avatar_url_as(format="png", size=4096))
        embed.description = "*```asciidoc\n[Ping! I pong back all this nice techy info. 🍺]```*"
        embed.add_field(name="CPU Usage", value="```ini\n" + str(TechyInfo["CPU"]) + "```")
        embed.add_field(name="Memory Usage", value="```ini\n" + str(TechyInfo["Memory"]) + "```")
        embed.add_field(name="Ping Latency", value="```ini\n"+ str(TechyInfo["Ping"]) + "```")
        embed.add_field(name="Uptime", value="```ini\n"+ str(TechyInfo["Uptime"]) + "```")
        embed.add_field(name="Code Length", value="```ini\n"+ str(TechyInfo["Code Length"]) + "```")
        embed.add_field(name="Unique Commands", value="```ini\n"+ str(TechyInfo["Command Count"]) + "```")

        await ctx.send(embed=embed)


    @commands.command(aliases=["icon"])
    async def avatar(self, ctx):
        spl = ctx.message.content.split(None, 1)
        if len(spl) > 1:
            try:
                member = await self.dottie.find_user(spl[-1], guild=ctx.guild)
            except:
                print2(traceback.format_exc(), end="")
                return await ctx.send(f"I can't find the user \"{spl[-1]}\"! Please specify a more specific identifier such a username#discriminator, or a user ID.")
        else:
            member = ctx.author
        embed = discord.Embed(colour=member.colour)
        embed.set_image(url=member.avatar_url_as(format="png", size=4096))
        embed.set_footer(text=f"{member.display_name}'s wonderful icon picture! 👍")
        await ctx.send(embed=embed)


    @commands.command()
    async def quote(self, ctx):
        with open("json/quotes.json", "r", encoding="utf-8") as f:
            quote_pool = json.load(f)
            random_quote = random.choice(quote_pool)
            embed = discord.Embed(colour=discord.Colour(pink_embed))
            embed.description = random_quote["quote"]
            embed.set_footer(text="Quote by " + random_quote["credit"])
            await ctx.send(embed=embed)
        

def setup(dottie):
    globals()["dottie"] = dottie
    dottie.add_cog(GENERAL(dottie))
