import asyncio
import csv
from datetime import datetime
import discord
from discord.ext import commands


class Lecture(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='start')
    async def lecture(self, ctx):
        embed = discord.Embed(description='Starting', color=discord.Color.from_rgb(114, 137, 218))
        message = await ctx.send(embed=embed)
        message.delete(delay=3)

        while True:
            while datetime.now().hour != 20:
                await asyncio.sleep(300)

            # Get the day index of the week starting from 0
            current_day_in_week_index = datetime.today().weekday()

            await ctx.send('@here')

            # TODO: Make the file open automatic corresponding to the day
            with open(f'rosters/timetable_2020-11-20.csv', 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Continue only if the row is on the correct day in the week
                    if self.get_lectures_for_day(row["Start day"]) != current_day_in_week_index:
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
