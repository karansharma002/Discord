import json

def currency():
    with open('Config.json') as f:
        config = json.load(f)
    
    if not 'Currency' in config:
        return ':coin:'
    
    else:
        return config['Currency']
    

