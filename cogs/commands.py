import discord
from discord.ext import commands
from modules.pagination_view import PaginationView
from modules.instagram_item import InstagramItem
import re

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #self.ig_item = InstagramItem('yuzuki_yzk030')
        #self.ig_item = InstagramItem('momiko_124')
        #self.ig_item = InstagramItem('eeelyeee')
        #self.ig_item = InstagramItem('walkerpretty96')
        #self.ig_item = InstagramItem('mei.x.mei')

        #self.profile = ig_item.get_user_profile()
        # self.latest_post = None
        # self.profile = None

    @commands.command()
    async def hello(self, ctx):
        await ctx.send('Hello from command!')

    def generate_embed(self, index, profile, latest_post):
       
        hashtags = latest_post.hashtags
        
        embed = discord.Embed(
            title=profile['fullname'],
            description='',
            #color=0x00ff00
            #color=0x2fd7d2
            color=0xff00ff
        )

        embed.set_author(name= profile['username'], 
                         url= f'https://www.instagram.com/{profile['username']}/', 
                         icon_url=profile['thumbnail'])
        
        embed.set_thumbnail(url=profile['thumbnail'])
        embed.url = f'https://www.instagram.com/{profile['username']}/'

        item = latest_post.post_items[index]
        embed.add_field(
            name="貼文連結：",
            value=f"[點擊這裡觀看](https://www.instagram.com/p/{latest_post.code})",
            inline=True
        ) 
        embed.add_field(
            name="貼文時間(UTC)：",
            value=latest_post.date_utc,
            inline=True
        ) 
        if item.type == 'image':
            embed.set_image(url=item.url).set_image(url=item.url)
            embed.add_field(
                name="圖片：",
                value='',
                inline=False
            )
        else:
            embed.set_image(url=item.url)
            embed.add_field(
                name="影片：",
                value=f"[點擊這裡觀看]({item.video_url})",
                inline=False
            )  

        #show hashtags
        embed.set_footer(text=hashtags if len(hashtags) > 0 else '')  
        #embed.set_footer(text=f'貼文時間(UTC): {self.latest_post['date_utc']}')

        return embed

    @commands.command()
    async def show_items(self, ctx, username: str):
        ig_item = InstagramItem(username)
        profile = ig_item.get_user_profile()
        latest_post = ig_item.get_latest_post()
        view = PaginationView(total_items=len(latest_post.post_items), update_embed_callback=self.generate_embed, profile=profile, latest_post=latest_post)
        embed = self.generate_embed(0, profile, latest_post)
        caption = latest_post.caption
        caption = re.sub(r'#\w+', '', caption).strip()
        if len(caption) > 100:
            caption = f'{caption[:100]} ... [<詳見貼文>](https://www.instagram.com/p/{latest_post.code})'
        await ctx.send(content=f'# {profile['fullname']}的貼文：\n{caption}', embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Commands(bot))