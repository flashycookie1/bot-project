import discord
import responses
import os

async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message, str(message.author))
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

def run_discord_bot():
    TOKEN = os.getenv("TOKEN")
    client = discord.Client(intents = discord.Intents.all())

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} said: '{user_message}' ({channel})")

        await send_message(message, user_message, is_private=False)

    client.run(TOKEN)