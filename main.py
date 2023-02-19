import hashlib
from torrent.parser import bdecode, bencode
from torrent.tracker import get_peer_list

if __name__ == "__main__":
    with open("data/small.torrent", "rb") as tfile:
        tdata = tfile.read()
    
    metainfo = bdecode(tdata)
    metainfo_info = bencode(metainfo["info"])
    metainfo_info_hash = hashlib.sha1(metainfo_info).digest()

    responses = get_peer_list(metainfo, metainfo_info_hash)
    # for response in responses:
    #     print(bdecode(response.text))

