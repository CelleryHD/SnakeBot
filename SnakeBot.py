# bot.py
import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix="$")

#Command to create all channels with the team name
@bot.command(name="addteam")
async def addteam(ctx, *args):
    # If the amount of arguments is not correct then it explains how to use the command
    if len(args)!=2:
        await ctx.send("The format to use this command is: $addteam {tier} {teamname}")
    else:
        # Instantiates the arguments into variables
        #tier = args[0]
        roles = ctx.guild.roles
        teamName = args[1]
        teamRole = await ctx.guild.create_role(name=teamName)
        modRole = await getrole(585433328354721825, roles)
        captainRole = await getrole(585433197106561035, roles)
        adminRole = await getrole(585213220764123186, roles)
        # Creates a category with the team name
        await ctx.guild.create_category(teamName)
        # Finds the category with the team name and sets it as the category to work on
        categories = ctx.guild.categories
        currentcategory = await getcategories(teamName, categories)
        # Sets the role and its perms for the category
        await currentcategory.set_permissions(teamRole, read_messages=True, view_channel=True, connect=True)
        await currentcategory.set_permissions(captainRole, move_members=True, connect=True, read_messages=True, view_channel=True)
        await currentcategory.set_permissions(modRole, read=True, connect=True)
        await currentcategory.set_permissions(adminRole, administrator=True)
        # Creates all channels to the team name category
        await ctx.guild.create_text_channel("team-schedule", category=currentcategory)
        await ctx.guild.create_text_channel("team-availability", category=currentcategory)
        await ctx.guild.create_text_channel("team-discussion", category=currentcategory)
        await ctx.guild.create_text_channel("screenshots", category=currentcategory)
        await ctx.guild.create_text_channel("team-announcements", category=currentcategory)
        await ctx.guild.create_voice_channel(teamName, category=currentcategory)

#Command to delete all channels related to the team
@bot.command(name="delteam")
async def delteam(ctx, *args):
    teamName = args[0]
    currentcategory = None
    categories = ctx.guild.categories
    # If the amount of arguments is not correct then it explains how to use the command
    if len(args)!=1:
        await ctx.send("The format to use this command is: $delteam {teamname}")
    else:
        # Gets the category with the team name and checks if it exists
        currentcategory = await getcategories(teamName, categories)
        if(currentcategory==None):
            await ctx.send("The team " + teamName + " does not exist.")
        else:
            # Instantiates a list of channel objects to be deleted and a toggle to be switched when the team name has been found.
            channelsToDelete = []
            channeltoggle = False 
            # Each channel is checked for the occurance of the team name
            for channel in ctx.guild.channels:
                # Finds the first occurance of the team name, if it is the team name the toggle is switched and the channel is added to a list to be deleted
                if channel.name == teamName:
                    channeltoggle = True
                    channelsToDelete.append(channel)
                    # If the toggle has been switched then add all channels to the list until the team name is found again
                elif channeltoggle == True:
                    if channel.name == teamName:
                        channeltoggle = False
                    channelsToDelete.append(channel)
            # Delete all channels in the list.
            for channel in channelsToDelete:
                await channel.delete()

async def getcategories(teamName, categories):
    for category in categories:
        if category.name == teamName:
            return category
    return None

async def getrole(roleID, roles):
    for role in roles:
        if role.id == roleID:
            return role
    return None

bot.run(TOKEN)