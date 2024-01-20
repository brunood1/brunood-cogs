# Required by Red.
import discord
from redbot.core import commands
from redbot.core.bot import Red


class length(commands.Cog):
    """Spotify now playing"""

    __author__ = "brunood"
    __red_end_user_data_statement__ = "No user data is stored by this cog."

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
        if user is None:
            user = ctx.author
            length = len(user.name)
            
            # Create embed.
            embed = discord.Embed(colour="ffffff")
            embed.title = "User {}".format(user.name)
            embed.add_field(name="Length", value=f"Your username has {length} characters", inline=False)
            await ctx.reply(embed=embed, mention_author=False)

    # Config
    async def red_delete_data_for_user(self, *, _requester, _user_id):
        """Do nothing, as no user data is stored."""
        pass
