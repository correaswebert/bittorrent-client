import pytest
from ..parser import bencode, bdecode

def test_str_bad_str():
    with pytest.raises(ValueError):
        bdecode("nice")
        bdecode("-1why")
        bdecode("4:cow")
        bdecode("4:catch")


def test_str_good_str():
    assert bdecode("0:") == ""
    assert bdecode("4:down") == "down"


def test_str_bad_int():
    with pytest.raises(ValueError):
        bdecode("i123")
        bdecode("iASDe")


def test_str_good_int():
    assert bdecode("i0e") == 0
    assert bdecode("i123e") == 123
    assert bdecode("i-123e") == -123


def test_str_bad_list():
    with pytest.raises(ValueError):
        bdecode("lASDe")
        bdecode("l4:spam4:eggs")
        bdecode("l4:catche")


def test_str_good_list():
    assert bdecode("l4:spam4:eggse") == ["spam", "eggs"]
    assert bdecode("le") == []


def test_str_bad_dict():
    with pytest.raises(ValueError):
        bdecode("d4:spam4:eggs")
        bdecode("dASDe")
        bdecode("d4:spam1:a1:bee")


def test_str_good_dict():
    assert bdecode("de") == {}
    assert bdecode("d3:cow3:moo4:spam4:eggse") == {"cow": "moo", "spam": "eggs"}


def test_str_good_mixed():
    assert bdecode("ld3:cow3:moo4:spam4:eggsed4:spaml1:a1:beei0e4:briee") == [
        {"cow": "moo", "spam": "eggs"},
        {"spam": ["a", "b"]},
        0,
        "brie",
    ]

def test_bytes_bad_str():
    with pytest.raises(ValueError):
        bdecode(b"nice")
        bdecode(b"-1why")
        bdecode(b"4:cow")
        bdecode(b"4:catch")


def test_bytes_good_str():
    assert bdecode(b"0:") == ""
    assert bdecode(b"4:down") == "down"


def test_bytes_bad_int():
    with pytest.raises(ValueError):
        bdecode(b"i123")
        bdecode(b"iASDe")


def test_bytes_good_int():
    assert bdecode(b"i0e") == 0
    assert bdecode(b"i123e") == 123
    assert bdecode(b"i-123e") == -123


def test_bytes_bad_list():
    with pytest.raises(ValueError):
        bdecode(b"lASDe")
        bdecode(b"l4:spam4:eggs")
        bdecode(b"l4:catche")


def test_bytes_good_list():
    assert bdecode(b"l4:spam4:eggse") == ["spam", "eggs"]
    assert bdecode(b"le") == []


def test_bytes_bad_dict():
    with pytest.raises(ValueError):
        bdecode(b"d4:spam4:eggs")
        bdecode(b"dASDe")
        bdecode(b"d4:spam1:a1:bee")


def test_bytes_good_dict():
    assert bdecode(b"de") == {}
    assert bdecode(b"d3:cow3:moo4:spam4:eggse") == {"cow": "moo", "spam": "eggs"}


def test_bytes_good_mixed():
    assert bdecode(b"ld3:cow3:moo4:spam4:eggsed4:spaml1:a1:beei0e4:briee") == [
        {"cow": "moo", "spam": "eggs"},
        {"spam": ["a", "b"]},
        0,
        "brie",
    ]
