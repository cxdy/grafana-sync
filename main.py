import logging
import time
import concurrent.futures
import util

# Configure logging
logging.basicConfig(
    filename='app.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s - %(lineno)d',
    level=logging.DEBUG
)

config = util.buildConfig()

def getUniqueIDs(config, env, endpoints):
    results = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(endpoints)) as executor:
        futures = {type_: executor.submit(util.getUIDs, config, env, endpoint, type_)
                   for type_, endpoint in endpoints.items()}

        for type_, future in futures.items():
            try:
                results[type_] = future.result()
                logging.info(f"Successfully retrieved UIDs for {type_}")
            except Exception as e:
                logging.error(f"Error retrieving UIDs for {type_}: {e}", exc_info=True)
    
    return results

def makeBackups(config, env, endpoints, uids):
    
    results = {}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(endpoints)) as executor:

        for type_, endpoint in endpoints.items():
            if type_ in uids.keys():
                futures = {type_: executor.submit(util.createBackup, config, env, endpoint, uids[type_], type_)
                   for type_, endpoint in endpoints.items()}
            else:
                logging.warning(f"No UIDs found for {type_}")

        for type_, future in futures.items():
            try:
                results[type_] = future.result()
                logging.info(f"Backup completed successfully")
            except Exception as e:
                logging.error(f"Error in backup task: {e}", exc_info=True)

def main():
    start_time = time.time()

    search_endpoints = {
        "dashboards": "/api/search?type=dash-db&limit=5000&permission=View&sort=alpha-asc",
        "folders": "/api/search?type=dash-folder&limit=5000&permission=View",
        "teams": "/api/teams/search?page=1&perpage=1000"
    }

    backup_endpoints = {
        "dashboards": "/api/dashboards/uid/",
        "folders": "/api/folders/",
        "teams": "/api/teams/",
    }

    logging.info("Starting to get UIDs for environment_1")
    env1UIDs = getUniqueIDs(config, 'environment_1', search_endpoints)
    logging.info("Starting to get UIDs for environment_2")
    env2UIDs = getUniqueIDs(config, 'environment_2', search_endpoints)

    # Log UID counts
    for key, value in env1UIDs.items():
        logging.info(f"environment_1 {key} - {len(value)} UIDs")
    for key, value in env2UIDs.items():
        logging.info(f"environment_2 {key} - {len(value)} UIDs")

    perform_backups = True  # Set to False to skip backups

    logging.info("Starting backup for environment_1")
    if perform_backups:
        env1Backups = makeBackups(config, 'environment_1', backup_endpoints, env1UIDs)
        logging.info(f"Completed backup for environment_1: {env1Backups}")

    logging.info("Starting backup for environment_2")
    if perform_backups:
        env2Backups = makeBackups(config, 'environment_2', backup_endpoints, env2UIDs)
        logging.info(f"Completed backup for environment_2: {env2Backups}")

    end_time = time.time() - start_time
    logging.info(f"Time elapsed: {end_time} seconds")
    print(f"Time elapsed: {end_time} seconds") # just cause i like to see stuff in my terminal

if __name__ == "__main__":
    main()