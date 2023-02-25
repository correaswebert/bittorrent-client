import click

from torrent.common.metainfo import Metainfo
from torrent import tracker
from torrent.util.logger import set_log_level, stream_logs
from torrent.peer.connect import Client


@click.command()
@click.option("-v", "--verbose", help="Set logging verbosity")
@click.argument("torrent", type=click.Path(exists=True))
def main(verbose: str, torrent: str):
    """Download torrent"""

    set_log_level(verbose)
    stream_logs()

    metainfo = Metainfo(torrent)

    peers = tracker.get_peers(metainfo)
    client = Client(metainfo)
    client.download(peers)


if __name__ == "__main__":
    main()
