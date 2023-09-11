from imports import *


class IMAGE(commands.Cog):
    def __init__(self, dottie):
        self.dottie = dottie

    with open("json/lmor.json", "rb") as f:
        lmor = json.load(f)

    @commands.command(aliases=["lmor"])
    async def letmeoutroaring(self, ctx):
        icon = random.choice(["https://cdn.discordapp.com/attachments/756891683765092395/867006708857569290/Ruin_Eye.PNG", "https://cdn.discordapp.com/attachments/756891683765092395/867006711247536139/Eon_Eye.png"])
        if "Ruin_Eye" in icon:
            embed_colour = 4787720
        elif "Eon_Eye" in icon:
            embed_colour = 8957637
        menu = discord.Embed(colour=discord.Colour(embed_colour))
        menu.set_author(name="⛓ Let Me Out Roaring ⛓", url="https://www.deviantart.com/smudgedpasta/gallery/73630013/let-me-out-roaring", icon_url=icon)
        menu.description = """Please select what you would like to view!\n(Works on a per user basis!)\n
<:LMOR_Lore:867008087889805332> = *LMOR Lore*\n<:LMOR_Speedpaint:867008777327476756> = *LMOR Speedpaints*\n<:LMOR_Iss1:867008362436886558> = *LMOR Issue 1*"""
        menu.set_image(url="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/b9573a17-63e8-4ec1-9c97-2bd9a1e9b515/delxq14-14be918d-ddcd-44cc-8c45-68d85eaf71f9.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcL2I5NTczYTE3LTYzZTgtNGVjMS05Yzk3LTJiZDlhMWU5YjUxNVwvZGVseHExNC0xNGJlOTE4ZC1kZGNkLTQ0Y2MtOGM0NS02OGQ4NWVhZjcxZjkucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.uqcOqvLjS42h1afzaInCaVjuDkRzNVr0OxnimQFMJpY")
        menu.set_footer(text=f"Let Me Out Roaring created by {', '.join(str(self.dottie.get_user(u))[:-5] for u in OWNERS[:-1])}")
        message = await ctx.send(embed=menu)

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

        async def page_reaction_listener(page, waiter, lmor_selection, cleared, event_type="add"):
            while True:
                react = await self.dottie.wait_for(f"reaction_{event_type}", check=user_check)
                if cleared[0]:
                    continue
                emoji = str(react[0])
                pages = lmor_selection[0]
                swap = False
                if emoji == "🔺" and page[0] > 0:
                    page[0] -= 1
                    swap = True
                elif emoji == "🔻" and page[0] < len(pages) - 1:
                    page[0] += 1
                    swap = True
                elif emoji == "🏚️":
                    cleared[0] = True
                    SmellyFeet = create_task(message.clear_reactions())
                    await message.edit(embed=menu)
                    await SmellyFeet
                    eloop.call_soon_threadsafe(waiter[0].set_result, None)
                if swap:
                    selection = discord.Embed(colour=discord.Colour(embed_colour))
                    selection.set_author(name="⛓ Let Me Out Roaring ⛓", url="https://www.deviantart.com/smudgedpasta/gallery/73630013/let-me-out-roaring", icon_url=icon)
                    selection.description = f"*{pages[page[0]]['title']}*"
                    selection.set_image(url=pages[page[0]]["url"])
                    selection.set_footer(text="Click the reactions to scroll through the pages!")
                    await message.edit(embed=selection)

        await message.add_reaction("<:LMOR_Lore:867008087889805332>")
        await message.add_reaction("<:LMOR_Speedpaint:867008777327476756>")
        await message.add_reaction("<:LMOR_Iss1:867008362436886558>")

        cleared = [False]
        waiter = [asyncio.Future()]
        page = [0]
        lmor_selection = [None]
        create_task(page_reaction_listener(page, waiter, lmor_selection, cleared, "add"))
        create_task(page_reaction_listener(page, waiter, lmor_selection, cleared, "remove"))
        lmor = self.lmor

        while True:
            react = await self.dottie.wait_for(f"reaction_add", check=user_check)
            emoji = str(react[0])
            if emoji == "<:LMOR_Lore:867008087889805332>":
                lmor_response = lmor["lore"]
            elif emoji == "<:LMOR_Speedpaint:867008777327476756>":
                lmor_response = lmor["speedpaints"]
            elif emoji == "<:LMOR_Iss1:867008362436886558>":
                lmor_response = lmor["issue1"]
            else:
                continue
            lmor_selection[0] = lmor_response
            SmellyFeet = create_task(message.clear_reactions())
            selection = discord.Embed(colour=discord.Colour(embed_colour))
            selection.set_author(name="⛓ Let Me Out Roaring ⛓", url="https://www.deviantart.com/smudgedpasta/gallery/73630013/let-me-out-roaring", icon_url=icon)
            selection.description = f"*{lmor_response[0]['title']}*"
            selection.set_image(url=lmor_response[0]["url"])
            selection.set_footer(text="Click the reactions to scroll through the pages!")
            await message.edit(embed=selection)
            await SmellyFeet
            await message.add_reaction("🔺")
            await message.add_reaction("🔻")
            await message.add_reaction("🏚️")
            await waiter[0]
            waiter[0] = asyncio.Future()
            await message.add_reaction("<:LMOR_Lore:867008087889805332>")
            await message.add_reaction("<:LMOR_Speedpaint:867008777327476756>")
            await message.add_reaction("<:LMOR_Iss1:867008362436886558>")
            cleared[0] = False


    hug_source = "https://cdn.discordapp.com/attachments/687567100767633432/814812448678739968/unknown.gif"
    hug_frames = []
    @commands.command(aliases=["nuzzle", "cuddle"])
    async def hug(self, ctx, url=None):
        output_size = (440, 356)
        pos = (183, 161)
        diameter = 103
        caption = "Your image"
        if not url:
            if ctx.message.attachments:
                url = ctx.message.attachments[0].url
            else:
                url = ctx.author.avatar_url
                caption = ctx.author.name
        else:
            if url.isnumeric():
                u_ids = (url,)
            else:
                u_ids = re.findall("<@!?([0-9]+)>", url)
            if u_ids:
                u_id = int(u_ids[0])
                user = self.dottie.get_user(u_id)
                if user is None:
                    user = await self.dottie.fetch_user(u_id)
                url = user.avatar_url
                caption = user.display_name
        url = str(url).strip("<>")
        resp = await create_future(requests.get, url, _timeout_=12)
        resp.raise_for_status()
        b = io.BytesIO(resp.content)
        img = Image.open(b)
        if not self.hug_frames:
            resp = await create_future(requests.get, self.hug_source, _timeout_=12)
            resp.raise_for_status()
            b = io.BytesIO(resp.content)
            hug = Image.open(b)
            for i in range(2147483648):
                try:
                    hug.seek(i)
                except EOFError:
                    break
                frame = hug.convert("RGB").resize(output_size, resample=Image.LANCZOS)
                self.hug_frames.append(frame)
            self.crop = Image.new("L", (diameter,) * 2)
            shape_tool = ImageDraw.Draw(self.crop)
            shape_tool.ellipse((0, 0) + (diameter,) * 2, 255, 159, width=1)
        aspect_ratio = img.width / img.height
        if aspect_ratio < 1:
            width = round(diameter * aspect_ratio)
            height = diameter
        else:
            width = diameter
            height = round(diameter / aspect_ratio)
        size = (width, height)
        if width != height:
            x = (diameter - width) // 2
            y = (diameter - height) // 2
            crop = self.crop.crop((x, y, x + width, y + height))
        else:
            crop = self.crop
        target = tuple(pos[i] - size[i] // 2 for i in range(2))
        source_frames = []
        for i in range(2147483648):
            try:
                img.seek(i)
            except EOFError:
                break
            frame = img.resize(size, resample=Image.LANCZOS)
            if frame.mode == "P":
                frame = frame.convert("RGBA")
            source_frames.append(frame)
        ts = time.time_ns() // 1000
        fn = str(ts) + ".gif"
        args = [
            "ffmpeg", "-threads", "2", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-framerate", "1", "-pix_fmt", "rgb24", "-video_size", "x".join(map(str, output_size)), "-i", "-",
            "-gifflags", "-offsetting", "-an", "-vf", "split[s0][s1];[s0]palettegen=reserve_transparent=1:stats_mode=diff[p];[s1][p]paletteuse=diff_mode=rectangle:alpha_threshold=128", "-loop", "0", fn
        ]
        proc = psutil.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            dest_frames = []
            for i, frame in enumerate(self.hug_frames):
                source = source_frames[i % len(source_frames)]
                frame = frame.convert("RGBA")
                if source.mode == "RGBA":
                    alpha = ImageChops.multiply(source.getchannel("A"), crop)
                else:
                    alpha = crop
                source.putalpha(alpha)
                frame.alpha_composite(source, target)
                if frame.mode != "RGB":
                    frame = frame.convert("RGB")
                b = frame.tobytes()
                await create_future(proc.stdin.write, b)
            proc.stdin.close()
            await create_future(proc.wait)
            f = discord.File(fn, filename="huggies.gif")
            await ctx.channel.send(f"<:miza_dottie_hug:788165800448098324> ***{caption}*** *gets a hug!*", file=f)
        except:
            try:
                os.remove(fn)
            except:
                pass
            raise
        else:
            try:
                os.remove(fn)
            except:
                pass


    @commands.command()
    async def photo(self, ctx):
        with open("json/Image_Pool.json", "r") as f:
            Image_Pool = json.load(f)
            random_image = random.choice(Image_Pool)
            embed = discord.Embed(colour=discord.Colour(pink_embed))
            embed.description = random_image["desc"]
            embed.set_image(url=random_image["img"])
            embed.set_footer(text="Art by " + random_image["artist"])
            await ctx.send(embed=embed)


    @commands.command()
    async def nsfw_photo(self, ctx):
        with open("json/NSFW_Image_Pool.json", "r") as f:
            NSFW_Image_Pool = json.load(f)
            random_image = random.choice(NSFW_Image_Pool)
            embed = discord.Embed(colour=discord.Colour(pink_embed))
            embed.description = random_image["desc"]
            embed.set_image(url=random_image["img"])
            embed.set_footer(text="Art by " + random_image["artist"])
            if ctx.channel.is_nsfw():
                await ctx.send(embed=embed)
            else:
                await ctx.send("Woah, be careful, this command pulls **graphic imagery**! Try again in an **NSFW channel**!")


    @commands.command(aliases=["smudge", "txin", "smudgetxin", "txinsmudge", "critter_cuddle", "crittercuddle"])
    async def smudgin(self, ctx):
        with open("json/Cuddly_Image_Pool.json", "r", encoding="utf-8") as f:
            Cuddle_Pool = json.load(f)
            random_cuddle = random.choice(Cuddle_Pool)
            embed = discord.Embed(colour=discord.Colour(pink_embed))
            embed.description = random.choice(["<a:RainbowCritterTransparent:516974531852632066>", "<a:Smudge_FaceSprites:776855303282229278>", "<:Txin_Smudge_Hug:799211332632969256>"])
            embed.set_image(url=random_cuddle["img"])
            embed.set_footer(text="Art by " + random_cuddle["artist"] + " 🤍")
            await ctx.send(embed=embed)


    @commands.command()
    async def art(self, ctx):
        async for message in ctx.channel.history(limit=None):
            if message.attachments:
                embed = discord.Embed(colour=discord.Colour(pink_embed))
                embed.description = "𝒴𝑜𝓊 𝓌𝒶𝓃𝓃𝒶 𝓈𝑒𝑒 𝑔𝓇𝑒𝒶𝓉 𝒶𝓇𝓉?\n𝒮𝓊𝓇𝑒, 𝓉𝒽𝑒𝓇𝑒'𝓈 𝓈𝑜𝓂𝑒 𝓪𝓶𝓪𝔃𝓲𝓷𝓰 𝒶𝓇𝓉 𝓇𝒾𝑔𝒽𝓉 𝒽𝑒𝓇𝑒! :blush:"
                embed.set_footer(text=f"Art by {message.author.name}")
                embed.set_image(url=message.attachments[0].proxy_url)
                await ctx.send(embed=embed)
                break

        
    @commands.command(aliases=["cats", "http"])
    async def http_cats(self, ctx, code=None):
        with open("json/http_cats.json", "r", encoding="utf-8") as f:
            http_cats = json.load(f)
            for name in http_cats:
                if name["name"] == 404:
                    cat_response = name
            if code is None:
                cat_response = random.choice(http_cats)
            if code is not None:
                for name in http_cats:
                    if str(name["name"]) == code or code.lower() in name["description"].lower():
                        cat_response = name
                        break
            embed = discord.Embed(colour=discord.Colour(random.choice(rainbow_embeds)))
            embed.set_footer(text="Images are from https://http.cat/")
            embed.description = cat_response["description"]
            embed.set_image(url=cat_response["image"])
            await ctx.send(embed=embed)

    
    @commands.command(aliases=["cats_list"])
    async def http_list(self, ctx):
        with open("json/http_cats.json", "r", encoding="utf-8") as f:
            http_names = json.load(f)

        http_list = []
        prev = curr = ""
        for names in http_names:
            prev = curr
            if curr:
                curr += "\n\n"
            new = "**" + str(names["name"]) + "**:\n" + str(names["description"])
            curr += new
            if len(curr) > 2048:
                http_list.append(prev)
                curr = new
        if curr:
            http_list.append(curr)

        pages = []
        for item in http_list:
            embed = discord.Embed(colour=discord.Colour(pink_embed))
            embed.set_author(name=f"All HTTP responses registered in {self.dottie.user.name}.", url="https://github.com/smudgedpasta/Dottie", icon_url=self.dottie.user.avatar_url_as(format="png", size=4096))
            embed.description = item
            pages.append(embed)

        message = await ctx.send(embed=pages[0])

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
                
    
    @commands.command(aliases=["inspirobot", "inspiration"])
    async def inspiro(self, ctx):
        embed = discord.Embed(colour=discord.Colour(random.choice(rainbow_embeds)))
        embed.set_footer(text="Images are from https://inspirobot.me/")
        quote = inspirobot.generate()
        embed.set_image(url=quote.url)
        if ctx.channel.is_nsfw():
                await ctx.send(embed=embed)
        else:
            await ctx.send("Woah, be careful, this command pulls **sexual references**! Try again in an **NSFW channel**!")


    @commands.command(aliases=["marble"])
    async def marble_fox(self, ctx):
        with open("json/marble_foxes.json", "r") as f:
                dreamstime_imgs = json.load(f)
                marble_foxes = random.choice(dreamstime_imgs)
                embed = discord.Embed(colour=discord.Colour(random.choice(rainbow_embeds)))
                embed.set_footer(text="Images are from https://www.dreamstime.com/photos-images/marble-fox.html")
                embed.set_image(url=marble_foxes["image"])
                embed.description = random.choice(["Yip!", "Yap!", "🦊", "<:Smudge:751543624268775526>"])
                await ctx.send(embed=embed)


    @commands.command(aliases=["sea_doggo", "seals"])
    async def seal(self, ctx):
        seal_number = random.randint(1, 83)
        if seal_number >= 10:
            seal = f"https://raw.githubusercontent.com/FocaBot/random-seal/master/seals/00{seal_number}.jpg"
        else:
            seal = f"https://raw.githubusercontent.com/FocaBot/random-seal/master/seals/000{seal_number}.jpg"
        embed = discord.Embed(colour=discord.Colour(random.choice(rainbow_embeds)))
        embed.set_footer(text="Images are from https://github.com/FocaBot/random-seal")
        embed.set_image(url=seal)
        embed.description = random.choice(["Egg!", ":ocean: :dog:", ":seal:", "<a:curiouseal:748840270069760072>", "<:seal_ball:670143859149242369>"])
        await ctx.send(embed=embed)


    @commands.command(aliases=["og", "doggo", "puppo"])
    async def dog(self, ctx):
        r = requests.get("https://dog.ceo/api/breeds/image/random")
        data = r.json()
        embed = discord.Embed(colour=discord.Colour(random.choice(rainbow_embeds)))
        embed.set_footer(text="Images are from https://dog.ceo/api/breeds/image/random")
        embed.set_image(url=data["message"])
        embed.description = random.choice(["Bärk!", "Börk!", "🐶", "🐕"])
        await ctx.send(embed=embed)


    @commands.command()
    async def fox(self, ctx):
        r = requests.get("https://randomfox.ca/floof/")
        data = r.json()
        embed = discord.Embed(colour=discord.Colour(random.choice(rainbow_embeds)))
        embed.set_footer(text="Images are from https://randomfox.ca/")
        embed.set_image(url=data["image"])
        embed.description = random.choice(["Squeak!", "Ring-ding-ding-ding-dingeringeding!", "🦊", "<:sleepy_fox:762367799150510164>"])
        await ctx.send(embed=embed)


    @commands.command(aliases=["muffins"])
    async def muffin(self, ctx):
        def get_random_page():
            html = requests.get(f"https://www.gettyimages.co.uk/photos/muffin?page={random.randint(1, 100)}").text
            url = "https://media.gettyimages.com/photos/"
            spl = html.split(url)[1:]
            imageset = {url + i.split('"', 1)[0].split("?", 1)[0] for i in spl}
            images = list(imageset)
            return images
        images = get_random_page()
        embed = discord.Embed(colour=discord.Colour(random.choice(rainbow_embeds)))
        embed.set_footer(text="Images are from https://www.gettyimages.co.uk/photos/")
        embed.set_image(url=random.choice(images))
        embed.description = random.choice(["It's muffin time!", "Muffin!!! 🤗", "🧁", "🧁🧁🧁"])
        await ctx.send(embed=embed)
 
    
    @commands.command(aliases=["dab"])
    async def ab(self, ctx):
        await ctx.send("https://cdn.discordapp.com/attachments/688253918890688521/739424083556696104/unknown.gif")


    @commands.command()
    async def how(self, ctx):
        await ctx.send("https://imgur.com/gallery/8cfRt")


def setup(dottie):
    dottie.add_cog(IMAGE(dottie))