#FwEln0ZYPFL7E9gW5Y9Lx7PdHgBI-GqJ
import discord
from discord.ext import commands
import youtube_dl
import os
from keep_alive import keep_alive

client = commands.Bot(command_prefix=">")

@client.command()
async def help_me(ctx):
  await ctx.send("Hello! I'm the IHOP radio bot created by the genius himself, Jodie!\nKeep in mind there's probably a humongous amount of errors, this hasn't been tested at all.")
  await ctx.send("Remember, this is freshly in development so don't be too rough. If you come across an error, message my creator @Lance A#1696.")
  await ctx.send("The commands are:\n-----**play**\n-----**leave**\n-----**pause**\n-----**resume**\n-----**stop**")
  await ctx.send("The way to play a song is to join a voice channel, and you put a YouTube link.\nFor example: >play https://www.youtube.com/watch?v=BSNDJ3U5DyY\nMy creator hasn't looked into making a search engine so you can use just the name of the video yet, what a dummy.")

@client.command()
async def play(ctx, url : str):
  song_there = os.path.isfile("song.webm")
  try:
      if song_there:
          os.remove("song.webm")
  except PermissionError:
      await ctx.send("Wait for the current playing music to end or use the 'stop' command")
      return

  voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voice and voice.is_connected():
    await voiceChannel.connect()

  
  ydl_opts = {
      'format': '249/250/251'
  }
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      ydl.download([url])
  for file in os.listdir("./"):
      if file.endswith(".webm"):
          os.rename(file, "song.webm")
  voice.play(discord.FFmpegOpusAudio ("song.webm"))

@client.command()
async def leave(ctx):
  voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
  if not (voice == None):
    await voice.disconnect()
  else:
    await ctx.send("I'm not in a voice channel.")

@client.command()
async def pause(ctx):
  voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
  if voice != None and voice.is_playing():
    await voice.pause()
  else:
    await ctx.send("I'm not talking right now! Please chill tf out.")

@client.command()
async def resume(ctx):
  voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
  if voice != None and voice.is_paused():
    await voice.resume()
  else:
    await ctx.send("Don't interrupt me while I'm playing, baka~.")

@client.command()
async def stop(ctx):
  voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
  if voice != None:
    voice.stop()

keep_alive()
client.run("ODQ0NzI3ODYzODM1MDk5MTM2.YKWoIQ.iCwZnXFuEkQw542C0FQL5lDoATs")