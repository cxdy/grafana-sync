import argparse
import sys

def CLI():

  parser = argparse.ArgumentParser(description='grafana-sync CLI')

  global_arguments = {
    '--sync': {
      'help': 'Sync the specified resources',
      'action': 'store_true',
      'dest': 'sync',
      'default': False
    },
    '--diff': {
      'help': 'Diff the specified resources',
      'action': 'store_true',
      'dest': 'diff',
      'default': False
    },
    '--show': {
      'help': 'Show the specified resources',
      'action': 'store_true',
      'dest': 'show',
      'default': False
    },
    '--config': {
      'type': str,
      'help': 'Path to the config file',
      'dest': 'config',
      'default': 'config.yaml'
    },
    '--debug': {
      'help': 'Enable debug logging',
      'action': 'store_true',
      'dest': 'debug',
      'default': False
    },
    '--dry-run': {
      'help': 'Run without making any changes',
      'action': 'store_true',
      'dest': 'dry_run',
      'default': False
    },
    '--daemon': {
      'help': 'Run in daemon mode',
      'action': 'store_true',
      'dest': 'daemon',
      'default': False
    },
    '--resources': {
      'type': str,
      'help': 'Resources to sync, takes multiple arguments or "all"',
      'nargs': '+',
      'dest': 'resources',
      'default': []
    },
    '--delete': {
      'help': 'Delete resources from destination prior to syncing, defaults to False (which will overwrite existing resources)',
      'action': 'store_true',
      'dest': 'delete',
      'default': False
    },
  }

  for arg, params in global_arguments.items():
    name_or_flags = [arg] if not arg.startswith('--') else [arg]
    if not arg.startswith('--'):
        params.pop('dest', None)
    parser.add_argument(*name_or_flags, **params)

  if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)
  
  args = parser.parse_args()
  
  return args
