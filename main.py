import discord
from discord.ext import commands
import json

if __name__ == "__main__":
    #載入設定檔
    with open('configs/config.json') as f:
        config = json.load(f)
    
    intents = discord.Intents.default()
    #需要處理訊息
    intents.message_content = True 
    bot = commands.Bot(intents=intents, command_prefix=config['PREFIX'])
  
    #定義on_ready event
    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user.name}')
        await bot.load_extension('cogs.commands')
        await bot.load_extension('cogs.events')
  
  
    bot.run(config['TOKEN'])