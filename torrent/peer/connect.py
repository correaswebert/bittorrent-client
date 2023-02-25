import asyncio
from typing import NamedTuple

import torrent.peer_wire_protocol as pwp
from torrent.common.metainfo import Metainfo


class PeerReaderWriter(NamedTuple):
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter


class PeerAddress(NamedTuple):
    ip: str
    port: int


class Client:
    def __init__(self, metainfo: Metainfo):
        self.peers: dict[PeerAddress, PeerReaderWriter] = {}
        self.our_peer_id = self.generate_peer_id()
        self.pending_peices = len(metainfo.pieces)
        self.metainfo = metainfo

    @staticmethod
    def generate_peer_id():
        """Generate a peer ID using 'some' convention

        :ref: https://wiki.theory.org/BitTorrentSpecification#peer_id
        """

        return b"-CS0001-123456789012"  # TODO: generate this

    async def connect(self, peer_addr: tuple[str, int]):
        reader, writer = await asyncio.open_connection(*peer_addr)
        self.peers[peer_addr] = (reader, writer)

    async def handshake(self, peer_addr):
        """Generate the conventional BitTorrent protocol handshake message"""

        peer_stream = self.peers[peer_addr]

        our_handshake = pwp.generate.handshake(
            self.our_peer_id, self.metainfo.info_hash
        )
        peer_stream.writer.write(our_handshake)
        await peer_stream.writer.drain()

        their_handshake = await peer_stream.reader.read(68)
        their_peer_id = pwp.parse.handshake(their_handshake, self.metainfo.info_hash)


class TorrentDownload:
    def __init__(self, file: str):
        self.file: str = file
        self.bitfield: int


if __name__ == "__main__":
    ...
