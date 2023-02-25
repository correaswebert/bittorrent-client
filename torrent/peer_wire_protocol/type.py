import enum


class PeerMessageType(enum.Enum):
    """Non-keepalive messages

    :ref: https://www.bittorrent.org/beps/bep_0003.html#peer-messages
    """

    choke = 0x00
    unchoke = 0x01
    interested = 0x02
    not_interested = 0x03
    have = 0x04
    bitfield = 0x05
    request = 0x06
    piece = 0x07
    cancel = 0x08
