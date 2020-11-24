import asyncio
import csv
from datetime import datetime
import discord
from discord.ext import commands


class Lecture(commands.Cog):
    # The users that can send the bot commands
    allowed_ids = [368317619838779393]

    def __init__(self, client):
        self.client = client

    @commands.command(name='auth')
    async def auth_user(self, ctx, user_id):
        if not await self.is_auth_user(ctx):
            return

        # Add auth user
        self.allowed_ids.__add__(user_id)

        # Create a new Discord embed
        embed = discord.Embed(description=f':white_check_mark: User `{user_id}` succesfully added to the auth list!',
                              color=discord.Color.from_rgb(114, 137, 218))

        message = await ctx.send(embed=embed)
        await message.delete(delay=3)
        await ctx.message.delete(delay=3)

    @commands.command(name='start')
    async def lecture(self, ctx, show_now=False, debug_day=-2):
        if not await self.is_auth_user(ctx):
            return

        # Create a new Discord embed
        embed = discord.Embed(description='Starting to watch the roster', color=discord.Color.from_rgb(114, 137, 218))
        message = await ctx.send(embed=embed)
        await message.delete(delay=3)
        await ctx.message.delete(delay=3)

        while True:
            # Allow debugging when 'show_now' is set to 'True'
            if not show_now:
                while datetime.now().hour != 20:
                    await asyncio.sleep(300)

            # Get the day index of the week starting from 0
            current_day_in_week_index = datetime.today().weekday()

            # See the roster of the day you want starting from 0
            if debug_day != -2:
                current_day_in_week_index = debug_day

            # Mention everybody with access to that channel
            await ctx.send('@here')

            # Weekend message (Friday and Saturday)
            if current_day_in_week_index == 4 or \
                    current_day_in_week_index == 5:
                await self.weekend(ctx)
                return

            with open(f'rosters/timetable_2020-11-20.csv', 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Show the roster for monday when its Sunday
                    if current_day_in_week_index == 6:
                        current_day_in_week_index = -1

                    # Continue only if the row is on the correct day in the week
                    if self.get_lectures_for_day(row["Start day"]) != current_day_in_week_index + 1:
                        continue

                    # Check if there are more than 0 teachers, else replace teachers field with 'None'
                    teachers = row["Staff member(s)"]
                    if teachers == '':
                        teachers = 'None'

                    # Create a new Discord embed
                    embed = discord.Embed(color=discord.Color.from_rgb(114, 137, 218))
                    embed.add_field(name=':memo: Name:', value=f'`{row["Name"].capitalize()}`', inline=True)
                    embed.add_field(name=':man_teacher: Teacher(s):', value=f'`{teachers}`', inline=True)

                    # Check if the lecture has to be followed in a classroom, else leave blank
                    classroom = row["Room(s)"]
                    if classroom != '':
                        embed.add_field(name=':classical_building: Classroom:', value=classroom, inline=True)

                    embed.add_field(name=':date: Day and Time:',
                                    value=f'**{self.get_full_day_name(row["Start day"])}** '
                                          f'at **{row["Start time"]}** until **{row["End time"]}** '
                                          f'Total duration: **{row["Duration"]}**', inline=False)

                    # Send the embed
                    await ctx.send(embed=embed)

                # Sleep for 3601 seconds to make sure it only triggers the while loop once
                await asyncio.sleep(3601)

    async def weekend(self, ctx):
        embed = discord.Embed(description='It\'s weekend! :partying_face:',
                              color=discord.Color.from_rgb(114, 137, 218))
        await ctx.send(embed=embed)

    async def is_auth_user(self, ctx):
        # If the user is not authenticated, let the user know
        if ctx.author.id not in self.allowed_ids:
            # Create a new Discord embed
            embed = discord.Embed(description=':robot: I can only accept commands from authenticated users!',
                                  color=discord.Color.from_rgb(114, 137, 218))

            message = await ctx.send(embed=embed)
            await message.delete(delay=3)
            await ctx.message.delete(delay=3)
            return False

        return True

    def get_lectures_for_day(self, day: str):
        switch = {
            'Mon': 0,
            'Tue': 1,
            'Wed': 2,
            'Thu': 3,
            'Fri': 4,
        }

        return switch.get(day, 'Unknown day')

    def get_full_day_name(self, day: str):
        switch = {
            'Mon': 'Monday',
            'Tue': 'Tuesday',
            'Wed': 'Wednesday',
            'Thu': 'Thursday',
            'Fri': 'Friday',
        }

        return switch.get(day, 'Unknown day')


def setup(client):
    client.add_cog(Lecture(client))
