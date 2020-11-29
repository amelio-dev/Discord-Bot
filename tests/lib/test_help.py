import pytest
from lib.help import Help

@pytest.mark.parametrize("mes, expect", [
    ("/rl -h"         , True),
    ("/team -h"       , True),
    ("/rl"            , None),
    ("-h"             , None),
    (""               , None),
    ("/rl -h /team -h", True)
])
def test_is_help(mes, expect):
    assert Help().is_help(mes) == expect

@pytest.mark.parametrize("mes, expect", [
    ("/rl -h"         , Help()._rl_help()  ),
    ("/team -h"       , Help()._team_help()),
    ("/rl"            , ""                 ),
    ("-h"             , ""                 ),
    (""               , ""                 ),
    ("/rl -h /team -h", Help()._rl_help()  )
])
def test_get_help_mes(mes, expect):
    assert Help().get_help_mes(mes) == expect
