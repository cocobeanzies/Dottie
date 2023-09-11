from imports import *


def replace_map(s, mapping):
    temps = {k: chr(65535 - i) for i, k in enumerate(mapping.keys())}
    trans = "".maketrans({chr(65535 - i): mapping[k] for i, k in enumerate(mapping.keys())})
    for key, value in temps.items():
        s = s.replace(key, value)
    for key, value in mapping.items():
        s = s.replace(value, key)
    return s.translate(trans)


def grammarly_2_point_0(string):
    s = string.lower().replace("am i", "are y\uf000ou").replace("i am", "y\uf000ou are")
    s = replace_map(s, {
        "yourself": "myself",
        "your ": "my ",
        "are you": "am I",
        "you are": "I am",
        "you're": "i'm",
        "you'll": "i'll"
    })
    modal_verbs = "shall should shan't shalln't shouldn't must mustn't can could couldn't may might mightn't will would won't wouldn't have had haven't hadn't do did don't didn't"
    r1 = re.compile(f"(?:{modal_verbs.replace(' ', '|')}) you")
    r2 = re.compile(f"you (?:{modal_verbs.replace(' ', '|')})")
    while True:
        m = r1.search(s)
        if not m:
            m = r2.search(s)
            if not m:
                break
            s = s[:m.start()] + "I" + s[m.start() + 3:]
        else:
            s = s[:m.end() - 3] + "I" + s[m.end():]
    res = alist(s.split())
    for sym in "!.,'":
        if sym in s:
            for word, rep in {"you": "m\uf000e", "me": "you", "i": "I"}.items():
                src = word + sym
                dest = rep + sym
                if res[0] == src:
                    res[0] = dest
                res.replace(src, dest)
    if res[0] == "you":
        res[0] = "I"
    s = " ".join(res.replace("you", "m\uf000e").replace("i", "you").replace("me", "you").replace("i", "I").replace("i'm", "I'm").replace("i'll", "I'll"))
    string = s[0].upper() + s[1:].replace("\uf000", "")
    return string


class FUN(commands.Cog):
    def __init__(self, dottie):
        self.dottie = dottie


    @commands.command(aliases=["8ball", "ask"], question=None)
    async def AskDottie(self, ctx, *, question):
        with open("misc/questions.txt", "r", encoding="utf-8") as f:
            f = f.read()

            Topic = f.splitlines()
            for i in Topic:
                if "sex" in i.lower() or "penis" in i.lower() or "suicide" in i.lower():
                    Topic.remove(i)

        opposite_responses = [
            "Don't you have any work you should be doing?",
            "How do you like to treat yourself? And if you don't, you should! :blush:",
            f"{random.choice(Topic)}",
            f"""{"".join(y for x in zip(question[::2].lower(), question[1::2].upper()) for y in x if y)}""",
            random.choice([f"Have you got a {random.choice(['puppy', 'kitten'])} from {PREFIX[0]}snake? Try to win one and maybe I'll speak to you. {get_random_emoji()}", f"Have you got a kitten from {random.choice([PREFIX[0] + 'quiz', PREFIX[0] + 'rps'])}? Try to win and one maybe I'll speak to you. {get_random_emoji()}", f"Have you got a cheesecake from {random.choice([PREFIX[0] + 'quiz', PREFIX[0] + 'rps'])}? Try to win one and maybe I'll speak to you. {get_random_emoji()}"])
        ]
        if set(question) == {"?"} or set(question) == {"!"} or set(question) == {"."}:
            _responses = [
                "Haha, nice try, I know that's not an actual question.",
                "You thinking of asking an actual question?",
                f"Congratulations, you can post a {question[:1]}."
            ]

            return await ctx.send(random.choice(_responses))

        elif "64 51 77 34 77 39 57 67 58 63 51" in question:
            responses = ["So you've found the Easter Egg. It translates to dQw4w9WgXcQ. Search that through Google and see what happens. :wink:"]

        elif "hi" in question or "hello" in question:
            responses = [
                f"Hello, {ctx.author.display_name}! {get_random_emoji()}",
                f"Hi, {ctx.author.display_name}. I'm feeling lonely, so I appreciate you talking to me. :blush:",
                f"Do you need something? {self.dottie.get_user(761641941511176262).name} and {self.dottie.get_user(668999031359537205).name} are also good fun!",
                f"Hi! {random.choice(opposite_responses)}",
                f"Ay, I'm busy with my 10 hour tunez. What do you want? {get_random_emoji()}",
                f"Hello? {get_random_emoji()}",
                "... Hi?",
                "Hi! :white_heart:"
            ]

        elif "bye" in question or "goodbye" in question:
            responses = [
                f"Goodbye, {ctx.author.display_name}! :white_heart:",
                f"I reckon you wont use this feature again for {str(random.randint(1, 21))} days. {get_random_emoji()}",
                "Bye? Whatever, I've got 10 hour tunez to catch up on.",
                "See you around!",
                "Finally, I was getting worried you'd procrastinate with me all day.",
                "'Later!",
                "Goodbye I guess...?",
                "Why leave now? I'm still lonely. :pensive:",
                "Cool, see you later."
            ]


        elif "when" in question:
            responses = [
                f"In the year {random.randint(2021, 10001)}!",
                f"In {random.randint(3, 11)} minutes!",
                f"Wait {random.randint(5, 11)} hours!",
                f"How about I ask you a question: {random.choice(opposite_responses)}",
                f"I'm only a bot, {', '.join(str(dottie.get_user(u))[:-5] for u in OWNERS[:-1])} hasn't figured out time travel code yet!",
                f"Go {random.choice(['browse some social media', 'watch some YouTube'])} and see if it's happened afterwards!",
                "Tomorrow?",
                "In a million years...",
                "Does it really matter when?",
                "Do you want it to happen now? Go out there and do it!",
                "Didn't that happen yesterday?",
                "Never. :smirk:",
                "How about an hour?",
                "I dunno. ¯\_(ツ)_/¯",
                "Try it and find out!"
            ]

        elif "why" in question or "is" in question or "how" in question or "are" in question or "was" in question or "you" in question or "yours" in question or "you're" in question:
            responses = [
                f"How about I ask you a question: {random.choice(opposite_responses)}",
                f"Just to tease you, I refuse to answer. {get_random_emoji()}",
                f"Ask a {random.choice(['therapist', 'doctor', 'parent', 'sibling', 'friend'])}!",
                "Eh?",
                "Wouldn't know, might Google help?",
                "Yeah!",
                "Heck yeah!",
                "Of course!",
                "I think so!",
                "I suppose so...",
                "Nah.",
                "Uuuhhhmmm... Yes...?",
                "Mhm! :blush:",
                "Definitely, yes!",
                "I believe so?",
                "What? No!",
                "Ay, ask me later, I'm busy with my 10 hour tunez! :headphones:"
            ]

        elif "can" in question or "would" in question or "does" in question or "should" in question or "do" in question:
            responses = [
                f"How about I ask you a question: {random.choice(opposite_responses)}",
                f"Ask a {random.choice(['therapist', 'doctor', 'parent', 'sibling', 'friend'])}!",
                "Eh?",
                "Yeah!",
                "Heck yeah!",
                "Of course!",
                "Sure!",
                "Nah.",
                "Uuuhhhmmm... Yes...?",
                "Mhm! :blush:",
                "Definitely, yes!",
                "I believe so?",
                "What? No!",
                "Do what you want to do, as long as it doesn't hurt you! :white_heart:",
                "Obviously, you goof!",
                "Hahaha, please.",
                "No! Seriously, I'm concerned.",
                "I guess?",
                "Why does that even matter?",
                "Uhhh, can I have a cookie instead?",
                "Ay, ask me later, I'm busy with my 10 hour tunez! :headphones:"
            ]

        else:
            responses = [
                f"How about I ask you a question: {random.choice(opposite_responses)}",
                f"My AI is ever growing, I think you should run. {get_random_emoji()}",
                "I'm apologize for whatever hardships you're going through that brings you to ask that question.",
                "Interesting!",
                "According to all known laws of aviation, there should be no way that a bee... Oh! Sorry, did you ask something?",
                "That makes me so sad. :cry:",
                "Hahaha, what is WRONG with you?!",
                "Try walking outside and screaming at the top of your lungs.",
                "Now, why would you bring that up?",
                "Heck yeah!",
                "Of course!",
                "I think so!",
                "Meh, sounds alright.",
                "I suppose so...",
                "Hmm, maybe?",
                "Eh?",
                "Probably not...",
                "Try it and find out!",
                "Heheh, I'd like to see you try.",
                "I didn't quite catch that...",
                "Ay, ask me later, I'm busy with my 10 hour tunez! :headphones:"
            ]

        if "64 51 77 34 77 39 57 67 58 63 51" not in question and "hi" not in question and "hello" not in question and "bye" not in question and "goodbye" not in question and ctx.guild is not None:
                if "who" in question:
                    responses = [
                        f"How about I ask you a question: {random.choice(opposite_responses)}",
                        f"Maybe it's your {random.choice(['therapist', 'doctor', 'parent', 'sibling', 'friend'])}!",
                        f"Hm... Maybe it's {random.choice(list(set(ctx.guild.members).difference({self.dottie.user}))).display_name}!",
                        f"I am certain it's {random.choice(list(set(ctx.guild.members).difference({self.dottie.user}))).display_name}!",
                        f"I think {random.choice(list(set(ctx.guild.members).difference({self.dottie.user}))).display_name} might know... :eyes:",
                        "Me. :smirk:"
                    ]
                else:
                    responses.append(f"Ask {random.choice(list(set(ctx.guild.members).difference({self.dottie.user}))).display_name}!")

        answer = [
            "So you asked...",
            "You'd like to know...",
            "Hi there, you asked me...",
            "Hm...",
            ""
        ]

        question = grammarly_2_point_0(question)

        for i in ("~~", "***", "**", "*", "||", "__", "```", "'"):
            if question.startswith(i) and question.endswith(i):
                await ctx.send(f"{i}{random.choice(answer)} {question[len(i):-len(i)]}? {random.choice(responses)}{i}")
                return
        
        await ctx.send(f"{random.choice(answer)} {question.strip('?')}? {random.choice(responses)}")
        

    @commands.command(input=None)
    async def rate(self, ctx, *, input):
        random.seed(input)
        rate = random.randint(0, 10)
        input = grammarly_2_point_0(input)
        embed = discord.Embed(colour=discord.Colour(pink_embed), timestamp=ctx.message.created_at)
        embed.description = f"**{input.capitalize()}**, hmm? I rate that a **{rate}/10**! " + get_random_emoji()
        embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png", size=4096), text=f"Requested by {ctx.author.display_name}")
        await ctx.send(embed=embed)

    
    @commands.command()
    async def topic(self, ctx):
        topic = random.choice(("misc/facts.txt", "misc/questions.txt"))
        if topic == "misc/facts.txt":
            opener = "fact"
        elif topic == "misc/questions.txt":
            opener = "question"
        with open(topic, "r", encoding="utf-8") as f:
            Topic = f.read().splitlines()

            openerlist = [
                f"Here's a {opener}: ",
                f"It's time for a {opener}: ",
                f"I've got a {opener} for you: ",
                f"I've been called! It's {opener} time: ",
                f"We meet again, {ctx.author.display_name}. Here's a {opener}: ",
                f"Here's a complete non-spammy {opener} for your introverted needs: ",
                f"{opener.capitalize()} time! ",
            ]
            await ctx.send(f"{random.choice(openerlist)}{random.choice(Topic)}")


    @commands.command(aliases=["ship", "love"])
    async def matchmaking(self, ctx, arg, arg2):
        heart_list = ["❤️", "🧡", "💛", "💚", "💙", "💜", "💗", "💞", "🤍", "🖤", "🤎", "❣️", "💕", "💖"]

        if re.fullmatch("<@[!&]?[0-9]+>", arg):
            u_id = int(arg.strip("<@!&>"))
            user = ctx.guild.get_member(u_id)
            if user is None:
                try:
                    user = await self.dottie.fetch_user(u_id)
                except discord.NotFound:
                    pass
                else:
                    arg = user.name
            else:
                arg = user.display_name
        elif re.fullmatch("<a?:[A-Za-z0-9\\-~_]+:[0-9]+>", arg):
            _, name, e_id = arg[:-1].rsplit(":", 2)
            e_id = int(e_id)
            emoji = self.dottie._connection._emojis.get(e_id)
            if emoji is not None:
                name = emoji.name
            arg = name

        if re.fullmatch("<@[!&]?[0-9]+>", arg2):
            u_id = int(arg2.strip("<@!&>"))
            user = ctx.guild.get_member(u_id)
            if user is None:
                try:
                    user = await self.dottie.fetch_user(u_id)
                except discord.NotFound:
                    pass
                else:
                    arg2 = user.name
            else:
                arg2 = user.display_name
        elif re.fullmatch("<a?:[A-Za-z0-9\\-~_]+:[0-9]+>", arg2):
            _, name, e_id = arg2[:-1].rsplit(":", 2)
            e_id = int(e_id)
            emoji = self.dottie._connection._emojis.get(e_id)
            if emoji is not None:
                name = emoji.name
            arg2 = name

        arg = arg.capitalize().replace("'", "").replace("`", "")
        arg2 = arg2.capitalize().replace("'", "").replace("`", "")
        arg, arg2 = sorted((arg, arg2))

        random.seed((arg, arg2))
        percentage = random.randint(0, 100)

        start = len(arg) / 2
        end = len(arg2) / 2
        ship_beg = arg[:-int(start)]
        ship_beg2 = arg2[:-int(end)]
        ship_tail = arg[-int(start):]
        ship_tail2 = arg2[-int(end):]
        ship_start = random.choice([ship_beg, ship_tail])
        ship_end = random.choice([ship_beg2, ship_tail2])
        random.seed((ship_start, ship_end))
        shipname = ship_start + ship_end

        random.seed(time.time())
        heart = random.choice(heart_list)

        bar = create_progress_bar(21, percentage / 100)

        embed = discord.Embed(colour=discord.Colour(pink_embed), timestamp=ctx.message.created_at)
        suspicious_function = lambda x: x / ((x ** 2 * 6254793562032913) // (7632048114126314 * 10 ** 24) - (x * 5638138161912547) // 2939758 + 1000000155240420236976462021787648)
        suspicious_function_2 = lambda x: int.from_bytes(bytes.fromhex(x.encode("utf-8").hex()), "little")
        if round(suspicious_function(suspicious_function_2(arg + arg2))) in (13264547, 47787122) and suspicious_function(suspicious_function_2(arg2 + arg)) in (5.869437322867208e-09, 1.0000614609767725e-08):
            inwards_heart = [
                "00111011100",
                "01122122110",
                "01223232210",
                "01234543210",
                "00123432100",
                "00012321000",
                "00001210000",
                "00000100000"
            ]
            emoji = {
                "0": "▪",
                "1": "<a:_" + ":797359273914138625>",
                "2": "<a:_" + ":797359354314620939>",
                "3": "<a:_" + ":797359351509549056>",
                "4": "<a:_" + ":797359341157482496>",
                "5": "<:_" + ":722354192995450912>"
            }
            e_calc = lambda x: (x * 15062629995394936) // 7155909327645687 - (x ** 2 * 3014475045596449) // (2062550437214859 * 10 ** 18) - 53
            e2 = self.dottie.get_emoji(e_calc(ctx.guild.id))
            if e2:
                emoji["5"] = f"<:_:{e2.id}>"

            trans = "".maketrans(emoji)
            rainbow_heart = "\n".join(inwards_heart).translate(trans)
            embed.description = f"```" + random.choice(["css", "ini"]) + f"\n[{arg}] ♡ [{arg2}]❔ 𝓣𝓱𝓮𝔂 𝓼𝓬𝓸𝓻𝓮 𝓪𝓷 [𝓲𝓷𝓯𝓲𝓷𝓲𝓽𝓮%]❕ 💜```" + rainbow_heart
        else:
            if arg == arg2:
                embed.description = f"```" + random.choice(["css", "ini"]) + f"\n[{arg}] ♡ [{arg2}]❔ 𝒯𝒽𝑒𝓎 [{percentage}%] 𝓁𝑜𝓋𝑒 𝓉𝒽𝑒𝓂𝓈𝑒𝓁𝓋𝑒𝓈❕ " + get_random_emoji() + "```" + bar
            else:
                embed.description = f"```" + random.choice(["css", "ini"]) + f"\n[{arg}] ♡ [{arg2}] ({shipname.capitalize()})❔ 𝓣𝓱𝓮𝔂 𝓼𝓬𝓸𝓻𝓮 𝓪 [{percentage}%]❕ " + get_random_emoji() + "```" + bar
        embed.set_footer(icon_url=ctx.author.avatar_url_as(format="png", size=4096), text=f"Shipped by {ctx.author.display_name} 🤍")
        await ctx.send(f"{heart}" + " ***MATCHMAKING*** " + f"{heart}", embed=embed)

    
    @commands.command(aliases=["snail"])
    async def snake(self, ctx):
        icons = {
            0: "▪",
            1: random.choice(("🐌", "🐍")),
            2: "🍎"
        }
        tail = "🟩" if icons[1] == "🐍" else "🟫"
        snaek_colour = 7975512 if icons[1] == "🐍" else 12740942
        size = 8
        grid = [[0] * size for i in range(size)]

        def snaek_bwain(grid):
            output = ""
            for y in grid:
                line = ""
                for x in y:
                    line += icons.get(x, tail)
                output += line + "\n"
            return output
        
        def spawn_apple(grid):
            x = random.randint(0, size - 1)
            y = random.randint(0, size - 1)
            while grid[y][x] != 0:
                x = random.randint(0, size - 1)
                y = random.randint(0, size - 1)
            grid[y][x] = 2

        x = y = size >> 1
        if not size & 1:
            x -= random.randint(0, 1)
            y -= random.randint(0, 1)
        grid[y][x] = 1
        snake_position = [x, y]
        snake_direction = [None]
        snake_length = [1]
        snake_alive = [True]

        spawn_apple(grid)

        game = discord.Embed(colour=discord.Colour(snaek_colour))
        game.set_author(name="Playing Snake!", url="https://sites.google.com/view/snake--game/#h.68gyhyo7vk15", icon_url="https://cdn.discordapp.com/attachments/687567100767633432/880812464739074048/image0.png")
        game.description = snaek_bwain(grid)
        game.set_footer(text=f"Currently playing: {ctx.author.display_name}!", icon_url=str(ctx.author.avatar_url))
        message = await ctx.send(embed=game)

        await message.add_reaction("⬅️")
        await message.add_reaction("⬆️")
        await message.add_reaction("➡️")
        await message.add_reaction("⬇️")

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

        async def snaek_reaction_listener(event_type="add"):
            while snake_alive[0]:
                react = await self.dottie.wait_for(f"reaction_{event_type}", check=user_check)
                emoji = str(react[0])
                if emoji == "⬅️":
                    snake_direction[0] = (-1, 0)
                elif emoji == "➡️":
                    snake_direction[0] = (1, 0)
                elif emoji == "⬆️":
                    snake_direction[0] = (0, -1)
                elif emoji == "⬇️":
                    snake_direction[0] = (0, 1)
        create_task(snaek_reaction_listener("add"))
        create_task(snaek_reaction_listener("remove"))

        while snake_alive[0]:
            if snake_direction[0]:
                for y, row in enumerate(grid):
                    for x, v in enumerate(row):
                        if v < 0:
                            row[x] = v + 1
                grid[snake_position[1]][snake_position[0]] = 1 - snake_length[0]
                snake_position[0] += snake_direction[0][0]
                snake_position[1] += snake_direction[0][1]
                if snake_position[0] < 0 or snake_position[1] < 0:
                    snake_alive[0] = False
                    break
                try:
                    colliding_with = grid[snake_position[1]][snake_position[0]]
                except IndexError:
                    snake_alive[0] = False
                    break
                if colliding_with == 2:
                    snake_length[0] += 1
                    spawn_apple(grid)
                elif colliding_with < 0:
                    snake_alive[0] = False
                    break
                grid[snake_position[1]][snake_position[0]] = 1
                game.description = snaek_bwain(grid)
                await message.edit(embed=game)
                tile_count = size ** 2 - 1
                for y in grid:
                    for x in y:
                        if x < 0:
                            tile_count -= 1
                if tile_count <= 0:
                    await ctx.send(f"{ctx.author.mention}, **you won**! You now get showered with 100 fluffy puppies and kittens, as well as 100 yummy cheesecakes. <:puppy:881202126070624286> <:kitten:881205443320479754> <:cheesecake:881133619983302718>")
                    try:
                        with open("database/prizes.json", "r+") as f:
                            prize_userbase = json.load(f)
                    except:
                        prize_userbase = {}
                    try:
                        prize_userbase[str(ctx.author.id)][1] += 100
                        prize_userbase[str(ctx.author.id)][0] += 100
                        prize_userbase[str(ctx.author.id)][2] += 100
                    except KeyError:
                        prize_userbase[str(ctx.author.id)] = [100, 100, 100]
                    with open("database/prizes.json", "w") as f:
                        json.dump(prize_userbase, f, indent=4)
                    break 
            await asyncio.sleep(1)
        
        if not snake_alive[0]:
            if snake_length[0] - 1 == 0:
                await ctx.send(f"{ctx.author.mention}, **game over**! Your score was {snake_length[0] - 1}, did you even try? {get_random_emoji()}")
            elif snake_length[0] - 1 >= 20:
                await ctx.send(f"{ctx.author.mention}, **game over**! Your score was {snake_length[0] - 1}, you win a puppy! <:puppy:881202126070624286>")
                try:
                    with open("database/prizes.json", "r+") as f:
                        prize_userbase = json.load(f)
                except:
                    prize_userbase = {}
                try:
                    prize_userbase[str(ctx.author.id)][1] += 1
                except KeyError:
                    prize_userbase[str(ctx.author.id)] = [0, 1, 0]
                with open("database/prizes.json", "w") as f:
                    json.dump(prize_userbase, f, indent=4)
            else:
                await ctx.send(f"{ctx.author.mention}, **game over**! Your score was {snake_length[0] - 1}, have a participation kitten. <:kitten:881205443320479754>")
                try:
                    with open("database/prizes.json", "r+") as f:
                        prize_userbase = json.load(f)
                except:
                    prize_userbase = {}
                try:
                    prize_userbase[str(ctx.author.id)][2] += 1
                except KeyError:
                    prize_userbase[str(ctx.author.id)] = [0, 0, 1]
                with open("database/prizes.json", "w") as f:
                    json.dump(prize_userbase, f, indent=4)
        else:
            snake_alive[0] = False


    @commands.command(aliases=["quiz"])
    async def numberguess(self, ctx):
        await ctx.send("I am thinking of a number between 1 and 100... Can you guess what it is?")
        answer = random.randint(1, 101)
        attempts = 10
        try:
            for i in range(attempts):
                response = await self.dottie.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
                number = int(response.content)
                if number == answer:
                    await ctx.send(f"Bingo! This took you **{i + 1} attempts**! You now get a cheesecake. <:cheesecake:881133619983302718>")
                    try:
                        with open("database/prizes.json", "r+") as f:
                            prize_userbase = json.load(f)
                    except:
                        prize_userbase = {}
                    try:
                        prize_userbase[str(ctx.author.id)][0] += 1
                    except KeyError:
                        prize_userbase[str(ctx.author.id)] = [1, 0, 0]
                    with open("database/prizes.json", "w") as f:
                        json.dump(prize_userbase, f, indent=4)
                        return
                elif i >= attempts - 1:
                    await ctx.send("🛑 Sorry, you ran out of chances! Try again any time!")
                    return
                elif number > answer:
                    await ctx.send("Your guess was **too high**! Try again!")
                elif number < answer:
                    await ctx.send("Your guess was **too low**! Try again!")
        except:
            await ctx.send("Yo, I ain't that smart! Please use **integers** written in **numbers**!")


    @commands.command(Aliases=["rockpaperscissors", "rock_paper_scissors"])
    async def rps(self, ctx):
        try:
            await ctx.send("Lets play Rock, Paper, Scissors! Post your choice!")
            response = await self.dottie.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel)

            matches = {"rock": "scissors", "scissors": "paper", "paper": "rock"}
            decision = random.choice(list(matches.keys()))
            await ctx.send(f"I'll go with {decision}!")

            if response.content.lower() not in matches.keys():
                await ctx.send("We- Hold on a minute, you didn't even respond with an answer! <:colondead:833117645863780402>")
            if matches[decision] == response.content.lower():
                await ctx.send("I win! Mwahaha! :grin:")
            if matches[response.content.lower()] == decision:
                await ctx.send("Aw, I lost... :pensive: You win a cheesecake though! Wanna rematch? <:cheesecake:881133619983302718>")
                try:
                    with open("database/prizes.json", "r+") as f:
                        prize_userbase = json.load(f)
                except:
                    prize_userbase = {}
                try:
                    prize_userbase[str(ctx.author.id)][0] += 1
                except KeyError:
                    prize_userbase[str(ctx.author.id)] = [1, 0, 0]
                with open("database/prizes.json", "w") as f:
                    json.dump(prize_userbase, f, indent=4)
                response2 = await self.dottie.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
                if "no" in response2.content.lower() or "nope" in response2.content.lower() or "nah" in response2.content.lower():
                    await ctx.send("<a:cries_gif:818530242971959337>")
                elif "yes" in response2.content.lower() or "yep" in response2.content.lower() or "sure" in response2.content.lower():
                    await ctx.send("<a:dummy_gif:818530180431741009>")
                    return
            if response.content.lower() == decision:
                await ctx.send("Wow, we tied! Great minds thing alike. :smirk: Have a participation kitten. <:kitten:881205443320479754>")
                try:
                    with open("database/prizes.json", "r+") as f:
                        prize_userbase = json.load(f)
                except:
                    prize_userbase = {}
                try:
                    prize_userbase[str(ctx.author.id)][2] += 1
                except KeyError:
                    prize_userbase[str(ctx.author.id)] = [0, 0, 1]
                with open("database/prizes.json", "w") as f:
                    json.dump(prize_userbase, f, indent=4)
        except:
            return


    @commands.command(aliases=["say"], speach=None)
    async def speak(self, ctx, *, speach):
        try:
            await ctx.message.delete()
        except:
            pass

        speach = speach.replace("@", "@\u200b")
        speach = speach.replace("<@&", "<@&\u200b")

        if ctx.author.id in OWNERS:
            await ctx.send(f"{speach[:1999]}")
        else:
            await ctx.send(f"\u200b {speach[:1999]}")


    @commands.command()
    async def heart(self, ctx, arg1, arg2):
        heart = [
            "00111011100",
            "01222122210",
            "12222222221",
            "12222222221",
            "12222222221",
            "01222222210",
            "00122222100",
            "00012221000",
            "00001210000",
            "00000100000"
        ]

        emoji = {
            "0": "<:_:760062353063936000>",
            "1": arg1,
            "2": arg2
        }

        trans = "".maketrans(emoji)
        for line in heart:
            create_task(ctx.send("\u200b" + line.translate(trans)))
            await asyncio.sleep(0.2)


    @commands.command()
    async def pyramid(self, ctx):
        await ctx.send(":desert: Y'know what I'm in the mood for? Building a pyramid! How tall should it be?")
        try:
            message = await self.dottie.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
            size = (int(message.content))
            if size >= 26:
                await ctx.send("Yeah no, let's not go *too* spammy! :sweat_drops:")
            elif size <= -1:
                await ctx.send("Oi, quit try'na break the universe, I can't exactly dig underground on Discord! :upside_down:")
            elif size == 0:
                await ctx.send("Uh, okay, guess I'll go build elsewhere... :pensive:")
            else:
                for i in range(size):
                    create_task(ctx.send("\u200b" + ("<:empty" + ":760062353063936000>") * (size-i-1) + ("<:empty" + ":760062353063936000>" + ":orange_square:") * (i+1)))
                    await asyncio.sleep(0.2)
        except:
            await ctx.send("Yo, I ain't that smart! Please use **integers** written in **numbers**!")


    @commands.command(aliases=["annoying", "name", "myname"])
    async def useless(self, ctx):
        await ctx.send(f"So, \"{ctx.author.display_name}\", what's your name?")
        uname = await self.dottie.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
        await ctx.send("Yes, interesting, now what's your name?")
        pointless = await self.dottie.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
        await ctx.send("Mhm, mhm, very nice, now what's your name?")
        pointless = await self.dottie.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
        await ctx.send("Uhuh that's very nice, now would you like to tell me your name?")
        pointless = await self.dottie.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
        await ctx.send("That's nice, but I don't think I know your name yet. What's your name?")
        uname2 = await self.dottie.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
        await ctx.send(f"Woah, calm down there \"{''.join(y for x in zip(uname2.content[::2].lower(), uname2.content[1::2].upper()) for y in x if y)}\". I have concluded that your name might possibly be \"{uname.content.capitalize()}\".")


    @commands.command(aliases=["chachaslide", "ccs"])
    async def cha_cha_slide(self, ctx):
        lyrics = """We're going to get funky...
To the left!
Take it back now y'all
One hop this time!
Right foot let's stomp
Left foot let's stomp
Cha cha real smooth
Yeah, yeah, do that stuff, do it!
Ah yeah, I'm outta here y'all.
Peace!
""".splitlines()

        await ctx.send(lyrics[0])
        time.sleep(1)
        error_message = "Boo, that's not how the lyrics go!"

        await ctx.send(f"Sing it with me now. {lyrics[1]}")
        next1 = await self.dottie.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
        next1.content = next1.content.capitalize().replace("!", "").replace("?", "").replace(".", "")
        if next1.content.replace("yall", "y'all").replace("ya'll", "y'all") == lyrics[2]:
            await ctx.send(lyrics[3])
        else:
            await ctx.send(error_message)
            return
        next2 = await self.dottie.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
        next2.content = next2.content.capitalize().replace("!", "").replace("?", "").replace(".", "")
        if next2.content.replace("lets", "let's") == lyrics[4]:
            await ctx.send(lyrics[5])
        else:
            await ctx.send(error_message)
            return
        next3 = await self.dottie.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
        if next3.content.capitalize().replace("!", "").replace("?", "").replace(".", "") == lyrics[6]:
            await ctx.send(lyrics[7])
            time.sleep(1)
            await ctx.send(lyrics[8])
            time.sleep(1)
            await ctx.send(lyrics[9])
        else:
            await ctx.send("C'mon, we were so close!")


def setup(dottie):
    dottie.add_cog(FUN(dottie))
