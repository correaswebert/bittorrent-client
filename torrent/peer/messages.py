import enum


class PeerMessageType(enum.Enum):
    """Non-keepalive messages

    :ref: https://www.bittorrent.org/beps/bep_0003.html#peer-messages
    """

    choke = 0x00
    unchoke = 0x01
    interested = 0x02
    not_interested = 0x03

    # Index which that downloader just completed and checked the hash of.
    have = 0x04

    # Optionally sent as the first message. If the downloader already has a
    # piece, the corresponding index in the bitfield is set. MSB is index 0.
    bitfield = 0x05

    # Piece index, begin offset, and length. Length is a power of two unless it
    # gets truncated by the end of the file.
    request = 0x06

    # Piece index, begin offset, and piece data.
    piece = 0x07

    # Piece index, begin offset, and length. Sent to everyone when a piece arrives.
    cancel = 0x08


class PeerMessage:
    """<length prefix><message ID><payload>
    The length prefix is a four byte big-endian value.
    The message ID is a single decimal byte.
    The payload is message dependent.
    """

    type: PeerMessageType
    payload: None  # payload or piggy-backed data
    extra: None  # piggy-backed data
    verified: None  # are hashes verified
    continuation: False  # are hashes verified
    len: 0


def generate_message(message_id: PeerMessageType, payload: bytes = b"") -> bytes:
    message: bytes = message_id + payload
    return len(message).to_bytes(4, "big") + message


def keepalive():
    """
    Peers may close a connection if they receive no messages (keep-alive or
    any other message) for a certain period of time, generally two minutes.
    """
    return b"\x00\x00\x00\x00"


def choke():
    return generate_message(PeerMessageType.choke)


def unchoke():
    return generate_message(PeerMessageType.unchoke)


def interested():
    return generate_message(PeerMessageType.interested)


def not_interested():
    return generate_message(PeerMessageType.not_interested)


def have(index: int):
    """
    :param index: piece index
    """

    return generate_message(PeerMessageType.have, index.to_bytes(4, "big"))


def bitfield(bitfield: bytes):
    """
    :param bitfield: bitfield of pieces already owned (MSB is index 0)
    """

    return generate_message(PeerMessageType.have, bitfield)


def request(index: int, begin: int, length: int):
    """
    :param index: piece index
    :param begin: byte offset within the piece
    :param length: requested length
    """

    payload = index.to_bytes(4, "big")
    payload += begin.to_bytes(4, "big")
    payload += length.to_bytes(4, "big")
    
    return generate_message(PeerMessageType.have, payload)


def piece(index: int, begin: int, block: int):
    """
    :param index: piece index
    :param begin: byte offset within the piece
    :param block: block of data
    """

    payload = index.to_bytes(4, "big")
    payload += begin.to_bytes(4, "big")
    payload += block

    return generate_message(PeerMessageType.have, payload)


def cancel(index: int, begin: int, length: int):
    """
    :param index: piece index
    :param begin: byte offset within the piece
    :param length: requested length
    """

    payload = index.to_bytes(4, "big")
    payload += begin.to_bytes(4, "big")
    payload += length.to_bytes(4, "big")

    return generate_message(PeerMessageType.have, payload)
