from collections import namedtuple

ParseData = namedtuple("ParseData", ["data", "end_idx"])


def _parse_str(tdata: bytes, idx: int = 0):
    len_idx = idx
    strlen = 0
    while ord("0") <= tdata[len_idx] <= ord("9"):
        strlen = strlen * 10 + tdata[len_idx] - ord("0")
        len_idx += 1

    start = len_idx + 1 # skip the colon
    end = start + strlen

    string = tdata[start:end]
    if string.isascii():
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

    while end < len(tdata) and tdata[end] != ord("e"):
        end += 1

    if end == len(tdata) or tdata[end] != ord("e"):
        raise ValueError("Input integer did not end with 'e'")

    if tdata[start] == "-":
        sign = -1
        start += 1

    try:
        integer = int(tdata[start:end])
    except ValueError:
        raise ValueError("Input cannot be converted to an integer")

    if idx == 0 and tdata[end] != ord("e"):
        raise ValueError("There are additional characters")

    return ParseData(sign * int(integer), end + 1)


def _parse_list(tdata: bytes, idx: int = 0):
    start = idx + 1
    end = start
    item_start = start
    data = []

    try:
        while end < len(tdata) and tdata[end] != ord("e"):
            item = _parse(tdata, item_start)
            item_start = item.end_idx
            end = item.end_idx

            data.append(item.data)
    except ValueError as ve:
        raise ve

    if end == len(tdata) and tdata[end - 1] != ord("e"):
        raise ValueError("Input list did not end with 'e'")

    return ParseData(data, end + 1)


def _parse_dict(tdata: bytes, idx: int = 0) -> ParseData:
    start = idx + 1
    end = start
    item_start = start
    data = {}

    try:
        while end < len(tdata) and tdata[end] != ord("e"):
            key = _parse(tdata, item_start)
            item_start = key.end_idx

            val = _parse(tdata, item_start)
            item_start = val.end_idx
            end = val.end_idx

            data[key.data] = val.data
    except ValueError as ve:
        raise ve

    if end == len(tdata) or tdata[end] != ord("e"):
        raise ValueError("Input dictionary did not end with 'e'")

    return ParseData(data, end + 1)


def _parse(tdata: bytes, idx: int = 0):
    char = tdata[idx]
    result = None

    if char == ord("d"):
        result = _parse_dict(tdata, idx)

    elif char == ord("l"):
        result = _parse_list(tdata, idx)

    elif char == ord("i"):
        result = _parse_int(tdata, idx)

    elif ord("0") <= char <= ord("9"):
        result = _parse_str(tdata, idx)

    else:
        print(char, idx)
        raise ValueError("Unknown bencoding input")

    return result

def parse(tdata: bytes):
    return _parse(tdata).data

if __name__ == "__main__":
    tdata = b'd8:announce41:https://academictorrents.com/announce.php13:announce-listll41:https://academictorrents.com/announce.phpel34:udp://tracker.coppersurfer.tk:6969el42:udp://tracker.opentrackr.org:1337/announceel44:udp://tracker.openbittorrent.com:80/announceee10:created by25:Transmission/2.84 (14307)13:creation datei1483953530e8:encoding5:UTF-84:infod6:lengthi161539e4:name64:A-Brief-Review-of-NatureInspired-Algorithms-for-Optimization.pdf12:piece lengthi32768e6:pieces100:\x9a\xe4\xfa\x14\xb6\x1d\x91\xca\xa1y8\x96\xfd\xa6pzc\x06\x00Gq\xe4\xae\x1f\x1a\xd9\xd8[[m\x96\x9aT\xa8 \xad\xbc\x1a\xa9\x8a\x82>\x96\xe9\x16\x1b\xcfW\\\xce\x97 "\xeb@F3\x0bB\xf8\xc7F\xc7\xb5D\xe7?<\x16\x87?\xa5\x14Wv\xb1\xedb\xc8>\xf4;1\x11\xf9Qj\xf0)\xbd\xa4\xa6\x1aPA09|\xbbd7:privatei0ee8:url-listl56:http://www.iztok-jr-fister.eu/static/publications/21.pdfee'
    tdata = b'l41:https://academictorrents.com/announce.phpe'
    tdata = b'i0e'
    print(parse(tdata))
