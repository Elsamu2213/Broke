import discord
from discord.ext import commands
import requests

TOKEN = 'MTI5ODU0MjUyNTkwODM4NTgxMw.GN504t.7M-B0owLgS2e7mlWbmC6Jzr4T53Vy7CVm1VxHU'
CHANNEL_ID = 1298417233290072087  # Asegúrate de que sea un entero
API_URL = 'http://127.0.0.1:8000/api/actualizar_estado/'  # URL correcta de tu API

intents = discord.Intents.default()
intents.message_content = True 
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

ESTADOS_VALIDOS = ['iniciado', 'en_proceso', 'Anclaje_completado', 'cancelado','completado', 'pendiente_revision', 'reprogramado']

# Comando para actualizar el estado de la tarea
@client.command(name='actualizar_estado')
async def actualizar_estado(ctx, tarea_id: int, nuevo_estado: str):
    if nuevo_estado not in ESTADOS_VALIDOS:
        await ctx.send(f"Estado inválido. Los estados válidos son: {', '.join(ESTADOS_VALIDOS)}.")
        return
    
    url = API_URL
    data = {
        'id': tarea_id,
        'estado': nuevo_estado
    }

    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            await send_message_to_discord(f"El estado de la tarea {tarea_id} ha sido actualizado a {nuevo_estado}.")
        else:
            await send_message_to_discord(f"No se pudo actualizar el estado de la tarea {tarea_id}. Error: {response.json().get('error')}")
    except Exception as e:
        await send_message_to_discord(f"Hubo un error al intentar actualizar el estado: {e}")

@client.command(name='info_tarea')
async def info_tarea(ctx, tarea_id: int):
    try:
        # Hacer una solicitud GET a tu API para obtener los detalles de la tarea
        response = requests.get(f"http://127.0.0.1:8000/api/tarea/{tarea_id}/")
        if response.status_code == 200:
            data = response.json()
            mensaje = (
                f"Tarea ID: {data['id']}\n"
                f"Estado: {data['estado']}\n"
                f"Asignada a: {data['usuario']}\n"
                
            )
            await ctx.send(mensaje)
        else:
            await ctx.send(f"No se pudo encontrar la tarea con ID {tarea_id}.")
    except Exception as e:
        await ctx.send(f"Error al obtener la información de la tarea: {e}")

# Iniciar el bot
client.run(TOKEN)
