import libtorrent
import sys
import os.path

def mag2tor(name,mag_link):
    sess = libtorrent.session()
    prms = {
        'save_path':os.path.abspath(os.path.curdir),
    }
    torr = libtorrent.add_magnet_uri(sess, mag_link, prms)
    dots = 0
    while not torr.has_metadata():
        dots += 1
        sys.stdout.write('.')
        sys.stdout.flush()
    if (dots): sys.stdout.write('\n')
    sess.pause()
    tinf = torr.get_torrent_info()
    f = open(name + '.torrent', 'wb')
    f.write(libtorrent.bencode(
        libtorrent.create_torrent(tinf).generate()))
    f.close()