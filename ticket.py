import discord
from discord.ext import commands

class Tickets():
    def __init__(self,bot):
        self.bot = bot
        self.tickets = []
        self.id = 0

    @commands.command()
    async def ticket(self,ctx,*args):
        message = ' '.join(args)
        author = ctx.author
        self.tickets.insert(0,dict())
        self.tickets[0]["author"] = author
        self.tickets[0]["message"] = message
        self.tickets[0]["id"] = self.id
        self.id += 1
        await ctx.send("Ticket created it ID: `"+str(self.tickets[0]["id"])+"` To delete this ticket, type: `!rec delete "+str(self.tickets[0]["id"])+"`")

    @commands.command()
    async def viewtickets(self,ctx):
        if self.adminCheck(ctx.author):
            buffer = False
            for item in self.tickets:
                buffer = True
                embed = discord.Embed(color=0xdb2b2b)
                embed.add_field(name="ID: "+str(item["id"]),value=item["message"]+". ")
                embed.add_field(name="Sent by:",value=item["author"].display_name)
                await ctx.send(embed=embed)
            if not buffer:
                await ctx.send("All tickets have been resolved, thanks for helping the community")
        else:
            await ctx.send("Insufficent Permissions")
    @commands.command()
    async def resolve(self,ctx,index : int,*message):
        if self.adminCheck(ctx.author):
            text = ' '.join(message)
            for item in self.tickets:
                if item["id"] == index:
                    auth = item["author"]
                    message = item["message"]
                    self.tickets.remove(item)
            try:
                await auth.send(ctx.author.display_name+ """ has responded to your ticket:

    You said: """+item["message"]+"""

    Answer: """+text+"""
                """)
            except:
                await ctx.send("Ticket not found, make sure you have the right ID and format")
        else:
            await ctx.send("Insufficent Permissions")

    @commands.command()
    async def delete(self,ctx,id : int):
        buffer = False
        for item in self.tickets:
            if item["id"]==id and item["author"] == ctx.author or self.adminCheck(ctx.author):
                buffer = True
                self.tickets.remove(item)
                await ctx.send("Ticket has been removed!")
        if not buffer:
            await ctx.send("You cannot delete someone else's ticket.")


    def adminCheck(self,user):
        for id in user.roles:
            if id.id==423523019663736842:
                return True
        return False

def setup(bot):
    bot.add_cog(Tickets(bot))
