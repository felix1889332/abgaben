
import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
import os

# === Channel-IDs ===
EIN_AUSZAHLUNGEN_CHANNEL_ID = 1208870790934700104
ABGABEN_CHANNEL_ID = 1208869756518535228
# === Intents ===
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# === Bot-Klasse ===
class BotClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f"✅ Bot ist online als {self.user}")
        await self.tree.sync()
        print("✅ Slash-Commands synchronisiert.")

bot = BotClient()

# === Kalenderwoche berechnen ===
def get_kw():
    return datetime.now().isocalendar()[1]

# === Dropdown-Auswahl Geldart ===
geldarten = [
    app_commands.Choice(name="🟢 grün", value="grün"),
    app_commands.Choice(name="⚫️ schwarz", value="schwarz")
]

# === Slash-Command: Einzahlung ===
@bot.tree.command(name="einzahlen", description="Eine Einzahlung erfassen")
@app_commands.describe(
    person="Wer hat eingezahlt?",
    betrag="Wie viel wurde eingezahlt?",
    art="Welche Art von Geld?",
    grund="Wofür ist das Geld?"
)
@app_commands.choices(art=geldarten)
async def einzahlen(interaction: discord.Interaction, person: discord.Member, betrag: int, art: app_commands.Choice[str], grund: str):
    emoji = "🟢" if art.value == "grün" else "⚫️"
    embed = discord.Embed(title="💰 Einzahlungsbeleg", color=discord.Color.green(), timestamp=datetime.utcnow())
    embed.add_field(name="👤 Person", value=person.mention, inline=False)
    embed.add_field(name="💵 Betrag", value=f"{betrag}€ ({emoji} {art.value})", inline=False)
    embed.add_field(name="📝 Grund", value=grund, inline=False)
    embed.set_footer(text=f"Erstellt von {interaction.user.display_name} am {datetime.now().strftime('%d.%m.%Y – %H:%M Uhr')}")
    await bot.get_channel(EIN_AUSZAHLUNGEN_CHANNEL_ID).send(embed=embed)
    await interaction.response.send_message("✅ Einzahlung erfasst!", ephemeral=True)

# === Slash-Command: Auszahlung ===
@bot.tree.command(name="abheben", description="Eine Auszahlung erfassen")
@app_commands.describe(
    person="Wer bekommt das Geld?",
    betrag="Wie viel wird ausgezahlt?",
    art="Welche Art von Geld?",
    grund="Wofür ist das Geld?"
)
@app_commands.choices(art=geldarten)
async def abheben(interaction: discord.Interaction, person: discord.Member, betrag: int, art: app_commands.Choice[str], grund: str):
    emoji = "🟢" if art.value == "grün" else "⚫️"
    embed = discord.Embed(title="🏧 Abhebungsbeleg", color=discord.Color.red(), timestamp=datetime.utcnow())
    embed.add_field(name="👤 Person", value=person.mention, inline=False)
    embed.add_field(name="💵 Betrag", value=f"{betrag}€ ({emoji} {art.value})", inline=False)
    embed.add_field(name="📝 Grund", value=grund, inline=False)
    embed.set_footer(text=f"Erstellt von {interaction.user.display_name} am {datetime.now().strftime('%d.%m.%Y – %H:%M Uhr')}")
    await bot.get_channel(EIN_AUSZAHLUNGEN_CHANNEL_ID).send(embed=embed)
    await interaction.response.send_message("✅ Auszahlung erfasst!", ephemeral=True)


# === Slash-Command: Abgabe ===
@bot.tree.command(name="abgabe", description="Wöchentliche Abgabe eintragen")
@app_commands.describe(
    vonwem="Wer hat abgegeben?",
    betrag="Wie viel wurde abgegeben?",
    kw="Welche Kalenderwoche? (z. B. 15)"
)
async def abgabe(interaction: discord.Interaction, vonwem: str, betrag: str, kw: int):
    embed = discord.Embed(title="📤 Abgabe", color=discord.Color.light_grey(), timestamp=datetime.utcnow())
    embed.add_field(name="👤 Von", value=vonwem, inline=False)
    embed.add_field(name="📅 Kalenderwoche", value=f"**KW {kw}**", inline=False)
    embed.add_field(name="💵 Betrag", value=betrag, inline=False)
    embed.set_footer(text=f"Erstellt von {interaction.user.display_name} am {datetime.now().strftime('%d.%m.%Y – %H:%M Uhr')}")
    await bot.get_channel(ABGABEN_CHANNEL_ID).send(embed=embed)
    await interaction.response.send_message("✅ Abgabe eingetragen!", ephemeral=True)


# === Bot starten ===
bot.run(os.getenv("DISCORD_TOKEN"))
