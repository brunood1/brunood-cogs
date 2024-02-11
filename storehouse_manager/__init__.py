from .storehouse_manager import Storehouse

__red_end_user_data_statement__ = "No user data is stored by this cog."


async def setup(bot):
    await bot.add_cog(Storehouse(bot))
