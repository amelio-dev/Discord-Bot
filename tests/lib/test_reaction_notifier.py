import pytest
import re
from unittest import mock
from tests.create_mock import CreateMock

from lib.reaction_notifier import ReactionNotifier

poster = CreateMock().user("poster")
user_list = CreateMock().users()
@pytest.mark.parametrize("poster, user_list, expect", [
    (poster      , user_list, user_list + [poster]),
    (user_list[0], user_list, user_list           ),
    (poster      , []       , [poster]            ),
])
def test_get_unique_users(poster, user_list, expect):
    assert ReactionNotifier().get_unique_users(poster, user_list) == expect

gathered_users = CreateMock().users(6)
list_head_reaction = CreateMock().reaction(gathered_users[0])
author = CreateMock().user("author")
author_reaction = CreateMock().reaction(author)
@pytest.mark.parametrize("users, reaction, expect",[
    (
        gathered_users,
        list_head_reaction,
        ReactionNotifier()._create_gathered_message(list_head_reaction, gathered_users)
    ),
    (
        gathered_users[:6],
        author_reaction,
        ReactionNotifier()._create_gathered_message(author_reaction, gathered_users[:6] + [author])
    ),
    (
        gathered_users[:5],
        list_head_reaction,
        None
    ),
    (
        [],
        author_reaction,
        None
    )
])

def test_is_rl_gathered(users, reaction, expect):
    assert ReactionNotifier().is_rl_gathered(reaction, users) == expect

@pytest.mark.parametrize("reaction, expect", [
    (CreateMock().reaction("author", emoji = ":rl:"  ), True ),
    (CreateMock().reaction("author", emoji = ":rlx:" ), False),
    (CreateMock().reaction("author", emoji = ":rl:x" ), True ),
    (CreateMock().reaction("author", emoji = ":fill:"), False),
    (CreateMock().reaction("author", emoji = ""      ), False)
])
def test_is_rl_reaction(reaction, expect):
    result = ReactionNotifier().is_rl_reaction(reaction)
    assert bool(result) == expect

@pytest.mark.parametrize("reaction, user_names, expect", [
    (
        CreateMock().reaction("author", emoji = ":rl:"),
        CreateMock().users(6),
        "6人集まりました:rl:\n@listuser_0\n@listuser_1\n@listuser_2\n@listuser_3\n@listuser_4\n@listuser_5\n"
    ),
    (
        CreateMock().reaction("author", emoji = ":rl:"),
        CreateMock().users(8),
        "6人集まりました:rl:\n@listuser_0\n@listuser_1\n@listuser_2\n@listuser_3\n@listuser_4\n@listuser_5\n@listuser_6\n@listuser_7\n"
    ),
])
def test_create_gathered_message(reaction, user_names, expect):
    assert ReactionNotifier()._create_gathered_message(reaction, user_names) == expect
