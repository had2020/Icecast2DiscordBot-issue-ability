import discord
from discord import FFmpegPCMAudio
import yaml

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print('Bot is ready.')

@bot.event
async def on_voice_state_update(member, before, after):
    guild = discord.utils.get(bot.guilds, id=int(config["guild_id"]))

    if guild is None:
        print('Server not found!')
        return

    channel = discord.utils.get(guild.voice_channels, id=int(config["voice_channel_id"]))

    if channel is None:
        print('Voice channel not found!')
        return

    # If someone joined the configured voice channel
    if after.channel == channel:
        if len(after.channel.members) == 1:  # Just the bot
            return

        # If the bot is not already in the channel, join it and start playing
        if not any(voice_client.channel == channel for voice_client in bot.voice_clients):
            voice_client = await channel.connect()
            voice_client.play(FFmpegPCMAudio(config["icecast_url"]))

    # If someone left the configured voice channel
    elif before.channel == channel:
        if len(before.channel.members) > 1:  # Someone other than the bot is still in the channel
            return

        # If the bot is the only one left in the channel, disconnect
        for voice_client in bot.voice_clients:
            if voice_client.channel == channel:
                await voice_client.disconnect()

bot.run(config["discord_bot_key"])