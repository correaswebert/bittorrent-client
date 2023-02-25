import asyncio
import logging
import struct
from urllib.parse import urlencode

import httpx

from torrent.parser import bdecode

log = logging.getLogger("root")


async def get_peer_list_http(
    http_requests, payload: dict[str, bytes | int]
) -> list[httpx.Response]:
    log.info("getting peer list using HTTP")

    urlencoded_payload = urlencode(payload)
    async with httpx.AsyncClient() as client:
        try:
            coros = [client.get(f"{url}?{urlencoded_payload}") for url in http_requests]
            return await asyncio.gather(*coros)
        except httpx.ReadTimeout as rte:
            log.error("Read timeout while getting peer list over HTTP")
            return []


def get_peer_list_from_responses(responses: list[httpx.Response]) -> tuple[str, int]:
    peers = []

    for benc_response in responses:
        response = bdecode(benc_response.text)
        log.debug(response)

        if "failure reason" in response:
            raise Exception(response["failure reason"])

        enc_peers: list[bytes] | bytes = response["peers"]

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

    log.debug(peers)
    return peers


def get_peers(http_requests, payload: dict[str, bytes | int]) -> tuple[str, int]:
    responses = asyncio.run(get_peer_list_http(http_requests, payload))
    return get_peer_list_from_responses(responses)
