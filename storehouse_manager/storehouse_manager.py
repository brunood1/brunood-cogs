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
        
        ids = {
            929409087731531827: "albania",
            929409225648652288: "armenia",
            929409403088699412: "australia",
            929409326165155840: "austria",
            929409478586171503: "azerbaijan",
            929409553936838758: "belgium",
            929409624677961769: "bulgaria",
            929410876451205141: "croatia",
            929409791292477470: "cyprus",
            929409853695356978: "czechia",
            406133769263644693: "denmark",
            929410032460771338: "estonia",
            929410138916392970: "finland",
            929410257946546246: "france",
            929410588398981190: "georgia",
            929409941406642256: "germany",
            929410760541610095: "greece",
            406132729588088843: "island",
            929410981505945700: "ireland",
            515896947962413073: "israel",
            401060366399832084: "italy",
            407574926996930563: "latvia",
            401058593090306048: "lithuania",
            999999930829647964: "luxembourg",
            498206361533022219: "malta",
            407591565960413184: "moldova",
            929411157037576192: "montenegro",
            929411396872077412: "netherlands",
            929411282589872188: "north macedonia",
            401057924107206667: "norway",
            284093620750123010: "poland",
            410457203556876299: "portugal",
            401059251486720051: "romania",
            929411787953143819: "san marino",
            404816797708058624: "serbia",
            410455540603551746: "slovenia",
            491018710098903047: "spain",
            393480622590394369: "sweden",
            809387654852378674: "sweden2",
            929409724015853578: "switzerland",
            407578430910234635: "ukraine",
            929410455443767296: "united kingdom"
        }
        
        mention = channel.mention
        
        # DEFINING THE CATEGORIES BASED ON THEIR ID
        strhouse = discord.utils.get(channel.guild.categories, id=356050097152327680) 
        national = discord.utils.get(channel.guild.categories, id=1104339301283663902)
        
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
    @commands.guild_only()
    @commands.admin_or_permissions(manage_channels=True)
    async def red_circle(
        self,
        ctx: commands.Context,
        channel: discord.TextChannel | discord.Thread,
        ):
        """(Adds/Removes) :red_circle: (to/from) a channel name"""
        
        ids = {
            929409087731531827: "albania",
            929409225648652288: "armenia",
            929409403088699412: "australia",
            929409326165155840: "austria",
            929409478586171503: "azerbaijan",
            929409553936838758: "belgium",
            929409624677961769: "bulgaria",
            929410876451205141: "croatia",
            929409791292477470: "cyprus",
            929409853695356978: "czechia",
            406133769263644693: "denmark",
            929410032460771338: "estonia",
            929410138916392970: "finland",
            929410257946546246: "france",
            929410588398981190: "georgia",
            929409941406642256: "germany",
            929410760541610095: "greece",
            406132729588088843: "island",
            929410981505945700: "ireland",
            515896947962413073: "israel",
            401060366399832084: "italy",
            407574926996930563: "latvia",
            401058593090306048: "lithuania",
            999999930829647964: "luxembourg",
            498206361533022219: "malta",
            407591565960413184: "moldova",
            929411157037576192: "montenegro",
            929411396872077412: "netherlands",
            929411282589872188: "north macedonia",
            401057924107206667: "norway",
            284093620750123010: "poland",
            410457203556876299: "portugal",
            401059251486720051: "romania",
            929411787953143819: "san marino",
            404816797708058624: "serbia",
            410455540603551746: "slovenia",
            491018710098903047: "spain",
            393480622590394369: "sweden",
            809387654852378674: "sweden2",
            929409724015853578: "switzerland",
            407578430910234635: "ukraine",
            929410455443767296: "united kingdom"
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
                        
                index = count + red_count
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

    