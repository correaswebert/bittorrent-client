import hashlib
import pathlib
from torrent import parser

import logging

log = logging.getLogger("root")


class Metainfo:
    def __init__(self, metainfo_filepath: pathlib.Path):
        with open(metainfo_filepath, "rb") as tfile:
            tdata = tfile.read()

        metainfo = parser.bdecode(tdata)

        if "name" in metainfo["info"]:
            self.name: str = metainfo["info"]["name"]
        else:
            self.name = metainfo_filepath.stem

        self.piece_length: str = metainfo["info"]["piece length"]

        pieces_combined = metainfo["info"]["pieces"]
        self.pieces = [
            pieces_combined[i : i + 20] for i in range(0, len(pieces_combined), 20)
        ]

        self.files: list[tuple[int, str]] = []
        if "files" in metainfo["info"]:
            for file in metainfo["info"]["files"]:
                self.files.append((file["length"], file["path"][0]))
        else:
            self.files.append((metainfo["info"]["length"], self.name))

        metainfo_info_benc = parser.bencode(metainfo["info"])
        self.info_hash = hashlib.sha1(metainfo_info_benc).digest()

    def __str__(self):
        string = ""
        string += "Name".rjust(15) + "  " + self.name + "\n"
        string += "Piece Length".rjust(15) + "  " + str(self.piece_length) + "\n"
        string += "Pieces".rjust(15) + "  " + str(len(self.pieces)) + "\n"

        for idx, file in enumerate(self.files):
            length, name = file
            string += f"\n{idx + 1:2d}.  {length:10d}  {name}"

        return string
