"""
May download necessary datasets:
- GloVe word vectors
- SST (Stanford Sentiment TreeBank Dataset)
"""

from __future__ import print_function

import os, sys
import urllib2
import errno
import zipfile
import shutil

base_dir = 'data/'
sst_url = 'http://nlp.stanford.edu/~socherr/stanfordSentimentTreebank.zip'
glove_url = 'http://www-nlp.stanford.edu/data/glove.840B.300d.zip'


def download(url, dirpath):
    filename = url.split('/')[-1]
    filepath = os.path.join(base_dir, filename)

    try:
        u = urllib2.urlopen(url)
    except:
        print("URL {} is not accessible".format(url))
        raise Exception

    try:
        os.makedirs(base_dir)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(base_dir):
            pass
        else:
            raise

    try:
        f = open(filepath, 'wb')
    except:
        print("Cannot write {}".format(filepath))
        raise Exception

    try:
        filesize = int(u.info().getheaders("Content-Length")[0])
    except:
        print("Cannot not retrieve file size")
        raise Exception

    print("Downloading {}: {} Bytes".format(filename, filesize))

    # progress
    downloaded = 0
    block_sz = 8192
    status_width = 70
    while True:
        buf = u.read(block_sz)
        if not buf:
            print('')
            break
        else:
            print('', end='\r')
        downloaded += len(buf)

        f.write(buf)
        status = (("[%-" + str(status_width + 1) + "s] %3.2f%%") %
                  ('=' * int(float(downloaded) / filesize * status_width) + '>',
                   downloaded * 100. / filesize))
        print(status, end='')
        sys.stdout.flush()
    f.close()
    return filepath


def unzip(filepath):
    print("Extracting: " + filepath)
    dirpath = os.path.dirname(filepath)
    with zipfile.ZipFile(filepath) as zf:
        zf.extractall(dirpath)
    os.remove(filepath)


def get_glove():
    glove_path = os.path.join(base_dir, 'glove')
    if os.path.exists((glove_path)):
        return
    unzip(download(glove_url, base_dir))


def get_sst():
    sst_path = os.path.join(base_dir, 'sst')
    if os.path.exists(sst_path):
        return
    unzip(download(sst_url, base_dir))
    os.rename(
        os.path.join(base_dir, 'stanfordSentimentTreebank'),
        os.path.join(base_dir, 'sst'))
    shutil.rmtree(os.path.join(base_dir, '__MACOSX'))  # remove extraneous dir

if __name__ == '__main__':
    get_glove()
    get_sst()
