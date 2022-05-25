#!/usr/bin/env python3

from dataclasses import dataclass, field
from enum import Enum

import discord

class UrlType(Enum):
    """Type of Service URL to be interfaced with"""
    SPOTIFY = 0
    YOUTUBE = 1


@dataclass(frozen=True)
class URL:
    """Class that represents the url for a specific track/video on some service"""
    full_url: str
    url_type: UrlType = field(compare=False)
    message: discord.Message = field(compare=False)
