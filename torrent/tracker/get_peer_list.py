import asyncio

from torrent.common.metainfo import Metainfo

from . import http_tracker


def get_peers(metainfo: Metainfo):
    payload_args = {
        "info_hash": metainfo.info_hash,
        "peer_id": b"12345678901234567890",
        "port": 1234,
        "left": metainfo.files[0][0],
        "downloaded": 0,
        "uploaded": 0,
        "compact": 1,
    }

    http_requests: list[str] = []
    udp_requests: list[str] = []

    for tracker_url in metainfo.trackers:
        if tracker_url.startswith("udp"):
            udp_requests.append(tracker_url)
        else:
            http_requests.append(tracker_url)

    http_responses = http_tracker.get_peers(http_requests, payload_args)
    # TODO: implement UDP tracker communications

    return http_responses
