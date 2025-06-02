import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Configurar intents con todos habilitados
intents = discord.Intents.all()

# Crear instancia del bot con intents y prefijo "!"
bot = commands.Bot(command_prefix='!', intents=intents)

# Comando 1: pong con "lactancia real" (nombre del bot)
@bot.command(name='pong')
async def pong(ctx):
    await ctx.send(f'Pong, soy {bot.user.name} 🍼')

# Comando 2: hola
@bot.command(name='hola')
async def hola(ctx):
    await ctx.send(f'Hola, {ctx.author.mention}! 👋')

# Comando 3: info
@bot.command(name='info')
async def info(ctx):
    await ctx.send('Soy un bot básico con comandos de moderación y más. 🚀')

# Comandos de moderación

# Kick: Expulsa a un usuario del servidor
@bot.command(name='kick')
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    try:
        await member.kick(reason=reason)
        await ctx.send(f'Usuario {member.mention} ha sido expulsado. 🚪')
    except Exception as e:
        await ctx.send(f'No pude expulsar al usuario: {e}')

# Ban: Banea a un usuario del servidor
@bot.command(name='ban')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    try:
        await member.ban(reason=reason)
        await ctx.send(f'Usuario {member.mention} ha sido baneado. ⛔')
    except Exception as e:
        await ctx.send(f'No pude banear al usuario: {e}')

# Unban: Desbanea a un usuario (por su nombre#discriminator)
@bot.command(name='unban')
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Usuario {user.mention} ha sido desbaneado. ✅')
            return
    await ctx.send(f'No encontré a {member} en la lista de baneados.')

# Evento on_ready para indicar que el bot está activo
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

# Ejecutar el bot
bot.run(TOKEN)
