import pygame
from pygame.locals import *
import random

from utils import load_image, render_text


class Combat():
    """
    Controls the combat functionality in the game
    """

    def __init__(self, parent):
        self.parent = parent

    def update_combat(self):
        """
        Redraws combat GUI
        """
        # Enemy Sprite
        self.screen.blit(load_image(self.enemy.data.get_down_walk_sprite().get_frame_1().get_path(), 125, 125), (50, 10))
        # Player HP
        self.screen.blit(render_text(f"{str(self.player.hp)}/{str(self.player.max_hp)}"), (100, 320))
        # Enemy HP
        self.screen.blit(render_text(f"{str(self.enemy.hp)}/{str(self.enemy.max_hp)}"), (260, 60))
        # Combat Text
        self.screen.blit(render_text(self.combat_text()), (40, 400))
        # Make Update
        pygame.display.update()

    def take_turn(self):
        """
        Control turn taking between the player and enemy
        """
        acc = random.randint(0, 100)
        if acc < 80:
            self.enemy.hp -= 5

        acc = random.randint(0, 100)
        if acc < 60:
            self.player.hp -= 2

    def combat_text(self):
        """
        Control the text displayed on the combat screen
        """
        if self.player.hp > 0 and self.enemy.hp > 0:
            return "Mash Space to see who wins!!"
        elif self.player.hp <= 0:
            self.finished = True
            return f"{self.enemy.data.getName()} wins!"
        elif self.enemy.hp <= 0:
            self.finished = True
            return "The Trainer wins!"

    def finish(self):
        pygame.time.delay(2000)
        self.parent.change_state(0)

    def on_init(self):
        """
        Initialises and opens a new Pygame window
        """
        # Initialise module
        pygame.init()

        # Await end of combat
        self.finished = False

        # Set window width and height
        self.screen = pygame.display.set_mode([400, 500])

        # Set background
        self.combat_surface = load_image("assets/images/battle_bg.png", 400, 500)

        # Get player and enemy data from parent
        self.player = self.parent.data[0]
        self.enemy = self.parent.data[1]

        # Draw GUI
        self.update_combat()

        # Control the game loop
        self._running = True

    def on_event(self, event):
        # Closing the window (with the X) ends the game
        if event.type == QUIT:
            self._running = False

        # Detect spacebar being pressed
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            # Make turn in combat
            self.take_turn()

    def on_loop(self):
        pass

    def on_render(self):
        # Redraw GUI
        pygame.display.flip()

        # Draw combat background
        self.screen.blit(self.combat_surface, (0, 0))
        # Run combat
        self.update_combat()

        # Check for finish
        if self.finished:
            self.finish()

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