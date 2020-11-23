class Util:
    def __init__(self, client):
        self.client = client

    #メッセージ送信者のボイスチャンネルを取得
    def GetAuthorVChannel(self, message):
        for server in self.client.guilds:
            for channel in server.voice_channels:
                if message.author in channel.members:
                    return channel
