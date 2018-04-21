import discord
from discord.ext import commands
from requests_html import HTMLSession

class Misc():
    def __init__(self,bot):
        self.bot = bot
        self.session = HTMLSession()
    @commands.command()
    async def status(self,ctx):
        loading = await ctx.send("Loading status...")
        rr = self.session.get('https://redeyecheats.com/pages/CSGO-Pro-Cheats/')
        detected = rr.html.find('.gridCheatInfoText')[3].text
        if detected=="Undetected":
            await loading.edit(content="The cheat is currently undetected! :thumbsup:")
        else:
            await loading.edit(content="The cheat is DETECTED :thumbsdown:")
    @commands.command()
    async def helpme(self,ctx):
        await ctx.send("Learn what the commands do here: https://github.com/shtabbbe/redeye-bot#redeye-bot")
    @commands.command()
    async def donate(self,ctx):
        embed = discord.Embed(title="Donate to Redeye",description="Support the Redeye Staff and Dev's and gain the 'Donator' role on discord and the forums",color=0xdb2b2b)
        embed.add_field(name="Donate using PayPal",value="https://goo.gl/oyJPPE")
        embed.add_field(name="Donate using PaymentWall", value="https://goo.gl/kJSJcw")
        await ctx.send(embed=embed)
    @commands.command()
    async def changelog(self,ctx):
        await ctx.send("""""``` Redeye bot update V3.4:
        
        Added a way to see your XP using !rec rank
        Added a way to see other peoples rank using !rec rank @user
        Nerfed leveling
        Fixed a bug where your role didn't get updated
        Fixed a bug where !rec status would get stuck on loading
        Added some sick admin commands
        Added this command
        ```""")


def setup(bot):
    bot.add_cog(Misc(bot))