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

# Comando para actualizar el estado de la tarea
@client.command(name='actualizar_estado')
async def actualizar_estado(ctx, tarea_id: int, nuevo_estado: str):
    url = API_URL  # Usamos la URL correcta 
    data = {
        'id': tarea_id,
        'estado': nuevo_estado
    }
    
    headers = {
        # Si la API no requiere autenticación, puedes eliminar este encabezado
        'Authorization': 'Bearer MTI5ODU0MjUyNTkwODM4NTgxMw.GN504t.7M-B0owLgS2e7mlWbmC6Jzr4T53Vy7CVm1VxHU'  # Asegúrate de reemplazarlo si es necesario
    }

    try:
        # Realizar la solicitud POST a la API de Django con el encabezado de autenticación
        response = requests.post(url, json=data, headers=headers)

        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            await send_message_to_discord(f"El estado del sitio {tarea_id} ha sido actualizado a {nuevo_estado}.")
        else:
            await send_message_to_discord(f"No se pudo actualizar el estado de la tarea {tarea_id}. Error: {response.json().get('error')}")
    except Exception as e:
        await send_message_to_discord(f"Hubo un error al intentar actualizar el estado: {e}")

# Iniciar el bot
client.run(TOKEN)
