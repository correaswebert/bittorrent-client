import random
import socket
import asyncio
import struct
from typing import Optional


class UDPTrackerProtocol:
    def __init__(self, message, on_con_lost):
        self.message = message
        self.on_con_lost = on_con_lost
        self.transport = ...

    def connection_made(self, transport):
        self.transport = transport
        print("Send:", self.message)
        self.transport.sendto(self.message.encode())

    def datagram_received(self, data, addr):
        print("Received:", data.decode())

        print("Close the socket")
        self.transport.close()

    def error_received(self, exc):
        print("Error received:", exc)

    def connection_lost(self, exc):
        print("Connection closed")
        self.on_con_lost.set_result(True)


async def tracker_connect(tracker_addr: tuple[str, int]) -> Optional[bytes]:
    """connect phase of UDP tracker"""

    PROTOCOL_ID = 0x41727101980
    REQ_ACTION = 0
    req_transaction_id = random.randint(-2147483648, 2147483647)

    tracker_req_buffer = struct.pack(
        "!qii", PROTOCOL_ID, REQ_ACTION, req_transaction_id
    )

    tracker_res_buffer: bytes = ...
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.settimeout(5)
        sock.sendto(tracker_req_buffer, tracker_addr)
        tracker_res_buffer = sock.recvfrom(16)
    except socket.timeout:
        print("Could not connect!")
        return None
    finally:
        sock.close()

    res_action, res_transaction_id, connection_id = struct.unpack(
        "!iiq", tracker_res_buffer[0]
    )

    if req_transaction_id != res_transaction_id or res_action != REQ_ACTION:
        return None
    return connection_id


async def tracker_announce():
    ...


async def get_peer_list():
    loop = asyncio.get_running_loop()

    on_con_lost = loop.create_future()
    message = "Hello World!"

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: UDPTrackerProtocol(message, on_con_lost),
        remote_addr=("127.0.0.1", 9999),
    )

    try:
        await on_con_lost
    finally:
        transport.close()
