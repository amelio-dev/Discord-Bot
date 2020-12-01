import random
import re
from lib.util import Util

class TeamSplitter:
    DEFAULT_TEAM_NUM = 2
    DEFAULT_TEAM_SIZE = 50

    def set_team_num(self, message):
        pattern = r"\-num\s(\d+)"
        result = re.search(pattern, message.content)
        if result:
            return int(result.group(1))
        else:
            return self.DEFAULT_TEAM_NUM

    def set_team_size(self, message):
        pattern = r"\-size\s(\d+)"
        result = re.search(pattern, message.content)
        if result:
            return int(result.group(1))
        else:
            return self.DEFAULT_TEAM_SIZE

    # 手動でユーザの追加、除外設定を行う場合
    # TODO: [a, b]のようにコンマ後にスペースがある場合も名前の一部として認識されるので要修正(#20)
    def modify_user_list(self, target_list, message):
        appending_users = []
        removing_users = []
        pattern = r"\-user\s\[(.+)\]"
        result = re.search(pattern, message.content)
        if result:
            print("modify_user_list :", result.group(1))
            for user in result.group(1).split(","):
                if not user:
                    continue
                if user.startswith("-"):
                    removing_users.append(user[1:])
                else:
                    appending_users.append(user)
        else:
            print("modify_user_list : no item")
        target_list.extend(appending_users)
        target_list = list(set(target_list) - set(removing_users))
        return target_list

    # 手動でユーザの追加を行う場合 未使用関数
    def add_user(self, target_list, message):
        appending_users = []
        pattern = r"\-user\s([^\-]*)"
        result = re.search(pattern, message.content)
        if result:
            appending_users = result.group(1).split()
        else:
            return target_list
        target_list.extend(appending_users)
        return target_list

    def split_list(self, users, team_num):
        if len(users) < team_num:
            return self.split_list(users,len(users))
        else:
            res=[[]for i in range(team_num)]
            for i in range(len(users)):
                res[i % team_num].append(users[i])

            return res

    # チーム数2, チーム人数5で残りは余りとしてチームを作成
    def make_lol_team(self, rand_users):
        team_num = 2
        team_size = 5
        res = [ [] for i in range(team_num + 1)]

        res[0] = rand_users[0:team_size]
        res[1] = rand_users[team_size:10]
        res[2] = rand_users[10:]
        return res

    def is_team_command(self, message):
        return message.startswith('/team')

    def create_teams(self, client, message):
        util = Util(client)
        vc = util.GetAuthorVChannel(message)
        
        if vc is None:
            return "error:投稿者はボイスチャンネルに接続していません"
        
        member_names = [a.display_name for a in vc.members]
        member_names = self.modify_user_list(member_names,message)
        randomized_names = random.sample(member_names,len(member_names))

        team_num  = self.set_team_num(message)
        team_size = self.set_team_size(message)
        
        if "-lol" in message.content:
            if len(randomized_names) < 10:
                return "error: 人数が10人未満です。"
            teams = self.make_lol_team(randomized_names)
            mes = self.lol_result(teams)
        else:
            teams = self.split_list(randomized_names, team_num)
            mes = self.normal_result(teams)
        
        return self.create_team_headder(team_num, team_size) + mes

    def create_team_headder(self, team_num, team_size):
        team_stat = f"teamNum = {team_num}"
        if team_size != self.DEFAULT_TEAM_SIZE:
            team_stat = f"teamNum = {team_num}, TeamSize = {team_size}"

        mes = ""
        mes += "-" * 10 + "|" + team_stat + "|" + "-" * 10
        mes += "\n"

        return mes

    def normal_result(self, teams):
        mes = ""
        for i,team in enumerate(teams):
            mes += f"Team {i+1}:\n"
            for user in team:
                mes += f":bust_in_silhouette: {user}\n"
        return mes

    def lol_result(self, teams):
        IconDict = {"Red Side" :":person_raising_hand:",
                    "Blue Side":":man_raising_hand:",
                    "抽選漏れ"  :":no_entry_sign:"}
        WrapDict = {"Red Side" :[":red_car: ",":red_car: "],
                    "Blue Side":[":blue_car:",":blue_car:"],
                    "抽選漏れ"  :["",""]}
        
        mes = ""
        for team,side in zip(teams,["Blue Side", "Red Side", "抽選漏れ"]):
            mes += f"{WrapDict[side][0]}{side}{WrapDict[side][1]}\n"
            
            for u in team:
                mes += f"  {IconDict[side]} {u}\n"

        return mes
