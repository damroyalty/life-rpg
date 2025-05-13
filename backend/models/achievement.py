from enum import Enum

class Achievement(Enum):
    NOVICE = ("Novice Adventurer", "Reach level 5")
    APPRENTICE = ("Apprentice Adventurer", "Reach level 10")
    CONSISTENT = ("Consistent Performer", "Maintain a 7-day streak")
    
    def __init__(self, title, description):
        self.title = title
        self.description = description