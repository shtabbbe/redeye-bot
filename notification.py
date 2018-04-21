import discord
from discord.ext import commands
import asyncio
from ticket import adminCheck
class notification():
    def __init__(self,bot):
        self.bot = bot
        self.notifications = []
        self.tasks = {}
        self.bot.remove_command('help')
        self.index = -1

    async def notifymessage(self,ctx,notifs):
        while True:
            await asyncio.sleep(0.001)
            while notifs["running"]:
                await asyncio.sleep(notifs["interval"])
                if notifs["running"]:
                    await ctx.send(notifs["message"])

    @commands.command()
    async def notify(self,ctx,name : str,interval : int, *message : str):
        if adminCheck(ctx.author):
            text = ' '.join(message)
            self.index += 1
            self.notifications.insert(0,dict())
            self.notifications[0]["name"] = name
            self.notifications[0]["interval"] = interval
            self.notifications[0]["message"] = text
            self.notifications[0]["running"] = True
            self.tasks[name] = self.bot.loop.create_task(self.notifymessage(ctx,self.notifications[0]))
            print(self.tasks[name])
        else:
            await ctx.send("Insufficient Permissions")

    @commands.command()
    async def turn(self,ctx, name: str,choice : str):
        if adminCheck(ctx.author):
            if choice == "on":
               for item in self.notifications:
                   if item["name"] == name:
                       item["running"] = True
            elif choice=="off":
               for item in self.notifications:
                   if item["name"] == name:
                       item["running"] = False
        else:
            await ctx.send("Insufficient Permissions")
    @commands.command()
    async def viewnotifications(self,ctx):
        if adminCheck(ctx.author):
            for item in self.notifications:
                run = "OFF"
                if item["running"]:
                    run = "ON"
                embed = discord.Embed(title="Name: " + item["name"], color=0xf73e42)
                embed.add_field(name="Interval: ", value=item["interval"], inline=True)
                embed.add_field(name="Message: ", value=item["message"], inline=True)
                embed.add_field(name="Status: ", value=run, inline=True)
                await ctx.send(embed=embed)
        else:
            await ctx.send("Insufficient Permissions")

    @commands.command()
    async def delnotification(self,ctx,name : str):
        if adminCheck(ctx.author):
            select = None
            for item in self.notifications:
                if item["name"]==name:
                    select=item["name"]
            try:
                self.tasks[select].cancel()
                self.notifications.remove(item)
                self.tasks.pop(select)
            except:
                await ctx.send("Notification not found")
        else:
            await ctx.send("Insufficient Permissions")


def setup(bot):
    bot.add_cog(notification(bot))