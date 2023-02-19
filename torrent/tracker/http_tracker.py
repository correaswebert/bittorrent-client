from urllib.parse import urlencode
import httpx
import asyncio


async def get_peer_list_http(http_requests, payload: dict[str, bytes | int]):
    urlencoded_payload = urlencode(payload)
    async with httpx.AsyncClient() as client:
        coros = [client.get(f"{url}?{urlencoded_payload}") for url in http_requests]
        responses = await asyncio.gather(*coros)

    return responses
