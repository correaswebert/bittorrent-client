BitTorrent Client
=================

BitTorrent is a protocol for distributing files. It identifies content by URL
and is designed to integrate seamlessly with the web. Its advantage over plain
HTTP is that when multiple downloads of the same file happen concurrently, the
downloaders upload to each other, making it possible for the file source to
support very large numbers of downloaders with only a modest increase in its
load.

Installation
------------

Clone and `cd` into the repository

```
git clone https://github.com/correaswebert/bittorrent-client.git
cd bittorrent-client
```

Create and activate a virtual environment. It prevents polluting the global
environment. _This step is optional_.

```
python3 -m venv venv
source venv/bin/activate
```

Install the dependencies using `pip`

```
python -m pip install -r requirements.txt
```

Usage
-----

_Enter your virtual environment if created_.

```
python main.py
```

License
-------

This project is under the MIT License.
