import discord
from discord.ext import commands
import youtube_dl
import os
from keep_alive import keep_alive
from discord import Color
import urllib.request
import re



client = commands.Bot(command_prefix=">")
client.remove_command("help")


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=">help"))
    print("I'm ready!")

@client.group(invoke_without_command = True)
async def help(ctx):
  em = discord.Embed(title = "Help", description = "Use >help <command> for extended info\nRemember, this is freshly in development so don't be too rough. If you come across an error, message my creator <@184833237535686658>.",color = Color.random())
  em.add_field(name = "Music", value = "play, stop, resume, pause, leave")
  em.add_field(name = "Fun", value = "kiss")
  await ctx.send(embed = em)

@help.command()
async def kiss(ctx):
  em = discord.Embed(title = "Kiss",description = "Kisses the person that you mention",color = Color.random())
  em.add_field(name = "**Syntax**", value = ">kiss <@User>")
  await ctx.send(embed = em)

@help.command()
async def play(ctx):
  em = discord.Embed(title = "Play",description = "Plays a song given a name. If not already in a voice channel, it will join the channel that the command caller is in.",color = Color.random())
  em.add_field(name = "**Syntax**", value = ">play <Name>")
  await ctx.send(embed = em)

@help.command()
async def playURL(ctx):
  em = discord.Embed(title = "PlayURL",description = "Plays a song given a URL. If not already in a voice channel, it will join the channel that the command caller is in.",color = Color.random())
  em.add_field(name = "**Syntax**", value = ">play <YouTube URL>")
  await ctx.send(embed = em)

@help.command()
async def leave(ctx):
  em = discord.Embed(title = "Leave",description = "Makes the bot leave the voice channel that it's in.",color = Color.random())
  em.add_field(name = "**Syntax**", value = ">leave")
  await ctx.send(embed = em)

@help.command()
async def stop(ctx):
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
async def playURL(ctx, url : str):
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

@client.command(help = "Plays a song given a name.")
async def play(ctx, *names : str):
  if not ctx.message.author.voice:
    await ctx.send("You need to be in a voice channel to do this.")
    return
  else: 
    channel = ctx.message.author.voice.channel 

  L = []
  for name in names:
    L.append(name)

  video_name = "+"
  video_name = video_name.join(L)

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
  html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + video_name)
  video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
  ydl_opts = {
      'format': '249/250/251'
  }
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      ydl.download(["https://www.youtube.com/watch?v=" + video_ids[0]])
  for file in os.listdir("./"):
      if file.endswith(".webm"):
          os.rename(file, "song.webm")

  try:
    RV.play(discord.FFmpegOpusAudio ("song.webm"))
    await ctx.send("Now playing:")
    await ctx.send("https://www.youtube.com/watch?v=" + video_ids[0])

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
async def stop(ctx):
  voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
  if voice != None:
    voice.stop()

@client.command(help = "Sends a kiss to someone you mention")
async def kiss(ctx, user:discord.Member = None ):
  try:
    await user.send(ctx.message.author.name + " has sent you a kiss!")
    await ctx.send("The kiss has been sent successfully!")
  except discord.ext.commands.errors.MemberNotFound as e:
    await ctx.send(e)
    return

keep_alive()
client.run("FAKE TOKEN")
