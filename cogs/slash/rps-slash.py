import random
import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands

from helpers import checks

class RockPaperScissors(disnake.ui.Select):
    def __init__(self):

        options = [
            disnake.SelectOption(
                label="Scissors", description="You choose scissors.", emoji="✂"
            ),
            disnake.SelectOption(
                label="Rock", description="You choose rock.", emoji="🪨"
            ),
            disnake.SelectOption(
                label="paper", description="You choose paper.", emoji="🧻"
            ),
        ]

        super().__init__(
            placeholder="Choose...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        choices = {
            "rock": 0,
            "paper": 1,
            "scissors": 2,
        }
        user_choice = self.values[0].lower()
        user_choice_index = choices[user_choice]

        opponent_choice = random.choice(list(choices.keys()))
        opponent_choice_index = choices[opponent_choice]

        result_embed = disnake.Embed(color=0x9C84EF)
        result_embed.set_author(name=interaction.author.display_name, icon_url=interaction.author.avatar.url)

        if user_choice_index == opponent_choice_index:
            result_embed.description = f"**That's a draw!**\nYou've chosen {user_choice} and I've chosen {opponent_choice}."
            result_embed.colour = 0xF59E42
        elif user_choice_index == 0 and opponent_choice_index == 2:
            result_embed.description = f"**You won!**\nYou've chosen {user_choice} and I've chosen {opponent_choice}."
            result_embed.colour = 0x9C84EF
        elif user_choice_index == 1 and opponent_choice_index == 0:
            result_embed.description = f"**You won!**\nYou've chosen {user_choice} and I've chosen {opponent_choice}."
            result_embed.colour = 0x9C84EF
        elif user_choice_index == 2 and opponent_choice_index == 1:
            result_embed.description = f"**You won!**\nYou've chosen {user_choice} and I've chosen {opponent_choice}."
            result_embed.colour = 0x9C84EF
        else:
            result_embed.description = f"**I won!**\nYou've chosen {user_choice} and I've chosen {opponent_choice}."
            result_embed.colour = 0xE02B2B
        await interaction.response.defer()
        await interaction.edit_original_message(embed=result_embed, content=None, view=None)


class RockPaperScissorsView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(RockPaperScissors())


class Rps(commands.Cog, name="rps-slash"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="rpss",
        description="Play the rock paper scissors game against the bot."
    )
    @checks.not_blacklisted()
    async def rock_paper_scissors(self, interaction: ApplicationCommandInteraction) -> None:
        """
        Play the rock paper scissors game against the bot.
        :param interaction: The application command interaction.
        """
        view = RockPaperScissorsView()
        await interaction.send("Please make your choice", view=view)


def setup(bot):
    bot.add_cog(Rps(bot))
