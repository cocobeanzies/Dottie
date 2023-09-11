from imports import *


class MODERATION(commands.Cog):
    def __init__(self, dottie):
        self.dottie = dottie


    @commands.command(aliases=["topicloop_e"])
    async def topicloop_add(self, ctx):
        if ctx.author.guild_permissions.administrator == True or ctx.author.id in OWNERS:
            if ctx.guild.id not in TOPICLOOP_CHANNELS:
                TOPICLOOP_CHANNELS.add(ctx.channel.id)
            with open("database/topicloop_channels.txt", "a") as f:
                f.write("\n" + str(ctx.channel.id))
                await ctx.send(f":smiling_imp: `{ctx.guild}... Prepare for spam of an introvert's worst nightmare.`")
        else:
            await ctx.send("You don't have permissions to use that command, you lil' delinquent!")

    
    @commands.command(aliases=["topicloop_d"])
    async def topicloop_remove(self, ctx):
        if ctx.author.guild_permissions.administrator == True or ctx.author.id in OWNERS:
            TOPICLOOP_CHANNELS.discard(ctx.channel.id)
            with open("database/topicloop_channels.txt", "w") as f:
                f.write("\n".join(str(i) for i in TOPICLOOP_CHANNELS))
                await ctx.send(f":imp: `{ctx.guild} is free from the extroverted purgatory.`")
        else:
            await ctx.send("You don't have permissions to use that command, you lil' delinquent!")

    
    async def topicloop(self):
        await self.dottie.wait_until_ready()
        while not self.dottie.is_closed():
            t = time.time()

            topic = random.choice(("misc/facts.txt", "misc/questions.txt"))
            with open(topic, "r", encoding="utf-8") as f:
                f = f.read()
                if topic == "misc/facts.txt":
                    opener = "fact"
                elif topic == "misc/questions.txt":
                    opener = "question"

                Topic = f.splitlines()
                for i in Topic:
                    if "sex" in i.lower() or "penis" in i.lower() or "suicide" in i.lower():
                        Topic.remove(i)

                for cid in TOPICLOOP_CHANNELS:
                    ctx = self.dottie.get_channel(cid)
                    if ctx:
                        openerlist = [
                            f"HEY THERE, IS THE SERVER DEAD?! Here's a {opener} to compensate: ",
                            f"You know what time it is, here's a {opener}: ",
                            f"I've got a {opener} for you: ",
                            f"Hey there, it's {opener} time: ",
                            f"We meet again, {ctx.guild}. Here's a {opener}: ",
                            f"Hope I'm not interrupting, but if I'm enabled let's be honest, interrupting what exactly? Here's a {opener}: ",
                            f"{opener.capitalize()} time! ",
                        ]
                        create_task(ctx.send(f"{random.choice(openerlist)}{random.choice(Topic)}"))

            self.dottie.next_time = 10800 + t
            while time.time() < self.dottie.next_time:
                await asyncio.sleep(1)


    @commands.command()
    @has_permissions(administrator=True)
    async def purge(self, ctx, amount=1):
        if amount == 1:
            await ctx.channel.purge(limit=amount+1)
            await ctx.send(f":broom: swept away **1** message!")
        elif amount > 0:
            await ctx.channel.purge(limit=amount+1)
            await ctx.send(f":broom: Swept away **{amount}** messages!")
        elif amount < 1:
            await ctx.send(f"How am I meant to purge **{amount}** messages, silly?".format(amount))


    @commands.command()
    @has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reasons=None):
        await member.ban(reason=reasons)
        await ctx.send(f"Good riddance, {member.name}#{member.discriminator}! :closed_lock_with_key:")


    @commands.command()
    @has_permissions(administrator=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"Granted access back to the server for {user.name}#{user.discriminator}. :unlock:")
                return

    
    @commands.command(pass_context=True)
    @has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reasons=None):
        await member.kick(reason=reasons)
        await ctx.send(f"{member.name}#{member.discriminator} has been *yeet* right out the server! :lock:")


def setup(dottie):
  moderation = MODERATION(dottie)
  dottie.add_cog(moderation)
  create_task(moderation.topicloop())