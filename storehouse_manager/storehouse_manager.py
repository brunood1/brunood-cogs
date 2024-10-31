# Required by Red.
import discord
import typing
from redbot.core import commands
from redbot.core.bot import Red

import json
import os.path

# Configure files.
current_folder = os.path.dirname(os.path.realpath(__file__))  # Get the directory in which this codefile is located.
data_folder = os.path.join(current_folder, "data")  # Get its subdirectory named "data".

# ...

json_filepath = os.path.join(data_folder, "test.json")  # Get the "dict.json" in the subdirectory.
with open(json_filepath, "r") as f:  # Load the data (read-only) from the aforementioned file.
    ids = json.load(f)


class Storehouse(commands.Cog):
    """Commands for managing the national final channels in the Eurovision Discord"""

    __author__ = "brunood"
    __red_end_user_data_statement__ = "No user data is stored by this cog."
    
    X = ":x: Error ::: "

    CHANNEL_RENAME = ":white_check_mark: Channel renamed to {}"
    CHANNEL_NO_PERMS = X + "I need 'Manage {}' permissions in {}"
    CHANNEL_NO_NAME = X + "The new name can't be blank"
    ADD_RED_CIRCLE = ":white_check_mark: Added :red_circle: to {}"
    REMOVE_RED_CIRCLE = ":white_check_mark: Removed :red_circle: from {}"
    MOVED_FROM_STOREHOUSE = "Moved {} from the storehouse"
    MOVED_TO_STOREHOUSE = "Moved {} to the storehouse"
    CHANNEL_OPENED = "Channel {} is already opened"
    CHANNEL_CLOSED = "Channel {} is already closed"

    def __init__(self, bot: Red):
        super().__init__()
        self.bot = bot

    # Commands        
    @commands.command()
    @commands.guild_only()
    @commands.admin_or_permissions(manage_channels=True)
    async def storehouse(
        self,
        ctx: commands.Context,
        status: typing.Literal["open", "close"],
        channel: discord.TextChannel
        ):
        """Moves a channel to and from the storehouse"""
        
        mention = channel.mention
        
        # DEFINING THE CATEGORIES BASED ON THEIR ID (esc id)
        # strhouse = discord.utils.get(channel.guild.categories, id=356050097152327680) 
        # national = discord.utils.get(channel.guild.categories, id=1104339301283663902)
        
        # (test server id)
        strhouse = discord.utils.get(channel.guild.categories, id=1198407644021522452) 
        national = discord.utils.get(channel.guild.categories, id=1198634992796975115)
        
        # dictionaries that will store the channels currently in use (separated by if the have a red circle)
        # and the channels not in use (in the storehouse)
        # required to make sure the channels get sorted alphabetically when they're opened or closed
        current_channels = {}
        red_channels = {}
        storehouse_channels = {}
        
        x = national.text_channels # aux variable, all channels currently in use
        y = strhouse.text_channels # aux variable, all channels not in use (storehouse)
                
        new_id = channel.id # takes the id of the channel that the command is being used upon
        new_name = ids[new_id] # uses the id to check the name of the country
            
        if status == "open": # adds it channel to its repsective dict
            if new_id in current_channels.keys(): # if the channel is already opened
                notice = self.CHANNEL_OPENED.format(mention)
            else:   
                # taking all opened channels and putting them into their respective dictionaries
                # (based on if they have a red circle or not)
                for i in range(len(x)): # for all channels currently in use
                    channel_id = x[i].id
                    channel_name = ids[channel_id] 
                    
                    if x[i].name.startswith("🔴"):
                        red_channels.update({channel_id:channel_name})
                    else:
                        current_channels.update({channel_id:channel_name})
                    
                # then we add the new channel to the dictionary and sort it
                # the way i see it the sorting doesnt add to the complexity of the algorithm because
                # the dictionary is already sorted besides the new channel so there arent many changes that need to be
                # done so it gets sorted
                current_channels.update({new_id:new_name})
                current_channels = dict(sorted(current_channels.items(), key=lambda item: item[1]))

                # takes the index for the new channel, so that discord knows where to place the new channel
                # acknolowdging that the red channels stay on top
                red_count = len(red_channels)
                count = current_channels.keys().index(new_id)
                index = count + red_count
                
                try:
                    # adds channel to the national category in the beginning and moves it to the index
                    await channel.move(beginning=True, offset=index, category=national, sync_permissions=True)
                except discord.Forbidden:  # Manage channel perms required.
                    perm_needed = "Channel" if isinstance(channel, discord.TextChannel) else "Thread"
                    notice = self.CHANNEL_NO_PERMS.format(perm_needed, mention)
                else:
                    notice = self.MOVED_FROM_STOREHOUSE.format(mention)
        elif status == "close":
            if new_id in storehouse_channels.keys(): # if the channel we want to close is already closed
                notice = self.CHANNEL_CLOSED.format(mention)
            else:
                for i in range(len(y)):
                    channel_id = y[i].id
                    channel_name = ids[channel_id]
                    
                    # adds channels in the storehouse to a dict
                    storehouse_channels.update({channel_id:channel_name})
                
                # check if the channel has a red circle so we can remove it before storing
                if channel.name.startswith("🔴"):
                    try:
                        # removes red circle
                        await channel.edit(name=channel.name[1:])    
                    except discord.Forbidden:  # Manage channel perms required.
                        perm_needed = "Channel" if isinstance(channel, discord.TextChannel) else "Thread"
                        notice = self.CHANNEL_NO_PERMS.format(perm_needed, mention)
                    else:
                        notice = self.REMOVE_RED_CIRCLE.format(mention)
                        
                # adds channel we want to close to the storehouse dict and sorts it
                storehouse_channels.update({new_id:new_name})
                storehouse_channels = dict(sorted(storehouse_channels.items(), key=lambda item: item[1])) # why sort
                        
                # takes its index
                index_storehouse = storehouse_channels.keys().index(new_id)
                        
                try:
                    # moves category
                    await channel.move(beginning=True, offset=index_storehouse, category=strhouse, sync_permissions=True)
                except discord.Forbidden:  # Manage channel perms required.
                    perm_needed = "Channel" if isinstance(channel, discord.TextChannel) else "Thread"
                    notice = self.CHANNEL_NO_PERMS.format(perm_needed, mention)
                else:
                    notice = self.MOVED_TO_STOREHOUSE.format(mention)
        else:
            notice = ":x: Invalid Syntax ::: First argument needs to be ``open`` or ``close``"
        await ctx.reply(notice, mention_author=False)
    
    @commands.command()  
    @commands.guild_only()
    @commands.admin_or_permissions(manage_channels=True)
    async def red_circle(
        self,
        ctx: commands.Context,
        channel: discord.TextChannel | discord.Thread,
        ):
        """(Adds/Removes) :red_circle: (to/from) a channel name"""
        
        mention = channel.mention
        
        # the ordering will only work with the country channels, so if for example some runs this command on #esc250 the channel
        # will not be ordered, it will only get the red circle and stay in the same place
        # unlike with the country channels where it will get moved to the top of the category and be ordered alphabetically
        if channel.id in ids.keys():
            
            x = channel.category.text_channels # aux variable, all channels in the same category as the channel we're adding the circle to
            
            current_channels = {}
            red_channels = {}
            
            for i in range(len(x)):  
                channel_id = x[i].id
                channel_name = ids[channel_id]
                
                
                # separates between channels with and without the circle
                if x[i].name.startswith("🔴"):
                    red_channels.update({channel_id:channel_name})
                else:
                    current_channels.update({channel_id:channel_name})
            
            current = channel.name
            if channel.name.startswith("🔴"): # if the channel already has the red circle the command will remove it
                # adds the channel we ran the command on in the dict (no circle) and sorts it
                current_channels.update({channel.id:ids[channel.id]})
                current_channels = dict(sorted(current_channels.items(), key=lambda item: item[1]))

                # gets the index
                red_count = len(red_channels)
                count = current_channels.keys().index(channel.id)
                index = count + red_count - 1
                
                try:
                    # removes the red circle from the name
                    await channel.edit(name="{}".format(current[1:]))
                    # moves it down
                    await channel.move(beginning=True, offset=index)
                except discord.Forbidden:  # Manage channel perms required.
                    perm_needed = "Channel" if isinstance(channel, discord.TextChannel) else "Thread"
                    notice = self.CHANNEL_NO_PERMS.format(perm_needed, mention)
                else:
                    notice = self.REMOVE_RED_CIRCLE.format(mention)
            else: # if the channel doesnt have a red circle, then we add one
                # adds channel to the red channel dictionary and sorts it
                red_channels.update({channel.id:ids[channel.id]})
                red_channels = dict(sorted(red_channels.items(), key=lambda item: item[1]))
                        
                # gets its index
                index = red_channels.keys().index(channel.id)
                
                try:
                    # adds circle and moves it up
                    await channel.edit(name="🔴 {}".format(current))
                    await channel.move(beginning=True, offset=index)
                except discord.Forbidden:  # Manage channel perms required.
                    perm_needed = "Channel" if isinstance(channel, discord.TextChannel) else "Thread"
                    notice = self.CHANNEL_NO_PERMS.format(perm_needed, mention)
                else:
                    notice = self.ADD_RED_CIRCLE.format(mention)
            await ctx.reply(notice, mention_author=False)
        else: # when the channel isnt a country channel we just add or remove the circle
            current = channel.name
            if channel.name.startswith("🔴"):
                try:
                    await channel.edit(name="{}".format(current[1:]))
                    # await channel.move(end=True)
                except discord.Forbidden:  # Manage channel perms required.
                    perm_needed = "Channel" if isinstance(channel, discord.TextChannel) else "Thread"
                    notice = self.CHANNEL_NO_PERMS.format(perm_needed, mention)
                else:
                    notice = self.REMOVE_RED_CIRCLE.format(mention)
            else:
                try:
                    await channel.edit(name="🔴 {}".format(current))
                    # await channel.move(beginning=True)
                except discord.Forbidden:  # Manage channel perms required.
                    perm_needed = "Channel" if isinstance(channel, discord.TextChannel) else "Thread"
                    notice = self.CHANNEL_NO_PERMS.format(perm_needed, mention)
                else:
                    notice = self.ADD_RED_CIRCLE.format(mention)
            await ctx.reply(notice, mention_author=False) 
            
    # Config
    async def red_delete_data_for_user(self, *, _requester, _user_id):
        """Do nothing, as no user data is stored."""
        pass

    