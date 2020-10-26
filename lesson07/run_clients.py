import os
from multiprocessing import Pool


def run_process(process):
    print('RUN > python {}'.format(process))
    os.system('python {}'.format(process))


pool = Pool(processes=3)
pool.map(run_process, (
    'client.py --id=c1',
    'client.py --id=c2',
    'client.py --id=c3',
))
