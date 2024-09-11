import discord
from discord.ext import commands
from modules.pagination_view import PaginationView
from modules.instagram_item import InstagramItem

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #self.ig_item = InstagramItem('yuzuki_yzk030')
        #self.ig_item = InstagramItem('momiko_124')
        #self.ig_item = InstagramItem('eeelyeee')
        self.ig_item = InstagramItem('walkerpretty96')

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
        
        hashtags = self.latest_post['hashtages']
        
        embed = discord.Embed(
            title=caption,
            description=hashtags if len(hashtags) > 0 else '',
            color=0x00ff00
        )
        embed.url = f'https://www.instagram.com/p/{self.latest_post['code']}'
        #embed.set_footer(text=f'https://www.instagram.com/p/{self.latest_post['code']}')
        post_items = self.latest_post['post_items']
        item = post_items[index]
        if item.type == 'image':
            embed.set_image(url=item.url)
        else:
            embed.set_image(url=item.url)
            embed.add_field(
                name="影片連結：",
                value=f"[點擊這裡觀看]({item.video_url})",
                inline=False
            )            

        return embed

    @commands.command()
    async def show_items(self, ctx):
        self.latest_post = self.ig_item.get_latest_posts()
        view = PaginationView(total_items=len(self.latest_post['post_items']), update_embed_callback=self.generate_embed)
        embed = self.generate_embed(0)
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Commands(bot))