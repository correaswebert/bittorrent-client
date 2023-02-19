from contextlib import closing
import random
import socket
import struct

import asyncio
from urllib.parse import urlparse
from async_dns.resolver import ProxyResolver


import asyncio_dgram

resolver = ProxyResolver()


async def tracker_connect(tracker_addr, stream):
    """connect phase of UDP tracker"""

    protocol_id = 0x41727101980  # constant
    req_action = 0  # connect
    req_transaction_id = random.randint(-2147483648, 2147483647)

    tracker_req_buffer = struct.pack(
        "!qii", protocol_id, req_action, req_transaction_id
    )

    tracker_res_buffer = ...
    await stream.send(tracker_req_buffer, tracker_addr)
    tracker_res_buffer, _ = await stream.recv(16)

    res_action, res_transaction_id, connection_id = struct.unpack(
        "!iiq", tracker_res_buffer[0]
    )

    if req_transaction_id == res_transaction_id and res_action == req_action:
        return connection_id
    return None


def tracker_announce(tracker_addr, client_port, payload: dict[str, bytes | int]):
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
        payload["connection_id"],
        req_action,
        req_transaction_id,
        payload["info_hash"],
        payload["peer_id"],
        downloaded,
        left,
        uploaded,
        event,
        req_ip,
        key,
        num_want,
        client_port,
    )

    tracker_res_buffer = b""
    with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as sock:
        try:
            sock.settimeout(5)
            sock.sendto(tracker_req_buffer, tracker_addr)
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


# async def get_peer_list_udp(tracker_addr, info_hash, client_port, peer_id):
async def get_peer_list_udp(request_urls: list[str], payload: dict[str : bytes | int]):

    # tracker_ip = socket.getaddrinfo(
    #     tracker_url.hostname, tracker_url.port, proto=socket.IPPROTO_UDP
    # )[0][4][0]


    client_port = 8888
    stream = await asyncio_dgram.bind(("", client_port))

    tracker_addrs: list[tuple(str, int)] = []
    for url in request_urls:
        tracker_url = urlparse(url)
        # result, _ = resolver.query(tracker_url.hostname, types.A)   # https://pypi.org/project/async-dns/
        
        tracker_ip = socket.getaddrinfo(
            tracker_url.hostname, tracker_url.port, proto=socket.IPPROTO_UDP
        )[0][4][0]
        tracker_addrs.append((tracker_ip, tracker_url.port))

    tracker_connect(tracker_addrs[0], stream)

