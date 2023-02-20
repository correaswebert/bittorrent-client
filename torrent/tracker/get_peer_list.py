import asyncio
import socket
from urllib.parse import urlparse

from .http_tracker import get_peer_list_http
from .udp_tracker import get_peer_list_udp


def get_peer_list(metainfo: dict, metainfo_info_hash: bytes):
    payload_args = {
        "info_hash": metainfo_info_hash,
        "peer_id": b"12345678901234567890",
        "port": 1234,
        "left": metainfo["info"]["length"],
        "downloaded": 0,
        "uploaded": 0,
        "compact": 1,
    }

    urls: list[str] = [*metainfo["announce-list"], [metainfo["announce"]]]

    http_requests: list[str] = []
    udp_requests: list[str] = []

    for lurl in urls:
        url = lurl[0]
        if url.startswith("udp"):
            udp_requests.append(url)
        else:
            http_requests.append(url)

    # http_responses = asyncio.run(get_peer_list_http(http_requests, payload_args))
    udp_responses = get_peer_list_udp(udp_requests, payload_args)
    print(udp_responses)
    # return http_responses
