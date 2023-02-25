from typing import Optional

from .type import PeerMessageType

def handshake(message: bytes, info_hash: bytes) -> Optional[bytes]:
    """Check protocol type and info_hash of the handshake"""

    if not message.startswith(b"\x13BitTorrent protocol"):
        return None

    if info_hash != message[28:48]:
        return None

    return message[48:68]


def parse_message(message: bytes):
    message_length = int.from_bytes(message[:4], "big")

    if message_length == 0:
        keepalive()

    message_type = message[4]
    message_payload = message[5:]

    match message_type:
        case PeerMessageType.choke:
            choke()
        case PeerMessageType.unchoke:
            unchoke()
        case PeerMessageType.interested:
            interested()
        case PeerMessageType.not_interested:
            not_interested()
        case PeerMessageType.have:
            have()
        case PeerMessageType.bitfield:
            bitfield()
        case PeerMessageType.request:
            request()
        case PeerMessageType.piece:
            piece()
        case PeerMessageType.cancel:
            cancel()


def keepalive():
    """
    Peers may close a connection if they receive no messages (keep-alive or
    any other message) for a certain period of time, generally two minutes.
    """

    ...


def choke():
    ...


def unchoke():
    ...


def interested():
    ...


def not_interested():
    ...


def have(payload: bytes):
    """Index which that downloader just completed and checked the hash of.

    :param index: piece index
    """

    return int.from_bytes(payload, "big")


def bitfield(payload: bytes):
    """Bitfield of the data owned by peer

    Optionally sent as the first message. If the downloader already has a
    piece, the corresponding index in the bitfield is set. MSB is index 0.

    :param bitfield: bitfield of owned pieces
    """

    return payload


def request(payload: bytes):
    """Piece request by peer

    :param index: piece index
    :param begin: byte offset within the piece
    :param length: requested length (power of 2, unless truncated by EOF)
    """

    index = payload[:4]
    begin = payload[4:8]
    length = payload[8:]

    return index, begin, length


def piece(payload: bytes):
    """Response for the piece request

    :param index: piece index
    :param begin: byte offset within the piece
    :param block: block of data
    """

    index = payload[:4]
    begin = payload[4:8]
    block = payload[8:]

    return index, begin, block


def cancel(payload: bytes):
    """Cancellation of piece request

    :param index: piece index
    :param begin: byte offset within the piece
    :param length: requested length
    """

    index = payload[:4]
    begin = payload[4:8]
    length = payload[8:]

    return index, begin, length
