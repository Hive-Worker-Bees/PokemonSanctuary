import pygame
from pygame.locals import *
import sys

from utils import load_image
from Combat import Combat
from Explore import Explore

class App:
    def __init__(self):
        self._state = None
        self._windows = [Explore(self), Combat(self)]

        self.change_state(0)

    def change_state(self, state):
        """
        Update the state of the app (essentially changes the window displayed)
        """
        # Set new state
        self._state = state

        # Set all methods to methods belonging to window
        self.on_init = self._windows[state].on_init
        self.on_event = self._windows[state].on_event
        self.on_loop = self._windows[state].on_loop
        self.on_render = self._windows[state].on_render
        self.on_cleanup = self._windows[state].on_cleanup
        self.on_execute = self._windows[state].on_execute

        # Restart game loop
        self._running = False
        self.on_execute()
        
    def receive_data(self, data):
        """
        Receives data from a window so data can be transferred between windows
        """
        self.data = data

    def on_init(self):
        """
        Initialises and opens a new Pygame window
        """
        # Initialise module
        pygame.init()

        # Set window width and height
        self.screen = pygame.display.set_mode([400, 500])

        # Control the game loop
        self._running = True

    def on_event(self, event):
        # Closing the window (with the X) ends the game
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        # Redraw GUI
        pygame.display.flip()

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
