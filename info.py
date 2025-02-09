import os
info = {
    "API_KEY": os.environ['X_RIOT_TOKEN'],
    "REGIONV1": 'americas',
    "REGIONV4": 'na1',
    'headers': {
        "X-Riot-Token": os.environ['X_RIOT_TOKEN']
    }
}