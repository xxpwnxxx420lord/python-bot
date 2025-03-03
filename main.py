import discord
from discord import app_commands
import requests
import random
import roblox
import re
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import asyncio

BotToken = ""
ops = ["heads", "tails"]
bot_name = "xxpwnxxx420lord"

def get_roblox_info(place_id):
    service = Service(r"D:/code/iownyoukid/chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get(f"https://www.roblox.com/games/{place_id}")
        
        # Wait for elements with explicit waits
        visits = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "game-visits-count"))
        ).text
        
        title = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.game-name"))
        ).text
        
        author = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.game-creator"))
        ).text
        
    except Exception as e:
        return {"error": str(e)}
    finally:
        driver.quit()
    
    return {
        "visits": visits,
        "title": title,
        "author": author,
        "link": f"https://www.roblox.com/games/{place_id}"
    }

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
            print("Synced Commands")
        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="https://github.com/xxpwnxxx420lord"
            )
        )
        print('working <3')

    async def on_close(self):
        print("Bot is shutting down...")

client = aclient()
tree = app_commands.CommandTree(client)

@tree.command(name="validate", description="validate roblox usernames")
async def bazinga(interaction: discord.Interaction, user: str):
    requesturl = f'https://auth.roblox.com/v1/usernames/validate?request.username={user}&request.birthday=1999-04-20'
    response = requests.get(requesturl)
    if response.status_code == 200:
        await interaction.response.send_message(f"**the api returned**: {response.json()}")
    else:
        await interaction.response.send_message(f"**Error**: {response.json()}")

@tree.command(name="define", description="See the definition of a word or phrase from the Dictionary")
async def define(interaction: discord.Interaction, term: str):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{term}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()[0]
        dictionary = discord.Embed(
            title=f"Definition of {' '.join(word.capitalize() for word in term.split())}",
            color=discord.Color.orange()
        )
        for meaning in data["meanings"]:
            part_of_speech = meaning["partOfSpeech"]
            definitions = meaning["definitions"][0]["definition"]
            example = meaning["definitions"][0].get("example", "No example available")
            dictionary.add_field(name="Part Of Speech", value=part_of_speech, inline=False)
            dictionary.add_field(name="Definition", value=definitions, inline=False)
            dictionary.add_field(name="Example", value=example, inline=False)
        await interaction.response.send_message(f"We've defined {term} for you, <@{interaction.user.id}>", embed=dictionary)
    else:
        dictionary = discord.Embed(
            title="Error",
            description=f"Sorry, I could not find the definition of {' '.join(word.lower() for word in term.split())}.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(f"Looks like we couldn't define {term}, <@{interaction.user.id}>", embed=dictionary)

@tree.command(name="headsortails", description="heads or tails")
async def idk(interaction: discord.Interaction):
    await interaction.response.send_message(random.choice(ops))

@tree.command(name="gameinfo", description="Get detailed information about a Roblox game")
async def game_info(interaction: discord.Interaction, place_id: int):
    await interaction.response.defer()
    
    try:
        data = await asyncio.to_thread(get_roblox_info, place_id)
        
        if "error" in data:
            raise RuntimeError(data["error"])
            
        embed = discord.Embed(
            title=data["title"],
            description=f"**Game ID:** {place_id}",
            color=0x00FF00
        )
        embed.add_field(name="Visits", value=data["visits"], inline=True)
        embed.add_field(name="Creator", value=data["author"], inline=True)
        embed.add_field(name="Link", value=data["link"], inline=False)
        embed.set_footer(text="Powered by Roblox API")
        
        await interaction.followup.send(embed=embed)
        
    except Exception as e:
        error_embed = discord.Embed(
            title="Error",
            description=f"Failed to fetch game info: {str(e)}",
            color=0xFF0000
        )
        await interaction.followup.send(embed=error_embed) # this is so peak am i right

@tree.command(name="userinfo", description="Get detailed information about a Roblox user")
async def userinfo(interaction: discord.Interaction, user: int):
    url = f'https://users.roblox.com/v1/users/{user}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        embed = discord.Embed(
            title=f"👤 {data['name']}",
            description=f"🔗 [Profile](https://www.roblox.com/users/{user}/profile)",
            color=0x00FF00
        )
        
        embed.add_field(name="📛 Display Name", value=data['displayName'], inline=False)
        embed.add_field(name="📜 Description", value=data['description'] if data['description'] else "No description", inline=False)
        embed.add_field(name="📅 Creation Date", value=data['created'], inline=False)
        embed.add_field(name="✅ Verified Badge", value="Yes" if data['hasVerifiedBadge'] else "No", inline=False)
        embed.add_field(name="🚫 Banned", value="Yes" if data['isBanned'] else "No", inline=False)
        embed.set_footer(text="https://")

        await interaction.response.send_message(embed=embed)

    else:
        await interaction.response.send_message(f"❌ Error: Unable to fetch user data. ({response.status_code})")

try:
    client.run(BotToken)
except Exception as e:
    print(f"An error occurred: {e}")
