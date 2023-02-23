class Metainfo:
    name: str
    piece_length: int
    pieces: list[str]
    files: list[dict[str, str | int]]
    announce: str
    announce_list: list[str]

    def __init__(self):
        self.name = ""
        self.piece_length = 0
        self.pieces = b""
        self.length = 0
        self.files = []

    def __str__(self):
        string = ""
        string += "Name".rjust(15) + "  " + self.name + "\n"
        string += "Piece Length".rjust(15) + "  " + str(self.piece_length) + "\n"
        string += "Pieces".rjust(15) + "  " + str(len(self.pieces) // 20) + "\n"

        for idx, file in enumerate(self.files):
            length, name = file
            string += f"\n{idx:2d}.  {length:10d}  {name}"

        return string