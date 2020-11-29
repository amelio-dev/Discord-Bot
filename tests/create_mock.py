from unittest import mock
class CreateMock:
    def user(self, name):
        attr = {"name":name, "display_name":name, "mention":f"@{name}"}
        user = mock.Mock()
        user.configure_mock(**attr)
        return user

    def users(self, user_count = 10, name_begin = 0):
        user_list = []
        for i in range(0,user_count):
            user_list.append(self.user(f"listuser_{i + name_begin}"))
        return user_list

    def reaction(self, author, emoji=":rl:"):
        a = {"author":author}
        message = mock.Mock()
        message.configure_mock(**a)

        attr = {"message":message, "emoji":emoji}
        reaction = mock.Mock()
        reaction.configure_mock(**attr)
        return reaction

    def message(self, mes, author=""):
        attr = {"content":mes, "author":author}
        res = mock.Mock()
        res.configure_mock(**attr)
        return res

    def voice_channel(self, name, members):
        attr = {"name":name, "members":members}
        res = mock.Mock()
        res.configure_mock(**attr)
        return res
