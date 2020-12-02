import discord
import setting
import datetime

from lib.help import Help
from lib.reaction_notifier import ReactionNotifier
from lib.team_splitter import TeamSplitter

if __name__ == "__main__":  
    client = discord.Client()

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
            mes = TeamSplitter().create_teams(client, message)
            await message.channel.send(mes)

    @client.event
    async def on_reaction_add(reaction, user):
        if ReactionNotifier().is_rl_reaction(reaction):    
            reacted_users = await reaction.users().flatten()
            mes = ReactionNotifier().is_rl_gathered(reaction, reacted_users)
            if mes:
                await reaction.message.channel.send(mes)
        elif ReactionNotifier().is_test_reaction(reaction):
            print("hit")
            reacted_users = await reaction.users().flatten()
            mes = ReactionNotifier().is_test_gathered(reaction, reacted_users)
            if mes:
                print("tru")
                await reaction.message.channel.send(mes)

    client.run(setting.API_KEY)
