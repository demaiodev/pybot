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
RAPI_KEY2 = os.environ.get("RAPI_KEY2")
RAPI_URL = os.environ.get("RAPI_URL")

headers = {
    "Authorization": RAPI_KEY,
    "X-RapidAPI-Key": RAPI_KEY2,
    "X-RapidAPI-Host": "random-stuff-api.p.rapidapi.com"
}

def list_to_string(arg):
    """
    transform a list of words into a single string
    """
    value = ''
    for item in arg:
        value = value + item + " "
    return value

# Here we name the cog and create a new class for the cog.


class Template(commands.Cog, name="template-normal"):
    def __init__(self, bot):
        self.bot = bot
       
    @commands.command(
        name="joke"
    )
    @checks.not_blacklisted()
    async def joke(self, context: Context):
      
        async with aiohttp.ClientSession() as session:
            async with session.request("GET", f'{RAPI_URL}/joke', headers=headers) as request:
                if request.status == 200:
                    data = await request.json()
                    embed = disnake.Embed(
                        title="Joke Time",
                        description=data["joke"],
                        color=random.randint(0, 0xFFFFFF)
                    )
                else:
                    embed = disnake.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B
                    )
                await context.send(embed=embed)

    @commands.command(
        name="chatbot"
    )
    @checks.not_blacklisted()
    async def chatbot(self, context: Context, *text):
        str = list_to_string(text).capitalize()
        async with aiohttp.ClientSession() as session:
            async with session.request("GET", f'{RAPI_URL}/ai', params={
                "msg": str
            },
                headers=headers) as request:
                if request.status == 200:
                    data = await request.json()
                    embed = disnake.Embed(
                        title=str,
                        description=data["AIResponse"],
                        color=random.randint(0, 0xFFFFFF)
                    )
                else:
                    embed = disnake.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B
                    )
                await context.send(embed=embed)

    @commands.command(
        name="generateimage"
    )
    @checks.not_blacklisted()
    async def generateimage(self, context: Context, *search):
        async with aiohttp.ClientSession() as session:
            await context.send(embed=disnake.Embed(title=f"Brb, getting {list_to_string(search)}."))
            prompt = list_to_string(search)
            async with session.post("https://bf.dallemini.ai/generate",
                json={"prompt": prompt}) as request:
                print(request)
                if request.status == 200:
                    data = await request.json()
                    file = disnake.File(io.BytesIO(base64.b64decode(data["images"][0])), f"{prompt}.jpg")
                    await context.send(file=file)
                else:
                    await context.send(embed=disnake.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B
                    ))

    @commands.command(
        name="roll",
        description="Roll some dice (between 1 and x).",
    )
    @checks.not_blacklisted()
    @checks.is_owner()
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
                    embed = disnake.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B
                    )
                await context.send(embed=embed)

    @commands.command(
        name="affirmation"
    )
    @checks.not_blacklisted()
    async def affirmation(self, context: Context):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.affirmations.dev/") as request:
                print(request)
                if request.status == 200:
                    data = await request.json()
                    embed = disnake.Embed(
                        description=data["affirmation"],
                        color=random.randint(0, 0xFFFFFF)
                    )
                else:
                    embed = disnake.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B
                    )
                await context.send(embed=embed)

def setup(bot):
    bot.add_cog(Template(bot))
