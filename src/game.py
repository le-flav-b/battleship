import time

import pygame as pg

from src.physics import Pos, Speed
from src.player import Player
from src.terrainGen import GenerateMap, ColorMap


class Game:
    """General class for the game
    """

    CATEGORY_NONE = 0
    CATEGORY_MENU = 1
    CATEGORY_GAME = 2
    CATEGORY_GAME_OVER = 3

    def __init__(self, screen_width, screen_height):
        """Create the pygame window and initialize all the elements of the game
        """

        # screen size
        self.screen_size = (screen_width, screen_height)

        # window creation
        pg.init()
        self.screen = pg.display.set_mode(self.screen_size)
        pg.display.set_icon(pg.image.load('assets/images/icon.png'))
        pg.display.set_caption('Battleship')

        # main settings
        self.music = True
        self.sound = True

        # CATEGORY : menu, game, or game over
        self.category = Game.CATEGORY_NONE

        # input gestion
        self.pressing_keys = {pg.K_z: False,
                              pg.K_q: False,
                              pg.K_s: False,
                              pg.K_d: False}


    def run(self):
        """Run the game
        """

        print("\n" * 2
              + "=" * 73 + "\n"
              + "=" * 26 + " " * 4 + "GAME  OPENING" + " " * 4 + "=" * 26 + "\n"
              + "=" * 73 + "\n" * 2)

        while True:

            # 3 states of the game :
            #   menu (choose settings and make connection then press play),
            #   game (the map with all the elements and the control of our personal boat),
            #   game over (the last game screen with omni visibility and a filter as background,
            #              resume of the game stats, and a button to go back to the menu)
            self.menu_update()
            self.game_update()
            self.game_over_update()
    
    def menu_update(self):  # TODO: create a menu
        """Generate the window content when the game is in the menu state
        """

        self.category = Game.CATEGORY_MENU

        background = pg.transform.scale(pg.image.load('assets/images/menu_background.png'), self.screen_size)
        play_button = pg.transform.scale(pg.image.load('assets/images/start_button.png'), (int(self.screen_size[0] / 2), int(self.screen_size[1] / 6.5)))
        play_button_place = (int(self.screen_size[0] / 4.25), int(self.screen_size[1] / 1.41))
        play_button_rect = play_button.get_rect()
        play_button_rect.x, play_button_rect.y = play_button_place

        print("\n" * 2 + "\t" * 2 + "~~~ MENU ~~~" + "\n" * 2)

        start = False
        while not start:

            # apply background image scaled to the screen size
            self.screen.blit(background, (0, 0))

            # apply the start button
            self.screen.blit(play_button, play_button_place)

            # will be a user choice (like a slider or something)
            self.sea_level = 145
            self.sand_height = 5

            # update the screen
            pg.display.flip()

            # check for events
            for event in pg.event.get():

                self.manage_general_events(event)

                if event.type == pg.MOUSEBUTTONDOWN:
                    if play_button_rect.collidepoint(event.pos):
                        start = True

        # map generation
        self.map_data = GenerateMap(self.screen_size)

        # map image generation TODO : change the way to do it by putting a blue background and drawing the islands on it
        self.map_image = pg.surfarray.make_surface(ColorMap(self.map_data).get_color_map_array(self.sea_level, self.sand_height))

    def game_update(self):
        """Generate the window content when the game is in the game state
        """

        self.category = Game.CATEGORY_GAME

        print("\n" * 2 + "\t" * 2 + "~~~ GAME ~~~" + "\n" * 2)

        # player
        self.player = Player(Pos(self.screen_size[0] / 2, self.screen_size[1] / 2), Speed(0, 0),
                             mass=10, max_power=500, image=Player.boat_1_image)
        last_frame = time.time()
        time_step = 0

        while True:

            # map image
            self.screen.blit(self.map_image, (0, 0))

            # gestion du temps pour que la vitesse du joueur ne depende pas de la vitesse du processeur
            time_now = time.time()
            time_step = time_now - last_frame
            last_frame = time_now

            # player moves
            if self.pressing_keys[pg.K_z]:
                self.player.set_engine_power(self.player.max_power)
            if self.pressing_keys[pg.K_s]:
                self.player.set_engine_power(-self.player.max_power)
            if not self.pressing_keys[pg.K_z] and not self.pressing_keys[pg.K_s]:
                self.player.set_engine_power(0)
            if self.pressing_keys[pg.K_q]:
                self.player.rotate(-1, time_step)
            if self.pressing_keys[pg.K_d]:
                self.player.rotate(1, time_step)

            self.player.run(time_step)

            # player image
            self.player.display_boat(self.screen)

            # update the screen
            pg.display.flip()

            # check for events
            for event in pg.event.get():

                self.manage_general_events(event)

    def game_over_update(self):  # TODO: create a game over screen
        """Generate the window content when the game is in the game over state
        """

        self.category = Game.CATEGORY_GAME_OVER

        print("\n" * 2 + "\t" * 2 + "~~~ GAME OVER ~~~" + "\n" * 2)

        while True:

            # update the screen
            pg.display.flip()

            # check for events
            for event in pg.event.get():

                self.manage_general_events(event)

    def manage_general_events(self, event):
        """The updates that are common to all the states of the game
        """

        print(time.ctime(), self.pressing_keys)

        # switch the music or the sound effects on/off if the user press the 'm' or 'p' key
        if event.type == pg.KEYDOWN:
            # music
            if event.key == pg.K_m:
                self.music = not self.music
                print(f"|| music {'ON' if self.music else 'OFF'}")
            # sound effects
            if event.key == pg.K_p:
                self.sound = not self.sound
                print(f"|| sound effects {'ON' if self.sound else 'OFF'}")

        # quit the game if the user press the cross
        if event.type == pg.QUIT:
            self.close()

        # change the dict related to the currently inputs
        if self.category == Game.CATEGORY_GAME:
            if event.type == pg.KEYDOWN:
                self.pressing_keys[event.key] = True
            if event.type == pg.KEYUP:
                self.pressing_keys[event.key] = False


    def close(self):
        """Close the game
        """
        print("\n" * 2 + "=" * 73 + "\n" + "=" * 26 + " " * 4 + "GAME  CLOSING" + " " * 4 + "=" * 26 + "\n" + "=" * 73 + "\n" * 2)
        pg.quit()
