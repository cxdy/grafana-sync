import logging
import requests
import json
import os
import yaml

# Configure logging
logging.basicConfig(
    filename='util.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s - %(lineno)d'
)

def buildConfig():
    cfg = {}
    config = {}

    with open("config.yaml", "r") as f:
        cfg = yaml.safe_load(f)
    
    for env, pairs in cfg['config'].items():
        config[env] = {}
        for key, value in pairs.items():
            config[env][key] = value

    for env in config:
        token = config[env]['token']
        config[env]['headers'] = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        }

    logging.info(f"Configuration built successfully for {list(config.keys())}")
    return config

def getUIDs(config, env, endpoint, type_):
    uids = []
    debug_file = f"{config[env]['dir']}{env}/debug/getUIDs-{type_}.json"

    try:
        response = requests.get(f"{config[env]['url']}{endpoint}", headers=config[env]['headers'])
        response.raise_for_status()
        data = response.json()

        with open(debug_file, "w") as f:
            json.dump(data, f, indent=4)

        logging.info(f"Fetched UIDs for {type_} from {endpoint}")
        
        # Depending on the type, extract relevant UIDs
        if type_ == "dashboards":
            uids = [item['uid'] for item in data]
        elif type_ == "folders":
            uids = [folder["uid"] for folder in data]
        elif type_ == "users":
            uids = [user["userId"] for user in data]
        elif type_ == "teams":
            uids = [str(team["id"]) for team in data['teams']]

        # Only return unique UIDs
        return list(set(uids))

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching UIDs for {type_} from {endpoint}: {e}", exc_info=True)
        return []

def createBackup(config, env, endpoint, uids, type):
    logging.info(f"Starting backup for {type} in {env}")
    
    backup_dir = f"{config[env]['dir']}{env}/{type}"
    logging.debug(f"Backup directory: {backup_dir}")
    if not os.path.exists(backup_dir):
        logging.debug(f"Making backup directory: {backup_dir}")
        os.makedirs(backup_dir)

    logging.debug(f"Backup UIDs for {type}: {uids}")
    
    logging.debug(f"Backing up {len(uids)} items for {env} - {type}")
    for id in uids:
        backup_file = f"{backup_dir}/{id}.json"
        logging.debug(f"Backing up UID: {id} to file: {backup_file}")

        # Make the request to backup
        response = requests.get(f"{config[env]['url']}{endpoint}{id}", headers=config[env]['headers'])
        if response.status_code == 200:
            data = response.json()
            with open(backup_file, "w") as b:
                json.dump(data, b, indent=4)
            logging.info(f"Successfully backed up {id} to {backup_file}")
        else:
            logging.error(f"Failed to backup {id}: {response.status_code} - {response.text}", exc_info=True)

    return f"Backed up {len(uids)} {type} to {backup_dir}/"
