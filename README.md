Discord Bot
Overview

This is a custom Discord bot built using the discord.py library. The bot interacts with the Mobafire and U.GG websites to fetch League of Legends champion builds, runes, matchups, and stats. Additionally, it can handle image download, manipulation, and sending images as attachments within the Discord server.
Features

    Fetch champion builds: Retrieves item build paths for champions.
    Fetch rune setups: Retrieves rune setups for champions.
    Fetch toughest matchups: Provides a list of toughest matchups for a specified champion.
    Image manipulation: Downloads, processes (e.g., crop or merge), and sends images within Discord.

Requirements

    Python 3.7+
    discord.py: For creating and running the bot.
    requests: For making HTTP requests to retrieve data from websites.
    Pillow (PIL): For image processing (e.g., cropping, merging).
    beautifulsoup4: For parsing HTML content and scraping websites.

Commands

    .ct <champion>: Retrieves the toughest matchups for the specified champion from U.GG.

    .rune <champion>: Retrieves and sends the rune setup images for the specified champion.

    .build <champion>: Fetches and sends the item build images for the specified champion from Mobafire.

    .stat <champion>: Retrieves statistical data for a champion (placeholder for further implementation).

Image Manipulation Functions

    Image Download and Send: Downloads and sends single or multiple images to the Discord channel.
    Merge Images: Merges multiple images horizontally and sends them as one image.
    Crop Image: Crops a specified portion of an image and sends it.
![Screenshot 2024-09-24 232442](https://github.com/user-attachments/assets/1e312f63-fa0d-44ea-bf14-0eaf0590a53e)
![Screenshot 2024-09-24 232428](https://github.com/user-attachments/assets/5b0cadf3-8016-4ffc-9556-602c5895a799)
