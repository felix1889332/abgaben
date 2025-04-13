import discord
from discord.ext import commands
from discord import option
from datetime import datetime
import os

# === Channel-IDs ===
EIN_AUSZAHLUNGEN_CHANNEL_ID = 1208870790934700104
ABGABEN_CHANNEL_ID = 1256267489231376454

# === Intents & Bot Setup ===
intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(intents=intents)

def get_kw():
    return datetime.now().isocalendar()[1]

@bot.event
async def on_ready():
    print(f"✅ Bot ist online als {bot.user}")

@bot.slash_command(description="Eine Einzahlung buchen")
@option("person", description="Wer zahlt ein?", type=discord.Member)
@option("betrag", description="Wie viel?", type=int)
@option("grund", description="Wofür?", type=str)
async def einzahlen(ctx, person: discord.Member, betrag: int, grund: str):
    embed = discord.Embed(
        title="💰 Einzahlungsbeleg",
        color=discord.Color.green(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="👤 Person", value=person.mention, inline=False)
    embed.add_field(name="💵 Betrag", value=f"{betrag}€", inline=False)
    embed.add_field(name="📝 Grund", value=grund, inline=False)
    embed.set_footer(text=f"Erstellt von {ctx.author.name} am {datetime.now().strftime('%d.%m.%Y – %H:%M Uhr')}")

    channel = bot.get_channel(EIN_AUSZAHLUNGEN_CHANNEL_ID)
    await channel.send(embed=embed)
    await ctx.respond("✅ Einzahlung erfasst!", ephemeral=True)

@bot.slash_command(description="Eine Abhebung buchen")
@option("person", description="Wer hebt ab?", type=discord.Member)
@option("betrag", description="Wie viel?", type=int)
@option("grund", description="Wofür?", type=str)
async def abheben(ctx, person: discord.Member, betrag: int, grund: str):
    embed = discord.Embed(
        title="🏧 Abhebungsbeleg",
        color=discord.Color.red(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="👤 Person", value=person.mention, inline=False)
    embed.add_field(name="💵 Betrag", value=f"{betrag}€", inline=False)
    embed.add_field(name="📝 Grund", value=grund, inline=False)
    embed.set_footer(text=f"Erstellt von {ctx.author.name} am {datetime.now().strftime('%d.%m.%Y – %H:%M Uhr')}")

    channel = bot.get_channel(EIN_AUSZAHLUNGEN_CHANNEL_ID)
    await channel.send(embed=embed)
    await ctx.respond("✅ Abhebung erfasst!", ephemeral=True)

@bot.slash_command(description="Wöchentliche Abgabe eintragen")
@option("vonwem", description="Wer gibt ab? (Name)", type=str)
@option("betrag", description="Wie viel?", type=int)
async def abgabe(ctx, vonwem: str, betrag: int):
    embed = discord.Embed(
        title="📤 Abgabe",
        color=discord.Color.light_grey(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="👤 Von", value=vonwem, inline=False)
    embed.add_field(name="📅 Kalenderwoche", value=f"KW {get_kw()}", inline=False)
    embed.add_field(name="💵 Betrag", value=f"{betrag}€", inline=False)
    embed.set_footer(text=f"Erstellt von {ctx.author.name} am {datetime.now().strftime('%d.%m.%Y – %H:%M Uhr')}")

    channel = bot.get_channel(ABGABEN_CHANNEL_ID)
    await channel.send(embed=embed)
    await ctx.respond("✅ Abgabe erfasst!", ephemeral=True)

# === Bot starten ===
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("❌ Umgebungsvariable DISCORD_TOKEN wurde nicht gesetzt!")
bot.run(TOKEN)
