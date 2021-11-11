import pygame as pg
import numpy as np
from numba import njit
import math
import random

class VoxelRender:
    def __init__(self, app):
        self.app = app
        self.player = app.player
        self.fov = math.pi /3
        self.h_fov = self.fov / 2
        self.num_rays = app.width
        self.delta_angle = self.fov / self.num_rays
        self.ray_distance = 2000
        self.scale_height = 620
        self.screen_array = np.full((app.width, app.height, 3), (0, 0, 0))
        
    
    def update(self):
        # Заполнение экрана случайными цветами случайно выбранного пиксела. Вариант 1.
        # Медленный способ.
        x = random.randint(0, self.app.width - 1)
        y = random.randint(0, self.app.height - 1)
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color = (r, g, b)        
        self.screen_array[x, y] = color
        #-------------------------------------------------------------------
        
        # Заполнение экрана случайными цветами случайно выбранного пиксела. Вариант 2.
        # Быстрый способ.
        self.screen_array = np.random.randint(0, 255, size = self.screen_array.shape)
        #-------------------------------------------------------------------
        
    
    def draw(self):
        self.app.screen.blit(pg.surfarray.make_surface(self.screen_array), (0, 0))
        
