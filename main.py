import hashlib
from torrent.parser import bdecode, bencode
from torrent.tracker import http_tracker

if __name__ == "__main__":
    with open("data/small.torrent", "rb") as tfile:
        tdata = tfile.read()
    
    metainfo = bdecode(tdata)

    responses = http_tracker(metainfo)
    for response in responses:
        print(response.text)
        # print(bdecode(response.text))

