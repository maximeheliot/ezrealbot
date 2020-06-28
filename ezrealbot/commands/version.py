import discord
import requests

from ezrealbot.commands import BaseCommand


class Version(BaseCommand):
    """
        **Return the lastest application version number and a list of the latest features it includes.**

        You will want to use this function to know about what's new in the latest version of the application.

```py
@return message: The version information
```
        **Example**

        > **ez!help**
    """

    def __init__(self):
        description = "Display the lastest application version number and a *what's new* list of information"
        params = None
        super().__init__(description, params)

    async def handle(self, params, message, client):
        r = None

        try:
            r = requests.get('https://api.github.com/repos/maximeheliot/ezrealbot/releases/latest').json()
        except ConnectionError as err:
            await message.channel.send("ConnectionError: ", err)
            return
        except requests.HTTPError as err:
            await message.channel.send("HTTPError: ", err)
            return
        except requests.Timeout as err:
            await message.channel.send("Timeout: ", err)
            return

        embed = discord.Embed(title="**Ezreal Version " + r['tag_name'] + " **", color=0xff0000, description=r['body'])

        await message.channel.send(embed=embed)