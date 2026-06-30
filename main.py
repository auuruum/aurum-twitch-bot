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


def format_elo(data):
    return f"ELO: {data['elo']}, LVL: {data['lvl']}, Today: {data['telo']}, W: {data['tw']}, L: {data['tl']}"


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token=env("TOKEN"), prefix=['!', '?', '$'], initial_channels=['auurummm'])

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    @commands.command(name="links", aliases=("link",))
    async def link_command(self, ctx: commands.Context):
        print(f"Links command invoked by {ctx.author.name}")
        await ctx.send('https://auuruum.github.io')

    @commands.command(name="help", aliases=("commands", "command"))
    async def help_command(self, ctx: commands.Context):
        print(f"Help command invoked by {ctx.author.name}")
        command_list = ', '.join([command.name for command in self.commands.values()])
        await ctx.send(f'Available commands: {command_list}')

    @commands.command(name="steam")
    async def steam_command(self, ctx: commands.Context):
        print(f"Steam command invoked by {ctx.author.name}")
        await ctx.send('https://steamcommunity.com/id/auuruum')

    @commands.command(name="youtube")
    async def youtube_command(self, ctx: commands.Context):
        print(f"Youtube command invoked by {ctx.author.name}")
        await ctx.send('https://youtube.com/@auurummm')

    @commands.command(name="website")
    async def website_command(self, ctx: commands.Context):
        print(f"Website command invoked by {ctx.author.name}")
        await ctx.send('https://auuruum.github.io')

    @commands.command(name="elo")
    async def elo_command(self, ctx: commands.Context):
        try:
            response = requests.get(env("STRUGLY_URL"), timeout=5)
            response.raise_for_status()
            data = response.json()
            print(f"ELO command invoked by {ctx.author.name}")
            await ctx.send(format_elo(data))

        except (requests.RequestException, ValueError, KeyError) as e:
            print(f"Error fetching ELO data: {e}")
            await ctx.send("Error fetching ELO data. Try again later.")

if __name__ == "__main__":
    missing = [name for name in REQUIRED_ENV if not os.getenv(name)]
    if missing:
        raise RuntimeError(f"Missing required .env values: {', '.join(missing)}")

    bot = Bot()
    bot.run()
