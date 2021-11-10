import pygame as pg
from player import Player

class App:
    def __init__(self):
        pass
        
    def update(self):
        pass
        
    def draw(self):
        pass
        
    def run(self):
        while True:
            self.update()
            self.draw()
            
        [exit() for i in pg.event.get() if i.type == pg.QUIT]
        self.clock.tick(60)
        pg.display.set_caption(f'FPS: {self.clock.get_fps()}')
        
if __name__ == '__main__':
    app = App()
    app.run()
