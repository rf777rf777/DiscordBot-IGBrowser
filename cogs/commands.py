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
        #self.ig_item = InstagramItem('walkerpretty96')
        #self.ig_item = InstagramItem('mei.x.mei')

        #self.profile = ig_item.get_user_profile()
        self.latest_post = None
        self.profile = None

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
            title=self.profile['username'],
            description=self.profile['fullname'],
            color=0x00ff00
        )
        embed.set_thumbnail(url=self.profile['thumbnail'])
        embed.url = f'https://www.instagram.com/{self.profile['username']}/'
        embed.set_footer(text=hashtags if len(hashtags) > 0 else '')
        post_items = self.latest_post['post_items']
        item = post_items[index]
        embed.add_field(
            name="貼文連結：",
            value=f"[點擊這裡觀看](https://www.instagram.com/p/{self.latest_post['code']})",
            inline=False
        ) 
        embed.add_field(
            name="說明文字：",
            value=caption,
            inline=False
        ) 
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
    async def show_items(self, ctx, username: str):
        ig_item = InstagramItem(username)
        self.latest_post = ig_item.get_latest_posts()
        self.profile = ig_item.get_user_profile()
        view = PaginationView(total_items=len(self.latest_post['post_items']), update_embed_callback=self.generate_embed)
        embed = self.generate_embed(0)
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Commands(bot))