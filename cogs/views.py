import discord
from .menu_data import MENU_DATA


class CategoryDropdown(discord.ui.Select):
    def __init__(self, category):
        self.category = category
        options = [
            discord.SelectOption(
                label=item,
                value=item
            )
            for item in MENU_DATA[category]
        ]

        super().__init__(
            placeholder=f"Select a {category} Item",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        # Get the selected item
        item = self.values[0]

        # Look up the description
        description = MENU_DATA[self.category][item]

        # Create a brand new view (all dropdowns reset)
        new_view = MenuView()

        # Reset the dropdowns by editing the original message
        await interaction.response.edit_message(view=new_view)

        # Send the description privately to the user
        await interaction.followup.send(
            description,
            ephemeral=True
        )


class MenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(CategoryDropdown("Red"))
        self.add_item(CategoryDropdown("Blue"))
        self.add_item(CategoryDropdown("Green"))
        self.add_item(CategoryDropdown("Yellow"))