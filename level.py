import discord
from discord.ext import commands
import asyncio
import sqlite3
import math
from ticket import adminCheck

class mainDB():
    def __init__(self,bot):
        self.bot = bot
        conn = sqlite3.connect('levels.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS lvl(dID BIGINT,xp INT, level INT)')
        conn.commit()
        c.close()
        conn.close()
        #replace these roles
        self.role_5 = 428689668129685505
        self.role_10 = 428702194615975936
        self.role_15 = 428702200911626240
        self.role_20 = 428702907580547072
        self.role_25 = 428703307801034753
        self.role_30 = 428703861050703879
        self.role_50 = 428704119352590336

    async def on_command_error(self,ctx,error):
        if ctx.command.name == "rank":
            conn = sqlite3.connect('levels.db')
            c = conn.cursor()
            c.execute('SELECT dID,xp,level FROM lvl ORDER BY level DESC')
            n = 0
            returnvalue = c.fetchall()
            total = str(len(returnvalue))
            for item in returnvalue:
                n += 1
                if item[0] == ctx.author.id:
                    level = item[2]
                    xp = item[1]
                    rank = n
                    user = item[0]
                    base = 10
                    multiplier = 1.4
                    xptolevel = math.floor(base * math.pow(level, multiplier))
                    member = discord.utils.get(ctx.guild.members, id=user)
                    await ctx.send(member.mention + " is level: `" + str(level) + "` and has: `" + str(xp) + "/" + str(
                        xptolevel) + "`XP and is rank: `" + str(rank) + "/" + str(total) + "`")
                    c.close()
                    conn.close()
                    break
    async def on_message(self,message):
        conn = sqlite3.connect('levels.db')
        c = conn.cursor()
        id = message.author.id
        if not message.author.bot:
            try:
                if not message.channel.id==424789301742665738 and not message.channel.id==424661957166235658:
                    c.execute('UPDATE lvl SET xp=xp+1 WHERE dID=?', (id,))
                    conn.commit()
                    c.execute('SELECT xp,level FROM lvl WHERE dID=?', (id,))
                    nume = c.fetchone()
                    base = 10
                    multiplier = 1.4
                    xptolevel = math.floor(base * math.pow(nume[1],multiplier))
                    if nume[0] >= xptolevel:
                        c.execute('UPDATE lvl SET xp=0,level=level+1 WHERE dID=?', (id,))
                        conn.commit()
                        c.execute('SELECT level FROM lvl WHERE dID=?',(id,))
                        nums = c.fetchone()[0]
                        await message.channel.send(message.author.mention + " has leveled up to: " + str(nums))
                    if nume[1] >= 5 and nume[1] < 10:
                        await self.removeAll(message,message.author)
                        await message.author.add_roles(discord.utils.get(message.guild.roles, id=self.role_5))
                    if nume[1] >= 10 and nume[1] < 15:
                        await self.removeAll(message, message.author)
                        await message.author.add_roles(discord.utils.get(message.guild.roles, id=self.role_10))
                    if nume[1] >= 15 and nume[1] < 20:
                        await self.removeAll(message, message.author)
                        await message.author.add_roles(discord.utils.get(message.guild.roles, id=self.role_15))
                    if nume[1] >= 20 and nume[1] < 25:
                        await self.removeAll(message, message.author)
                        await message.author.add_roles(discord.utils.get(message.guild.roles, id=self.role_20))
                    if nume[1] >= 25 and nume[1] < 30:
                        await self.removeAll(message, message.author)
                        await message.author.add_roles(discord.utils.get(message.guild.roles, id=self.role_25))
                    if nume[1] >= 30 and nume[1] < 50:
                        await self.removeAll(message, message.author)
                        await message.author.add_roles(discord.utils.get(message.guild.roles, id=self.role_30))
                    if nume[1] >= 50:
                        await self.removeAll(message,message.author)
                        await message.author.add_roles(discord.utils.get(message.guild.roles, id=self.role_50))
                    c.close()
                    conn.close()
                else:
                    print("value no")
            except TypeError as e:
                conn = sqlite3.connect('levels.db')
                c = conn.cursor()
                print(e)
                c.execute('INSERT INTO lvl VALUES(?,?,?)', (message.author.id, 1, 1))
                conn.commit()
                c.close()
                conn.close()

    @commands.command()
    async def leaders(self,ctx):
        conn = sqlite3.connect('levels.db')
        c = conn.cursor()
        n = 0
        total = len(ctx.guild.members)
        c.execute('SELECT dID,level FROM lvl ORDER BY level DESC')
        embed = discord.Embed(title="Leaderboard", description="Top 5 ranked members", color=0xed474b)
        for item in c.fetchall():
            n+=1
            if n >= 20: break
            person = discord.utils.get(ctx.guild.members, id=item[0])
            try:
                embed.add_field(name=str(n)+". "+person.name,value="Level: "+str(item[1]),inline=False)
            except:
                pass
        await ctx.send(embed=embed)

        c.close()
        conn.close()
    @commands.command()
    async def rank(self,ctx, person : discord.Member):
        conn = sqlite3.connect('levels.db')
        c = conn.cursor()
        c.execute('SELECT dID,xp,level FROM lvl ORDER BY level DESC')
        n = 0
        returnvalue = c.fetchall()
        total = str(len(returnvalue))
        for item in returnvalue:
            n += 1
            if item[0]== person.id:

                level = item[2]
                xp = item[1]
                rank = n
                user = item[0]
                base = 10
                multiplier = 1.4
                xptolevel = math.floor(base * math.pow(level, multiplier))
                member = discord.utils.get(ctx.guild.members, id=user)
                await ctx.send(member.mention+" is level: `"+str(level)+"` and has: `"+str(xp)+"/"+str(xptolevel)+"`XP and is rank: `"+str(rank)+"/"+str(total)+"`")
                c.close()
                conn.close()
                break
    @commands.command()
    async def set(self,ctx,person : discord.Member,type: str,amount : int):
        if adminCheck(ctx.author):
            set = False
            conn = sqlite3.connect('levels.db')
            c = conn.cursor()
            #change to redeye channel
            channel=discord.utils.get(ctx.guild.channels,id=434103345255415808)
            changeme=person.id
            if type=="xp":
                set = True
                c.execute('UPDATE lvl SET xp=? WHERE dID=?',(amount,changeme))
                conn.commit()
            if type=="level":
                c.execute('UPDATE lvl SET level=? WHERE dID=?',(amount,changeme))
                conn.commit()
            if set:
                await channel.send(ctx.author.display_name+ " set "+person.display_name+"'s xp to `"+str(amount)+"`")
            else:
                await channel.send(ctx.author.display_name + " set " + person.display_name + "'s level to `" + str(amount) + "`")
            c.close()
            conn.close()

    @commands.command()
    async def add(self, ctx, person: discord.Member, type: str, amount: int):
        if adminCheck(ctx.author):
            add = False
            conn = sqlite3.connect('levels.db')
            c = conn.cursor()
            # change to redeye channel
            channel = discord.utils.get(ctx.guild.channels, id=434103345255415808)
            changeme = person.id
            if type == "xp":
                add = True
                c.execute('UPDATE lvl SET xp=xp+? WHERE dID=?', (amount, changeme))
                conn.commit()
            if type == "level":
                c.execute('UPDATE lvl SET level=level+? WHERE dID=?', (amount, changeme))
                conn.commit()
            if add:
                await channel.send(
                    ctx.author.display_name + " added " + person.display_name + "'s xp to `" + str(amount) + "`")
            else:
                await channel.send(
                    ctx.author.display_name + " added " + person.display_name + "'s level to `" + str(amount) + "`")
            c.close()
            conn.close()
    async def removeAll(self,ctx,user):
        role5 = discord.utils.get(ctx.guild.roles,id=self.role_5)
        role10 = discord.utils.get(ctx.guild.roles, id=self.role_10)
        role15 = discord.utils.get(ctx.guild.roles, id=self.role_15)
        role20 = discord.utils.get(ctx.guild.roles, id=self.role_20)
        role25 = discord.utils.get(ctx.guild.roles, id=self.role_25)
        role30 = discord.utils.get(ctx.guild.roles, id=self.role_30)
        role50 = discord.utils.get(ctx.guild.roles, id=self.role_50)
        await user.remove_roles(role5,role10,role15,role20,role25,role30,role50)
def setup(bot):
    bot.add_cog(mainDB(bot))
