import logging
import yaml

def Init(args):
  config, daemon = Config(args.config)

  return config, daemon

def Config(file="config.yaml"):
  cfg = {}
  config = {}
  daemon = {}

  try:
    with open(file, "r") as f:
        cfg = yaml.safe_load(f)
    
    for env, pairs in cfg['config'].items():
        config[env] = {}
        for key, value in pairs.items():
            config[env][key] = value

    for dict, item in cfg['daemon'].items():
        daemon[dict] = {}
        if dict == "enabled":
            daemon[dict] = item
        else:
          for key, value in item.items():
            daemon[dict][key] = value

    for env in config:
        token = config[env]['token']
        config[env]['headers'] = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        }

  except FileNotFoundError as e:
      logging.error(f"Error reading configuration file: {e}")
      return 0, e
  except Exception as e:
      logging.error(f"Error building configuration: {e}")
      return 0, e

  return config if config else 0 , daemon if daemon else 0

