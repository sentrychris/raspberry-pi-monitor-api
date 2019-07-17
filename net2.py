import time
import psutil
import os

count = 0
qry = ''
interface = 'lo'

def main():
    ul=0.00
    dl=0.00
    t0 = time.time()
    upload=psutil.net_io_counters(pernic=True)[interface].bytes_sent
    download=psutil.net_io_counters(pernic=True)[interface].bytes_recv
    up_down=(upload,download)
    while True:
        last_up_down = up_down
        upload=psutil.net_io_counters(pernic=True)[interface].bytes_sent
        download=psutil.net_io_counters(pernic=True)[interface].bytes_recv
        t1 = time.time()
        up_down = (upload,download)
        try:
            ul, dl = [(now - last) / (t1 - t0) / 1024.0
            for now,last in zip(up_down, last_up_down)]
            t0 = time.time()
        except:
            pass
        if dl > 0.1 or ul >= 0.1:
            time.sleep(0.75)
            os.system('clear')
            yield 'UL: {:0.2f} kB/s \n'.format(ul)+'DL: {:0.2f} kB/s'.format(dl)