from torrent.parser import parse

if __name__ == "__main__":
    with open("data/small.torrent", "rb") as tfile:
        tdata = tfile.read()
    
    data = parse(tdata)
    print(data)
