import discord
from discord.ext import commands
from datetime import datetime
import os

# === Channel IDs (anpassen, falls nötig) ===
EIN_AUSZAHLUNGEN_CHANNEL_ID = 1208870790934700104
ABGABEN_CHANNEL_ID = 1256267489231376454

# === Intents ===
intents = discord.Intents.default()
intents.message_content = True  # Aktiv, weil Commands Inhalt brauchen

bot = commands.Bot(command_prefix="!", intents=intents)

# === Utility-Funktionen ===
def get_kw():
    return datetime.now().isocalendar()[1]

def create_embed(titel, farbe, fields: list, autorname):
    embed = discord.Embed(
        title=titel,
        color=farbe,
        timestamp=datetime.utcnow()
    )
    for name, value in fields:
        embed.add_field(name=name, value=value, inline=False)
    embed.set_footer(text=f"Erstellt von {autorname} am {datetime.now().strftime('%d.%m.%Y – %H:%M Uhr')}")
    return embed

# === Commands ===
@bot.command()
async def einzahlen(ctx, person: discord.Member, betrag: int, *, grund: str):
    channel = bot.get_channel(EIN_AUSZAHLUNGEN_CHANNEL_ID)
    if not channel:
        await ctx.send("❌ Channel nicht gefunden.")
        return

    embed = create_embed(
        titel="💰 Einzahlungsbeleg",
        farbe=discord.Color.green(),
        fields=[
            ("👤 Person", person.mention),
            ("💵 Betrag", f"{betrag}€"),
            ("📝 Grund", grund)
        ],
        autorname=ctx.author.name
    )
    await channel.send(embed=embed)
    await ctx.message.add_reaction("✅")

@bot.command()
async def abheben(ctx, person: discord.Member, betrag: int, *, grund: str):
    channel = bot.get_channel(EIN_AUSZAHLUNGEN_CHANNEL_ID)
    if not channel:
        await ctx.send("❌ Channel nicht gefunden.")
        return

    embed = create_embed(
        titel="🏧 Abhebungsbeleg",
        farbe=discord.Color.red(),
        fields=[
            ("👤 Person", person.mention),
            ("💵 Betrag", f"{betrag}€"),
            ("📝 Grund", grund)
        ],
        autorname=ctx.author.name
    )
    await channel.send(embed=embed)
    await ctx.message.add_reaction("✅")

@bot.command()
async def abgabe(ctx, vonwem: str, betrag: int):
    channel = bot.get_channel(ABGABEN_CHANNEL_ID)
    if not channel:
        await ctx.send("❌ Channel nicht gefunden.")
        return

    embed = create_embed(
        titel="📤 Abgabe",
        farbe=discord.Color.greyple(),
        fields=[
            ("👤 Von", vonwem),
            ("📅 Kalenderwoche", f"KW {get_kw()}"),
            ("💵 Betrag", f"{betrag}€")
        ],
        autorname=ctx.author.name
    )
    await channel.send(embed=embed)
    await ctx.message.add_reaction("✅")

# === Bot starten ===
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("❌ Umgebungsvariable DISCORD_TOKEN wurde nicht gesetzt!")

bot.run(TOKEN)
