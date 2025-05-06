import json

def save_player(data):
    with open('player.json', 'w') as f:
        json.dump(data, f)

def load_player():
    with open('player.json') as f:
        return json.load(f)