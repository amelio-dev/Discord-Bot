import discord
import random
import re
import setting

from lib import help, reaction_notifier

#メッセージ送信者のボイスチャンネルを取得
def GetAuthorVChannel(message):
    for server in client.guilds:
        for channel in server.voice_channels:
            if message.author in channel.members:
                return channel

def SetteamNum(message):
    pattern = r"\-num\s(\d+)"
    result = re.search(pattern, message.content)
    if result:
        return int(result.group(1))
    else:
        return 2

def SetTeamSize(message):
    pattern = r"\-size\s(\d+)"
    result = re.search(pattern, message.content)
    if result:
        return int(result.group(1))
    else:
        return 50

def ModUser(ml, message):
    ExtraUsers = []
    RemoveUsers = []
    pattern = r"\-user\s\[(.+)\]"
    result = re.search(pattern, message.content)
    if result:
        print(result.group(1))
        for n in result.group(1).split(","):
            if not n:
                continue
            if n.startswith("-"):
                RemoveUsers.append(n[1:])
            else:
                ExtraUsers.append(n)
    else:
        print("no item")
    ml.extend(ExtraUsers)
    ml = list(set(ml) - set(RemoveUsers))
    return ml

def AddUser(ml, message):
    ExtraUsers = []
    pattern = r"\-user\s([^\-]*)"
    result = re.search(pattern, message.content)
    if result:
        ExtraUsers = result.group(1).split()
    else:
        return ml
    ml.extend(ExtraUsers)
    return ml


def split_list(l, n):
    if len(l) < n:
        return split_list(l,len(l))
    else:
        res=[[]for i in range(n)]
        for i in range(len(l)):
            res[i%n].append(l[i])

        return res

def MakeLoLTeam(l):
    num = 2
    size = 5
    res = [ [] for i in range(num+1)]

    res[0] = l[0:5]
    res[1] = l[5:10]
    for item in l[10:]:
        res[2].append(item)

    print(res)
    return res



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

        elif message.content.startswith('/team'):
            vc = GetAuthorVChannel(message)
            if vc is None:
                await message.channel.send("error:投稿者はボイスチャンネルに接続していません")
            else:
                MemberName = [a.display_name for a in vc.members]
                MemberName = ModUser(MemberName,message)
                #ランダムに並び替え
                randUsers = random.sample(MemberName,len(MemberName))

                teamNum  = SetteamNum(message)
                teamsize = SetTeamSize(message)
                TeamStatMes = f"teamNum = {teamNum}"
                if teamsize != 50:
                    TeamStatMes = f"teamNum = {teamNum}, TeamSize = {teamsize}"

                mes = ""
                mes += "-"*10 +"|"+TeamStatMes+"|"+ "-"*10
                mes += "\n"
                
                TeamList = split_list(randUsers, teamNum)
                if "-lol" in message.content:
                    if len(randUsers) < 10:
                        await message.channel.send("error: 人数が10人未満です。")
                    else:
                        iconDict = {"Red Side" :":person_raising_hand:",
                                    "Blue Side":":man_raising_hand:",
                                    "抽選漏れ"  :":no_entry_sign:"}
                        WrapDict = {"Red Side" :[":red_car: ",":red_car: "],
                                    "Blue Side":[":blue_car:",":blue_car:"],
                                    "抽選漏れ"  :["",""]}

                        TeamList = MakeLoLTeam(randUsers)
                        for team,side in zip(TeamList,["Blue Side", "Red Side", "抽選漏れ"]):
                            
                            mes += f"{WrapDict[side][0]}{side}{WrapDict[side][1]}\n"
                            
                            for u in team:
                                iconDict = {"Red Side" :":person_raising_hand:",
                                            "Blue Side":":man_raising_hand:",
                                            "抽選漏れ"  :":no_entry_sign:"}

                                mes += f"  {iconDict[side]} {u}\n"
                #チームを表示
                else:
                    for i,team in enumerate(TeamList):
                        mes += f"Team {i+1}:\n"
                        for u in team:
                            mes += f":bust_in_silhouette: {u}\n"

                await message.channel.send(mes)

    @client.event
    async def on_reaction_add(reaction, user):
        if reaction_notifier.is_rl_reaction(reaction):    
            reacted_users = await reaction.users().flatten()
            mes = reaction_notifier.is_rl_gathered(reaction, reacted_users)
            if mes:
                await reaction.message.channel.send(mes)

    client.run(setting.API_KEY)
