import logging
import time

from grafanasync.cli import CLI
from grafanasync.app import Init
from grafanasync.common import getUIDs
from grafanasync.dashboards import get

def main():

    start_time = time.time()

    argparse = CLI()

    cfg, daemon = Init(argparse)

    if cfg == 0 or daemon == 0:
        logging.error("Couldn't initialize configuration!")
        return 0

    uids = getUIDs(cfg['destination'], "dashboards")
    print(f'Found {len(uids)} dashboards on {cfg["destination"]["url"]}!')

    counter = 0 
    for uid in uids:
        data = get(cfg["destination"], uid)
        counter += 1

    print(f'Fetched {counter} dashboards from {cfg["destination"]["url"]}!')    

    end_time = time.time() - start_time
    logging.info(f"Time elapsed: {end_time} seconds")
    print(f"Time elapsed: {end_time} seconds") # just cause i like to see stuff in my terminal

if __name__ == "__main__":
    main()
