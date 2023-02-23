import hashlib
from torrent.parser import bdecode, bencode
from torrent.tracker import get_peers

import click
from torrent.utils.logger import log, stream_logs, set_log_level

@click.command()
@click.option("--verbose", help="Set logging verbosity")
def main(verbose):
    set_log_level(verbose)
    stream_logs()

    with open("data/small.torrent", "rb") as tfile:
        tdata = tfile.read()
    
    metainfo = bdecode(tdata)
    metainfo_info = bencode(metainfo["info"])
    metainfo_info_hash = hashlib.sha1(metainfo_info).digest()

    peers = get_peers(metainfo, metainfo_info_hash)
    log.info(peers)


if __name__ == "__main__":
    main()
