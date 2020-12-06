class Help:
    def is_help(self, message):
        if message.startswith("/rl -h") or message.startswith("/team -h"):
            return True

    def get_help_mes(self, message):
        if message.startswith("/rl -h"):
            return self._rl_help()
        elif message.startswith("/team -h"):
            return self._team_help()
        else:
            print("error: unexpected help type")
            return ""

    def _rl_help(self):
        mes = ""
        mes += "rocket league メンバー集めツール　v1.3 作者：amelio\n"
        mes += ":rl:が6人集まるとメンションを投稿します\n"
        mes += "  注意)投稿者はリアクションしてもカウントされません\n"
        return mes

    def _team_help(self):
        mes = ""
        mes += "チーム分け支援システム　v1.3 作者：amelio\n"
        mes += "使い方：以下のコマンドをチャット欄に入力\n     /team\n"
        mes += "説明：自分が居るボイスチャンネルのユーザを2チームに分けます．\n\n"
        mes += "オプション：\n"
        mes += "  -num 数字：チーム数を指定．指定が無い場合は2\n"
        mes += "  -user [文字列]：チーム分けにユーザを追加(-を付けると除外)．スペース区切りで複数追加可能\n"
        mes += "例) /team -num 4 -user [taro,tanaka,-mike,bob] \n     VC中のユーザにtaro, tanaka, bobを加え，mikeを除いて4チームに分ける"
        mes += "\n"
        mes += "  :new:-lol :LoLのカスタムゲーム向けに振り分け\n"
        return mes
