# Required by Red.
import discord
import typing
from redbot.core import commands
from redbot.core.bot import Red


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
        status: str,
        channel: discord.TextChannel
        ):
        """Moves a channel to and from the storehouse"""
        
        idDataBase = [
            [929409087731531827, "albania"],
            [929409225648652288, "armenia"],
            [929409403088699412, "australia"],
            [929409326165155840, "austria"],
            [929409478586171503, "azerbaijan"],
            [929409553936838758, "belgium"],
            [929409624677961769, "bulgaria"],
            [929410876451205141, "croatia"],
            [929409791292477470, "cyprus"],
            [929409853695356978, "czechia"],
            [406133769263644693, "denmark"],
            [929410032460771338, "estonia"],
            [929410138916392970, "finland"],
            [929410257946546246, "france"],
            [929410588398981190, "georgia"],
            [929409941406642256, "germany"],
            [929410760541610095, "greece"],
            [406132729588088843, "island"],
            [929410981505945700, "ireland"],
            [515896947962413073, "israel"],
            [401060366399832084, "italy"],
            [407574926996930563, "latvia"],
            [401058593090306048, "lithuania"],
            [999999930829647964, "luxembourg"],
            [498206361533022219, "malta"],
            [407591565960413184, "moldova"],
            [929411157037576192, "montenegro"],
            [929411396872077412, "netherlands"],
            [929411282589872188, "north macedonia"],
            [401057924107206667, "norway"],
            [284093620750123010, "poland"],
            [410457203556876299, "portugal"],
            [401059251486720051, "romania"],
            [929411787953143819, "san marino"],
            [404816797708058624, "serbia"]
            [410455540603551746, "slovenia"],
            [491018710098903047, "spain"],
            [393480622590394369, "sweden"],
            [809387654852378674, "sweden2"],
            [929409724015853578, "switzerland"],
            [407578430910234635, "ukraine"],
            [929410455443767296, "united kingdom"]
        ]
        
        mention = channel.mention
        
        # DEFINING THE CATEGORIES BASED ON THEIR ID
        strhouse = discord.utils.get(channel.guild.categories, id=356050097152327680) 
        national = discord.utils.get(channel.guild.categories, id=1104339301283663902)
        
        # CREATES ARRAY WITH ID AND COUNTRY
        new_channel = []
        new_channel.append(channel.id)
        for i in range(len(idDataBase)):
            if idDataBase[i][0] == new_channel[0]:
                new_channel.append(idDataBase[i][1])
        
        
        x = national.text_channels # STORES ALL CHANNELS IN THE NAT. CATEGORY
        aux = []
        red_count = 0
        for i in range(len(x)):
            if x[i].name.startswith("🔴"):
                red_count += 1
            else:
                aux.append(x[i].id) # SAVES THE IDS OF THE CHANNELS WITHOUT 🔴
                
        # basically this bit ^^ is to count the channels that have 🔴 so the bot knows where to place the new channel
            
        # STORES ALL CHANNELS (that don't have 🔴) IN A MATRIX OF THE SAME STYLE AS THE DB
        current_channels = []
        for i in range(len(aux)):
            blank = []
            blank.append(aux[i])
            current_channels.append(blank)
            
        for i in range(len(current_channels)):
            for j in range(len(idDataBase)):
                if current_channels[i][0] == idDataBase[j][0]:
                    current_channels[i].append(idDataBase[j][1])
        
        # DOES THE SAME FOR THE STOREHOUSE CHANNELS (aka just looks at the channels from the database that are NOT in the current channels)
        storehouse_channels = []
        for i in range(len(idDataBase)):
            if idDataBase[i] not in current_channels:
                storehouse_channels.append(idDataBase[i])
            

        if status == "open":
            # ADDS CHANNEL AND ORDERS IT
            current_channels.append(new_channel)
            current_channels.sort(key=lambda x: x[1])

            # THE NEW CHANNEL INDEX
            index_current = current_channels.index(new_channel)
            index = index_current + red_count
            try:
                await channel.move(beginning=True, offset=index, category=national, sync_permissions=True)
            except discord.Forbidden:  # Manage channel perms required.
                perm_needed = "Channel" if isinstance(channel, discord.TextChannel) else "Thread"
                notice = self.CHANNEL_NO_PERMS.format(perm_needed, mention)
            else:
                notice = self.MOVED_FROM_STOREHOUSE.format(mention)
        elif status == "close":
            if channel.name.startswith("🔴"):
                try:
                    await channel.edit(name="{}".format(channel.name[1:]))
                except discord.Forbidden:  # Manage channel perms required.
                    perm_needed = "Channel" if isinstance(channel, discord.TextChannel) else "Thread"
                    notice = self.CHANNEL_NO_PERMS.format(perm_needed, mention)
                else:
                    notice = self.REMOVE_RED_CIRCLE.format(mention)
                    
            storehouse_channels.append(new_channel)
            storehouse_channels.sort(key=lambda x: x[1])

            index_storehouse = storehouse_channels.index(new_channel)
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
    @commands.guild_only()
    @commands.admin_or_permissions(manage_channels=True)
    async def red_circle(
        self,
        ctx: commands.Context,
        channel: discord.TextChannel | discord.Thread,
        ):
        """Adds or removes a red circle from a channel name"""
        
        idDataBase = [
            [929409087731531827, "albania"],
            [929409225648652288, "armenia"],
            [929409403088699412, "australia"],
            [929409326165155840, "austria"],
            [929409478586171503, "azerbaijan"],
            [929409553936838758, "belgium"],
            [929409624677961769, "bulgaria"],
            [929410876451205141, "croatia"],
            [929409791292477470, "cyprus"],
            [929409853695356978, "czechia"],
            [406133769263644693, "denmark"],
            [929410032460771338, "estonia"],
            [929410138916392970, "finland"],
            [929410257946546246, "france"],
            [929410588398981190, "georgia"],
            [929409941406642256, "germany"],
            [929410760541610095, "greece"],
            [406132729588088843, "island"],
            [929410981505945700, "ireland"],
            [515896947962413073, "israel"],
            [401060366399832084, "italy"],
            [407574926996930563, "latvia"],
            [401058593090306048, "lithuania"],
            [999999930829647964, "luxembourg"],
            [498206361533022219, "malta"],
            [407591565960413184, "moldova"],
            [929411157037576192, "montenegro"],
            [929411396872077412, "netherlands"],
            [929411282589872188, "north macedonia"],
            [401057924107206667, "norway"],
            [284093620750123010, "poland"],
            [410457203556876299, "portugal"],
            [401059251486720051, "romania"],
            [929411787953143819, "san marino"],
            [404816797708058624, "serbia"]
            [410455540603551746, "slovenia"],
            [491018710098903047, "spain"],
            [393480622590394369, "sweden"],
            [809387654852378674, "sweden2"],
            [929409724015853578, "switzerland"],
            [407578430910234635, "ukraine"],
            [929410455443767296, "united kingdom"]
        ]
        
        check = []
        for i in range(len(idDataBase)):
            check.append(idDataBase[i][0])
        
        mention = channel.mention
        if channel.id in check:
            # CREATES ARRAY WITH ID AND COUNTRY
            new_channel = []
            new_channel.append(channel.id)
            for i in range(len(idDataBase)):
                if idDataBase[i][0] == new_channel[0]:
                    new_channel.append(idDataBase[i][1])
            
            
            x = channel.category.text_channels
            aux = []
            aux_red = []
            for i in range(len(x)):
                if x[i].name.startswith("🔴"):
                    aux_red.append(x[i].id)
                else:
                    aux.append(x[i].id) # SAVES THE IDS OF THE CHANNELS WITHOUT 🔴
                
            # STORES ALL CHANNELS IN A MATRIX OF THE SAME STYLE AS THE DB
            current_channels = []
            red_channels = []
            for i in range(len(aux)):
                blank = []
                blank.append(aux[i])
                current_channels.append(blank)
                
            for i in range(len(aux_red)):
                blank = []
                blank.append(aux_red[i])
                red_channels.append(blank)
                
            for i in range(len(current_channels)):
                for j in range(len(idDataBase)):
                    if current_channels[i][0] == idDataBase[j][0]:
                        current_channels[i].append(idDataBase[j][1])
            
            for i in range(len(red_channels)):
                for j in range(len(idDataBase)):
                    if red_channels[i][0] == idDataBase[j][0]:
                        red_channels[i].append(idDataBase[j][1])
            
            current = channel.name
            if channel.name.startswith("🔴"):
                current_channels.append(new_channel)
                current_channels.sort(key=lambda x: x[1])

                # THE NEW CHANNEL INDEX
                index_current = current_channels.index(new_channel)
                index = index_current + len(red_channels)
                try:
                    await channel.edit(name="{}".format(current[1:]))
                    await channel.move(beginning=True, offset=index)
                except discord.Forbidden:  # Manage channel perms required.
                    perm_needed = "Channel" if isinstance(channel, discord.TextChannel) else "Thread"
                    notice = self.CHANNEL_NO_PERMS.format(perm_needed, mention)
                else:
                    notice = self.REMOVE_RED_CIRCLE.format(mention)
            else:
                red_channels.append(new_channel)
                red_channels.sort(key=lambda x: x[1])

                # THE NEW CHANNEL INDEX
                index = red_channels.index(new_channel)
                
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

    