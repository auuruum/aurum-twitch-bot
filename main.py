from dotenv import load_dotenv
import os

from twitchio.ext import commands
import requests

load_dotenv()

REQUIRED_ENV = ("TOKEN", "STRUGLY_URL")


def env(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing {name} in .env")
    return value


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token=env("TOKEN"), prefix=['!', '?', '$'], initial_channels=['auurummm'])

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    @commands.command(name="links", aliases=("link",))
    async def link_command(self, ctx: commands.Context):
        await ctx.send('https://auuruum.github.io')

    @commands.command(name="help", aliases=("commands", "command"))
    async def help_command(self, ctx: commands.Context):
        command_list = ', '.join([command.name for command in self.commands.values()])
        await ctx.send(f'Available commands: {command_list}')

    @commands.command(name="steam")
    async def steam_command(self, ctx: commands.Context):
        await ctx.send('https://steamcommunity.com/id/auuruum')

    @commands.command(name="youtube")
    async def youtube_command(self, ctx: commands.Context):
        await ctx.send('https://youtube.com/@auurummm')

    @commands.command(name="website")
    async def website_command(self, ctx: commands.Context):
        await ctx.send('https://auuruum.github.io')

    @commands.command(name="elo")
    async def elo_command(self, ctx: commands.Context):
        try:
            # Fetch data from the API
            response = requests.get(env("STRUGLY_URL"))
            data = response.json()

            # Extract and format the ELO information
            message = f"ELO: {data['elo']}, LVL: {data['lvl']}, Today: {data['telo']}, W: {data['tw']}, L: {data['tl']}"
            await ctx.send(message)

        except Exception as e:
            print(f"Error fetching ELO data: {e}")
            await ctx.send("Error fetching ELO data. Try again later.")

missing = [name for name in REQUIRED_ENV if not os.getenv(name)]
if missing:
    raise RuntimeError(f"Missing required .env values: {', '.join(missing)}")

bot = Bot()
bot.run()
