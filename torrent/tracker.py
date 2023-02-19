import hashlib
from urllib.parse import urlencode
import httpx
import asyncio

from .parser import bencode


async def _http_tracker(metainfo: dict):
    metainfo_info = bencode(metainfo["info"])
    metainfo_info_hash = hashlib.sha1(metainfo_info).digest()

    payload_args = urlencode(
        {
            "info_hash": metainfo_info_hash,
            "peer_id": b"12345678901234567890",
            "port": 1234,
            "left": metainfo["info"]["length"],
            "downloaded": 0,
            "uploaded": 0,
            "compact": 1,
        }
    )

    urls: list[str] = [*metainfo["announce-list"], [metainfo["announce"]]]

    http_requests = []
    udp_requests = []

    for url in urls:
        if url[0].startswith("udp"):
            udp_requests.append(f"{url[0]}?{payload_args}")
        else:
            http_requests.append(f"{url[0]}?{payload_args}")

    async with httpx.AsyncClient() as client:
        coros = [client.get(url) for url in http_requests]
        responses = await asyncio.gather(*coros)

    return responses


def http_tracker(metainfo: dict):
    return asyncio.run(_http_tracker(metainfo))
