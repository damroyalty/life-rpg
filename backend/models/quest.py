from enum import Enum
import random
from models.player import Attribute

class QuestType(Enum):
    DAILY = "Daily"
    WEEKLY = "Weekly"
    STORY = "Story"
    HABIT = "Habit"

class QuestRarity(Enum):
    COMMON = "Common"
    RARE = "Rare"
    EPIC = "Epic"
    LEGENDARY = "Legendary"

class Quest:
    DESCRIPTORS = {
        "strength": ["Brawny", "Mighty", "Powerful"],
        "intelligence": ["Wise", "Brilliant", "Sagacious"],
        "charisma": ["Charming", "Persuasive", "Silver-tongued"]
    }
    
    def __init__(self, name, description, quest_type, xp_reward=0, gold_reward=0, rarity=QuestRarity.COMMON):
        self.name = self._generate_quest_name(name) if rarity != QuestRarity.COMMON else name
        self.description = description
        self.quest_type = quest_type
        self.xp_reward = int(xp_reward * (1 + 0.5 * list(QuestRarity).index(rarity)))
        self.gold_reward = int(gold_reward * (1 + 0.5 * list(QuestRarity).index(rarity)))
        self.rarity = rarity
        self.completed = False
    
    def _generate_quest_name(self, base_name):
        adjective = random.choice(list(self.DESCRIPTORS.values()))[0]
        return f"{adjective} {base_name}"
    
    @classmethod
    def daily_quests(cls):
        """Basic daily quests without rarity modifiers"""
        return [
            cls("Morning Ritual", "Complete your morning routine", QuestType.DAILY, 25, 10),
            cls("Code Training", "Practice coding for 1 hour", QuestType.DAILY, 50, 25),
            cls("Dragon Exercise", "30 minutes of physical activity", QuestType.DAILY, 30, 15)
        ]
    
    @classmethod
    def generate_daily_quests(cls, count=3):
        """Generate quests with random rarity modifiers"""
        base_quests = [
            ("Morning Ritual", "Complete your sacred morning rites", QuestType.DAILY, 25, 10),
            ("Code Training", "Study the arcane coding tomes", QuestType.DAILY, 50, 25),
            ("Dragon Exercise", "Train like the ancient dragon warriors", QuestType.DAILY, 30, 15)
        ]
        return [
            cls(*quest, random.choice(list(QuestRarity))) 
            for quest in random.sample(base_quests, min(count, len(base_quests)))
        ]