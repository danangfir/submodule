from camoufox.async_api import AsyncCamoufox
from browserforge.fingerprints import Screen
import asyncio
import re

async def main():
    async with AsyncCamoufox() as camoufox:
        await camoufox.login(username="missavd", password="missavd")