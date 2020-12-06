import discord
import setting

from lib.help import Help
from lib.reaction_notifier import ReactionNotifier
from lib.team_splitter import TeamSplitter

if __name__ == "__main__":  
    intents = discord.Intents(messages=True, guilds=True, members=True, voice_states=True, reactions=True)
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print('ログインしました')

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

    client.run(setting.API_KEY)
