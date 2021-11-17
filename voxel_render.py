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
        self.screen_array2 = np.full((app.width, app.height, 3), (110, 110, 110))
        
    
    def update(self):
        # Заполнение экрана случайными цветами каждого пиксела. Вариант 1.
        # Медленный способ.
        '''
        x = random.randint(0, self.app.width - 1)
        y = random.randint(0, self.app.height - 1)
        
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color = (r, g, b)        
        self.screen_array[x, y] = color
        '''
        #-------------------------------------------------------------------
        
        # Заполнение экрана случайными цветами каждого пиксела. Вариант 2.
        # Медленный способ(Чуть быстрее первого варианта). FPS = 1
        '''
        n, m = self.app.height, self.app.width
        masScreen = [[random.randint(1, 10) for j in range(m)] for i in range(n)]

        for i in range(0, self.app.height):
            for j in range(0, self.app.width):
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)
                color = (r, g, b)
                masScreen[i][j] = color     
        for i in range(0, self.app.height):
            for j in range(0, self.app.width):
                self.screen_array[j, i] = masScreen[i][j]
        '''
        
        #-------------------------------------------------------------------
        

        # Вариант 3. Заполнение экрана случайными цветами каждого пиксела.
        # FPS = 0.7
        '''
        for i in range(0, self.app.height):
            for j in range(0, self.app.width):
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)
                color = (r, g, b)
        
                pg.draw.circle(self.app.screen, color, (j, i), 1)
        '''
        
        
        # Заполнение экрана случайными цветами каждого пиксела. Вариант 4.
        # Самый быстрый способ. FPS >= 59
        self.screen_array = np.random.randint(0, 255, size = self.screen_array.shape)
        '''
        self.screen_array2 = np.random.randint(0, 255, size = self.screen_array.shape)
        r = self.screen_array2[:, :, 2]
        g = self.screen_array2[:, :, 1]
        b = self.screen_array2[:, :, 0]
        g = (r + g + b) // 3
        self.screen_array2[:, :, 2] = self.screen_array2[:, :, 1] = self.screen_array2[:, :, 0] = g
        '''
        #-------------------------------------------------------------------
        
    
    def draw(self):
        self.app.screen.blit(pg.surfarray.make_surface(self.screen_array), (100, 100))  # Кординаты вывода x = 100 y = 100
        # self.app.screen.blit(pg.surfarray.make_surface(self.screen_array2), (200, 200))
        

        
