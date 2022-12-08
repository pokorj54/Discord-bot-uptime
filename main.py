import discord
import my_secret_token
import time
from socket_checker import SocketChecker
import json

TOKEN = my_secret_token.get_token()

intents = discord.Intents.default()

client = discord.Client(intents=intents)


def load_json_file(filename):
    data = dict()
    with open(filename) as file:
        data = json.load(file)
    return data

config = load_json_file("config.json")

from discord.ext import tasks

@tasks.loop(seconds=config["cooldown"]) # alternatively, minutes=60, seconds=3600, etc.
async def f(channel, checkers):
    for checker in checkers:
        try: 
            await channel.send("Checking: " + checker.identify())
            msg = checker.check()
            await channel.send("Check successful:\n" + msg)
        except Exception as e:
            await channel.send(content=f"{channel.guild.default_role} error: {e}")


@client.event
async def on_ready():
    print('Logged in as {}'.format(client.user))
    channel = client.get_channel(config["channel"])
    checkers = []
    for thing in config["things"]:
        checkers.append(SocketChecker(thing["IP"], thing["port"]))
    f.start(channel, checkers)

client.run(TOKEN)