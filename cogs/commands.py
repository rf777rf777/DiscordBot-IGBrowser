import discord
from discord.ext import commands
from modules.view import PaginationView
from modules.instagram_retriever import InstagramItem

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ig_item = InstagramItem('duckie_elle')
        #self.profile = ig_item.get_user_profile()
        self.latest_post = None

    @commands.command()
    async def hello(self, ctx):
        await ctx.send('Hello from command!')

    def generate_embed(self, index):
        #item = self.items[index]
        caption = self.latest_post['caption']
        if len(caption) > 256:
            caption = caption[:256]  # 截斷到 256 個字元
        
        embed = discord.Embed(
            title=caption,
            description=self.latest_post['hashtages'],
            color=0x00ff00
        )
        
        embed.set_footer(text=self.latest_post['code'])
        image = self.latest_post['content']['images'][index]
        if image:
            embed.set_image(url=image)
        
        #if item.get("video"):
        #    embed.video(url=item['video'])
        return embed

    @commands.command()
    async def show_items(self, ctx):
        self.latest_post = self.ig_item.get_latest_posts(False)
        view = PaginationView(total_items=len(self.latest_post['content']['images']), update_embed_callback=self.generate_embed)
        embed = self.generate_embed(0)
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Commands(bot))