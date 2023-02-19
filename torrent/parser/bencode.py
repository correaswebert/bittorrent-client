def bencode(tdata: str | int | list | dict) -> bytes:
    meta_info = b""

    if isinstance(tdata, dict):
        meta_info += b"d"
        for k, v in tdata.items():
            if not isinstance(k, str):
                raise TypeError("Dictionary key can only be string")

            meta_info += bencode(k)
            meta_info += bencode(v)
        meta_info += b"e"

    elif isinstance(tdata, list):
        meta_info += b"l"
        for i in tdata:
            meta_info += bencode(i)
        meta_info += b"e"

    elif isinstance(tdata, int):
        meta_info += b"i"
        meta_info += f"{tdata}".encode()
        meta_info += b"e"

    elif isinstance(tdata, str):
        meta_info += f"{len(tdata)}:".encode()
        meta_info += tdata.encode()

    elif isinstance(tdata, bytes):
        meta_info += f"{len(tdata)}:".encode()
        meta_info += tdata

    else:
        raise TypeError("Unknown type passed. Only str, int, list and dict allowed.")

    return meta_info
