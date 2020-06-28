from os import remove, makedirs
from os import path

from discord import HTTPException

# Folders utilities
base_folder = path.join(path.expanduser("~"), '.config', 'ezreal_bot')
token_location = path.join(base_folder, 'discord_token.txt')

if not path.exists(base_folder):
    makedirs(base_folder)


# Discord token acquisition
def get_discord_token():
    try:
        with open(token_location) as file:
            discord_token = file.read()
    except FileNotFoundError:
        print(f'Discord token not found\n'
              f'If you don’t have one, you can create it at https://discord.com/developers/applications\n'
              f'It will be saved in clear text at {path.join(base_folder, "discord_token.txt")}\n'
              f'Please input the bot’s Discord token:')
        discord_token = input()
        with open(token_location, 'w+') as file:
            file.write(discord_token)
    return discord_token


# A shortcut to get a channel by a certain attribute
# Uses the channel name by default
# If many matching channels are found, returns the first one
def get_channel(client, value, attribute="name"):
    channel = next((c for c in client.get_all_channels()
                    if getattr(c, attribute).lower() == value.lower()), None)
    if not channel:
        raise ValueError("No such channel")
    return channel


# Shortcut method to send a message in a channel with a certain name
# You can pass more positional arguments to send_message
# Uses get_channel, so you should be sure that the bot has access to only
# one channel with such name
async def send_in_channel(client, channel_name, *args):
    await client.send_message(get_channel(client, channel_name), *args)


# Attempts to upload a file in a certain channel
# content refers to the additional text that can be sent alongside the file
# delete_after_send can be set to True to delete the file afterwards
async def try_upload_file(client, channel, file_path, content=None,
                          delete_after_send=False, retries=3):
    used_retries = 0
    sent_msg = None

    while not sent_msg and used_retries < retries:
        try:
            sent_msg = await client.send_file(channel, file_path,
                                              content=content)
        except HTTPException:
            used_retries += 1

    if delete_after_send:
        remove(file_path)

    if not sent_msg:
        await client.send_message(channel,
                                 "Oops, something happened. Please try again.")

    return sent_msg