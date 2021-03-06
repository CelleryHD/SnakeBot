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
@commands.has_role('Admin')
async def addteam(ctx, *args):
        # If the amount of arguments is not correct then it explains how to use the command
        if len(args)!=1:
            await ctx.send("The format to use this command is: $addteam {teamname} (Remember the teamname should to be one word!)")
        else:
            roles = ctx.guild.roles
            teamName = args[0]
            # Creates a role for the team
            teamRole = await ctx.guild.create_role(name=str(teamName), colour=discord.Colour(int('9b59b6',16)))
            modRole = await getrolebyName('Moderator', roles)
            captainRole = await getrolebyName('Captain (2v2)', roles)
            everyoneRole = await getrolebyName('@everyone',roles)
            # Creates a category with the team name
            await ctx.guild.create_category(teamName)
            # Finds the category with the team name and sets it as the category to work on
            categories = ctx.guild.categories
            currentcategory = await getcategories(teamName, categories)
            # Sets the role and its perms for the category
            await currentcategory.set_permissions(teamRole, read_messages=True, view_channel=True, connect=True)
            await currentcategory.set_permissions(captainRole, move_members=True, connect=True, read_messages=True, view_channel=True)
            await currentcategory.set_permissions(modRole, read_messages=True, connect=True, manage_permissions=True, manage_messages=True, )
            await currentcategory.set_permissions(everyoneRole, read_messages=False, connect=False)
            # Creates all channels to the team name category
            await ctx.guild.create_text_channel("team-schedule", category=currentcategory)
            await ctx.guild.create_text_channel("team-availability", category=currentcategory)
            await ctx.guild.create_text_channel("team-discussion", category=currentcategory)
            await ctx.guild.create_text_channel("screenshots", category=currentcategory)
            await ctx.guild.create_text_channel("team-announcements", category=currentcategory)
            await ctx.guild.create_voice_channel(teamName, category=currentcategory)
            await ctx.send("Done!")

#Command to delete all channels related to the team
@bot.command(name="delteam")
@commands.has_role('Admin')
async def delteam(ctx, *args):
    # If the amount of arguments is not correct then it explains how to use the command
    if len(args)!=1:
        await ctx.send("The format to use this command is: $delteam {teamname} (Remember: teamname should be one word)")
    else:
        teamName = args[0]
        currentcategory = None
        categories = ctx.guild.categories
        # checks roles and deletes the team role
        roles = ctx.guild.roles
        role = await getrolebyName(teamName, roles)
        if role == None:
            await ctx.send("The role " + teamName + "does not exist")
        await role.delete()
        # Gets the category with the team name and checks if it exists
        currentcategory = await getcategories(teamName, categories)
        if(currentcategory==None):
            await ctx.send("The team " + teamName + " does not exist.")
        else:
            categoryID = currentcategory.id
            # Instantiates a list of channel objects to be deleted and a toggle to be switched when the team name has been found.
            channelsToDelete = []
            # Each channel is checked for the occurance of the category ID
            for channel in ctx.guild.channels:
                if(channel.category_id == categoryID):
                    channelsToDelete.append(channel)
            for channel in channelsToDelete:
                await channel.delete()
            await currentcategory.delete()
            await ctx.send("Done!")


@bot.command(name="categories")
@commands.has_role('Admin')
async def categories(ctx):
    categories = ctx.guild.categories
    for category in categories:
        print(category)

@bot.command(name="roles")
@commands.has_role('Admin')
async def roles(ctx):
    roles = ctx.guild.roles
    print(roles)
            

async def getcategories(teamName, categories):
    for category in categories:
        if category.name == teamName:
            return category
    return None

async def getrolebyID(roleID, roles):
    for role in roles:
        if role.id == roleID:
            return role
    return None

async def getrolebyName(roleName, roles):
    for role in roles:
        if role.name == roleName:
            return role

bot.run(TOKEN)