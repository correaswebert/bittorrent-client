from .type import PeerMessageType


def handshake(peer_id: bytes, info_hash: bytes) -> bytes:
    """First message transmitted by the client to peer

    Message format is as follows:
    <pstrlen><pstr><reserved><info_hash><peer_id>

    :param peer_id:
    :param info_hash:
    """

    return b"\x13BitTorrent protocol" + b"\x00" * 8 + info_hash + peer_id


def generate_message(message_id: PeerMessageType, payload: bytes = b"") -> bytes:
    message: bytes = message_id + payload
    return len(message).to_bytes(4, "big") + message


def keepalive():
    """
    Peers may close a connection if they receive no messages (keep-alive or
    any other message) for a certain period of time, generally two minutes.
    """

    return generate_message(b"")


def choke():
    return generate_message(PeerMessageType.choke)


def unchoke():
    return generate_message(PeerMessageType.unchoke)


def interested():
    return generate_message(PeerMessageType.interested)


def not_interested():
    return generate_message(PeerMessageType.not_interested)


def have(index: int):
    """Index which that downloader just completed and checked the hash of.

    :param index: piece index
    """

    return generate_message(PeerMessageType.have, index.to_bytes(4, "big"))


def bitfield(bitfield: bytes):
    """Bitfield of the data owned by peer

    Optionally sent as the first message. If the downloader already has a
    piece, the corresponding index in the bitfield is set. MSB is index 0.

    :param bitfield: bitfield of owned pieces
    """

    return generate_message(PeerMessageType.have, bitfield)


def request(index: int, begin: int, length: int):
    """Piece request by peer

    :param index: piece index
    :param begin: byte offset within the piece
    :param length: requested length (power of 2, unless truncated by EOF)
    """

    payload = index.to_bytes(4, "big")
    payload += begin.to_bytes(4, "big")
    payload += length.to_bytes(4, "big")

    return generate_message(PeerMessageType.have, payload)


def piece(index: int, begin: int, block: int):
    """Response for the piece request

    :param index: piece index
    :param begin: byte offset within the piece
    :param block: block of data
    """

    payload = index.to_bytes(4, "big")
    payload += begin.to_bytes(4, "big")
    payload += block

    return generate_message(PeerMessageType.have, payload)


def cancel(index: int, begin: int, length: int):
    """Cancellation of piece request

    :param index: piece index
    :param begin: byte offset within the piece
    :param length: requested length
    """

    payload = index.to_bytes(4, "big")
    payload += begin.to_bytes(4, "big")
    payload += length.to_bytes(4, "big")

    return generate_message(PeerMessageType.have, payload)
