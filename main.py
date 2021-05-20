#FwEln0ZYPFL7E9gW5Y9Lx7PdHgBI-GqJ
import discord
from discord.ext import commands
import youtube_dl
import os
from keep_alive import keep_alive
from discord import Color

client = commands.Bot(command_prefix=">")
client.remove_command("help")
'''
@client.command()
async def help_me(ctx):
  await ctx.send("Hello! I'm the IHOP radio bot created by the genius himself, Jodie!\nKeep in mind there's probably a humongous amount of errors, this hasn't been tested at all. The prefix is '>'")
  await ctx.send("Remember, this is freshly in development so don't be too rough. If you come across an error, message my creator <@184833237535686658>.")
  await ctx.send("The commands are:\n-----**play**\n-----**leave**\n-----**pause**\n-----**resume**\n-----**clear**")
  await ctx.send("The way to play a song is to join a voice channel, and you put a YouTube link.\nFor example: >play https://www.youtube.com/watch?v=BSNDJ3U5DyY\nMy creator hasn't looked into making a search engine so you can use just the name of the video yet, what a dummy.")
'''

@client.group(invoke_without_command = True)
async def help(ctx):
  em = discord.Embed(title = "Help", description = "Use >help <command> for extended info",color = Color.random())
  em.add_field(name = "Music", value = "play, clear, resume, pause, leave")
  em.add_field(name = "Fun", value = "nothing yet; todo (am open to suggestions)")
  await ctx.send(embed = em)

@help.command()
async def play(ctx):
  em = discord.Embed(title = "Play",description = "Plays a song given a YouTube URL. If not already in a voice channel, it will join the channel that the command caller is in.",color = Color.random())
  em.add_field(name = "**Syntax**", value = ">play <YouTube URL>")
  await ctx.send(embed = em)

@help.command()
async def leave(ctx):
  em = discord.Embed(title = "Leave",description = "Makes the bot leave the voice channel that it's in.",color = Color.random())
  em.add_field(name = "**Syntax**", value = ">leave")
  await ctx.send(embed = em)

@help.command()
async def clear(ctx):
  em = discord.Embed(title = "Clear",description = "Clears the bot of the current song and puts the bot in a ready state.",color = Color.random())
  em.add_field(name = "**Syntax**", value = ">clear")
  await ctx.send(embed = em)

@help.command()
async def resume(ctx):
  em = discord.Embed(title = "Resume",description = "Resumes the bot if it is paused.",color = Color.random())
  em.add_field(name = "**Syntax**", value = ">resume")
  await ctx.send(embed = em) 
  
@help.command()
async def pause(ctx):
  em = discord.Embed(title = "Pause",description = "Pauses the bot if it is playing.",color = Color.random())
  em.add_field(name = "**Syntax**", value = ">pause")
  await ctx.send(embed = em) 

@client.command(help = "Plays a song given a YouTube URL.")
async def play(ctx, url : str):
  if not ctx.message.author.voice:
    await ctx.send("You need to be in a voice channel to do this.")
    return
  else: 
    channel = ctx.message.author.voice.channel 
  song_there = os.path.isfile("song.webm")
  try:
    if song_there:
      os.remove("song.webm")
  except PermissionError:
    await ctx.send("Permission Error!")
    return

  voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=channel.name)
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if not (voice and voice.is_connected()):
    await voiceChannel.connect()
  RV = discord.utils.get(client.voice_clients, guild=ctx.guild)
  
  ydl_opts = {
      'format': '249/250/251'
  }
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      ydl.download([url])
  for file in os.listdir("./"):
      if file.endswith(".webm"):
          os.rename(file, "song.webm")

  try:
    RV.play(discord.FFmpegOpusAudio ("song.webm"))
  except:
    await ctx.send("Please wait for the song to finish, or use the clear command to clear the bot. This bot can only take 1 song at a time for now. Queue is on the to-do list.")
    return

@client.command(help = "Makes the bot leave the current voice channel it's in.")
async def leave(ctx):
  voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
  if not (voice == None):
    await voice.disconnect()
  else:
    await ctx.send("I'm not in a voice channel.")

@client.command(help = "Pauses the audio.")
async def pause(ctx):
  voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
  if voice != None and voice.is_playing():
    await voice.pause()
  else:
    await ctx.send("I'm not talking right now! Please chill tf out.")

@client.command(help = "Resumes the audio.")
async def resume(ctx):
  voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
  if voice != None and voice.is_paused():
    await voice.resume()
  else:
    await ctx.send("Don't interrupt me while I'm playing, baka~.")

@client.command(help = "Clears the bot of the song its playing.")
async def clear(ctx):
  voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
  if voice != None:
    voice.stop()

keep_alive()
client.run("ODQ0NzI3ODYzODM1MDk5MTM2.YKWoIQ.iCwZnXFuEkQw542C0FQL5lDoATs")