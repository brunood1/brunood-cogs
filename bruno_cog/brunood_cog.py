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

    def __init__(self, bot: Red):
        super().__init__()
        self.bot = bot

    # Commands
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
            except discord.Forbidden:  # Manage channel perms required.
                perm_needed = "Channel" if isinstance(channel, discord.TextChannel) else "Thread"
                notice = self.CHANNEL_NO_PERMS.format(perm_needed, mention)
            else:
                notice = self.REMOVE_RED_CIRCLE.format(mention)
        else:
            try:
                await channel.edit(name=f"🔴 {current}")
            except discord.Forbidden:  # Manage channel perms required.
                perm_needed = "Channel" if isinstance(channel, discord.TextChannel) else "Thread"
                notice = self.CHANNEL_NO_PERMS.format(perm_needed, mention)
            else:
                notice = self.ADD_RED_CIRCLE.format(mention)
        await ctx.reply(notice, mention_author=False)   
        
    @commands.command()  
    async def channel_category(
        self,
        ctx: commands.Context,
        channel: discord.TextChannel | discord.Thread,
        ):
        """Adds or removes a red circle from a channel name"""
        
        mention = channel.mention
        
        await ctx.reply(f"{mention} is in the {channel.category} category", mention_author=False)   
        
    
    # Config
    async def red_delete_data_for_user(self, *, _requester, _user_id):
        """Do nothing, as no user data is stored."""
        pass
