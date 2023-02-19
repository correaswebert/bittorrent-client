from torrent.parser import bdecode

if __name__ == "__main__":
    with open("data/small.torrent", "rb") as tfile:
        tdata = tfile.read()
    
    data = bdecode(tdata)
    print(data)
