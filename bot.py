from config import *
from logic import *
import discord
from discord.ext import commands
from config import TOKEN
import os

# Veri tabanı yöneticisini başlatma
manager = DB_Map("database.db")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot başlatıldı!")

@bot.command()
async def start(ctx: commands.Context):
    await ctx.send(f"Merhaba, {ctx.author.name}. Mevcut komutlarin listesini keşfetmek için !help_me yazin.")

@bot.command()
async def help_me(ctx: commands.Context):
    commands_list = (
        "**Mevcut Komutlarimiz:**\n"
        "`!start` - Botu baslatir.\n"
        "`!help_me` - Yardim mesajini gonderir.\n"
        "`!remember_city <şehir adı>` - Sehri kaydeder.\n"
        "`!show_city <şehir adı>` - Belirtilen sehrin haritasini gosterir.\n"
        "`!show_my_cities` - Kayitli sehirlerin hartisini gosterir.\n"
    )
    await ctx.send(commands_list)

@bot.command()
async def show_city(ctx: commands.Context, *, city_name=""):
    # Belirtilen şehirle birlikte haritayı gösterecek komutu yazın.
    if not city_name:
        await ctx.send("Hatalı format. Lütfen şehir adını İngilizce olarak ve komutan sonra bir boşluk bırakarak çerçevesinde bulunmaktadır.")
        return
    manager.create_graph(f'{ctx.author.id}.png', [city_name])
    await ctx.send(file=discord.File(f'{ctx.author.id}.png'))


@bot.command()
async def show_my_cities(ctx: commands.Context):
    cities = manager.select_cities(ctx.author.id)  # Kullanıcının kaydettiği şehirlerin listesini alma
    # Kullanıcının şehirleriyle birlikte haritayı gösterecek komutu yazın
    if cities:
        manager.create_graph(f'{ctx.author.id}.cities.png', cities)
        await ctx.send(file=discord.File(f'{ctx.author.id}_cities.png'))
    else:
        await ctx.send("Henüz hiç şehir kaydetmediniz.")

@bot.command()
async def remember_city(ctx: commands.Context, *, city_name=""):
    if not city_name:
        await ctx.send("Istediginiz sehir adini girin, orn olarak: `!remember_city Tokyo`")
        return

    if manager.add_city(ctx.author.id, city_name):
        await ctx.send(f"'{city_name}' Kayit basarili")
    else:
        await ctx.send("Sehir veritabaninda yok.")

if __name__ == "__main__":
    bot.run(TOKEN)
