import hashlib
from torrent.parser import bdecode, bencode
from torrent.tracker import get_peers
import uuid

from torrent.common.metainfo import Metainfo
import click
from torrent.util.logger import log, stream_logs, set_log_level

@click.command()
@click.option("-v", "--verbose", help="Set logging verbosity")
@click.argument("torrent", type=click.Path(exists=True))
def main(verbose: str, torrent: str):
    """Download torrent"""

    set_log_level(verbose)
    stream_logs()

    with open(torrent, "rb") as tfile:
        tdata = tfile.read()
    
    metainfo_data = bdecode(tdata)
    # for file in metainfo_data["info"]["files"]:
    #     print(file)

    metainfo = Metainfo()
    if "name" in metainfo_data["info"]:
        metainfo.name = metainfo_data["info"]["name"]
    metainfo.piece_length = metainfo_data["info"]["piece length"]
    metainfo.pieces = metainfo_data["info"]["pieces"]
    metainfo.pieces = metainfo_data["info"]["pieces"]

    if "files" in metainfo_data["info"]:
        for file in metainfo_data["info"]["files"]:
            metainfo.files.append((file["length"], file["path"][0]))
    else:
        metainfo.files.append((metainfo_data["info"]["length"], metainfo.name))
    print(metainfo)

    # metainfo_info = bencode(metainfo["info"])
    # metainfo_info_hash = hashlib.sha1(metainfo_info).digest()

    # peers = get_peers(metainfo, metainfo_info_hash)
    # print(peers)

    # uuid.uuid4()


if __name__ == "__main__":
    main()
