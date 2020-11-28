import discord
import setting

from lib import help, reaction_notifier, team_splitter

if __name__ == "__main__":  
    client = discord.Client()

    @client.event
    async def on_ready():
        print('ログインしました')

    @client.event
    async def on_message(message):
        if message.author.bot:
            return

        if help.is_help(message.content):
            await message.channel.send(help.get_help_mes(message.content))

        elif team_splitter.is_team_command(message.content):
            mes = team_splitter.create_teams(client, message)
            await message.channel.send(mes)

    @client.event
    async def on_reaction_add(reaction, user):
        if reaction_notifier.is_rl_reaction(reaction):    
            reacted_users = await reaction.users().flatten()
            mes = reaction_notifier.is_rl_gathered(reaction, reacted_users)
            if mes:
                await reaction.message.channel.send(mes)

    client.run(setting.API_KEY)
