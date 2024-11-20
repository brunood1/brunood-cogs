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
    
json_filepath = os.path.join(data_folder, "countries.json")  # Get the "dict.json" in the subdirectory.
with open(json_filepath, "r") as f:  # Load the data (read-only) from the aforementioned file.
    countries = json.load(f)


class Storehouse(commands.Cog):
    """Commands for managing the national final channels in the Eurovision Discord"""

    __author__ = "brunood"
    __red_end_user_data_statement__ = "No user data is stored by this cog."
    
    X = ":x: Error "

    CHANNEL_RENAME = ":white_check_mark: Channel renamed to {}"
    CHANNEL_NO_PERMS = X + "I need 'Manage {}' permissions in {}"
    CHANNEL_NO_NAME = X + "The new name can't be blank"
    ADD_RED_CIRCLE = ":white_check_mark: Added :red_circle: to {}"
    REMOVE_RED_CIRCLE = ":white_check_mark: Removed :red_circle: from {}"
    MOVED_FROM_STOREHOUSE = "Moved {} from the storehouse"
    MOVED_TO_STOREHOUSE = "Moved {} to the storehouse"
    CHANNEL_OPENED = "Channel {} is already opened"
    CHANNEL_CLOSED = "Channel {} is already closed"
    CANT_GO_LIVE = X + "Archived channels cannot go live"
    ONLY_COUNTRIES = "Can only open/close country channels"
    NOT_OPEN_OR_CLOSE = X + "You can only open or close a channel"
    
    indicatorConvert = {chr(n): chr(x) for n, x in zip(range(127462, 127488), range(97, 123))}

    def __init__(self, bot: Red):
        super().__init__()
        self.bot = bot
    
    # Commands                
    @commands.command()  
    @commands.guild_only()
    @commands.admin_or_permissions(manage_channels=True)
    async def red_circle(
        self,
        ctx: commands.Context,
        channel: discord.TextChannel | discord.Thread):
        """Adds or removes :red_circle: from a channel name"""
        
        STOREHOUSE = discord.utils.get(channel.guild.categories, id=1198407644021522452) 
        OPENED_CHANNELS = discord.utils.get(channel.guild.categories, id=1198634992796975115)
        
        flagEmoji = "".join(c for c in channel.name if "🇦" <= c <= "🇿")
        
        mention = channel.mention
        channel_name = channel.name
        
        isCountry = False
        if flagEmoji != "":
            isCountry = True
        else:
            isCountry = False
        
        if channel in STOREHOUSE.channels:
            # Can't make storehouse channels live
            notice = self.CANT_GO_LIVE
        else: 
            if isCountry == True and channel in OPENED_CHANNELS.channels:
                # Channel needs to be a country channel in the national category
                
                # Get country name
                country_code = "".join(self.indicatorConvert.get(c, c) for c in flagEmoji.lower())
                country_name = countries[country_code]
                
                # Organize channels into RED and NON-RED (Necessary for sorting)
                red_channels = []    
                non_red_channels = []                
                for ch in OPENED_CHANNELS.channels:
                    # Get country name
                    ch_flagEmoji = "".join(c for c in ch.name if "🇦" <= c <= "🇿")
                    ch_country_code = "".join(self.indicatorConvert.get(c, c) for c in ch_flagEmoji.lower())
                    ch_country_name = countries[ch_country_code]
                    
                    if ch.name.startswith("🔴"):
                        red_channels.append(ch_country_name)
                    else:
                        non_red_channels.append(ch_country_name)
                
                # If the channel already has a red circle, it's gonna be removed
                if channel.name.startswith("🔴"):
                    # Add the channel to it's new list and sort it
                    non_red_channels.append(country_name)
                    non_red_channels.sort()
                    # Get its index so the bot knows where to place it in the list
                    index = len(red_channels) + non_red_channels.index(country_name) - 1
                    
                    try:
                        await channel.edit(name=channel_name[1:])
                        await channel.move(beginning=True, offset=index)
                    except discord.Forbidden:  # Manage channel perms required.
                        perm_needed = "Channel" if isinstance(channel, discord.TextChannel) else "Thread"
                        notice = self.CHANNEL_NO_PERMS.format(perm_needed, mention)
                    else:
                        notice = self.ADD_RED_CIRCLE.format(mention)
                 
                # If the channel doesn't have a red circle, it's gonna be added           
                else:          
                    # Add the channel to it's new list and sort it                  
                    red_channels.append(country_name)
                    red_channels.sort()
                    # Get its index so the bot knows where to place it in the list
                    index = red_channels.index(country_name)
                    
                    try:
                        await channel.edit(name="🔴 {}".format(channel_name))
                        await channel.move(beginning=True, offset=index)
                    except discord.Forbidden:  # Manage channel perms required.
                        perm_needed = "Channel" if isinstance(channel, discord.TextChannel) else "Thread"
                        notice = self.CHANNEL_NO_PERMS.format(perm_needed, mention)
                    else:
                        notice = self.ADD_RED_CIRCLE.format(mention)
                        
                
            # If the channel is not a country channel then simply add or remove the red circle
            else:
                if channel_name.startswith("🔴"):
                    try:
                        await channel.edit(name=channel_name[1:])
                    except discord.Forbidden:  # Manage channel perms required.
                        perm_needed = "Channel" if isinstance(channel, discord.TextChannel) else "Thread"
                        notice = self.CHANNEL_NO_PERMS.format(perm_needed, mention)
                    else:
                        notice = self.REMOVE_RED_CIRCLE.format(mention)
                else:
                    try:
                        await channel.edit(name="🔴 {}".format(channel_name))
                    except discord.Forbidden:  # Manage channel perms required.
                        perm_needed = "Channel" if isinstance(channel, discord.TextChannel) else "Thread"
                        notice = self.CHANNEL_NO_PERMS.format(perm_needed, mention)
                    else:
                        notice = self.ADD_RED_CIRCLE.format(mention)
                        
        await ctx.reply(notice, mention_author=False) 
        
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
        
        STOREHOUSE = discord.utils.get(channel.guild.categories, id=1198407644021522452) 
        OPENED_CHANNELS = discord.utils.get(channel.guild.categories, id=1198634992796975115)
        
        flagEmoji = "".join(c for c in channel.name if "🇦" <= c <= "🇿")
        
        mention = channel.mention
        channel_name = channel.name
        
        isCountry = False
        if flagEmoji != "":
            isCountry = True
        else:
            isCountry = False
        
        if isCountry == True:    
            country_code = "".join(self.indicatorConvert.get(c, c) for c in flagEmoji.lower())
            country_name = countries[country_code]
            
            if status == "open":
                if channel in OPENED_CHANNELS.channels:
                    # Can't open a channel that is already open
                    notice = self.CHANNEL_OPENED.format(mention)
                elif channel in STOREHOUSE.channels:
                    # When we move a channel to the opened channels category, we want them to be ordered alphabetically
                    # So, we first need to check where we should place the channel
                    # For that we need to consider two things, the currently opened channels with and without a red circle separately
                    red_channels = []    
                    non_red_channels = []          
                    for ch in OPENED_CHANNELS.channels:
                        # Get country name
                        ch_flagEmoji = "".join(c for c in ch.name if "🇦" <= c <= "🇿")
                        ch_country_code = "".join(self.indicatorConvert.get(c, c) for c in ch_flagEmoji.lower())
                        ch_country_name = countries[ch_country_code]
                        
                        if ch.name.startswith("🔴"):
                            red_channels.append(ch_country_name)
                        else:
                            non_red_channels.append(ch_country_name)
                            
                    # Gets index of the channel
                    non_red_channels.append(country_name)
                    non_red_channels.sort()
                    index = len(red_channels) + non_red_channels.index(country_name)
                    
                    try:
                        # adds channel to the national category in the beginning and moves it to the index
                        await channel.move(beginning=True, offset=index, category=OPENED_CHANNELS, sync_permissions=True)
                    except discord.Forbidden:  # Manage channel perms required.
                        perm_needed = "Channel" if isinstance(channel, discord.TextChannel) else "Thread"
                        notice = self.CHANNEL_NO_PERMS.format(perm_needed, mention)
                    else:
                        notice = self.MOVED_FROM_STOREHOUSE.format(mention)
                else:
                    notice = self.X + "Can't open this channel" # TODO: add this message as a variable
                    
            elif status == "close":
                if channel in STOREHOUSE.channels:
                    notice = self.CHANNEL_CLOSED
                elif channel in OPENED_CHANNELS.channels:
                    # First thing is to check if the channel we're trying to close has a red circle
                    if channel_name.startswith("🔴"):
                        notice = self.X + "Can't close live channels" # TODO: add this message as a variable
                    else:
                        # When we close a channel we need check its position in the storehouse
                        STOREHOUSE_CHANNELS = []
                        for ch in STOREHOUSE.channels:
                            # Get country name
                            ch_flagEmoji = "".join(c for c in ch.name if "🇦" <= c <= "🇿")
                            if ch_flagEmoji != "":
                                ch_country_code = "".join(indicatorConvert.get(c, c) for c in ch_flagEmoji.lower())
                                ch_country_name = countries[ch_country_code]
                                STOREHOUSE_CHANNELS.append(ch_country_name)
                                
                        STOREHOUSE_CHANNELS.append(country_name)
                        STOREHOUSE_CHANNELS.sort()
                        index = STOREHOUSE_CHANNELS.index(country_name)
                        
                        try:
                            # Moves category
                            await channel.move(beginning=True, offset=index, category=STOREHOUSE, sync_permissions=True)
                        except discord.Forbidden:  # Manage channel perms required.
                            perm_needed = "Channel" if isinstance(channel, discord.TextChannel) else "Thread"
                            notice = self.CHANNEL_NO_PERMS.format(perm_needed, mention)
                        else:
                            notice = self.MOVED_TO_STOREHOUSE.format(mention)
                
                # If the channel is not on the opened channels list (ex: esc-main)        
                else:
                    notice = self.X + "Can't close this channel" # TODO: add this message as a variable
             
            # Wrong status       
            else:
                notice = self.NOT_OPEN_OR_CLOSE

        # Not a country channel
        else:
            notice = self.ONLY_COUNTRIES
            
        
        await ctx.reply(notice, mention_author=False) 
                
    # Config
    async def red_delete_data_for_user(self, *, _requester, _user_id):
        """Do nothing, as no user data is stored."""
        pass

    