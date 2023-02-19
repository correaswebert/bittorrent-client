from collections import namedtuple

ParseData = namedtuple("ParseData", ["data", "end_idx"])


def isend(tdata: bytes | str):
    return tdata not in ["e", ord("e")]


def _parse_str(tdata: bytes | str, idx: int = 0):
    len_idx = idx
    strlen = 0

    if isinstance(tdata[idx], int):
        while ord("0") <= tdata[len_idx] <= ord("9"):
            strlen = strlen * 10 + tdata[len_idx] - ord("0")
            len_idx += 1
    else:
        while tdata[len_idx].isdigit():
            strlen = strlen * 10 + int(tdata[len_idx])
            len_idx += 1

    start = len_idx + 1  # skip the colon
    end = start + strlen

    string = tdata[start:end]
    if isinstance(string, bytes) and string.isascii():
        string = string.decode()

    if len(string) != strlen:
        raise ValueError("Insufficient word length provided")

    if idx == 0 and end != len(tdata):
        raise ValueError("There are additional characters")

    return ParseData(string, end)


def _parse_int(tdata: bytes, idx: int = 0):
    start = idx + 1
    end = start
    sign = 1

    while end < len(tdata) and isend(tdata[end]):
        end += 1

    if end == len(tdata) or isend(tdata[end]):
        raise ValueError("Input integer did not end with 'e'")

    if tdata[start] == "-":
        sign = -1
        start += 1

    try:
        integer = int(tdata[start:end])
    except ValueError:
        raise ValueError("Input cannot be converted to an integer")

    if idx == 0 and isend(tdata[end]):
        raise ValueError("There are additional characters")

    return ParseData(sign * int(integer), end + 1)


def _parse_list(tdata: bytes, idx: int = 0):
    start = idx + 1
    end = start
    item_start = start
    data = []

    try:
        while end < len(tdata) and isend(tdata[end]):
            item = _parse(tdata, item_start)
            item_start = item.end_idx
            end = item.end_idx

            data.append(item.data)
    except ValueError as ve:
        raise ve

    if end == len(tdata) and isend(tdata[end - 1]):
        raise ValueError("Input list did not end with 'e'")

    return ParseData(data, end + 1)


def _parse_dict(tdata: bytes, idx: int = 0) -> ParseData:
    start = idx + 1
    end = start
    item_start = start
    data = {}

    try:
        while end < len(tdata) and isend(tdata[end]):
            key = _parse(tdata, item_start)
            item_start = key.end_idx

            val = _parse(tdata, item_start)
            item_start = val.end_idx
            end = val.end_idx

            data[key.data] = val.data
    except ValueError as ve:
        raise ve

    if end == len(tdata) or isend(tdata[end]):
        raise ValueError("Input dictionary did not end with 'e'")

    return ParseData(data, end + 1)


def _parse(tdata: bytes | str, idx: int = 0):
    char = tdata[idx]
    result = None

    if char in ["d", ord("d")]:
        result = _parse_dict(tdata, idx)

    elif char in ["l", ord("l")]:
        result = _parse_list(tdata, idx)

    elif char in ["i", ord("i")]:
        result = _parse_int(tdata, idx)

    elif isinstance(char, int) and ord("0") <= char <= ord("9"):
        result = _parse_str(tdata, idx)

    elif isinstance(char, str) and char.isdigit():
        result = _parse_str(tdata, idx)

    else:
        raise ValueError("Unknown bencoding input")

    return result


def bdecode(tdata: bytes) -> str | int | list | dict:
    return _parse(tdata).data
