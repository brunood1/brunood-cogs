# Required by Red.
import discord
import typing
from redbot.core import commands
from redbot.core.bot import Red


class Length(commands.Cog):
    """Get the length of a username"""

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
    
    idDataBase = [
        [1198634448531496980, "finland"],
        [1198634861641089146, "netherlands"],
        [1198634389551206420, "slovakia"]
    ]

    def __init__(self, bot: Red):
        super().__init__()
        self.bot = bot

    # Commands
    
    # returns an embed with your profile picture and the length of your username
    @commands.command()
    async def length(
        self, 
        ctx: commands.Context, 
        user: discord.Member = None
        ):
        """Returns the length of a username"""
        if user is None:
            user = ctx.author
        length = len(user.name)
            
        # Create embed.
        embed = discord.Embed(colour=0xfffff0)
        embed.title = "User {}".format(user.name)
        embed.add_field(name="Length", value="Your username has {} characters".format(length), inline=False)
        embed.set_thumbnail(url=user.display_avatar)
        await ctx.reply(embed=embed, mention_author=False)
     
    
    # renames a channel 
    @commands.command()  
    async def channel_rename(
        self,
        ctx: commands.Context,
        channel: discord.TextChannel | discord.Thread,
        rename: str
        ):
        """Renames a channel"""
        
        mention = channel.mention
        try:
            await channel.edit(name=rename)
        except discord.Forbidden:  # Manage channel perms required.
            perm_needed = "Channel" if isinstance(channel, discord.TextChannel) else "Thread"
            notice = self.CHANNEL_NO_PERMS.format(perm_needed, mention)
        else:
            if len(rename) == 0:
                notice = self.CHANNEL_NO_NAME
            else:
                notice = self.CHANNEL_RENAME.format(rename)
        await ctx.reply(notice, mention_author=False)
    
    # @commands.command(name="red_circle")  
    # async def red_circle_cmd(
    #     self,
    #     ctx: commands.Context,
    #     channel: discord.TextChannel | discord.Thread,
    #     ):
    #     """Adds or removes a red circle from a channel name"""
        
    #     await self.red_circle_logic(ctx, channel)
        
    # @commands.command()
    # async def storehouse(
    #     self,
    #     ctx: commands.Context,
    #     status: str,
    #     channel: discord.TextChannel
    #     ):
    #     """Moves a channel to and from the storehouse"""
        
    #     idDataBase = [
    #         [1198635880370405477, "albania"],
    #         [1198695703761932468, "brazil"],
    #         [1198634448531496980, "finland"],
    #         [1198634861641089146, "netherlands"],
    #         [1198634389551206420, "slovakia"]
    #     ]
        
    #     mention = channel.mention
        
    #     # DEFINING THE CATEGORIES BASED ON THEIR ID
    #     strhouse = discord.utils.get(channel.guild.categories, id=1198407644021522452) 
    #     national = discord.utils.get(channel.guild.categories, id=1198634992796975115)
        
    #     # CREATES ARRAY WITH ID AND COUNTRY
    #     new_channel = []
    #     new_channel.append(channel.id)
    #     for i in range(len(idDataBase)):
    #         if idDataBase[i][0] == new_channel[0]:
    #             new_channel.append(idDataBase[i][1])
        
        
    #     x = national.text_channels # STORES ALL CHANNELS IN THE NAT. CATEGORY
    #     aux = []
    #     red_count = 0
    #     for i in range(len(x)):
    #         if x[i].name.startswith("🔴"):
    #             red_count += 1
    #         else:
    #             aux.append(x[i].id) # SAVES THE IDS OF THE CHANNELS WITHOUT 🔴
            
    #     # STORES ALL CHANNELS IN A MATRIX OF THE SAME STYLE AS THE DB
    #     current_channels = []
    #     for i in range(len(aux)):
    #         blank = []
    #         blank.append(aux[i])
    #         current_channels.append(blank)
            
    #     for i in range(len(current_channels)):
    #         for j in range(len(idDataBase)):
    #             if current_channels[i][0] == idDataBase[j][0]:
    #                 current_channels[i].append(idDataBase[j][1])
        
    #     # DOES THE SAME FOR THE STOREHOUSE CHANNELS
    #     storehouse_channels = []
    #     for i in range(len(idDataBase)):
    #             if idDataBase[i] not in current_channels:
    #                 storehouse_channels.append(idDataBase[i])
            

    #     if status == "open":
    #         # ADDS CHANNEL AND ORDERS IT
    #         current_channels.append(new_channel)
    #         current_channels.sort(key=lambda x: x[1])

    #         # THE NEW CHANNEL INDEX
    #         index_current = current_channels.index(new_channel)
    #         index = index_current + red_count
    #         try:
    #             await channel.move(beginning=True, offset=index, category=national, sync_permissions=True)
    #         except discord.Forbidden:  # Manage channel perms required.
    #             perm_needed = "Channel" if isinstance(channel, discord.TextChannel) else "Thread"
    #             notice = self.CHANNEL_NO_PERMS.format(perm_needed, mention)
    #         else:
    #             notice = self.MOVED_FROM_STOREHOUSE.format(mention)
    #     elif status == "close":
    #         if channel.name.startswith("🔴"):
    #             try:
    #                 await channel.edit(name="{}".format(channel.name[1:]))  
    #             except discord.Forbidden:  # Manage channel perms required.
    #                 perm_needed = "Channel" if isinstance(channel, discord.TextChannel) else "Thread"
    #                 notice = self.CHANNEL_NO_PERMS.format(perm_needed, mention)
    #             else:
    #                 notice = self.REMOVE_RED_CIRCLE.format(mention)
                    
    #         storehouse_channels.append(new_channel)
    #         storehouse_channels.sort(key=lambda x: x[1])

    #         index_storehouse = storehouse_channels.index(new_channel)
    #         try:
    #             await channel.move(beginning=True, offset=index_storehouse, category=strhouse, sync_permissions=True)
    #         except discord.Forbidden:  # Manage channel perms required.
    #             perm_needed = "Channel" if isinstance(channel, discord.TextChannel) else "Thread"
    #             notice = self.CHANNEL_NO_PERMS.format(perm_needed, mention)
    #         else:
    #             notice = self.MOVED_TO_STOREHOUSE.format(mention)
    #     else:
    #         notice = ":x: Invalid Syntax ::: First argument needs to be ``open`` or ``close``"
    #     await ctx.reply(notice, mention_author=False)
    
    
    # # IDEA: if this is run on a storehouse channel, first move up then add circle
    # @commands.command()  
    # async def red_circle_new(
    #     self,
    #     ctx: commands.Context,
    #     channel: discord.TextChannel | discord.Thread,
    #     ):
    #     """Adds or removes a red circle from a channel name"""
        
    #     idDataBase = [
    #         [1198635880370405477, "albania"],
    #         [1198695703761932468, "brazil"],
    #         [1198634448531496980, "finland"],
    #         [1198634861641089146, "netherlands"],
    #         [1198634389551206420, "slovakia"]
    #     ]
        
    #     check = []
    #     for i in range(len(idDataBase)):
    #         check.append(idDataBase[i][0])
        
    #     mention = channel.mention
    #     if channel.id in check:
    #         # CREATES ARRAY WITH ID AND COUNTRY
    #         new_channel = []
    #         new_channel.append(channel.id)
    #         for i in range(len(idDataBase)):
    #             if idDataBase[i][0] == new_channel[0]:
    #                 new_channel.append(idDataBase[i][1])
            
            
    #         x = channel.category.text_channels
    #         aux = []
    #         aux_red = []
    #         for i in range(len(x)):
    #             if x[i].name.startswith("🔴"):
    #                 aux_red.append(x[i].id)
    #             else:
    #                 aux.append(x[i].id) # SAVES THE IDS OF THE CHANNELS WITHOUT 🔴
                
    #         # STORES ALL CHANNELS IN A MATRIX OF THE SAME STYLE AS THE DB
    #         current_channels = []
    #         red_channels = []
    #         for i in range(len(aux)):
    #             blank = []
    #             blank.append(aux[i])
    #             current_channels.append(blank)
                
    #         for i in range(len(aux_red)):
    #             blank = []
    #             blank.append(aux_red[i])
    #             red_channels.append(blank)
                
    #         for i in range(len(current_channels)):
    #             for j in range(len(idDataBase)):
    #                 if current_channels[i][0] == idDataBase[j][0]:
    #                     current_channels[i].append(idDataBase[j][1])
            
    #         for i in range(len(red_channels)):
    #             for j in range(len(idDataBase)):
    #                 if red_channels[i][0] == idDataBase[j][0]:
    #                     red_channels[i].append(idDataBase[j][1])
            
    #         current = channel.name
    #         if channel.name.startswith("🔴"):
    #             current_channels.append(new_channel)
    #             current_channels.sort(key=lambda x: x[1])

    #             # THE NEW CHANNEL INDEX
    #             index_current = current_channels.index(new_channel)
    #             index = index_current + len(red_channels)
    #             try:
    #                 await channel.edit(name="{}".format(current[1:]))
    #                 await channel.move(beginning=True, offset=index)
    #             except discord.Forbidden:  # Manage channel perms required.
    #                 perm_needed = "Channel" if isinstance(channel, discord.TextChannel) else "Thread"
    #                 notice = self.CHANNEL_NO_PERMS.format(perm_needed, mention)
    #             else:
    #                 notice = self.REMOVE_RED_CIRCLE.format(mention)
    #         else:
    #             red_channels.append(new_channel)
    #             red_channels.sort(key=lambda x: x[1])

    #             # THE NEW CHANNEL INDEX
    #             index = red_channels.index(new_channel)
                
    #             try:
    #                 await channel.edit(name="🔴 {}".format(current))
    #                 await channel.move(beginning=True, offset=index)
    #             except discord.Forbidden:  # Manage channel perms required.
    #                 perm_needed = "Channel" if isinstance(channel, discord.TextChannel) else "Thread"
    #                 notice = self.CHANNEL_NO_PERMS.format(perm_needed, mention)
    #             else:
    #                 notice = self.ADD_RED_CIRCLE.format(mention)
    #         await ctx.reply(notice, mention_author=False)
    #     else:
    #         current = channel.name
    #         if channel.name.startswith("🔴"):
    #             try:
    #                 await channel.edit(name="{}".format(current[1:]))
    #                 # await channel.move(end=True)
    #             except discord.Forbidden:  # Manage channel perms required.
    #                 perm_needed = "Channel" if isinstance(channel, discord.TextChannel) else "Thread"
    #                 notice = self.CHANNEL_NO_PERMS.format(perm_needed, mention)
    #             else:
    #                 notice = self.REMOVE_RED_CIRCLE.format(mention)
    #         else:
    #             try:
    #                 await channel.edit(name="🔴 {}".format(current))
    #                 # await channel.move(beginning=True)
    #             except discord.Forbidden:  # Manage channel perms required.
    #                 perm_needed = "Channel" if isinstance(channel, discord.TextChannel) else "Thread"
    #                 notice = self.CHANNEL_NO_PERMS.format(perm_needed, mention)
    #             else:
    #                 notice = self.ADD_RED_CIRCLE.format(mention)
    #         await ctx.reply(notice, mention_author=False) 
            
    
    # async def red_circle_logic(
    #     self,
    #     ctx: commands.Context,
    #     channel: discord.TextChannel | discord.Thread,
    #     ):
    #     mention = channel.mention
    #     current = channel.name
    #     if channel.name.startswith("🔴"):
    #         try:
    #             await channel.edit(name="{}".format(current[1:]))
    #             # await channel.move(end=True)
    #         except discord.Forbidden:  # Manage channel perms required.
    #             perm_needed = "Channel" if isinstance(channel, discord.TextChannel) else "Thread"
    #             notice = self.CHANNEL_NO_PERMS.format(perm_needed, mention)
    #         else:
    #             notice = self.REMOVE_RED_CIRCLE.format(mention)
    #     else:
    #         try:
    #             await channel.edit(name="🔴 {}".format(current))
    #             # await channel.move(beginning=True)
    #         except discord.Forbidden:  # Manage channel perms required.
    #             perm_needed = "Channel" if isinstance(channel, discord.TextChannel) else "Thread"
    #             notice = self.CHANNEL_NO_PERMS.format(perm_needed, mention)
    #         else:
    #             notice = self.ADD_RED_CIRCLE.format(mention)
    #     await ctx.reply(notice, mention_author=False) 
        
    @commands.command()
    async def storehouse(
        self,
        ctx: commands.Context,
        status: str,
        channel: discord.TextChannel
        ):
        """Moves a channel to and from the storehouse"""
        
  
        
        ids = {
            1198635880370405477: "albania", 
            1198695703761932468: "brazil",
            1198634448531496980: "finland",
            1198634861641089146: "netherlands",
            1198634389551206420: "slovakia",  
        }
        
        mention = channel.mention
        
        # DEFINING THE CATEGORIES BASED ON THEIR ID
        strhouse = discord.utils.get(channel.guild.categories, id=1198407644021522452) 
        national = discord.utils.get(channel.guild.categories, id=1198634992796975115)
        
        current_channels = {}
        red_channels = {}
        storehouse_channels = {}
        
        x = national.text_channels
        y = strhouse.text_channels
                
        new_id = channel.id
        new_name = ids[new_id]
            

        if status == "open":
            if new_id in current_channels.keys():
                notice = self.CHANNEL_OPENED.format(mention)
            else:   
                for i in range(len(x)):
                    if x[i].name.startswith("🔴"):
                        red_channels.update({x[i].id:ids[x[i].id]})
                    else:
                        current_channels.update({x[i].id:ids[x[i].id]})
                    
                current_channels.update({new_id:new_name})
                current_channels = dict(sorted(current_channels.items(), key=lambda item: item[1]))

                # THE NEW CHANNEL INDEX
                red_count = len(red_channels)
            
                count = 0
                for k in current_channels.keys():
                    if k == new_id:
                        break
                    if k != new_id:
                        count += 1
                        
                index = count + red_count
                
                try:
                    await channel.move(beginning=True, offset=index, category=national, sync_permissions=True)
                except discord.Forbidden:  # Manage channel perms required.
                    perm_needed = "Channel" if isinstance(channel, discord.TextChannel) else "Thread"
                    notice = self.CHANNEL_NO_PERMS.format(perm_needed, mention)
                else:
                    notice = self.MOVED_FROM_STOREHOUSE.format(mention)
        elif status == "close":
            if new_id in storehouse_channels.keys():
                notice = self.CHANNEL_CLOSED.format(mention)
            else:
                for i in range(len(y)):
                    storehouse_channels.update({y[i].id:ids[y[i].id]})
                
                if channel.name.startswith("🔴"):
                    try:
                        await channel.edit(name="{}".format(channel.name[1:]))  
                    except discord.Forbidden:  # Manage channel perms required.
                        perm_needed = "Channel" if isinstance(channel, discord.TextChannel) else "Thread"
                        notice = self.CHANNEL_NO_PERMS.format(perm_needed, mention)
                    else:
                        notice = self.REMOVE_RED_CIRCLE.format(mention)
                        
                storehouse_channels.update({new_id:new_name})
                storehouse_channels = dict(sorted(storehouse_channels.items(), key=lambda item: item[1]))

                index_storehouse = 0
                for k in storehouse_channels.keys():
                    if k == new_id:
                        break
                    if k != new_id:
                        index_storehouse += 1
                        
                try:
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
    async def red_circle(
        self,
        ctx: commands.Context,
        channel: discord.TextChannel | discord.Thread,
        ):
        """(Adds/Removes) :red_circle: (to/from) a channel name"""
        
  
        
        ids = {
            1198635880370405477: "albania", 
            1198695703761932468: "brazil",
            1198634448531496980: "finland",
            1198634861641089146: "netherlands",
            1198634389551206420: "slovakia",  
        }
        
        mention = channel.mention
        if channel.id in ids.keys():
            x = channel.category.text_channels
            current_channels = {}
            red_channels = {}
            for i in range(len(x)):
                if x[i].name.startswith("🔴"):
                    red_channels.update({x[i].id:ids[x[i].id]})
                else:
                    current_channels.update({x[i].id:ids[x[i].id]})
            
            current = channel.name
            if channel.name.startswith("🔴"):
                current_channels.update({channel.id:ids[channel.id]})
                current_channels = dict(sorted(current_channels.items(), key=lambda item: item[1]))

                # THE NEW CHANNEL INDEX
                red_count = len(red_channels)
            
                count = 0
                for k in current_channels.keys():
                    if k == channel.id:
                        break
                    if k != channel.id:
                        count += 1
                        
                index = count + red_count - 1
                try:
                    await channel.edit(name="{}".format(current[1:]))
                    await channel.move(beginning=True, offset=index)
                except discord.Forbidden:  # Manage channel perms required.
                    perm_needed = "Channel" if isinstance(channel, discord.TextChannel) else "Thread"
                    notice = self.CHANNEL_NO_PERMS.format(perm_needed, mention)
                else:
                    notice = self.REMOVE_RED_CIRCLE.format(mention)
            else:
                red_channels.update({channel.id:ids[channel.id]})
                red_channels = dict(sorted(red_channels.items(), key=lambda item: item[1]))

                # THE NEW CHANNEL INDEX
                index = 0
                for k in red_channels.keys():
                    if k == channel.id:
                        break
                    if k != channel.id:
                        index += 1
                
                try:
                    await channel.edit(name="🔴 {}".format(current))
                    await channel.move(beginning=True, offset=index)
                except discord.Forbidden:  # Manage channel perms required.
                    perm_needed = "Channel" if isinstance(channel, discord.TextChannel) else "Thread"
                    notice = self.CHANNEL_NO_PERMS.format(perm_needed, mention)
                else:
                    notice = self.ADD_RED_CIRCLE.format(mention)
            await ctx.reply(notice, mention_author=False)
        else:
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

    