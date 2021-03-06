import pygame
from pygame.locals import *
import sys
from random import randint
from MapManager import Background

from utils import load_image

from Player import Player
from Pokemon import Pokemon
from TextBox import TextBox
from Combat import Combat
from Start import Start
from PokemonManager import PokemonManager
import MapManager
import db


class App:
    def __init__(self):
        self._running = True
        self.screen = None
        self.map_background = None
        self.state = "start"

    def on_init(self):
        """
        Initialises and opens a new Pygame window
        """
        # Initialise module
        pygame.init()

        # Initialise sound module
        self.playing_music = True
        pygame.mixer.music.load("assets/audio/background.mp3")
        pygame.mixer.music.play(-1)

        # Set window width and height
        self.screen = pygame.display.set_mode([400, 500])

        # Generate start object
        self.start = Start(self.screen)

        # Generate textbox
        self.textbox = TextBox(self.screen)
        self.textbox.set_text("I gotta catch them all")

        # Generate player
        self.player = Player()
        self.player_list = pygame.sprite.Group()
        self.player_list.add(self.player)

        # Set initial player position
        self.player.rect.x = 200  # go to x
        self.player.rect.y = 140  # go to y

        # Set up Pokemon
        self.pokemon = None
        self.pokemon_list = pygame.sprite.Group()
        self.pokemon_manager = PokemonManager()

        # Set up map
        self.map = MapManager.get_first_map()
        self.map_background = load_image(self.map.get_image(), 400, 400)

        # Control the game loop
        self._running = True

        # Hide default mouse cursor
        pygame.mouse.set_visible(False)

        # Initialise custom cursor
        self.cursor = load_image("assets/images/cursor1.png", 20, 20)

    def on_event(self, event):
        # Closing the window (with the X) ends the game
        if event.type == QUIT:
            self._running = False

        if self.state == "start":
            if event.type == KEYDOWN:
                self.start.finished = True
                self.textbox = TextBox(self.screen)

        # Handle mouse clicks
        if event.type == MOUSEBUTTONDOWN:
            # Check if an interesting region has been clicked
            is_interesting_region = self.map.is_interesting_region(event.pos[0], event.pos[1])
            if is_interesting_region:
                # Display information in text box
                lines = is_interesting_region.split("/n")
                count = 1
                for line in lines:
                    self.textbox.set_text(line, count)
                    count += 1
                count = 1
            else:
                # Clear information in text box
                self.textbox.set_text("")

            # Check if a Pokemon has been clicked
            if self.pokemon:
                pokemon_x = self.pokemon.rect.x
                pokemon_y = self.pokemon.rect.y
                if pokemon_x < event.pos[0] < pokemon_x + 30 and pokemon_y < event.pos[1] < pokemon_y + 30:
                    # A Pokemon was clicked, so open the combat screen
                    self.state = "combat"
                    self.combat = Combat(self.screen, self.player, self.pokemon, self.pokemon_manager)
                    # Remove the Pokemon
                    self.pokemon = None
                    self.pokemon_list.empty()

        # Handle a keypress starting
        steps = 1
        if event.type == pygame.KEYDOWN:
            # Detect left key or "a" key
            if pygame.key.get_pressed()[pygame.K_LEFT] or event.key == ord("a"):
                # Move player left
                self.player.set_x_velocity(-steps)
            # Detect right key or "d" key
            if event.key == pygame.K_RIGHT or event.key == ord("d"):
                # Move player right
                self.player.set_x_velocity(steps)
            # Detect up key or "w" key
            if event.key == pygame.K_UP or event.key == ord("w"):
                # Move player up
                self.player.set_y_velocity(-steps)
            # Detect down key or "s" key
            if event.key == pygame.K_DOWN or event.key == ord("s"):
                # Move player down
                self.player.set_y_velocity(steps)
            # Redraw GUI
            pygame.display.flip()

        # Handle a keypress ending
        if event.type == pygame.KEYUP:
            if self.state == "combat":
                if event.key == ord("a"):
                    self.combat.player_attack("attack")
                elif event.key == ord("d"):
                    self.combat.player_attack("defend")
            # Detect if the player was moving left or right
            if event.key == pygame.K_LEFT or event.key == ord("a") or event.key == pygame.K_RIGHT or event.key == ord("d"):
                # Stop player moving left or right
                self.player.set_x_velocity(0)
            # Detect if the player was moving up or down
            if event.key == pygame.K_UP or event.key == ord("w") or event.key == pygame.K_DOWN or event.key == ord("s"):
                # Stop player moving up for down
                self.player.set_y_velocity(0)
            # Detect if the "q" key was released
            if event.key == ord("q"):
                # Quit the game
                pygame.quit()
                sys.exit()

            if event.key == ord("m"):
                # Mute/Unmute
                if self.playing_music:
                    pygame.mixer.music.pause()
                    self.playing_music = False
                else:
                    pygame.mixer.music.unpause()
                    self.playing_music = True


    def on_loop(self):
        """
        Defines what actions should happen each game tick
        """
        # Redraw player at their current location
        self.player.update()

        # Detect if player has entered a disallowed region
        if self.map.is_disallowed_region(self.player.rect.x, self.player.rect.y):
            # Prevent movement
            if self.player.velocity_x == 1:
                self.player.rect.x -= 1
            if self.player.velocity_x == -1:
                self.player.rect.x += 1
            if self.player.velocity_y == 1:
                self.player.rect.y -= 1
            if self.player.velocity_y == -1:
                self.player.rect.y += 1

        # Detect if player has entered a dangerous region
        if self.map.is_danger_region(self.player.rect.x, self.player.rect.y):
            # Kill player
            self.player.dead = True
        self.on_player_death()

        
        # print(self.map.get_name())
        # Detect if player should enter the sanctuary
        if self.map.get_name() == "Spawn" and 180 < self.player.rect.x < 230 and 110 < self.player.rect.y < 130:
            # print("Nppp")
            # input()
            self.map = Background(
                    "Pokemon Sanctuary",
                    "assets/images/maps/sanctuary.png",
                    [
                        [70, 100],
                        [95, 135], # Pokemon spawns - chairs?
                        [120, 120],
                        []

                    ],
                    [], # Interesting
                    [   [50, 0, 350, 0],
                        [350, 300, 50, 0]
                        ], # Disallowed
                    [] # Danger
                )
            self.map.set_beneath(MapManager.spawn, 150, 230)
            self.on_map_change()
            self.player.rect.x = 200
            self.player.rect.y = 200

        # Redraw Pokemon at their current position if they exist
        if self.pokemon_list:
            self.pokemon.update()

        # Detect if player should enter next zone to the left
        if self.player.rect.x == 0 and self.map.get_left() and self.map.get_left_bounds()[0] < self.player.rect.y < self.map.get_left_bounds()[1]:
            self.map = self.map.get_left()
            self.on_map_change()
            self.player.rect.x = 390 - self.player.rect.x
        elif self.player.rect.x < 0:
            self.player.rect.x = 0
            if self.map.get_left_bounds() and self.map.get_left_bounds()[0] < self.player.rect.y < self.map.get_left_bounds()[1]:
                self.textbox.set_text("We shouldn't go too far away.")
        # Detect if player should enter next zone to the right
        if self.player.rect.x == 395 and self.map.get_right() and self.map.get_right_bounds()[0] < self.player.rect.y < self.map.get_right_bounds()[1]:
            self.map = self.map.get_right()
            self.on_map_change()
            self.player.rect.x = 10
        elif self.player.rect.x > 395:
            self.player.rect.x = 395
            if self.map.get_right_bounds() and self.map.get_right_bounds()[0] < self.player.rect.y < self.map.get_right_bounds()[1]:
                self.textbox.set_text("We shouldn't go too far away.")
        # Detect if player should enter next zone at the top
        if self.player.rect.y == 0 and self.map.get_above() and self.map.get_above_bounds()[0] < self.player.rect.x < self.map.get_above_bounds()[1]:
            self.map = self.map.get_above()
            self.on_map_change()
            self.player.rect.y = 380
        elif self.player.rect.y < 0:
            self.player.rect.y = 0
            if self.map.get_above_bounds() and self.map.get_above_bounds()[0] < self.player.rect.x < self.map.get_above_bounds()[1]:
                self.textbox.set_text("We shouldn't go too far away.")
        # Detect if player should enter next zone at the bottom
        if self.player.rect.y == 215 and self.map.get_beneath() and 155<self.player.rect.x<200 and self.map.get_name()=="Pokemon Sanctuary":
            self.map = self.map.get_beneath()
            self.on_map_change()
            self.player.rect.y = 130
            self.player.rect.x = 200
        if self.player.rect.y == 385 and self.map.get_beneath() and self.map.get_beneath_bounds()[0] < self.player.rect.x < self.map.get_beneath_bounds()[1]:
            self.map = self.map.get_beneath()
            self.on_map_change()
            self.player.rect.y = 10
        elif self.player.rect.y > 385:
            self.player.rect.y = 385
            if self.map.get_beneath_bounds() and self.map.get_beneath_bounds()[0] < self.player.rect.x < self.map.get_beneath_bounds()[1]:
                self.textbox.set_text("We shouldn't go too far away.")

    def on_render(self):
        """
        Renders the GUI
        """
        # Render exploring screen
        if self.state == "exploring":
            # Draw map background
            self.screen.blit(self.map_background, (0, 0))
            # Draw player
            self.player_list.draw(self.screen)
            # Draw Pokemon
            self.pokemon_list.draw(self.screen)
        elif self.state == "combat":
            if self.combat.finished:
                # Wait 2 seconds after end of combat to change states
                pygame.time.wait(2000)
                # Reset textbox after combat
                self.textbox = TextBox(self.screen)
                # Change state to exploring
                self.state = "exploring"
                if self.combat.dead:
                    self.player.dead = True
                return
            # Draw combat background
            self.screen.blit(self.combat.combat_surface, (0, 0))
            # Run combat
            self.combat.update_combat()
        elif self.state == "start":
            if self.start.finished:
                self.textbox = TextBox(self.screen)
                self.textbox.set_text("Welcome to Pokemon Sanctuary")
                # Change state back to exploring
                self.state = "exploring"
                return
            # Draw start background
            self.screen.blit(self.start.start_surface, (0, 0))
            self.textbox.set_text("Press Anything to Start")

        # Draw mouse custom cursor
        if pygame.mouse.get_pos()[1] < 385:
            self.screen.blit(self.cursor, pygame.mouse.get_pos())

        # Redraw GUI
        pygame.display.flip()

    def on_map_change(self):
        """
        Defines what actions should happen after the map zone changes
        """
        # Load new map image
        self.map_background = load_image(self.map.get_image(), 400, 400)
        # Delete all Pokemon in previous zone
        self.pokemon_list.empty()
        # Possibly spawn new Pokemon
        if randint(0, 4) == 0:
            new_pokemon = self.pokemon_manager.get_random_available_pokemon()
            if new_pokemon:
                coords = self.map.get_random_pokemon_spawn()
                self.pokemon = Pokemon(new_pokemon)
                self.pokemon.rect.x = coords[0]
                self.pokemon.rect.y = coords[1]
                self.pokemon_list.add(self.pokemon)
                # Display text message
                analyse = db.analyse(self.pokemon.data.get_id())
                self.textbox.set_text(analyse[0])
                self.textbox.set_text(analyse[1], 2)
                self.textbox.set_text(analyse[2], 3)
        else:
            self.textbox.set_text("")

    def on_player_death(self):
        """
        Handle a player death
        """
        if self.player.dead:
            self.player_list.empty()
            pygame.mixer.music.pause()
            self.on_render()
            self.textbox.set_text("You died.")
            # Respawn after 5 seconds
            pygame.time.delay(5000)
            self.on_init()

    def on_cleanup(self):
        """
        Defines what actions should happen after the game loop ends
        """
        # Quit game
        pygame.quit()

    def on_execute(self):
        """
        Defines what should happen in the game execution sequence
        """
        # Wait for intialisation before running program
        if self.on_init() is False:
            self._running = False

        # Start game loop
        while self._running:
            # Handle events
            for event in pygame.event.get():
                self.on_event(event)
            # Do set tasks on each loop
            self.on_loop()
            self.on_render()
        # Do tasks after game loop
        self.on_cleanup()


# Start App
if __name__ == "__main__":
    app = App()
    app.on_execute()
