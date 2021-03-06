import random
import entity
import constants as const

def get_random_loot(slot, turns, player):
    if slot in const.FeatureSlot:
        return get_random_feature(slot, turns, player)
    elif slot in const.WeaponSlot:
        return get_random_weapon(slot, turns, player)
    assert False, slot

def get_random_feature(fslot, turns, player, level=None):
    # The "level" parameter is only used for generating the starting stuff
    (remaining_d, _, _, _) = turns.get_remaining()
    if not level:
        feature = player.fequiped.get(fslot)
        if not feature: # no feature ? generate mostly v1 features
            proba = [0.9,0.1]
        else:
            if feature.level == 1: # you currently have a v1 feature. Generate some v2 features (and v1, if you change your mind)
                proba = [0.3,0.7]
            else: # if you have a v2 feature, you probably don't want a v1 feature
                assert feature.level == 2, feature_level
                proba = [0.1,0.9]
        level = random.choices([1,2],proba)[0]
    fego = random.choices(list(const.FeatureEgo),const.fego_prob)[0]
    return entity.Feature(fslot, fego, level)

def get_random_weapon(wslot, turns, player, level=None):
    # The level of a weapon is based on the mean level of the player
    # You should find better weapon than features
    (remaining_d, _, _, _) = turns.get_remaining()
    flevel = player.flevel()
    if not level:
        rand = 10*flevel + 2 * (7 - remaining_d) + sum([random.randint(1,6) for i in range(1)])
        # Weapon are stronger than feature
        level = int(max(1,min(3, rand/10+1)))
    wego = random.choice(list(const.WeaponEgo))
    class_name = wego.value.get("w_class")
    the_class = getattr(entity, class_name)
    w = the_class(wslot, wego, level)
    return w

