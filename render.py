import tcod as tcod

import constants as const
from enum import Enum
import entity as ent
import math
import textwrap

def render_map(root_console, con, entities, player, game_map, screen_width, screen_height):
    """
    Render the map
    """
    # Draw all the tiles in the game map
    for y in range(game_map.height):
        for x in range(game_map.width):
            clear_cell(con, x, y, game_map)

    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    # Draw all entities in the list
    for entity in entities_in_render_order:
        draw_entity(con, entity, game_map, player)

    con.blit(dest=root_console)

def render_popup(root_console, popup_panel, map_width, map_height, strings):
    """
    Render the popup (description screen)
    """
    tcod.console_clear(popup_panel)
    tcod.console_set_default_foreground(popup_panel, const.base2)
    # the first item of the list is the window title
    popup_panel.print_frame(0, 0, popup_panel.width, popup_panel.height, string=strings[0])
    wraped_strings = []
    first = True
    for s in strings:
        if first:
            first = False
            continue
        if s == "":
            wraped_strings.append(s)
        else:
            wraped_strings += textwrap.wrap(s, int(0.75*popup_panel.width))
    y = int(popup_panel.height /2 - len(wraped_strings) / 2)
    for s in wraped_strings:
        tcod.console_print_ex(popup_panel, int(popup_panel.width / 2), y, tcod.BKGND_NONE, tcod.CENTER, s)
        y += 1
    popup_panel.blit(dest=root_console, dest_x = round(5*map_width/24), dest_y=round(5*map_height/24), bg_alpha=0.9)

def render_boss_hp(root_console, des_panel, map_height, boss):
    """
    render the boss hp bar
    replace the description during the boss fight
    """
    tcod.console_set_default_foreground(des_panel, const.base3)
    tcod.console_print_ex(des_panel, 1, 0, tcod.BKGND_NONE, tcod.LEFT, boss.name)
    x_start = 1
    x_width = des_panel.width - 2
    hp_width = round((boss.hp / boss.max_hp * x_width))

    for x in range(x_start, x_start+x_width):
        tcod.console_set_char_background(des_panel, x, 0, const.base02, tcod.BKGND_SET)
    for x in range(x_start, x_start + hp_width):
        tcod.console_set_char_background(des_panel, x, 0, const.red, tcod.BKGND_SET)

    des_panel.blit(dest=root_console, dest_y=map_height)

def render_des(root_console, des_panel, map_height, string):
    """
    render the description bar
    """
    tcod.console_set_default_foreground(des_panel, const.base2)
    tcod.console_print_ex(des_panel, 1, 0, tcod.BKGND_NONE, tcod.LEFT, string)
    des_panel.blit(dest=root_console, dest_y=map_height)

def render_log(root_console, log_panel, msglog, map_height, force=False):
    """
    Render the bottom panel (log)
    """
    if force or msglog.is_there_new():
        tcod.console_clear(log_panel)
        tcod.console_set_default_foreground(log_panel, const.base0)
        log_panel.print_frame(0, 0, log_panel.width, log_panel.height, string="Log")
        y = log_panel.height - 2 - len(msglog.messages)
        for msg in msglog.messages:
            if y >= msglog.last:
                tcod.console_set_default_foreground(log_panel, msg.color_active)
            else:
                tcod.console_set_default_foreground(log_panel, msg.color_inactive)
            log_panel.print_(1, y + 1, msg.string)
            y += 1
        msglog.set_rendered()
        log_panel.blit(dest=root_console, dest_y=map_height + 1)

def render_feature(inv_panel, feature, default_fore, y, player):
    """
    reader the feature part of the right panel
    """
    max_stab_width = 10
    start_stab = inv_panel.width - 1 - max_stab_width

    tcod.console_set_default_foreground(inv_panel, default_fore)
    effective_string = ""
    if feature.is_in_inventory:
        for wslot in player.wequiped:
            weapon = player.wequiped.get(wslot)
            if weapon and weapon.is_effective_on_fego(feature.fego):
                effective_string = " *"
                break

    tcod.console_print_ex(inv_panel, 3, y, tcod.BKGND_NONE, tcod.LEFT, feature.fego.value.get("name") + effective_string)
    y += 1
    tcod.console_print_ex(inv_panel, 3, y, tcod.BKGND_NONE, tcod.LEFT, feature.fslot.value.get("name") + " v" + str(feature.level))

    tcod.console_set_default_foreground(inv_panel, const.base3)
    stable = feature.is_stable()
    if stable:
        tcod.console_print_ex(inv_panel, start_stab, y, tcod.BKGND_NONE, tcod.LEFT, "Stable")
    else:
        tcod.console_print_ex(inv_panel, start_stab, y, tcod.BKGND_NONE, tcod.LEFT, "Unstable")
    stab_width = round(feature.stability / feature.max_stability * max_stab_width)
    if stable:
        color = const.green
    else:
        color = const.green*(feature.stability/feature.max_stability/const.stability_threshold) + const.red*(1 - feature.stability/feature.max_stability/const.stability_threshold)
    for x in range(start_stab, start_stab + stab_width):
        tcod.console_set_char_background(inv_panel, x, y, color, tcod.BKGND_SET)
    for x in range(start_stab + stab_width, start_stab + max_stab_width):
        tcod.console_set_char_background(inv_panel, x, y, const.base02, tcod.BKGND_SET)

def render_weapon(inv_panel, weapon, default_fore, y, active_weapon):
    """
    reader the weapon part of the right panel
    """
    x = len(weapon.wego.value.get("name")) + 4
    for fslot in weapon.fslot_effective:
        # tcod.console_set_char_background(inv_panel, x, y, fslot.value.get("color"), tcod.BKGND_SET)
        tcod.console_set_default_foreground(inv_panel, fslot.value.get("color"))
        tcod.console_put_char(inv_panel, x, y, "*", tcod.BKGND_NONE)
        x += 1
    tcod.console_set_default_foreground(inv_panel, default_fore)
    if active_weapon:
        tcod.console_set_default_foreground(inv_panel, const.base2)
    else:
        tcod.console_set_default_foreground(inv_panel, default_fore)
    tcod.console_print_ex(inv_panel, 1, y, tcod.BKGND_NONE, tcod.LEFT, weapon.wslot.value.get("key")+" "+weapon.wego.value.get("name"))
    y += 1
    tcod.console_print_ex(inv_panel, 3, y, tcod.BKGND_NONE, tcod.LEFT, weapon.wslot.value.get("name")+" v"+str(weapon.level))
    string = weapon.stat_string()
    tcod.console_print_ex(inv_panel, inv_panel.width-1, y, tcod.BKGND_NONE, tcod.RIGHT, string)

def render_sch(root_console, sch_panel, turns, map_width, time_malus):
    """
    render the time panel
    """
    # Time
    (remaining_d, remaining_h, remaining_m, remaining_s) = turns.get_remaining()
    w = sch_panel.width
    tcod.console_set_default_foreground(sch_panel, const.base0)
    sch_panel.print_frame(0, 0, w, 3, string="Remaining time")
    color = const.base0
    if remaining_d <= 0:
        color = const.red
    elif remaining_d <= 2:
        color = const.orange
    remaining_d = "{:01d}".format(remaining_d)
    remaining_h = "{:02d}".format(remaining_h)
    remaining_m = "{:02d}".format(remaining_m)
    remaining_s = "{:02d}".format(remaining_s)
    time_string = remaining_d+"d "+remaining_h+"h "+remaining_m+"m "+remaining_s+"s"
    if time_malus == 0:
        malus = ""
    elif time_malus == -1: # game over
        malus = ":("
        time_malus = 10000
    else:
        malus = "-"+str(time_malus)+"s"
    sch_panel.print(3, 1, time_string, alignment=tcod.LEFT, fg=color)
    sch_panel.print(4+len(time_string), 1, malus, alignment=tcod.LEFT, fg=const.red if time_malus >= 3600 else const.orange)
    sch_panel.blit(dest=root_console, dest_x=map_width)

def render_inv(root_console, inv_panel, player, map_width, sch_height):
    """
    Render the right panel (features, weapons, inventory) except time
    """
    tcod.console_clear(inv_panel)
    default_fore = const.base0
    tcod.console_set_default_foreground(inv_panel, default_fore)
    w = inv_panel.width

    # Features
    y = 0
    tcod.console_set_default_foreground(inv_panel, default_fore)
    inv_panel.print_frame(0, y, w, 5 * 3 + 1, string="Features")
    for fslot in const.FeatureSlot:
        y += 1
        feature = player.fequiped.get(fslot)
        tcod.console_set_char_background(inv_panel, 1, y, fslot.value.get("color"), tcod.BKGND_SET)
        if feature:
            render_feature(inv_panel, feature, default_fore, y, player)
            y += 2
        else:
            tcod.console_set_default_foreground(inv_panel, const.base02)
            tcod.console_print_ex(inv_panel, 3, y, tcod.BKGND_NONE, tcod.LEFT, "(none)")
            y += 1
            tcod.console_print_ex(inv_panel, 3, y, tcod.BKGND_NONE, tcod.LEFT, fslot.value.get("name"))
            y += 1

    y += 1
    tcod.console_set_default_foreground(inv_panel, default_fore)

    inv_panel.print_frame(0, y, w, 3, string="Resistance")
    y += 1
    x = 2
    at_least_one = False
    for fslot in const.FeatureSlot:
        r = player.resistances.get(fslot)
        if r > 0:
            at_least_one = True
            tcod.console_set_char_background(inv_panel, x, y, fslot.value.get("color"), tcod.BKGND_SET)
            x += 1
            if fslot in player.synergy:
                tcod.console_print_ex(inv_panel, x, y, tcod.BKGND_NONE, tcod.LEFT, ":"+str(r)+"*")
            else:
                tcod.console_print_ex(inv_panel, x, y, tcod.BKGND_NONE, tcod.LEFT, ":"+str(r))
            x += 4
        else:
            x += 5
    if not at_least_one:
        tcod.console_set_default_foreground(inv_panel, const.base02)
        tcod.console_print_ex(inv_panel, int(w / 2), y, tcod.BKGND_NONE, tcod.CENTER, "(none)")

    tcod.console_set_default_foreground(inv_panel, default_fore)
    y += 2
    inv_panel.print_frame(0, y, w, 3 * 3 + 1, string="Weapons")

    for wslot in const.WeaponSlot:
        y += 1
        weapon = player.wequiped.get(wslot)
        if weapon:
            render_weapon(inv_panel, weapon, default_fore, y, weapon == player.active_weapon)
            y += 1
        else:
            tcod.console_set_default_foreground(inv_panel, const.base02)
            tcod.console_print_ex(inv_panel, 1, y, tcod.BKGND_NONE, tcod.LEFT, wslot.value.get("key")+" (none)")
            y += 1
            tcod.console_print_ex(inv_panel, 3, y, tcod.BKGND_NONE, tcod.LEFT, wslot.value.get("name"))
            string = str(round(wslot.value.get("success_rate_base") * 100))+"% "+str(wslot.value.get("duration_base"))+"s"
            if wslot.value.get("unstable"):
                string = "Stab- "+string
            tcod.console_print_ex(inv_panel, w-1, y, tcod.BKGND_NONE, tcod.RIGHT, string)
        y += 1

    y += 1

    tcod.console_set_default_foreground(inv_panel, default_fore)
    inv_panel.print_frame(0, y, w, 5 * 3 + 1, string="Inventory")

    for k in player.inventory:
        y += 1
        item = player.inventory.get(k)
        if item:
            if isinstance(item, ent.Weapon):
                render_weapon(inv_panel, item, default_fore, y, False)
                tcod.console_put_char(inv_panel, 1, y, k, tcod.BKGND_NONE)
            else:
                render_feature(inv_panel, item, default_fore, y, player)
            tcod.console_set_default_foreground(inv_panel, default_fore)
            tcod.console_put_char(inv_panel, 1, y, k, tcod.BKGND_NONE)
        else:
            tcod.console_set_default_foreground(inv_panel, const.base02)
            tcod.console_print_ex(inv_panel, 1, y, tcod.BKGND_NONE, tcod.LEFT, k+" (none)")
        y += 2

    inv_panel.blit(dest=root_console, dest_x=map_width, dest_y=sch_height)

def draw_entity(con, entity, game_map, player):
    visible = game_map.is_visible(entity.x, entity.y)
    if visible\
    or (entity.is_seen and (isinstance(entity, ent.Weapon) or isinstance(entity, ent.Feature)))\
    or (isinstance(entity, ent.Monster) and isinstance(player.active_weapon, ent.TelepathicWeapon)):
        # are visible: what is directly visible, remembered weapon and feature. When telepathic, monster are visible too
        tcod.console_set_char_background(con, entity.x, entity.y, const.base03)
        if visible:
            if (isinstance(entity, ent.Monster) and entity.confusion_date):
                tcod.console_set_char_background(con, entity.x, entity.y, entity.visible_color)
                tcod.console_set_char_foreground(con, entity.x, entity.y, const.base03)
            else:
                tcod.console_set_char_foreground(con, entity.x, entity.y, entity.visible_color)
        else:
            tcod.console_set_char_foreground(con, entity.x, entity.y, entity.hidden_color)
        tcod.console_set_char(con, entity.x, entity.y, entity.char)

def clear_cell(con, x,y,game_map):
    # print the floor of a cell
    wall = game_map.is_blocked(x,y)
    door = game_map.is_door(x,y)
    visible = game_map.is_visible(x,y)

    if visible:
        game_map.tiles[x][y].is_seen = True

    tcod.console_set_char_background(con, x, y, const.base03)
    if game_map.tiles[x][y].is_seen:
        if visible:
            tcod.console_set_char_foreground(con, x, y, game_map.tiles[x][y].visible_color)
        else:
            tcod.console_set_char_foreground(con, x, y, game_map.tiles[x][y].hidden_color)
        tcod.console_set_char(con, x, y, game_map.tiles[x][y].char)
    else:
        tcod.console_set_char(con, x, y, ' ')

def get_object_under_mouse(mouse, turns, player, entities, game_map, screen_width, map_width):
    """
    Used to know what to describe
    """
    (x, y) = mouse
    if game_map.is_over_map(x,y):
        entities_in_render_order = sorted([entity for entity in entities
                if entity.x == x and entity.y == y and\
                                           (game_map.is_visible(x,y) or\
                                            ((isinstance(entity, ent.Weapon) or isinstance(entity, ent.Feature)) and entity.is_seen))], key=lambda x: x.render_order.value, reverse=True)
        if entities_in_render_order:
            return entities_in_render_order[0]
        if game_map.is_visible(x,y) and game_map.tiles[x][y].name:
            return game_map.tiles[x][y]
        return None
    if x >= map_width + 1 and x < screen_width - 1:
        i = 0
        if y == 1:
            return RemainingTime(turns, player)

        for fslot in const.FeatureSlot:
            if y >= 4+3*i and y <= 5+3*i:
                return player.fequiped.get(fslot)
            i += 1

        if y == 20:
            return Resistances()

        i = 0
        for wslot in const.WeaponSlot:
            if y >= 23+3*i and y <= 24+3*i:
                return player.wequiped.get(wslot)
            i += 1

        letter_index = ord('a')
        for i in range(const.inventory_max_size+1):
            if y >= 33+3*i and y <= 34+3*i:
                return player.inventory.get(chr(letter_index+i))
    return None

def get_names_under_mouse(mouse, entities, game_map, screen_width):
    (x, y) = mouse
    if game_map.is_over_map(x,y):
        entities_in_render_order = sorted([entity for entity in entities
                if entity.x == x and entity.y == y and\
                                           (game_map.is_visible(x,y) or\
                                            ((isinstance(entity, ent.Weapon) or isinstance(entity, ent.Feature)) and entity.is_seen))], key=lambda x: x.render_order.value, reverse=True)
        names = [e.name for e in entities_in_render_order]
        if game_map.is_visible(x,y):
            string = game_map.tiles[x][y].name
            if string:
                names.append(string)
        names = ', over a '.join(names)
        # space padding to remove the precedent description
        names = names.ljust(screen_width, ' ')

        return "%s%s" % (names[0].upper(), names[1:]) # fist letter in capital
    else:
        return "".ljust(screen_width, ' ')

def capitalize(string):
    return "%s%s" % (string[0].upper(), string[1:]) # fist letter in capital

class RemainingTime():
    """
    Dummy class, only used for description
    """
    def __init__(self, turns, player):
        self.turns = turns
        self.player = player
        self.name = "Remaining time"

    def describe(self):
        d = ["You have only 7 days to create your game.", "", "Each time a bug attacks you, your next move gets a time penalty."]
        if self.player.time_malus > 0:
            d += ["", "You current time penalty is "+str(self.player.time_malus)+"s."]
        return d

class Resistances():
    """
    Dummy class, only used for description
    """
    def __init__(self):
        self.name = "Resistance"

    def describe(self):
        return ["Resistance protects from bug attack.", "Each resistance matches one bug type.", "", "Resistances are granted by the features. They depend on:","- whether their feature is stable","- the level of their feature","- the synergy of their feature","","To get synergy, equip features with the same ego!  Resistances upgraded by synergy are noted with *."]
