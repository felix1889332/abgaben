import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
import os

# === Channel-IDs ===
EIN_AUSZAHLUNGEN_CHANNEL_ID = 1208870790934700104
ABGABEN_CHANNEL_ID = 1256267489231376454

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f"✅ Bot ist online als {self.user}")
        await self.tree.sync()
        print("✅ Slash-Commands synchronisiert.")

bot = MyClient()

def get_kw():
    return datetime.now().isocalendar()[1]

@bot.tree.command(name="einzahlen", description="Einzahlung erfassen")
@app_commands.describe(
    person="Wer hat eingezahlt?",
    betrag="Wie viel wurde eingezahlt?",
    art="Art des Geldes (grün oder schwarz)",
    grund="Wofür ist das Geld?"
)
async def einzahlen(interaction: discord.Interaction, person: discord.Member, betrag: int, art: str, grund: str):
    embed = discord.Embed(
        title="💰 Einzahlungsbeleg",
        color=discord.Color.green(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="👤 Person", value=person.mention, inline=False)
    embed.add_field(name="💵 Betrag", value=f"{betrag}€ ({art})", inline=False)
    embed.add_field(name="📝 Grund", value=grund, inline=False)
    embed.set_footer(text=f"Erstellt von {interaction.user.name} am {datetime.now().strftime('%d.%m.%Y – %H:%M Uhr')}")

    channel = bot.get_channel(EIN_AUSZAHLUNGEN_CHANNEL_ID)
    await channel.send(embed=embed)
    await interaction.response.send_message("✅ Einzahlung erfasst!", ephemeral=True)

@bot.tree.command(name="abheben", description="Auszahlung erfassen")
@app_commands.describe(
    person="Wer bekommt das Geld?",
    betrag="Wie viel wird ausgezahlt?",
    art="Art des Geldes (grün oder schwarz)",
    grund="Wofür ist das Geld?"
)
async def abheben(interaction: discord.Interaction, person: discord.Member, betrag: int, art: str, grund: str):
    embed = discord.Embed(
        title="🏧 Abhebungsbeleg",
        color=discord.Color.red(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="👤 Person", value=person.mention, inline=False)
    embed.add_field(name="💵 Betrag", value=f"{betrag}€ ({art})", inline=False)
    embed.add_field(name="📝 Grund", value=grund, inline=False)
    embed.set_footer(text=f"Erstellt von {interaction.user.name} am {datetime.now().strftime('%d.%m.%Y – %H:%M Uhr')}")

    channel = bot.get_channel(EIN_AUSZAHLUNGEN_CHANNEL_ID)
    await channel.send(embed=embed)
    await interaction.response.send_message("✅ Auszahlung erfasst!", ephemeral=True)

@bot.tree.command(name="abgabe", description="Wöchentliche Abgabe erfassen")
@app_commands.describe(
    vonwem="Wer zahlt die Abgabe?",
    betrag="Wie viel wird abgegeben?"
)
async def abgabe(interaction: discord.Interaction, vonwem: str, betrag: int):
    kw = get_kw()
    embed = discord.Embed(
        title="📤 Abgabe",
        color=discord.Color.light_grey(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="👤 Von", value=vonwem, inline=False)
    embed.add_field(name="📅 Kalenderwoche", value=f"KW {kw}", inline=False)
    embed.add_field(name="💵 Betrag", value=f"{betrag}€", inline=False)
    embed.set_footer(text=f"Erstellt von {interaction.user.name} am {datetime.now().strftime('%d.%m.%Y – %H:%M Uhr')}")

    channel = bot.get_channel(ABGABEN_CHANNEL_ID)
    await channel.send(embed=embed)
    await interaction.response.send_message("✅ Abgabe erfasst!", ephemeral=True)

# === Bot starten ===
bot.run(os.getenv("DISCORD_TOKEN"))
