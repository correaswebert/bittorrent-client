import pytest
from ..parser import parse


def test_bad_str():
    with pytest.raises(ValueError):
        parse(b"nice")
        parse(b"-1why")
        parse(b"4:cow")
        parse(b"4:catch")


def test_good_str():
    assert parse(b"0:") == ""
    assert parse(b"4:down") == "down"


def test_bad_int():
    with pytest.raises(ValueError):
        parse(b"i123")
        parse(b"iASDe")


def test_good_int():
    assert parse(b"i0e") == 0
    assert parse(b"i123e") == 123
    assert parse(b"i-123e") == -123


def test_bad_list():
    with pytest.raises(ValueError):
        parse(b"lASDe")
        parse(b"l4:spam4:eggs")
        parse(b"l4:catche")


def test_good_list():
    assert parse(b"l4:spam4:eggse") == ["spam", "eggs"]
    assert parse(b"le") == []


def test_bad_dict():
    with pytest.raises(ValueError):
        parse(b"d4:spam4:eggs")
        parse(b"dASDe")
        parse(b"d4:spam1:a1:bee")


def test_good_dict():
    assert parse(b"de") == {}
    assert parse(b"d3:cow3:moo4:spam4:eggse") == {"cow": "moo", "spam": "eggs"}


def test_good_mixed():
    assert parse(b"ld3:cow3:moo4:spam4:eggsed4:spaml1:a1:beei0e4:briee") == [
        {"cow": "moo", "spam": "eggs"},
        {"spam": ["a", "b"]},
        0,
        "brie",
    ]
