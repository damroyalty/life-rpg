import json
from datetime import datetime
from enum import Enum

class Attribute(Enum):
    STRENGTH = "strength"
    INTELLIGENCE = "intelligence"
    CHARISMA = "charisma"
    ENDURANCE = "endurance"
    CREATIVITY = "creativity"

class Player:
    def __init__(self):
        self.name = "Adventurer"
        self.level = 1
        self.xp = 0
        self.gold = 100
        self.attributes = {
            "strength": 5,
            "intelligence": 8,
            "charisma": 6,
            "endurance": 5,
            "creativity": 5
        }
        self.active_quests = []
        self.completed_quests = []
        self.last_login = datetime.now()
        self.daily_streak = 0
        self.habits = []
        self.visited_locations = [
            {"name": "Tokyo", "x_pct": 88, "y_pct": 50},
            {"name": "Paris", "x_pct": 46, "y_pct": 40},
        ]

    def save(self):
        with open('data/player.json', 'w') as f:
            json.dump({
                'name': self.name,
                'level': self.level,
                'xp': self.xp,
                'gold': self.gold,
                'attributes': self.attributes,
                'last_login': self.last_login.isoformat(),
                'daily_streak': self.daily_streak,
                'habits': self.habits,
                'visited_locations': self.visited_locations
            }, f)

    @classmethod
    def load(cls):
        try:
            with open('data/player.json') as f:
                data = json.load(f)
                player = cls()
                player.name = data.get('name', 'Adventurer')
                player.level = data.get('level', 1)
                player.xp = data.get('xp', 0)
                player.gold = data.get('gold', 100)
                player.attributes = data.get('attributes', {
                    "strength": 5,
                    "intelligence": 8,
                    "charisma": 6,
                    "endurance": 5,
                    "creativity": 5
                })
                player.last_login = datetime.fromisoformat(data.get('last_login', datetime.now().isoformat()))
                player.daily_streak = data.get('daily_streak', 0)
                player.habits = data.get('habits', [])
                player.visited_locations = data.get('visited_locations', [])
                return player
        except (FileNotFoundError, ValueError):
            return cls()

    def add_xp(self, amount):
        self.xp += amount
        if self.xp >= self.xp_to_next_level():
            self.level_up()

    def xp_to_next_level(self):
        return self.level * 100

    def level_up(self):
        self.level += 1
        self.xp = 0
        self.gold += self.level * 50

    def complete_quest(self, quest):
        self.add_xp(quest.xp_reward)
        self.gold += quest.gold_reward
        self.completed_quests.append(quest)
