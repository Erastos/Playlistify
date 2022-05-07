#!/usr/bin/env python3

import discord.ext.commands
from discord.channel import TextChannel
import re
import os

from url import URL, UrlType

SPOTIFY_URL_REGEX = r"(?:spotify)(?:.com/track/|:track:)(.+?)(?=\?|$)"

class Bot(discord.ext.commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='$')

        # Command Definition
        @self.command()
        async def urls(ctx, channel_query):
            """Return valid service url messages to the user"""
            # Get channel from argument passed to string
            channel = self.getChannelFromSubstring(ctx.guild.channels, channel_query)
            if channel:
                # Return messages from channel
                messages = await self.getChannelMessagesUrls(channel)
                messages_text = list(map(lambda x: x.message.content, messages))
                await ctx.send("Messages:\n" + "\n".join(messages_text))
            else:
                await ctx.send(f"Can't Find Channel {channel_query}")

    async def getChannelMessagesUrls(self, channel, limit=100):
        """Get messages from a specifc channel that are valid service URLs"""
        # Get Messages from Channel and filter them
        messages = await channel.history(limit=limit).flatten()
        urls = list(filter(lambda x: re.search(SPOTIFY_URL_REGEX, x.content),messages))
        # Remove Messages the Bot Sent
        urls = list(filter(lambda x: x.author.id != self.user.id, urls))
        # TODO: Move Spotify Logic Into its Own Function Once we are processing more than one platform
        spotify_ids = list(map(lambda x: re.findall(SPOTIFY_URL_REGEX, x.content)[0], urls))
        # Convert Messages to URL Dataclass Representation
        urls = [URL(spotify_ids[i], UrlType.SPOTIFY, url) for i, url in enumerate(urls)]
        return urls


    def getChannelFromSubstring(self, channel_list, channel_query):
        """Get all text channels from the server that the user is sending the message"""
        guild_text_channels = filter(lambda x: isinstance(x, TextChannel), channel_list)
        for c in guild_text_channels:
            if re.match(channel_query, c.name):
                return c




if __name__ == "__main__":
    Bot().run(os.getenv("DISCORD_BOT_TOKEN"))
