import pytest
import re
from unittest import mock
from tests.create_mock import CreateMock
from lib.team_splitter import TeamSplitter

@pytest.mark.parametrize("message, expect", [
    (CreateMock().message("/team -num 1" ), 1),
    (CreateMock().message("/team -num 10"), 10),
    (CreateMock().message("/team -num 1a"), 1),
    (CreateMock().message("/team-num 3"  ), 3),
    (CreateMock().message(""             ), TeamSplitter().DEFAULT_TEAM_NUM),
    (CreateMock().message("/team -num a1"), TeamSplitter().DEFAULT_TEAM_NUM),
])
def test_set_team_num(message, expect):
    assert TeamSplitter().set_team_num(message) == expect

@pytest.mark.parametrize("message, expect", [
    (CreateMock().message("/team -size 1" ), 1),
    (CreateMock().message("/team -size 10"), 10),
    (CreateMock().message("/team -size 1a"), 1),
    (CreateMock().message("/team-size 3"  ), 3),
    (CreateMock().message(""              ), TeamSplitter().DEFAULT_TEAM_SIZE),
    (CreateMock().message("/team -size a1"), TeamSplitter().DEFAULT_TEAM_SIZE),
])
def test_set_team_size(message, expect):
    assert TeamSplitter().set_team_size(message) == expect

@pytest.mark.parametrize("message, user_names, expect", [
    (
        CreateMock().message("/team"),
        ["a", "b", "c", "d", "e"],
        ["a", "b", "c", "d", "e"]
    ),
    (
        CreateMock().message("/team -user [y,z]"),
        ["a", "b", "c", "d", "e"],
        ["a", "b", "c", "d", "e", "y", "z"]
    ),
    (
        CreateMock().message("/team -user [-a,-b]"),
        ["a", "b", "c", "d", "e"],
        ["c", "d", "e"]
    ),
    (
        CreateMock().message("/team -user [z,-a]"),
        ["a", "b", "c", "d", "e"],
        ["b", "c", "d", "e", "z"]
    ),
    (
        CreateMock().message("/team -user [-a,z]"),
        ["a", "b", "c", "d", "e"],
        ["b", "c", "d", "e", "z"]
    ),
    (
        CreateMock().message("/team -user [z,-z]"),
        ["a", "b", "c", "d", "e"],
        ["a", "b", "c", "d", "e"]
    ),
    (
        CreateMock().message("/team -user [-z,z]"),
        ["a", "b", "c", "d", "e"],
        ["a", "b", "c", "d", "e"]
    ),
    (
        CreateMock().message("/team -user"),
        ["a", "b", "c", "d", "e"],
        ["a", "b", "c", "d", "e"]
    ),
    (
        CreateMock().message("/team -user []"),
        ["a", "b", "c", "d", "e"],
        ["a", "b", "c", "d", "e"]
    ),
])
def test_modify_user_list(message, user_names, expect):
    # modify_user_listは内部でリストをsetに変換しているので順番が入れ替わる
    assert set(TeamSplitter().modify_user_list(user_names, message)) == set(expect)

splitted_users = CreateMock().users(7)
@pytest.mark.parametrize("users, team_num, expect", [
    (
        splitted_users[:6],
        2,
        [
            [splitted_users[0], splitted_users[2], splitted_users[4]],
            [splitted_users[1], splitted_users[3], splitted_users[5]]
        ]
    ),
    (
        splitted_users[:7],
        2,
        [
            [splitted_users[0], splitted_users[2], splitted_users[4], splitted_users[6]],
            [splitted_users[1], splitted_users[3], splitted_users[5]]
        ]
    ),
    (
        splitted_users[:6],
        10,
        [[splitted_users[0]], [splitted_users[1]], [splitted_users[2]], [splitted_users[3]], [splitted_users[4]], [splitted_users[5]]]
    ),
    (
        [],
        2,
        []
    )
])
def test_split_list(users, team_num, expect):
    assert TeamSplitter().split_list(users, team_num) == expect

lol_users = CreateMock().users(12)
@pytest.mark.parametrize("users, expect", [
    (
        lol_users[:10],
        [ 
            lol_users[0:5 ],
            lol_users[5:10],
            []
        ]
    ),
    (
        lol_users[:12],
        [ 
            lol_users[0:5  ],
            lol_users[5:10 ],
            lol_users[10:12],
        ]
    ),
    (
        lol_users[:8],
        [ 
            lol_users[0:5],
            lol_users[5:8],
            []
        ]
    ),
    (
        [],
        [ [], [], [] ]
    )
])
def test_lol_team(users, expect):
    assert TeamSplitter().make_lol_team(users) == expect

@pytest.mark.parametrize("message, expect", [
    ("/team"         ,True ),
    ("/team -option" ,True ),
    ("/teams"        ,True ),
    ("team"          ,False),
    ("x/team"        ,False),
    ("/tea m"        ,False),
    (" /team"        ,False),
])
def test_is_team_command(message, expect):
    assert TeamSplitter().is_team_command(message) == expect

def rand_return_value(l,len):
    return l

def modify_user_list_mock(names, message):
    return names

@pytest.mark.parametrize("vc, message, expect", [
    (
        None,
        CreateMock().message("/team"),
        "error:投稿者はボイスチャンネルに接続していません"
    ),
    (
        CreateMock().voice_channel("VC_channel", CreateMock().users(6)),
        CreateMock().message("/team"),
        "----------|teamNum = 2|----------\n"
        "Team 1:\n"
        ":bust_in_silhouette: listuser_0\n"
        ":bust_in_silhouette: listuser_2\n"
        ":bust_in_silhouette: listuser_4\n"
        "Team 2:\n"
        ":bust_in_silhouette: listuser_1\n"
        ":bust_in_silhouette: listuser_3\n"
        ":bust_in_silhouette: listuser_5\n"
    ),
    (
        CreateMock().voice_channel("VC_channel", CreateMock().users(5)),
        CreateMock().message("/team"),
        "----------|teamNum = 2|----------\n"
        "Team 1:\n"
        ":bust_in_silhouette: listuser_0\n"
        ":bust_in_silhouette: listuser_2\n"
        ":bust_in_silhouette: listuser_4\n"
        "Team 2:\n"
        ":bust_in_silhouette: listuser_1\n"
        ":bust_in_silhouette: listuser_3\n"
    ),
    (
        CreateMock().voice_channel("VC_channel", CreateMock().users(1)),
        CreateMock().message("/team"),
        "----------|teamNum = 2|----------\n"
        "Team 1:\n"
        ":bust_in_silhouette: listuser_0\n"
    ),
    (
        CreateMock().voice_channel("VC_channel", CreateMock().users(9)),
        CreateMock().message("/team -lol"),
        "error: 人数が10人未満です。"
    ),

])
def test_create_teams(mocker, vc, message, expect):
    mocker.patch("lib.util.Util.GetAuthorVChannel", return_value=vc)
    mocker.patch("random.sample", side_effect=rand_return_value)
    # modify_user_listは内部でsetを使っているので、利用すると順番が入れ替わる
    mocker.patch("lib.team_splitter.TeamSplitter.modify_user_list", side_effect=modify_user_list_mock)
    assert TeamSplitter().create_teams(vc, message) == expect

@pytest.mark.parametrize("team_num, team_size, expect", [
    (2, 50, "----------|teamNum = 2|----------\n"),  
    (2, 2,  "----------|teamNum = 2, TeamSize = 2|----------\n"),
    (4, 50, "----------|teamNum = 4|----------\n"),
    (4, 2,  "----------|teamNum = 4, TeamSize = 2|----------\n"),
])
def test_create_team_headder(team_num, team_size, expect):
    assert TeamSplitter().create_team_headder(team_num, team_size) == expect

normal_result_users = ["listuser_" + str(i) for i in range(0,6)]
@pytest.mark.parametrize("teams, expect", [
    (
        [
            normal_result_users[0:3],
            normal_result_users[3:6]
        ],
        "Team 1:\n"
        ":bust_in_silhouette: listuser_0\n"
        ":bust_in_silhouette: listuser_1\n"
        ":bust_in_silhouette: listuser_2\n"
        "Team 2:\n"
        ":bust_in_silhouette: listuser_3\n"
        ":bust_in_silhouette: listuser_4\n"
        ":bust_in_silhouette: listuser_5\n"
    ),
    (
        [
            normal_result_users[0:2],
            normal_result_users[2:4],
            normal_result_users[4:6],
        ],
        "Team 1:\n"
        ":bust_in_silhouette: listuser_0\n"
        ":bust_in_silhouette: listuser_1\n"
        "Team 2:\n"
        ":bust_in_silhouette: listuser_2\n"
        ":bust_in_silhouette: listuser_3\n"
        "Team 3:\n"
        ":bust_in_silhouette: listuser_4\n"
        ":bust_in_silhouette: listuser_5\n"
    ),
    (
        [ [] ],
        "Team 1:\n"
    ),
    (
        [
            normal_result_users[0:2],
            []
        ],
        "Team 1:\n"
        ":bust_in_silhouette: listuser_0\n"
        ":bust_in_silhouette: listuser_1\n"
        "Team 2:\n"
    )
])
def test_normal_result(teams, expect):
    assert TeamSplitter().normal_result(teams) == expect

lol_result_users = ["listuser_" + str(i) for i in range(0,12)]
@pytest.mark.parametrize("teams, expect", [
    (
        [
            lol_result_users[0:5],
            lol_result_users[5:10]
        ],
        ":blue_car:Blue Side:blue_car:\n"
        "  :man_raising_hand: listuser_0\n"
        "  :man_raising_hand: listuser_1\n"
        "  :man_raising_hand: listuser_2\n"
        "  :man_raising_hand: listuser_3\n"
        "  :man_raising_hand: listuser_4\n"
        ":red_car: Red Side:red_car: \n"
        "  :person_raising_hand: listuser_5\n"
        "  :person_raising_hand: listuser_6\n"
        "  :person_raising_hand: listuser_7\n"
        "  :person_raising_hand: listuser_8\n"
        "  :person_raising_hand: listuser_9\n"
    ),
    (
        [
            lol_result_users[0:5],
            lol_result_users[5:10],
            lol_result_users[10:12],
        ],
        ":blue_car:Blue Side:blue_car:\n"
        "  :man_raising_hand: listuser_0\n"
        "  :man_raising_hand: listuser_1\n"
        "  :man_raising_hand: listuser_2\n"
        "  :man_raising_hand: listuser_3\n"
        "  :man_raising_hand: listuser_4\n"
        ":red_car: Red Side:red_car: \n"
        "  :person_raising_hand: listuser_5\n"
        "  :person_raising_hand: listuser_6\n"
        "  :person_raising_hand: listuser_7\n"
        "  :person_raising_hand: listuser_8\n"
        "  :person_raising_hand: listuser_9\n"
        "抽選漏れ\n"
        "  :no_entry_sign: listuser_10\n"
        "  :no_entry_sign: listuser_11\n"
    ),
    (
        [
            []
        ],
        ":blue_car:Blue Side:blue_car:\n"
    )
])
def test_lol_result(teams, expect):
    assert TeamSplitter().lol_result(teams) == expect
