import hashlib
from torrent.parser import bdecode, bencode
from torrent.tracker import get_peers

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

    metainfo = Metainfo(torrent)

    peers = get_peers(metainfo)
    print(peers)


if __name__ == "__main__":
    main()
