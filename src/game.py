from time import time as t
import pygame as pg
import pygame_widgets as pgw
from pygame_widgets.slider import Slider

from src.boat import Boat
from src.physics import Pos, Speed
from src.player import Player
from src.terrainGen import GenerateMap, ColorMap


class Game:
    """General class for the game, which generates and displays all the elements in each state of the game
    """

    def __init__(self, screen_width: int, screen_height: int) -> None:
        """Create the pygame window and initialize the main settings of the game

        Args:
            screen_width (int): the width of the window
            screen_height (int): the height of the window
        """

        # screen size
        self.screen_width, self.screen_height = screen_width, screen_height
        self.screen_size = (self.screen_width, self.screen_height)

        # window creation
        pg.init()
        self.screen = pg.display.set_mode(self.screen_size)
        pg.display.set_icon(pg.image.load('assets/images/icon.png'))
        pg.display.set_caption('Battleship')

        # main settings
        self.running = True
        self.music = True
        self.sound = True

        # input gestion
        useful_keys = [pg.K_z, pg.K_q, pg.K_s, pg.K_d, pg.K_UP, pg.K_LEFT, pg.K_DOWN, pg.K_RIGHT, pg.K_SPACE]
        self.pressing_keys = {key: False for key in useful_keys}

    def run(self) -> None:
        """Manages the loop of the different states of the game to chain the games
        The 3 states of the game :
            menu (choose settings and make connection then press play),
            game (the map with all the elements and the control of our personal boat),
            game over (the last game screen with omni visibility and a filter as background,
                       resume of the game stats, and a button to go back to the menu)
        """
        while self.game_over_update(self.game_update(self.menu_update())): pass

    def menu_update(self) -> int:
        """Generate the window content when the game is in the menu state

        Returns:
            int: 0 if the user has closed the game, 1 if he presses the play button
        """

        background = pg.transform.scale(pg.image.load('assets/images/menu_background.png'), self.screen_size)

        play_button = pg.transform.scale(pg.image.load('assets/images/start_button.png'),
                                         (int(self.screen_width / 2), int(self.screen_height / 6.5)))
        play_button_place = (int(self.screen_width / 4.25), int(self.screen_height / 1.41))
        play_button_rect = play_button.get_rect()
        play_button_rect.x, play_button_rect.y = play_button_place

        temp = [int(self.screen_width / 10), int(self.screen_width / 5.4), int(self.screen_width / 54)]
        slider_labels_font = pg.font.SysFont('monospace', 15, 1)  # TODO: Maybe make a file with all fonts
        # TODO: between 0 and 0.270 with a step of 0.018
        sea_level_label = slider_labels_font.render('Islands Quantity :', True, (0, 0, 0))
        sea_level_slider = Slider(self.screen, temp[0], int(self.screen_height / 1.97), temp[1], temp[2], min=0, max=28,
                                  step=2)
        # TODO: between 0 and 0.1092 with a step of 0.00728
        sand_height_label = slider_labels_font.render('Beaches Size :', True, (0, 0, 0))
        sand_height_slider = Slider(self.screen, temp[0], int(self.screen_height / 1.53), temp[1], temp[2], min=0,
                                    max=14, step=1)
        del temp

        labels_x_pos = int(self.screen_width / 11)
        sea_level_label_x_pos = int(self.screen_height * 0.489 - 15)
        sand_height_label_x_pos = int(self.screen_height * 0.635 - 15)

        start = False
        while not start:

            # apply background image scaled to the screen size
            self.screen.blit(background, (0, 0))

            # apply the sea and sand level labels
            self.screen.blit(sea_level_label, (labels_x_pos, sea_level_label_x_pos))
            self.screen.blit(sand_height_label, (labels_x_pos, sand_height_label_x_pos))

            # apply the start button
            self.screen.blit(play_button, play_button_place)

            # check for events
            events = pg.event.get()
            for event in events:

                if self.manage_general_events(event):
                    return 0

                if event.type == pg.MOUSEBUTTONDOWN:
                    if play_button_rect.collidepoint(event.pos):
                        start = True
                        #todo afficher un mask noir quazi transparent

                        # update the screen
            pgw.update(events)
            pg.display.flip()

        # TODO 0.255 - sea_level_slider.getValue()
        self.sea_level = 30 - sea_level_slider.getValue() + 130
        # TODO 0.00728 + sea_level_hand.getValue()
        self.sand_level = sand_height_slider.getValue() + 1

        # map generation
        self.map_data = GenerateMap(self.screen_size)

        # map image generation
        self.map_image = pg.surfarray.make_surface(
            ColorMap(self.map_data).get_color_map_array(self.sea_level, self.sand_level))

        return 1

    def game_update(self, running: int) -> int:
        """Generate the window content when the game is in the game state

        Args:
            running (int): 0 if the user has closed the game, 1 if he has pressed the play button

        Returns:
            int: 0 if the user has closed the game, 1 if the game is over
        """

        if not running: return 0

        # player
        player = Player(self.screen, Pos(self.screen_width / 2, self.screen_height / 2), Speed(0, 0),
                        mass=10, max_power=1000, boat_image=Player.boat_1_image)

        # enemy
        enemy = Boat(self.screen, Pos(self.screen_width / 4, self.screen_height / 2), Speed(0, 0),
                     mass=10, max_power=1000, boat_image=Player.boat_2_image)

        # create boat and bullet groups
        boat_group = pg.sprite.Group()
        bullet_group = pg.sprite.Group()

        boat_group.add(player)
        boat_group.add(enemy)

        last_frame = t()

        over = False
        while not over:

            # map image
            self.screen.blit(self.map_image, (0, 0))

            # gestion du temps pour que la vitesse du joueur ne depende pas de la vitesse du processeur
            time_now = t()
            time_step = time_now - last_frame
            last_frame = time_now

            # print fps
            font = pg.font.Font(None, 24)
            fps_value = 0
            if time_step != 0:
                fps_value = 1/time_step
            text = font.render("FPS: " + str(int(fps_value)), 1, (255, 255, 255))
            self.screen.blit(text, (0, 0))

            # print speed
            font = pg.font.Font(None, 24)
            speed_value = player.dot.speed.get_norm()
            text = font.render("Speed: " + str(int(speed_value)), 1, (255, 255, 255))
            self.screen.blit(text, (0, 20))

            # print height
            font = pg.font.Font(None, 24)
            height_value = player.get_height_level(self.map_data)
            text = font.render("Height: " + str(int(height_value)), 1, (255, 255, 255))
            self.screen.blit(text, (0, 40))

            # player moves
            # engine
            if self.pressing_keys[pg.K_z] or self.pressing_keys[pg.K_UP]:
                player.set_engine_power(player.max_power)
            if self.pressing_keys[pg.K_s] or self.pressing_keys[pg.K_DOWN]:
                player.set_engine_power(-player.max_power)
            elif not (self.pressing_keys[pg.K_z] or self.pressing_keys[pg.K_UP] or self.pressing_keys[pg.K_s] or
                      self.pressing_keys[pg.K_DOWN]):
                player.set_engine_power(0)

            # rotate
            if self.pressing_keys[pg.K_q] or self.pressing_keys[pg.K_LEFT]:
                player.rotate(-1, time_step, self.map_data, self.sea_level)
            if self.pressing_keys[pg.K_d] or self.pressing_keys[pg.K_RIGHT]:
                player.rotate(1, time_step, self.map_data, self.sea_level)

            player.run(time_step, self.map_data, self.sea_level)

            # bullets moves
            for bullet in bullet_group:
                bullet.run(time_step)
                # todo check collisions

            # player health
            player.display_health()
            enemy.display_health()

            boat_group.draw(self.screen)
            bullet_group.draw(self.screen)

            # update the screen
            pg.display.flip()

            # check for events
            for event in pg.event.get():

                if self.manage_general_events(event):
                    return 0

                # manage pressed keys
                if event.type == pg.KEYDOWN and event.key in self.pressing_keys.keys():
                    self.pressing_keys[event.key] = True
                if event.type == pg.KEYUP and event.key in self.pressing_keys.keys():
                    self.pressing_keys[event.key] = False

                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == pg.BUTTON_LEFT:
                        bullet_group.add(player.fire(True))
                    if event.button == pg.BUTTON_RIGHT:
                        bullet_group.add(player.fire(False))

        return 1

    def game_over_update(self, running: int) -> int:  # TODO: create a game over screen
        """Generate the window content when the game is in the game over state

        Args:
            running (int): 0 if the user has closed the game, 1 if the game is over

        Returns:
            int: 0 if the user has closed the game, 1 if he presses the space bar
        """

        if not running: return 0

        return_to_menu = False
        while not return_to_menu:

            # update the screen
            pg.display.flip()

            # check for events
            for event in pg.event.get():

                if self.manage_general_events(event):
                    return 0

        return 1

    def manage_general_events(self, event: pg.event.Event) -> bool:
        """The updates that are common to all the states of the game
        """

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
            return True

        return False

    def close(self):
        """Close the game
        """
        pg.quit()
