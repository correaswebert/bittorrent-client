import pytest
from ..parser import bencode, bdecode


def test_bad_str():
    with pytest.raises(ValueError):
        bdecode(b"nice")
        bdecode(b"-1why")
        bdecode(b"4:cow")
        bdecode(b"4:catch")


def test_good_str():
    assert bdecode(b"0:") == ""
    assert bdecode(b"4:down") == "down"


def test_bad_int():
    with pytest.raises(ValueError):
        bdecode(b"i123")
        bdecode(b"iASDe")


def test_good_int():
    assert bdecode(b"i0e") == 0
    assert bdecode(b"i123e") == 123
    assert bdecode(b"i-123e") == -123


def test_bad_list():
    with pytest.raises(ValueError):
        bdecode(b"lASDe")
        bdecode(b"l4:spam4:eggs")
        bdecode(b"l4:catche")


def test_good_list():
    assert bdecode(b"l4:spam4:eggse") == ["spam", "eggs"]
    assert bdecode(b"le") == []


def test_bad_dict():
    with pytest.raises(ValueError):
        bdecode(b"d4:spam4:eggs")
        bdecode(b"dASDe")
        bdecode(b"d4:spam1:a1:bee")


def test_good_dict():
    assert bdecode(b"de") == {}
    assert bdecode(b"d3:cow3:moo4:spam4:eggse") == {"cow": "moo", "spam": "eggs"}


def test_good_mixed():
    assert bdecode(b"ld3:cow3:moo4:spam4:eggsed4:spaml1:a1:beei0e4:briee") == [
        {"cow": "moo", "spam": "eggs"},
        {"spam": ["a", "b"]},
        0,
        "brie",
    ]
