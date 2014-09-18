fuploader
=========
Simple cli app to upload files through rsync to server
and get correct links

Dependencies
============
system:
- rsync

python:
- click

Install
=======

::

    sudo python setup.py install

Usage
=====
::

    $ fup --help
    Usage: fup [OPTIONS] [SRC_FILES]...

    Options:
      -t, --target TEXT      Target host to upload files
      -f, --folder TEXT      Base folder on remote host
      -s, --sub-folder TEXT  Sub folder on remote host, will be added to http
                             prefix as well
      -p, --prefix TEXT      Prefix to append after hostname for results
      -v, --verbose          Enable verbose output
      -c, --cleanup          Delete uploaded files from local machine
      --help                 Show this message and exit.


config
------
Copy example config *conf/fuploader.json.example*
into *~/.config/fuploader.json* and edit it to provide personal defaults.

