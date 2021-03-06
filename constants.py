import tcod
import enum
import random

# Solarized colors (https://en.wikipedia.org/wiki/Solarized_(color_scheme))

red = tcod.Color(220,50,47)
magenta = tcod.Color(211,54,130)
violet = tcod.Color(108,113,196)
blue = tcod.Color(38,139,210)
cyan = tcod.Color(42,161,152)
green = tcod.Color(133,153,0)
orange = tcod.Color(203,75,22)
yellow = tcod.Color(181,137,0)
base03 = tcod.Color(0,43,54) # background
base02 = tcod.Color(7,54,66)
base01 = tcod.Color(88,110,117) # "disabled" color
base00 = tcod.Color(101,123,131)
base0 = tcod.Color(131,148,150)
base1 = tcod.Color(147,161,161)
base2 = tcod.Color(238,232,213)
base3 = tcod.Color(253,246,227)

# Desaturated colors, used for items of the floor and stairs

door_color = tcod.Color(203,75,22)
tcod.color_scale_HSV(door_color, 0.7, 1)
desat_orange = door_color

desat_red = tcod.Color(220,50,47)
tcod.color_scale_HSV(desat_red, 0.7, 1)
desat_magenta = tcod.Color(211,54,130)
tcod.color_scale_HSV(desat_magenta, 0.7, 1)
desat_violet = tcod.Color(108,113,196)
tcod.color_scale_HSV(desat_violet, 0.7, 1)
desat_blue = tcod.Color(38,139,210)
tcod.color_scale_HSV(desat_blue, 0.7, 1)
desat_green = tcod.Color(133,153,0)
tcod.color_scale_HSV(desat_green, 0.7, 1)
desat_green2 = tcod.Color(133,153,0)
tcod.color_scale_HSV(desat_green2, 0.7, 0.6)
desat_yellow = tcod.Color(181,137,0)
tcod.color_scale_HSV(desat_yellow, 0.7, 1)
boss_stairs_color = desat_green

# Light colors used for the player

light_green = tcod.Color(133,153,0)*1.5
light_blue = tcod.Color(38,139,210)*1.5


stability_threshold = 0.7

# inventory size, constrained by the screen size
inventory_max_size = 5

mul = 2

# bug stats
bug_hp = [2, 4, 6]
bug_atk = [30, 40, 50]
bug_speed_atk = [50, 60, 80]
bug_speed_mov = [120, 100, 80]
nb_atk = [5,5,5] # nb atk max between two player turns
boss_level_invok = [1, 2, 3] # level of invoked bugs

time_equip = 40 # time to equip (from inventory). Changing weapon is free
time_move = 60
spawn_interval = 120
confusion_duration = 60*60
max_stab = [100,400] # stability max
stab_reward = [5,15,30] # stability reward per bug level
resistance_mul = [1, 0.9, 0.8, 0.75, 0.70, 0.65, 0.60, 0.55, 0.50] # multiplicative bonus resistance
monster_success_rate = [0.85, 0.9, 0.95]
max_item_per_room = 2 # max 2 items per room
# synergy bonus
bonus_idem = [0, 0, 1, 2, 2, 3]

# printed with paradoxical weapon
paradox_list = ["\"Illusions are not real, yet it's real that illusion itself exists.\"",\
                "\"I know one thing: that I know nothing.\"",\
                "\"Can the Wizard of Yendor create a rock too heavy for himself to lift?\"",\
                "\"What happens if Pinocchio says \"My nose will grow now\"?\"",\
                "\"I am lying.\"",\
                "\"What is the sound of one hand clapping?\"",\
                "\"I can resist anything but temptation.\"",\
                "\"The only rule is: ignore all the rules.\"",\
                "\"Let's kill Death.\"",\
                "\"Never say never.\"",\
                "\"The only constant is change.\"",\
                "\"Moderation in all things, including moderation.\"",\
                "\"What if you travel in time and kill your grandfather before he meets your grandmother?\"",\
                "\"Which came first, the chicken or the egg?\""]

class FeatureSlot(enum.Enum):
    m = {"name": "monsters", "color": magenta, "desat_color": desat_magenta, "bug_class": "MonsterBug"}
    i = {"name": "mapgen", "color": violet, "desat_color": desat_violet, "bug_class": "MapGenBug"}
    p = {"name": "RNG", "color": blue, "desat_color": desat_blue, "bug_class": "RNGBug"}
    c = {"name": "animation", "color": yellow, "desat_color": desat_yellow, "bug_class": "AnimationBug"}
    l = {"name": "loot", "color": green, "desat_color": desat_green, "bug_class": "LootBug"}

class WeaponSlot(enum.Enum):
    fast = {"name": "printf()", "success_rate_base": 0.6, "duration_base": 40, "unstable": False, "key": "1"}
    slow = {"name": "profiler", "success_rate_base": 0.8, "duration_base": 120, "unstable": False, "key": "2"}
    hack = {"name": "hack", "success_rate_base": 1, "duration_base": 20, "unstable": True, "key": "3"}

# probability for each feature ego
# one ego is twice as probable as the other of its family
fego_prob_c = [1/4,1/4,1/2]
fego_prob_b = [1/4,1/4,1/2]
fego_prob_p = [1/4,1/4,1/2]
fego_prob_m = [1/4,1/4,1/2]
random.shuffle(fego_prob_c)
random.shuffle(fego_prob_b)
random.shuffle(fego_prob_p)
random.shuffle(fego_prob_m)
fego_prob = fego_prob_c + fego_prob_b + fego_prob_p + fego_prob_m

class FeatureEgo(enum.Enum):
    c1 = {"name": "narcoleptic", "char": "t"}
    c2 = {"name": "occult", "char": "t"}
    c3 = {"name": "psychic", "char": "t"}

    b1 = {"name": "magic-based", "char": "b"}
    b2 = {"name": "reputation-based", "char": "b"}
    b3 = {"name": "pun-based", "char": "b"}

    p1 = {"name": "recursive", "char": "p"}
    p2 = {"name": "meta", "char": "p"}
    p3 = {"name": "self-referenced", "char": "p"}

    m1 = {"name": "Sisyphean", "char": "m"}
    m2 = {"name": "Lovecraftian", "char": "m"}
    m3 = {"name": "Tolkienesque", "char": "m"}

class WeaponEgo(enum.Enum):
    c = {"name": "telepathic", "fego": [FeatureEgo.c1, FeatureEgo.c2, FeatureEgo.c3], "char": "t", "w_class": "TelepathicWeapon", "player_color": base3}
    b = {"name": "basic", "fego": [FeatureEgo.b1, FeatureEgo.b2, FeatureEgo.b3], "char": "b", "w_class": "BasicWeapon", "player_color": light_green}
    p = {"name": "paradoxical", "fego": [FeatureEgo.p1, FeatureEgo.p2, FeatureEgo.p3], "char": "p", "w_class": "ParadoxicalWeapon", "player_color": base3}
    m = {"name": "mythical", "fego": [FeatureEgo.m1, FeatureEgo.m2, FeatureEgo.m3], "char": "m", "w_class": "MythicalWeapon", "player_color": light_blue}

class TurnType(enum.Enum):
    ENEMY = 0
    PLAYER = 1
    SPAWN = 2
    MSG = 3
    GAME_OVER = 4
    WIN = 5

class TileType(enum.Enum):
    WALL = {"name": "", "collision": True, "transparent": False, "char": "#", "color": base2}
    FLOOR = {"name": "", "collision": False, "transparent": True, "char": ".", "color": base2}
    STAIRS = {"name": "stairs", "collision": False, "transparent": True, "char": ">", "color": door_color}
    BOSS_STAIRS = {"name": "strange stairs", "collision": False, "transparent": True, "char": "<", "color": boss_stairs_color}
    DOOR = {"name": "door", "collision": False, "transparent": False, "char": "+", "color": door_color}

class RenderOrder(enum.Enum):
    TILE = 1
    ITEM = 2
    ACTOR = 3

class MenuState(enum.Enum):
    STANDARD = 1
    DROP = 2
    EQUIP = 3
    POPUP = 4

# click description strings

intro_strings = ["1RL: the story of your first roguelike","You have 7 days to create", "your first roguelike!","","Complete your game by choosing its features.","","Beware: unstable features generate bugs!","","Fight bugs with weapons.", "Get higher resistance from better features.", "", "Click on anything to get details.","Press ? to get command help."]
help_adjust = 16
help_adjust_name = 15
help_strings = ["Help",\
                "numpad/vi/arrows".ljust(help_adjust, ' ')+"move/attack".rjust(help_adjust_name, ' '),\
                "g".ljust(help_adjust_name, ' ')+"pick up".rjust(help_adjust, ' '),\
                "d".ljust(help_adjust_name, ' ')+"drop".rjust(help_adjust, ' '),\
                "w".ljust(help_adjust_name, ' ')+"equip".rjust(help_adjust, ' '),\
                "[123]".ljust(help_adjust_name, ' ')+"change weapon".rjust(help_adjust, ' '),\
                "ENTER".ljust(help_adjust_name, ' ')+"use stairs".rjust(help_adjust, ' '),\
                "",
                "f".ljust(help_adjust_name, ' ')+"fullscreen".rjust(help_adjust, ' '),\
                "hover".ljust(help_adjust_name, ' ')+"get name".rjust(help_adjust, ' '),\
                "click".ljust(help_adjust_name, ' ')+"describe".rjust(help_adjust, ' '),\
                "?".ljust(help_adjust_name, ' ')+"help".rjust(help_adjust, ' '),\
               "", "", "This is a GPLv3 game.","Feel free to contribute or fork at https://github.com/PFGimenez/1rl"]
