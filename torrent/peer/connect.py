import asyncio
import messages

from torrent.common.metainfo import Metainfo


def generate_peer_id() -> bytes:
    """Generate a peer ID using 'some' convention

    :ref: https://wiki.theory.org/BitTorrentSpecification#peer_id
    """
    return b"-CS0001-123456789012"  # TODO: generate this


from typing import NamedTuple

class PeerReaderWriter(NamedTuple):
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter

class PeerAddress(NamedTuple):
    ip: str
    port: int



def verify_handshake(message: bytes, info_hash: bytes):
    """Check protocol type and info_hash of the handshake"""

    if not message.startswith(b"\x13BitTorrent protocol"):
        return False

    if info_hash != message[28: 48]:
        return False

    return True


class Peer:
    def __init__(self, metainfo: Metainfo):
        self.peers: dict[PeerAddress, PeerReaderWriter] = {}
        self.peer_id = generate_peer_id()
        self.pending_peices = len(metainfo.pieces)
        self.metainfo = metainfo

    async def connect(self, peer_addr: tuple[str, int]):
        reader, writer = await asyncio.open_connection(*peer_addr)
        self.peers[peer_addr] = (reader, writer)


    async def handshake(self, peer_addr):
        """Generate the conventional BitTorrent protocol handshake message"""
        message = (
            b"\x13BitTorrent protocol"
            + b"\x00" * 8
            + self.metainfo.info_hash
            + self.peer_id
        )

        peer = self.peers[peer_addr]
        peer.writer.write(message)
        await peer.writer.drain()
        response = await peer.reader.read(68)
        verify_handshake(response, self.metainfo.info_hash)


class TorrentDownload:
    def __init__(self, file: str):
        self.file: str = file
        self.bitfield: int


if __name__ == "__main__":
    ...
