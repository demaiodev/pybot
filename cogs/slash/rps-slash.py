import random
import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands

from helpers import checks




class Choice(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.choice = None


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
        user1_choice = None
        user1_choice_index = None
        user2_choice = None
        user2_choice_index = None
        choices = {
            "rock": 0,
            "paper": 1,
            "scissors": 2,
        }
        if user1_choice is not None:
            # user 1 makes choice
            user1_choice = self.values[0].lower()
            user1_choice_index = choices[user1_choice]
            await interaction.send("User 1 made a choice")
            await interaction.send("User 2 needs to make a choice")
        else:
            # user 1 makes choice
            await interaction.send("User 2 made a choice")
            user2_choice = self.values[0].lower()
            user2_choice_index = choices[user2_choice]

        await interaction.response.defer()

        if user1_choice and user2_choice is not None:
            # calculate results and display
            result_embed = disnake.Embed(color=0x9C84EF)
            result_embed.set_author(
                name=interaction.author.display_name, icon_url=interaction.author.avatar.url)

            if user1_choice_index == user2_choice_index:
                result_embed.description = f"**That's a draw!**\nYou've chosen {user1_choice} and I've chosen {user2_choice}."
                result_embed.colour = 0xF59E42
            elif user1_choice_index == 0 and user2_choice_index == 2:
                result_embed.description = f"**You won!**\nYou've chosen {user1_choice} and I've chosen {user2_choice}."
                result_embed.colour = 0x9C84EF
            elif user1_choice_index == 1 and user2_choice_index == 0:
                result_embed.description = f"**You won!**\nYou've chosen {user1_choice} and I've chosen {user2_choice}."
                result_embed.colour = 0x9C84EF
            elif user1_choice_index == 2 and user2_choice_index == 1:
                result_embed.description = f"**You won!**\nYou've chosen {user1_choice} and I've chosen {user2_choice}."
                result_embed.colour = 0x9C84EF
            else:
                result_embed.description = f"**I won!**\nYou've chosen {user1_choice} and I've chosen {user2_choice}."
                result_embed.colour = 0xE02B2B
            user1_choice = None
            user1_choice_index = None
            user2_choice = None
            user2_choice_index = None
            await interaction.response.defer()
            await interaction.edit_original_message(embed=result_embed, content=None, view=None)


class RockPaperScissorsView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(RockPaperScissors())


class Rps(commands.Cog, name="Rps-slash"):
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
        await interaction.send("Please make your choice", view=view, ephemeral=True)


def setup(bot):
    bot.add_cog(Rps(bot))
