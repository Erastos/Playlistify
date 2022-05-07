#!/usr/bin/env python3

import discord.ext.commands
from discord.channel import TextChannel
import re

class Bot(discord.ext.commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='$')

        @self.command()
        async def urls(ctx, arg1):
            await self.getMessagesFromChannel(ctx, arg1)
            await ctx.send(f"Arg1: {arg1}")
    async def getMessagesFromChannel(self, ctx, arg):
        msg = "a"
        guild_channels = ctx.guild.channels
        guild_text_channels = filter(lambda x: isinstance(x, TextChannel), guild_channels)
        # channel_types = list(map(lambda x: type(x), channels))
        scan_channel = None
        for c in guild_text_channels:
            print(arg)
            print(c.name)
            if re.match(arg, c.name):
                await ctx.send("Found Channel\nGetting Messages")
                scan_channel = c
                # TODO: Split This Function up Into Getting Channel and Getting Messages
                return
        await ctx.send("Channel Not Found")




if __name__ == "__main__":
    Bot().run("")
