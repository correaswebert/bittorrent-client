import asyncio
import uuid

from torrent.common.metainfo import Metainfo

class TorrentNode:
    def __init__(self, metainfo: Metainfo):
        self.peers: list[tuple[asyncio.StreamReader, asyncio.StreamWriter]] = []
        self.id = b"-CS0001-123456789012" # TODO: generate this
        self.pending_peices = len(metainfo.pieces)

    
    async def connect(self, peer_addr: tuple[str, int]):
        reader, writer = await asyncio.open_connection(*peer_addr)
        self.peers.append((reader, writer))

            
class TorrentDownload:
    def __init__(self, file: str):
        self.file: str = file

if __name__ == "__main__":
    ...