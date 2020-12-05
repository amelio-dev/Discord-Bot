import discord
import setting
import datetime

from lib.help import Help
from lib.reaction_notifier import ReactionNotifier
from lib.team_splitter import TeamSplitter

def GetAuthorVChannel(client, message):
    for server in client.guilds:
        for channel in server.voice_channels:
            if message.author in channel.members:
                return channel
    

if __name__ == "__main__":
    intents = discord.Intents(messages=True, guilds=True, members=True, voice_states=True, reactions=True)
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print('ログインしました')

    @client.event
    async def on_disconnect():
        print("クライアントが切断されました")
        client.run(setting.API_KEY)

    @client.event
    async def on_error(event, *args, **kwargs): 
        message = args[0] #Gets the message object 
        print("warning :", message) #logs the error 

    @client.event
    async def on_message(message):
        if message.author.bot:
            return
        if Help().is_help(message.content):
            await message.channel.send(Help().get_help_mes(message.content))
        elif TeamSplitter().is_team_command(message.content):
            mes = TeamSplitter().create_teams(GetAuthorVChannel(client, message), message)
            await message.channel.send(mes)

    @client.event
    async def on_reaction_add(reaction, user):
        if ReactionNotifier().is_rl_reaction(reaction):    
            reacted_users = await reaction.users().flatten()
            mes = ReactionNotifier().is_rl_gathered(reaction, reacted_users)
            if mes:
                await reaction.message.channel.send(mes)
        elif ReactionNotifier().is_test_reaction(reaction):
            print("test is reacted")
            reacted_users = await reaction.users().flatten()
            mes = ReactionNotifier().is_test_gathered(reaction, reacted_users)
            if mes:
                print("test gatherd")
                await reaction.message.channel.send(mes)

    client.run(setting.API_KEY)
