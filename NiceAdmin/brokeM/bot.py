import discord
from discord.ext import commands

# Reemplaza 'your_token_here' con el token de tu bot
TOKEN = 'MTI5ODU0MjUyNTkwODM4NTgxMw.GN504t.7M-B0owLgS2e7mlWbmC6Jzr4T53Vy7CVm1VxHU'

# Reemplaza 'your_channel_id_here' con el ID del canal donde quieres enviar mensajes
CHANNEL_ID = 1298417233290072087  # Asegúrate de que sea un entero

intents = discord.Intents.default()
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print(f'Conectado como {client.user}')

# Función para enviar mensajes
async def send_message_to_discord(message):
    channel = client.get_channel(int(CHANNEL_ID))
    if channel:
        await channel.send(message)
    else:
        print(f'No se encontró el canal con ID: {CHANNEL_ID}')

# Iniciar el bot
client.run(TOKEN)