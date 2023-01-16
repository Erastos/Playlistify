#!/usr/bin/env python3

import discord.ext.commands
from discord.channel import TextChannel
from discord.member import Member
from discord.message import Message
import re
import os
import dotenv

from url import URL, UrlType
from spotify import SpotifyClient

dotenv.load_dotenv()

SPOTIFY_URL_REGEX = r"(?:spotify)(?:.com/track/|:track:)(.+?)(?=\?|$)"
MESSAGE_LIMIT = 1000
DEFAULT_MESSAGE_LENGTH = 1000

class Bot(discord.ext.commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='$')
        self.sclient = SpotifyClient()

        # Command Definition
        @self.command()
        async def urls(ctx, channel_query, limit=MESSAGE_LIMIT):
            """Return valid service url messages to the user"""
            # Get channel from argument passed to string
            channel = self.getChannelFromSubstring(ctx.guild.channels, channel_query)
            if channel:
                # Return messages from channel
                messages = await self.getChannelMessagesUrls(channel, limit)
                messages_text = list(map(lambda x: x.message.content, messages))
                print("Messages:\n" + "\n".join(messages_text))
                await ctx.send("Command Executed!")
            else:
                await ctx.send(f"Can't Find Channel {channel_query}")

        @self.command()
        async def addSongs(ctx: discord.ext.commands.Context, channel_query):
            channel = self.getChannelFromSubstring(ctx.guild.channels, channel_query)
            if channel:
                messages = await self.getChannelMessagesUrls(channel, MESSAGE_LIMIT)
                message_urls = list(map(lambda x: x.full_url, set(messages)))

                # Setup Client
                authorize_url = self.sclient.authorize_url
                user = ctx.author

                # Send DM to User with the Authorize URL
                dm_channel = await user.create_dm()
                await dm_channel.send(f"Authorize URL: {authorize_url}\nPaste this URL into your browser:\nReply to this message with the URL that your browser returns you too")

                redirect_url = await self.wait_for('message', check=lambda x: x.author == ctx.author and x.guild is None)

                # Add Tracks to Playlist
                tracks = self.addSongsPlaylist(message_urls, redirect_url.content)
                print(f"Tracks added: {tracks}")

                await ctx.send("Command Executed!")
            else:
                await ctx.send(f"Can't Find Channel {channel_query}")

    async def getChannelMessagesUrls(self, channel, limit):
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


    def addSongsPlaylist(self, message_urls, redirect_url):
        self.sclient.authorizeClient(redirect_url)
        playlist = self.sclient.getOrCreatePlaylist()
        tracks = self.sclient.addDifferentSongs(playlist["id"], message_urls)
        return tracks


    def getChannelFromSubstring(self, channel_list, channel_query):
        """Get all text channels from the server that the user is sending the message"""
        guild_text_channels = filter(lambda x: isinstance(x, TextChannel), channel_list)
        for c in guild_text_channels:
            if re.match(channel_query, c.name):
                return c

    def stripMessage(self, message):
        """In the case that the message is too long for discord to send, cut off the excess"""
        if (len(message) >= DEFAULT_MESSAGE_LENGTH):
            message = message[:message.rfind('\n', 0, DEFAULT_MESSAGE_LENGTH-1)]
        return message



if __name__ == "__main__":
    Bot().run(os.getenv("DISCORD_BOT_TOKEN"))
