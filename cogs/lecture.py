import asyncio
import csv
from datetime import datetime
import discord
from discord.ext import commands

"""
Summary:
    Send a Discord embed
"""
async def send_discord_embed(ctx: commands.Context, description: str, delete_after_seconds=False):
    # Create a Discord embed
    embed = discord.Embed(description=description,
                          color=discord.Color.from_rgb(114, 137, 218))
    # Add the footer is the message will not get deleted afterwards
    if delete_after_seconds:
        embed.set_footer(text='This message will automatically delete.')

    # Send the embed and delete it x seconds later
    message = await ctx.send(embed=embed)
    if delete_after_seconds:
        await message.delete(delay=7)


class Lecture(commands.Cog):

    owner_id = 368317619838779393

    @commands.command(name='start')
    async def start(self, ctx: commands.Context, force_start=False, force_day=-2):
        # Delete the user's message
        await ctx.message.delete(delay=0)

        # Only allow commands from the bot owner
        if ctx.author.id != self.owner_id:
            await send_discord_embed(ctx, description=':robot: Apologies, I can only accept commands from my owner.',
                                     delete_after_seconds=True)
            return

        # Let the user know the bot is running
        await send_discord_embed(ctx, description=':robot: _Beep Boop_! Starting to watch the rosters. You will receive'
                                                  ' notifications **around 20:00** every day with the roster for'
                                                  ' tomorrow.')

        while True:
            if not force_start:
                # While the hour of the day is not 20, sleep for 5 minutes and check again
                while datetime.now().hour != 20:
                    await asyncio.sleep(300)

            # Get the current day starting from 0
            current_weekday = datetime.now().weekday()

            # Execute if the force_day is set (-2 represents non-existing day)
            if force_day != -2:
                current_weekday = force_day

            # Set 6 to -1 to get the roster for Monday whenever its Sunday
            if current_weekday == 6:
                current_weekday = -1

            # Open the roster file and read the data inside
            with open('./rosters/roster.csv', 'r') as csv_file:
                await ctx.send(content='@here')

                reader = csv.DictReader(csv_file)
                # Loop through each row in the csv file
                row_index = -2
                for row in reader:
                    row_index += 1
                    # Executes whenever its weekend day tomorrow
                    # Weekday 4 is Friday and weekday 5 is Saturday
                    if current_weekday + 1 == 5 or current_weekday + 1 == 6:
                        await send_discord_embed(ctx, description=f':beers: **{self.get_full_weekday(current_weekday + 1)}**'
                                                                  f' is a weekend day! You\'re free tomorrow!')
                        return

                    # Loop until there has been a roster day found that is equal to the day of the current weekday + 1
                    if row["Start day"] != self.get_weekday(current_weekday + 1):
                        if row_index == current_weekday + 1:
                            await send_discord_embed(ctx, description=f':partying_face: On'
                                                                      f' **{self.get_full_weekday(current_weekday + 1)}**'
                                                                      f' there were to lectures found! You\'re free '
                                                                      f'tomorrow!')
                            return
                        continue

                    # Check if there are more than 0 teachers, else replace teachers field with 'None'
                    teachers = row["Staff member(s)"]
                    if teachers == '':
                        teachers = 'None'

                    # Create a Discord embed
                    embed = discord.Embed(color=discord.Color.from_rgb(114, 137, 218))
                    embed.add_field(name=':memo: Name:', value=f'`{row["Name"].capitalize()}`', inline=True)
                    embed.add_field(name=':man_teacher: Teacher(s):', value=f'`{teachers}`', inline=True)

                    # Check if the lecture has to be followed in a classroom, else leave blank
                    classroom = row["Room(s)"]
                    if classroom != '':
                        embed.add_field(name=':classical_building: Classroom:', value=classroom, inline=True)

                    embed.add_field(name=':date: Day and Time:',
                                    value=f'On **{self.get_full_weekday(current_weekday + 1)}**'
                                          f' starting at **{row["Start time"]}** until **{row["End time"]}**'
                                          f' \nTotal duration: **{row["Duration"]}**', inline=False)

                    # Send the embed
                    await ctx.send(embed=embed)

            # Wait six minutes shorter than a day and re-run the code above
            await asyncio.sleep(85800)

    """
    Get the first 3 letters of the day (used for equations)
    """
    def get_weekday(self, weekday: int):
        switch = {
            0: 'Mon',
            1: 'Tue',
            2: 'Wed',
            3: 'Thu',
            4: 'Fri',
            5: 'Sat',
            6: 'Sun'
        }

        return switch.get(weekday, 'Unknown weekday')

    """
    Get the full name of the day (used for output)
    """
    def get_full_weekday(self, weekday: int):
        switch = {
            0: 'Monday',
            1: 'Tuesday',
            2: 'Wednesday',
            3: 'Thursday',
            4: 'Friday',
            5: 'Saturday',
            6: 'Sunday'
        }

        return switch.get(weekday, 'Unknown weekday')


def setup(client):
    client.add_cog(Lecture(client))
