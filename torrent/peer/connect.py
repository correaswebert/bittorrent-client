import asyncio
import uuid

class TorrentNode:
    def __init__(self):
        self.peers = []
        self.id = b"-CS0001-123456789012" # TODO: generate this

    
    def connect(self, peer_addr: tuple[str, int]):
        reader, writer = await asyncio.open_connection(*peer_addr)

    def establish_connection(peer_list, meta_info, info_hash, peer_id, download_location):
        global DOWNLOADED_PIECES, downloading_file,  REMAINING_PIECES

        if download_location is None:
            download_location = "data/downloaded/"

        # # progressbar = ProgressBar(
        # "Downloading", max = len(meta_info['info']['pieces']))
        downloading_file = open(
            f"{download_location}/{meta_info['info']['name']}", "wb")

        REMAINING_PIECES = len(meta_info['info']['pieces'])
        DOWNLOADED_PIECES = [0] * REMAINING_PIECES

        # connect to all peers and download pieces
        for peer_addr in peer_list:
            Thread(target=connect,
                args=(peer_addr, info_hash, peer_id, meta_info)).start()
            # connect(peer_addr, info_hash, peer_id, meta_info)

        if not REMAINING_PIECES:
            log.critical("File downloaded!")

        # progressbar.finish()

        # TODO: implement rarest first approach for downloading a piece
        # pp.pprint(bitfield)

            
class TorrentDownload:
    def __init__(self, file: str):
        self.file: str = file

if __name__ == "__main__"
    ...