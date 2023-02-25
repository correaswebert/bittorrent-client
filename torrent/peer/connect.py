import asyncio
import logging
from typing import NamedTuple
import base64

import torrent.peer_wire_protocol as pwp
from torrent.common.metainfo import Metainfo

log = logging.getLogger("root")


class PeerStream(NamedTuple):
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter


class PeerAddress(NamedTuple):
    ip: str
    port: int


class Client:
    def __init__(self, metainfo: Metainfo):
        self.peers: dict[PeerAddress, PeerStream] = {}
        self.our_peer_id = self.generate_peer_id()
        self.pending_peices = len(metainfo.pieces)
        self.metainfo = metainfo

    @staticmethod
    def generate_peer_id():
        """Generate a peer ID using 'some' convention

        :ref: https://wiki.theory.org/BitTorrentSpecification#peer_id
        """

        return b"-CS0001-123456789012"  # TODO: generate this

    async def handshake(self, peer_addr):
        """Generate the conventional BitTorrent protocol handshake message"""

        reader, writer = await asyncio.open_connection(*peer_addr)
        peer_stream = PeerStream(reader, writer)

        our_handshake = pwp.generate.handshake(
            self.our_peer_id, self.metainfo.info_hash
        )
        peer_stream.writer.write(our_handshake)
        await peer_stream.writer.drain()

        their_handshake = await peer_stream.reader.read(68)
        their_peer_id = pwp.parse.handshake(their_handshake, self.metainfo.info_hash)

        if their_peer_id is None:
            log.error(f"Failed to connect to peer {peer_addr}")
            peer_stream.writer.close()
            return await peer_stream.writer.wait_closed()

        log.info(
            f"Connected to peer {peer_addr} "
            f"with peer_id {base64.b64encode(their_peer_id)}"
        )
        self.peers[peer_addr] = peer_stream

    async def receive_message(self, peer_addr: PeerAddress):
        

    async def run(self, peers):
        coros = [self.handshake(peer) for peer in peers]
        await asyncio.gather(*coros)

    def download(self, peers):
        asyncio.run(self.run(peers))


class TorrentDownload:
    def __init__(self, file: str):
        self.file: str = file
        self.bitfield: int


if __name__ == "__main__":
    ...
