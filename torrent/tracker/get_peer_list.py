from contextlib import closing
import random
import socket
import struct
from urllib.parse import urlencode, urlparse
import httpx
import asyncio


def tracker_connect(t_ip, t_port):
    """connect phase of UDP tracker"""

    protocol_id = 0x41727101980  # constant
    req_action = 0  # connect
    req_transaction_id = random.randint(-2147483648, 2147483647)

    tracker_req_buffer = struct.pack(
        "!qii", protocol_id, req_action, req_transaction_id
    )

    tracker_res_buffer = ...
    with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as sock:
        try:
            sock.settimeout(5)
            sock.sendto(tracker_req_buffer, (t_ip, t_port))
            tracker_res_buffer = sock.recvfrom(16)
        except socket.timeout:
            print("Could not connect!")
            return None

    res_action, res_transaction_id, connection_id = struct.unpack(
        "!iiq", tracker_res_buffer[0]
    )

    if req_transaction_id == res_transaction_id and res_action == req_action:
        return connection_id
    return None


def tracker_announce(
    connection_id, info_hash, tracker_ip, tracker_port, client_port, peer_id
):
    """announce phase of UDP tracker"""

    req_action = 1  # announce
    req_transaction_id = random.randint(-2147483648, 2147483647)
    downloaded = 0
    left = 0
    uploaded = 0
    event = 0
    req_ip = 0
    key = random.randint(-2147483648, 2147483647)
    num_want = -1

    tracker_req_buffer = struct.pack(
        "!qii20s20sqqqiiiiH",
        connection_id,
        req_action,
        req_transaction_id,
        info_hash,
        peer_id,
        downloaded,
        left,
        uploaded,
        event,
        req_ip,
        key,
        num_want,
        client_port,
    )

    tracker_res_buffer = ...
    with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as sock:
        try:
            sock.settimeout(5)
            sock.sendto(tracker_req_buffer, (tracker_ip, tracker_port))
            tracker_res_buffer = sock.recvfrom(4096)[0]
        except:
            print("Could not announce!")
            return []

    p2p_network_info = tracker_res_buffer[:20]
    p2p_peer_info = tracker_res_buffer[20:]

    res_action, res_transaction_id, interval, leechers, seeders = struct.unpack(
        "!iiiii", p2p_network_info
    )

    if req_transaction_id != res_transaction_id or req_action != res_action:
        print("Some tracker-side error occurred.")
        return []

    peer_list = []
    while p2p_peer_info:
        peer_addr = p2p_peer_info[:6]
        p2p_peer_info = p2p_peer_info[6:]

        p_ip, p_port = struct.unpack("!4sH", peer_addr)
        p_ip = ".".join(str(i) for i in p_ip)
        peer_list.append((p_ip, p_port))

    return peer_list


def get_peer_list_udp(tracker_addr, info_hash, client_port, peer_id):
    t_ip, t_port = tracker_addr

    try:
        # print("Connecting to tracker...")
        connection_id = tracker_connect(t_ip, t_port)

        if connection_id is None:
            return []

        # print("Announcing to tracker...")
        peer_list = tracker_announce(
            connection_id, info_hash, t_ip, t_port, client_port, peer_id
        )
        return peer_list

    except Exception as e:
        print(e)



async def get_peer_list_http(http_requests):
    async with httpx.AsyncClient() as client:
        coros = [client.get(url) for url in http_requests]
        responses = await asyncio.gather(*coros)

    return responses

def get_peer_list(metainfo: dict, metainfo_info_hash: bytes):
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
        url_info = urlparse(url[0])

        if url_info.scheme == "udp":
            udp_requests.append(f"{url[0]}?{payload_args}")
        else:
            http_requests.append(f"{url[0]}?{payload_args}")

    http_responses = asyncio.run(get_peer_list_http(http_requests))
    return http_responses

