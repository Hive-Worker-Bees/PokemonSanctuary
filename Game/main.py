# Import Modules
import os
import pygame
from pygame.locals import *
# import sklearn
from character import player
import sys

# if not pg.font:
#     print("Warning, fonts disabled")
# if not pg.mixer:
#     print("Warning, sound disabled")

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
      
    def load_image(self, filename, x_cord, y_cord):
      image = pygame.image.load(filename).convert()
      image = pygame.transform.scale(image,(x_cord, y_cord))
      return image
 
    def on_init(self):
        # Open a window on the screen
        screen_width=400
        screen_height=400
        self._display_surf = pygame.display.set_mode([screen_width,screen_height])
        pygame.init()
        self.character = player()   # spawn player
        self.character.rect.x = 10   # go to x
        self.character.rect.y = 10  # go to y
        self.player_list = pygame.sprite.Group()
        self.player_list.add(self.character)
        # this is the screen size, initial screen setup
        #self._display_surf = pygame.display.set_mode((400,400), pygame.HWSURFACE)

        self._running = True # is game running

        # this is how you load a Surface object (i.e. an image)
        self._image_surf = self.load_image("assets/sample_map.png", 400, 400)
        # this is how you resize an image
        self._water_tile= self.load_image("assets/water_anim.png", 40, 40)
        
 
    def on_event(self, event): #if we press the X button that quits
        if event.type == QUIT:
            self._running = False
            
    def on_loop(self): #game loop possibly
        pass
        
    def on_render(self):
      # this loads an image onto the surface (you can also load images on top of images)
      # surface_object_to_draw_on.blit(image_to_draw, (x,y)) # (0,0) is top left
        self._display_surf.blit(self._image_surf,(0,0))
        self._display_surf.blit(self._water_tile,(0,0))
        self.player_list.draw(self._display_surf) # draw player
        pygame.display.flip() #changes assets

        
 
    def on_cleanup(self): # Quit 
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        self.character.control(1,1)
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        print('right')
                    if event.key == pygame.K_UP or event.key == ord('w'):
                        print('jump')

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        print('left stop')
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        print('right stop')
                    if event.key == ord('q'):
                        pygame.quit()
                        sys.exit()
            self.on_loop()
            self.on_render()
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App() # runs __init__()
    theApp.on_execute() # runs on_init(), then the game loop


