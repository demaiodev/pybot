import random
import os
import io
import base64
import disnake
import aiohttp
import dotenv
from disnake.ext import commands
from disnake.ext.commands import Context
from helpers import checks

dotenv.load_dotenv()
RAPI_KEY = os.environ.get("RAPI_KEY")
RAPI_URL = os.environ.get("RAPI_URL")


def handle_error(status):
    embed = disnake.Embed(
        title="Error!",
        description="There is something wrong with the API, please try again later",
        color=0xE02B2B
    )
    embed.set_image(f"https://http.cat/{status}")
    return embed


class Template(commands.Cog, name="template-normal"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="choose"
    )
    @checks.not_blacklisted()
    async def choose(self, context: Context, *names):
        await context.send(embed=disnake.Embed(
            title="Who's it gonna be...",
            description=f"I choose {random.choice(list(names)).capitalize()}!",
            color=random.randint(0, 0xFFFFFF)
        ))

    @commands.command(
        name="joke"
    )
    @checks.not_blacklisted()
    async def joke(self, context: Context):
        async with aiohttp.ClientSession() as session:
            async with session.request("GET", 'https://jokeapi-v2.p.rapidapi.com/joke/Any', headers={
                "X-RapidAPI-Key": RAPI_KEY,
                "X-RapidAPI-Host": "jokeapi-v2.p.rapidapi.com"
            }) as request:
                if request.status == 200:
                    data = await request.json()
                    title, description = '', ''
                    if (data["type"] == "single"):
                        title, description = 'Joke Time', data["joke"]
                    else:
                        title, description = data["setup"], data["delivery"]
                    embed = disnake.Embed(
                        title=title,
                        description=description,
                        color=random.randint(0, 0xFFFFFF)
                    )

                else:
                    embed = handle_error(request.status)
                await context.send(embed=embed)

    @commands.command(
        name="generateimage"
    )
    @checks.not_blacklisted()
    async def generateimage(self, context: Context, search, x=1):
        async with aiohttp.ClientSession() as session:
            await context.send(embed=disnake.Embed(title=f"Brb, getting {search}."))
            async with session.post("https://bf.dallemini.ai/generate",
                                    json={"prompt": search}) as request:
                if request.status == 200:
                    data = await request.json()
                    for n in range(x):
                        file = disnake.File(io.BytesIO(
                            base64.b64decode(data["images"][n])), f"{search}.jpg")
                        await context.send(file=file)
                else:
                    await context.send(embed=handle_error(request.status))

    @commands.command(
        name="roll",
        description="Roll some dice (between 1 and x).",
    )
    @checks.not_blacklisted()
    async def roll(self, context: Context, number: int) -> None:
        if number <= 42069:
            roll = random.randint(1, number)
            text = ""
            if roll >= number/2:
                text = "😏 📈 Not Bad! 📈 😏"
            else:
                text = "😪 📉 😪 📉 😪"
            embed = disnake.Embed(
                title="🎲  🎲  🎲",
                description=f"You rolled {roll} out of {number}!",
                color=random.randint(0, 0xFFFFFF)
            )
            embed.set_footer(
                text=text
            )
            await context.send(embed=embed)

    @commands.command(
        name="waifu"
    )
    @checks.not_blacklisted()
    async def waifu(self, context: Context, category="waifu", type="sfw"):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.waifu.pics/{type}/{category}') as request:
                if request.status == 200:
                    data = await request.json()
                    embed = disnake.Embed(
                        title=f'Your {category}, sir.',
                        description="😍",
                        color=random.randint(0, 0xFFFFFF)
                    )
                    embed.set_image(data["url"])
                else:
                    embed = handle_error(request.status)
                await context.send(embed=embed)

    @commands.command(
        name="affirmation"
    )
    @checks.not_blacklisted()
    async def affirmation(self, context: Context):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.affirmations.dev/") as request:
                if request.status == 200:
                    data = await request.json()
                    embed = disnake.Embed(
                        description=data["affirmation"],
                        color=random.randint(0, 0xFFFFFF)
                    )
                else:
                    embed = handle_error(request.status)
                await context.send(embed=embed)


def setup(bot):
    bot.add_cog(Template(bot))
