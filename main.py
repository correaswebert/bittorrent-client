import hashlib

import click

from torrent.common.metainfo import Metainfo
from torrent.parser import bdecode, bencode
from torrent.tracker import get_peers
from torrent.util.logger import log, set_log_level, stream_logs


@click.command()
@click.option("-v", "--verbose", help="Set logging verbosity")
@click.argument("torrent", type=click.Path(exists=True))
def main(verbose: str, torrent: str):
    """Download torrent"""

    set_log_level(verbose)
    stream_logs()

    metainfo = Metainfo(torrent)

    peers = get_peers(metainfo)
    print(peers)


if __name__ == "__main__":
    main()
