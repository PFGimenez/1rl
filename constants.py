import tcod
import enum

red = tcod.Color(220,50,47)
magenta = tcod.Color(211,54,130)
violet = tcod.Color(108,113,196)
blue = tcod.Color(38,139,210)
cyan = tcod.Color(42,161,152)
green = tcod.Color(133,153,0)
orange = tcod.Color(203,75,22)
yellow = tcod.Color(181,137,0)
base03 = tcod.Color(0,43,54)
base02 = tcod.Color(7,54,66)
base01 = tcod.Color(88,110,117)
base00 = tcod.Color(101,123,131)
base0 = tcod.Color(131,148,150)
base1 = tcod.Color(147,161,161)
base2 = tcod.Color(238,232,213)
base3 = tcod.Color(253,246,227)

door_color = tcod.Color(203,75,22)
tcod.color_scale_HSV(door_color, 0.7, 1)

class FeatureSlot(enum.Enum):
    m = {"name": "monsters", "color": magenta}
    i = {"name": "id", "color": violet}
    p = {"name": "plot", "color": blue}
    c = {"name": "combat", "color": yellow}
    l = {"name": "loot", "color": green}

class WeaponSlot(enum.Enum):
    fast = {"name": "printf()", "success_rate_base": 0.3, "duration_base": 3, "instable": False}
    slow = {"name": "profiler", "success_rate_base": 0.7, "duration_base": 7, "instable": False}
    hack = {"name": "hack", "success_rate_base": 1, "duration_base": 4, "instable": True}

class FeatureEgo(enum.Enum):
    c1 = {"name": "evolutive", "char": "C"}
    c2 = {"name": "diplomatic", "char": "C"}
    c3 = {"eame": "artistic", "char": "C"}

    b1 = {"name": "minigame-based", "char": "B"}
    b2 = {"name": "reputation-based", "char": "B"}
    b3 = {"name": "pun-based", "char": "B"}

    p1 = {"name": "recursive", "char": "P"}
    p2 = {"name": "meta", "char": "P"}
    p3 = {"name": "self-contained", "char": "P"}

    m1 = {"name": "Sisyphean", "char": "M"}
    m2 = {"name": "Lovecraftian", "char": "M"}
    m3 = {"name": "Enochian", "char": "M"}

class WeaponEgo(enum.Enum):
    c = {"name": "conscious", "fego": [FeatureEgo.c1, FeatureEgo.c2, FeatureEgo.c3], "char": "c"}
    b = {"name": "basic", "fego": [FeatureEgo.b1, FeatureEgo.b2, FeatureEgo.b3], "char": "b"}
    p = {"name": "paradoxical", "fego": [FeatureEgo.p1, FeatureEgo.p2, FeatureEgo.p3], "char": "p"}
    m = {"name": "mythical", "fego": [FeatureEgo.m1, FeatureEgo.m2, FeatureEgo.m3], "char": "m"}

class TurnType(enum.Enum):
    ENNEMY = 0
    PLAYER = 1
    SPAWN = 2

class FloorType(enum.Enum):
    WALL = {"name": "wall", "collision": True, "transparent": False, "char": "#"}
    FLOOR = {"name": "floor", "collision": False, "transparent": True, "char": "."}
    DOOR = {"name": "door", "collision": False, "transparent": False, "char": "+"}
