import tcod
import entity
import constants as const
import game_map as gmap
import time

def main():
    screen_width = 100
    screen_height = 48

    # Size of the map
    map_width = screen_width
    map_height = screen_height

    player = entity.Player(None, None)
    entities = [player]

    tcod.console_set_custom_font('font.png', tcod.FONT_LAYOUT_ASCII_INROW)

    root_console = tcod.console_init_root(screen_width, screen_height, '1RL – 7DRL 2019')

    con = tcod.console.Console(screen_width, screen_height)
    tcod.console_set_default_background(con, const.base03)
    tcod.console_clear(con)

    game_map = gmap.GameMap(map_width, map_height,con)

    game_map.make_map_bsp(player)
    time.sleep(2)

if __name__ == '__main__':
    main()
