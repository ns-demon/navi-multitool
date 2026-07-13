#  _   _                 _ 
# | \ | |               (_)
# |  \| | __ ___   __ _  _ 
# | . ` |/ _` \ \ / /(_)| |
# | |\  | (_| |\ V /  _ | |
# |_| \_|\__,_| \_/  (_)|_|
# 
# Navi Multitool - Developed by glockinhand
# GitHub: https://github.com/glockinhand/navi-multitool

import asyncio
import aiohttp
import random
import string
import json
import logging
from datetime import datetime
from urllib.parse import urlparse
from core.display import Colorate, Theme

def run_bomber(target, count, proxy=None):
    cl = Theme.get_colors()

    print(Colorate.Horizontal(
        cl["num"],
        "[!] Notice: This feature is currently unavailable. Check for updates later."
    ))

 
    return