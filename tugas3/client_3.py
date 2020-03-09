import logging
import requests
import os
import threading
from tqdm import tqdm

BLOCK_SIZE = 1024

def download_gambar(url=None):
    if (url is None):
        return False
    ff = requests.get(url, stream=True)
    tipe = dict()
    tipe['image/png']='png'
    tipe['image/jpg']='jpg'
    tipe['image/jpeg']='jpg'

    content_type = ff.headers['Content-Type']

    total_size = int(ff.headers.get('content-length', 0))
    with tqdm(total=total_size, unit='iB', unit_scale=True) as t:
        if (content_type in list(tipe.keys())):
            namafile = os.path.basename(url)
            ekstensi = tipe[content_type]
            t.set_description(f'Writing {namafile[:30]}...')
            with open(f"{namafile}","wb") as fp:
                for data in ff.iter_content(BLOCK_SIZE):
                    t.update(len(data))
                    fp.write(data)
        else:
            return False


gambars = [
    'https://images.unsplash.com/photo-1583142499515-db3e66a57bdc?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
    'https://images.unsplash.com/photo-1520699894975-334692f3a636?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60',
    'https://images.unsplash.com/photo-1453904061941-02ada96e1f4a?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60',
]

if __name__=='__main__':
    for i in gambars:
        t = threading.Thread(target=download_gambar, args=(i,))
        t.start()

        # download_gambar('https://asset.kompas.com/crops/qz_jJxyaZgGgboomdCEXsfbSpec=/0x0:998x665/740x500/data/photo/2020/03/01/5e5b52f4db896.jpg')
