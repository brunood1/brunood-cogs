# Required by Red.
import discord
from redbot.core import commands
from redbot.core.bot import Red


class Length(commands.Cog):
    """Get the length of a username"""

    __author__ = "brunood"
    __red_end_user_data_statement__ = "No user data is stored by this cog."
    
    X = ":x: Error: "

    CHANNEL_RENAME = ":white_check_mark: Channel renamed to {}"
    CHANNEL_NO_PERMS = X + "I need Manage {} permissions in {} to change the name"
    CHANNEL_NO_NAME = X + "The new name can't be blank"
    ADD_RED_CIRCLE = ":white_check_mark: Added :red_circle: to {}"
    REMOVE_RED_CIRCLE = ":white_check_mark: Removed :red_circle: from {}"
    MOVED_FROM_STOREHOUSE = "Moved {} from the storehouse"
    MOVED_TO_STOREHOUSE = "Moved {} to the storehouse"

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
        embed = discord.Embed(colour=0xffffff)
        embed.title = "User {}".format(user.name)
        embed.add_field(name="Length", value=f"Your username has {length} characters", inline=False)
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
    
    # adds or removes a red circle for national final channels
    # IDEA: make it move to the top and then back down
    # PROBLEM: the channels are ordered alphabetically by country
    @commands.command()  
    async def red_circle(
        self,
        ctx: commands.Context,
        channel: discord.TextChannel | discord.Thread,
        ):
        """Adds or removes a red circle from a channel name"""
        
        mention = channel.mention
        current = channel.name
        if channel.name.startswith("🔴"):
            try:
                await channel.edit(name=f"{current[1:]}")
                await channel.move(end=True)
            except discord.Forbidden:  # Manage channel perms required.
                perm_needed = "Channel" if isinstance(channel, discord.TextChannel) else "Thread"
                notice = self.CHANNEL_NO_PERMS.format(perm_needed, mention)
            else:
                notice = self.REMOVE_RED_CIRCLE.format(mention)
        else:
            try:
                await channel.edit(name=f"🔴 {current}")
                await channel.move(beginning=True)
            except discord.Forbidden:  # Manage channel perms required.
                perm_needed = "Channel" if isinstance(channel, discord.TextChannel) else "Thread"
                notice = self.CHANNEL_NO_PERMS.format(perm_needed, mention)
            else:
                notice = self.ADD_RED_CIRCLE.format(mention)
        await ctx.reply(notice, mention_author=False) 
        
    @commands.command()
    async def storehouse(
        self,
        ctx: commands.Context,
        status: str,
        channel: discord.TextChannel
        ):
        mention = channel.mention
        strhouse = discord.utils.get(channel.guild.categories, id=1198407644021522452)
        national = discord.utils.get(channel.guild.categories, id=1198307468523085885)
        if status == "open":
            try:
                await channel.move(end=True, category=national, sync_permissions=True)
            except discord.Forbidden:  # Manage channel perms required.
                perm_needed = "Channel" if isinstance(channel, discord.TextChannel) else "Thread"
                notice = self.CHANNEL_NO_PERMS.format(perm_needed, mention)
            else:
                notice = self.MOVED_FROM_STOREHOUSE.format(mention)
        elif status == "close":
            try:
                await channel.move(end=True, category=strhouse, sync_permissions=True)
            except discord.Forbidden:  # Manage channel perms required.
                perm_needed = "Channel" if isinstance(channel, discord.TextChannel) else "Thread"
                notice = self.CHANNEL_NO_PERMS.format(perm_needed, mention)
            else:
                notice = self.MOVED_TO_STOREHOUSE.format(mention)
        else:
            notice = ":x: ERROR Invalid Syntax ::: First argument needs to be ``open`` or ``close``"
        await ctx.reply(notice)
    
    # Config
    async def red_delete_data_for_user(self, *, _requester, _user_id):
        """Do nothing, as no user data is stored."""
        pass
