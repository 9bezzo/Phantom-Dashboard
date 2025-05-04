import discord
from discord.ext import commands, tasks
import json
from discord.commands import Option
import os
from dotenv import load_dotenv
import platform
from datetime import datetime
import colorama
from colorama import Fore, Style
import pyfiglet

colorama.init()
load_dotenv()


intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, cache_app_emojis=True)
bot.remove_command('help')

with open("Rendex/phantom/config/config.json") as f:
    config = json.load(f)

cogs_list = [
]


def print_status(status, message):
    status_colors = {
        "LOADING": Fore.YELLOW,
        "READY": Fore.GREEN,
        "ERROR": Fore.RED,
        "SYNC": Fore.CYAN,
        "EVENT": Fore.MAGENTA
    }
    
    print(f"{status_colors.get(status, Fore.WHITE)}[{status.center(9)}]{Style.RESET_ALL} {message}")
    
    
@bot.event
async def on_ready():
    print_header()
    for cog in cogs_list:
        try:
            bot.load_extension(f'cogs.{cog}')
            print_status("LOADING", f"Cog geladen: {Fore.BLUE}{cog}{Style.RESET_ALL}")
        except Exception as e:
            print_status("ERROR", f"Fehler beim Laden von {cog}: {Fore.RED}{e}{Style.RESET_ALL}")
    update_status.start()
    guild_count = len(bot.guilds)
    member_count = sum(guild.member_count for guild in bot.guilds)
    print_status("READY", f"Bot eingeloggt als {Fore.YELLOW}{bot.user}{Style.RESET_ALL}")
    print_status("EVENT", f"Verbunden mit {Fore.CYAN}{guild_count}{Style.RESET_ALL} Servern und {Fore.CYAN}{member_count}{Style.RESET_ALL} Mitgliedern")
    print_status("READY", f"{Fore.GREEN}Bot ist online! 🚀{Style.RESET_ALL}")
    await bot.sync_commands()
    print_status("SYNC", f"Slash Commands global synchronisiert")
    print(Fore.LIGHTMAGENTA_EX + "\n" + "═" * 60)
    print(f"🔮 {Fore.BLUE}Phantom-System aktiv | Made with Bezzi {Fore.LIGHTMAGENTA_EX} 🔮")
    print("-" * 60 + Style.RESET_ALL)

@tasks.loop(seconds=15)
async def update_status():
    total_members = sum(guild.member_count for guild in bot.guilds)
    statuses = [
        discord.Activity(type=discord.ActivityType.listening, name=f"{total_members} Mitglieder"),
        discord.Activity(type=discord.ActivityType.playing, name="mit bezzo fangen"),
        discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.guilds)} Server")
    ]
    current_status = statuses[int(update_status.current_loop) % len(statuses)]
    await bot.change_presence(activity=current_status)
    
bot.run( ["token"])
    