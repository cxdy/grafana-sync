import requests
import logging
import json

def get(cfg, uid):
    try:
        response = requests.get(f"{cfg['url']}/api/dashboards/uid/{uid}", headers=cfg['headers'])
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching dashboard {uid}: {e}")
        return {}
