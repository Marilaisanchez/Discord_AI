import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import clases

load_dotenv()
token = os.getenv("dt")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="*", intents=intents)

@bot.event
async def on_ready():
    print(f"Se inició sesión con {bot.user}")

@bot.command(name = "file")
async def upload(ctx):
    if ctx.message.attachments:
        for file in ctx.message.attachments:
            file_name = file.filename
            file_url = file.url
            await file.save(f"./{file_name}")
            await ctx.send(f"Imágen guardada en ./ {file_name}")
    else:
        await ctx.send("Olvidaste subir una imágen.")

@bot.command(name="prediccion")
async def classify(ctx):
    if ctx.message.attachments:
        for ath in ctx.message.attachments:
            file_name = f"./{ath.filename}"
            file_url = ath.url
            class_name, confidence_score = clases.getClass(file_name)
            percentage = confidence_score*100
            await ath.save(f"./{ath.filename}")
            embed = discord.Embed(
                title = "Resultados",
                description = f"**Clase Predicha:**{class_name} \n **Confianza:**{percentage:.2f}%",
                color = 0x27548A
            )

            embed.set_footer(text="Analizando con Tensorflow y Keras")
            embed.set_author(name="Mariana Lai")
            embed.set_thumbnail(url=file_url)
            embed.add_field(name="Espero la predicción sea exacta", value="🥳", inline=True)
            await ctx.send(embed=embed)
    else: 
        await ctx.send("Te olvidaste el archivo.")

bot.run(token)