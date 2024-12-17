import logging
import requests
import json
import os

def getUIDs(cfg, kind):
    uids = []
    endpoints = {
        "dashboards": "/api/search?type=dash-db&limit=5000&permission=View&sort=alpha-asc",
        "folders": "/api/search?type=dash-folder&limit=5000&permission=View",
        "teams": "/api/teams/search?page=1&perpage=1000"
    }
    debug_file = f"{cfg['dir']}/debug/getUIDs-{kind}.json"

    try:
        response = requests.get(f"{cfg['url']}{endpoints[kind]}", headers=cfg['headers'])
        response.raise_for_status()
        data = response.json()

        with open(debug_file, "w") as f:
            json.dump(data, f, indent=4)

        logging.info(f"Fetched UIDs for {kind} from {endpoints[kind]}")
        
        # Depending on the type, extract relevant UIDs
        if kind == "dashboards":
            uids = [item['uid'] for item in data]
        elif kind == "folders":
            uids = [folder["uid"] for folder in data]
        elif kind == "teams":
            uids = [str(team["id"]) for team in data['teams']]

        # Only return unique UIDs
        return list(set(uids))

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching UIDs for {kind} from {endpoints[kind]}: {e}", exc_info=True)
        return []
    
def createBackup(cfg, uids, kind, env):
    
    endpoints = {
        "dashboards": "/api/dashboards/uid/",
        "folders": "/api/folders/",
        "teams": "/api/teams/",
    }
    logging.info(f"Starting backup for {kind} in {env}")
    
    backup_dir = f"{cfg[env]['dir']}{env}/{kind}"
    logging.debug(f"Backup directory: {backup_dir}")
    if not os.path.exists(backup_dir):
        logging.debug(f"Making backup directory: {backup_dir}")
        os.makedirs(backup_dir)

    logging.debug(f"Backup UIDs for {kind}: {uids}")
    
    logging.debug(f"Backing up {len(uids)} items for {env} - {kind}")
    for id in uids:
        backup_file = f"{backup_dir}/{id}.json"
        logging.debug(f"Backing up UID: {id} to file: {backup_file}")

        # Make the request to backup
        response = requests.get(f"{cfg[env]['url']}{endpoints[kind]}{id}", headers=cfg[env]['headers'])
        if response.status_code == 200:
            data = response.json()
            with open(backup_file, "w") as b:
                json.dump(data, b, indent=4)
            logging.info(f"Successfully backed up {id} to {backup_file}")
        else:
            logging.error(f"Failed to backup {id}: {response.status_code} - {response.text}", exc_info=True)

    return f"Backed up {len(uids)} {type} to {backup_dir}/"
