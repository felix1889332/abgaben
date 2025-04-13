import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
import os

# === Channel-IDs ===
EIN_AUSZAHLUNGEN_CHANNEL_ID = 1208870790934700104
ABGABEN_CHANNEL_ID = 1256267489231376454

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class MyClient(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        print("✅ Slash-Commands wurden synchronisiert.")

bot = MyClient()

def get_kw():
    return datetime.now().isocalendar()[1]

@bot.event
async def on_ready():
    print(f"✅ Bot ist online als {bot.user}")

@bot.tree.command(name="einzahlen", description="Erstellt eine Einzahlung")
@app_commands.describe(person="Wer zahlt ein?", betrag="Betrag in €", grund="Grund der Einzahlung")
async def einzahlen(interaction: discord.Interaction, person: discord.Member, betrag: int, grund: str):
    embed = discord.Embed(
        title="💰 Einzahlungsbeleg",
        color=discord.Color.green(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="👤 Person", value=person.mention, inline=False)
    embed.add_field(name="💵 Betrag", value=f"{betrag}€", inline=False)
    embed.add_field(name="📝 Grund", value=grund, inline=False)
    embed.set_footer(text=f"Erstellt von {interaction.user.name} am {datetime.now().strftime('%d.%m.%Y – %H:%M Uhr')}")
    
    channel = bot.get_channel(EIN_AUSZAHLUNGEN_CHANNEL_ID)
    await channel.send(embed=embed)
    await interaction.response.send_message("✅ Einzahlung wurde eingetragen!", ephemeral=True)

@bot.tree.command(name="abheben", description="Erstellt eine Abhebung")
@app_commands.describe(person="Wer hebt ab?", betrag="Betrag in €", grund="Grund der Abhebung")
async def abheben(interaction: discord.Interaction, person: discord.Member, betrag: int, grund: str):
    embed = discord.Embed(
        title="🏧 Abhebungsbeleg",
        color=discord.Color.red(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="👤 Person", value=person.mention, inline=False)
    embed.add_field(name="💵 Betrag", value=f"{betrag}€", inline=False)
    embed.add_field(name="📝 Grund", value=grund, inline=False)
    embed.set_footer(text=f"Erstellt von {interaction.user.name} am {datetime.now().strftime('%d.%m.%Y – %H:%M Uhr')}")
    
    channel = bot.get_channel(EIN_AUSZAHLUNGEN_CHANNEL_ID)
    await channel.send(embed=embed)
    await interaction.response.send_message("✅ Abhebung wurde eingetragen!", ephemeral=True)

@bot.tree.command(name="abgabe", description="Erstellt eine wöchentliche Abgabe")
@app_commands.describe(vonwem="Name der Person (frei wählbar)", betrag="Betrag in €")
async def abgabe(interaction: discord.Interaction, vonwem: str, betrag: int):
    embed = discord.Embed(
        title="📤 Abgabe",
        color=discord.Color.light_grey(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="👤 Von", value=vonwem, inline=False)
    embed.add_field(name="📅 Kalenderwoche", value=f"KW {get_kw()}", inline=False)
    embed.add_field(name="💵 Betrag", value=f"{betrag}€", inline=False)
    embed.set_footer(text=f"Erstellt von {interaction.user.name} am {datetime.now().strftime('%d.%m.%Y – %H:%M Uhr')}")
    
    channel = bot.get_channel(ABGABEN_CHANNEL_ID)
    await channel.send(embed=embed)
    await interaction.response.send_message("✅ Abgabe wurde eingetragen!", ephemeral=True)

# === Bot starten ===
bot.run(os.getenv("DISCORD_TOKEN"))
