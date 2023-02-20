import struct
from urllib.parse import urlencode
import httpx
import asyncio

from torrent.parser import bdecode


async def get_peer_list_http(http_requests, payload: dict[str, bytes | int]):
    urlencoded_payload = urlencode(payload)
    async with httpx.AsyncClient() as client:
        coros = [client.get(f"{url}?{urlencoded_payload}") for url in http_requests]
        responses = await asyncio.gather(*coros)

    for benc_response in responses:
        response = bdecode(benc_response.text)

        if "failure reason" in response:
            raise Exception(response["failure reason"])

        enc_peers: list[bytes] | bytes = response["peers"]
        peers = []

        if isinstance(enc_peers, list):
            peers = [(peer["ip"], peer["port"]) for peer in enc_peers]

        elif isinstance(enc_peers, bytes):
            while enc_peers:
                peer_addr = enc_peers[:6]
                enc_peers = enc_peers[6:]

                peer_ip, peer_port = struct.unpack("!4sH", peer_addr)
                peer_ip = ".".join(str(i) for i in peer_ip)
                peers.append((peer_ip, peer_port))

        else:
            print(f"Invalid peer list {enc_peers=}")

    return peers
