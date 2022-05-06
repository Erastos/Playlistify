#!/usr/bin/env python3

import discord.ext.commands

class Bot(discord.ext.commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='$')
    @super().command
    async def test(ctx, arg1):
        await ctx.send(f'You passed {arg1}')


if __name__ == "__main__":
    bot = Bot().run()
