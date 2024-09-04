import discord
from discord.ext import commands
from modules.view import PaginationView

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.items = [
            {"name": "Nike Air Max 270", "price": "$150", "size": "42", "status": "全新", "image": "https://instagram.ftpe8-1.fna.fbcdn.net/v/t51.29350-15/458413088_1956022628244917_3677759123784150843_n.jpg?stp=dst-jpg_e35&efg=eyJ2ZW5jb2RlX3RhZyI6ImltYWdlX3VybGdlbi4xNDQweDE4MDAuc2RyLmYyOTM1MC5kZWZhdWx0X2ltYWdlIn0&_nc_ht=instagram.ftpe8-1.fna.fbcdn.net&_nc_cat=105&_nc_ohc=cRhM5F-UKKsQ7kNvgFSWjcY&edm=ADW0ovcBAAAA&ccb=7-5&ig_cache_key=MzQ0OTYxMDc1NzUxMDY2OTEzMQ%3D%3D.2-ccb7-5&oh=00_AYCG7X47CJDH1pOPCK111eme4gBHApQQyazlkx8OhQ-3hQ&oe=66DE44EA&_nc_sid=db7772"},
            {"name": "Adidas Ultraboost", "price": "$180", "size": "43", "status": "全新", "image": "https://instagram.ftpe8-3.fna.fbcdn.net/v/t51.29350-15/455920025_839309535009614_3875311626818928475_n.jpg?stp=dst-jpg_e35&efg=eyJ2ZW5jb2RlX3RhZyI6ImltYWdlX3VybGdlbi4xNDQweDE4MDAuc2RyLmYyOTM1MC5kZWZhdWx0X2ltYWdlIn0&_nc_ht=instagram.ftpe8-3.fna.fbcdn.net&_nc_cat=102&_nc_ohc=wT6VNzxDSRAQ7kNvgGy5Cmj&_nc_gid=ebcd04fda6cb4b02b9a800e5bac53f84&edm=AJkpJWEBAAAA&ccb=7-5&ig_cache_key=MzQzNTYzNjExMDEyMTI1NzgxMg%3D%3D.2-ccb7-5&oh=00_AYC4J5BdSEmDt-_oDIVCxn-deHUUbQo6BhTcS18Z1wn1dw&oe=66DE6642&_nc_sid=c6ee3e"},
            {"name": "Puma RS-X", "price": "$130", "size": "41", "status": "八成新", "image": "https://instagram.ftpe8-2.fna.fbcdn.net/v/t51.29350-15/458492986_1032181578445803_4070476047221993206_n.jpg?stp=dst-jpg_e35&efg=eyJ2ZW5jb2RlX3RhZyI6ImltYWdlX3VybGdlbi4xNDQweDE4MDAuc2RyLmYyOTM1MC5kZWZhdWx0X2ltYWdlIn0&_nc_ht=instagram.ftpe8-2.fna.fbcdn.net&_nc_cat=103&_nc_ohc=-lVORBZqpkkQ7kNvgHHTAYD&edm=AJkpJWEBAAAA&ccb=7-5&ig_cache_key=MzQ0OTM1NDMzNzg1NDAxODc2Mw%3D%3D.3-ccb7-5&oh=00_AYBqtZPTRMTJLdueWd5sLK2MBlgHxiNddHQZPvpHT7IRWQ&oe=66DE770E&_nc_sid=c6ee3e"}
        ]

    @commands.command()
    async def hello(self, ctx):
        await ctx.send('Hello from command!')

    def generate_embed(self, index):
        item = self.items[index]
        embed = discord.Embed(
            title=item["name"],
            description=f"價格: {item['price']}\n尺寸: {item['size']}\n狀態: {item['status']}",
            color=0x00ff00
        )
        if item.get("image"):
            embed.set_image(url=item["image"])
        embed.set_footer(text=f"商品 {index + 1} / {len(self.items)}")
        
        if item.get("video"):
            embed.video(url=item['video'])
        return embed

    @commands.command()
    async def show_items(self, ctx):
        view = PaginationView(total_items=len(self.items), update_embed_callback=self.generate_embed)
        embed = self.generate_embed(0)
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Commands(bot))