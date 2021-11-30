import pygame as pg
import numpy as np
from numba import njit
import math
import random

height_map_img = pg.image.load('img/height_map.jpg')
height_map = pg.surfarray.array3d(height_map_img)

color_map_img = pg.image.load('img/color_map.jpg')
color_map = pg.surfarray.array3d(color_map_img)

'''
@njit(fastmath=True) # Увеличивает скорость выполнения многократно.
def ray_casting(screen_array, screen_width, screen_height):
    
    screen_array[:] = np.array([0, 0, 0])
    for y in range(0, screen_height - 1):
        for x in range(0, screen_width - 1):
            screen_array[x, y] = color_map[x, y]
    
    # screen_array = np.random.randint(0, 255, size = screen_array.shape)
    return screen_array
'''

map_height = len(height_map[0])
map_width  = len(height_map)
            
@njit(fastmath=True) # Увеличивает скорость выполнения многократно.
def ray_casting(screen_array, player_pos, player_angle, player_height, player_pitch, screen_width, screen_height, delta_angle, ray_distance, h_fov, scale_height):
    
    screen_array[:] = np.array([0, 0, 0])
    y_buffer = np.full(screen_width, screen_height)
    ray_angle = player_angle - h_fov
    for num_ray in range(screen_width):
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)
        first_contact = False
        
        for depth in range(1, ray_distance):
            x = int(player_pos[0] + cos_a * depth)
            if(0 < x < map_width):
                y = int(player_pos[1] + sin_a * depth)
                if(0 < y < map_height):
                    depth *= math.cos(player_angle - ray_angle)
    
    
    
        
        
        
        ray_angle = ray_angle + delta_angle
    
    
    for y in range(0, screen_height - 1):
        for x in range(0, screen_width - 1):
            screen_array[x, y] = color_map[x, y]
    
    return screen_array



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
        self.screen_array = np.full((app.width - 500, app.height - 200, 3), (0, 0, 0))
        self.screen_array2 = np.full((app.width, app.height, 3), (110, 110, 110))
        self.screen_array3 = np.full((app.width, app.height, 3), (0, 0, 0))
        
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
        # Цветной шум  FPS >= 59
        self.screen_array = np.random.randint(0, 255, size = self.screen_array.shape)
        
        
        # Черно-белый шум  FPS = 40
        self.screen_array2 = np.random.randint(0, 255, size = self.screen_array2.shape)
        # Быстрый способ преобразования. Цветные значения превращаем в черно-белые значения
        self.screen_array2[:, :, 0] = (self.screen_array2[:, :, 2] + self.screen_array2[:, :, 1] + self.screen_array2[:, :, 0]) // 3
        self.screen_array2[:, :, 1] = self.screen_array2[:, :, 0]
        self.screen_array2[:, :, 2] = self.screen_array2[:, :, 0]
        
        '''
        # Медленный способ преобразования каждого элемента(элемент для цветного пиксела в черно-белый).
        for y in range(0, self.app.width):
            for x in range(0, self.app.height):
                # for c in range(0, 3):
                r = self.screen_array2[y, x, 0]
                g = self.screen_array2[y, x, 1]
                b = self.screen_array2[y, x, 2]
                g = (r + g + b) // 3
                self.screen_array2[y, x, 0] = g
                self.screen_array2[y, x, 1] = g
                self.screen_array2[y, x, 2] = g
        '''

        
        #-------------------------------------------------------------------
        self.screen_array = ray_casting(self.screen_array, self.player.pos, self.player.angle, self.player.height, self.player.pitch, self.app.width, self.app.height, self.delta_angle, self.ray_distance, self.h_fov, self.scale_height)
        
    
    def draw(self):
        self.app.screen.blit(pg.surfarray.make_surface(self.screen_array), (0, 0))       # Цветной шум. Кординаты вывода x = 0 y = 0
        self.app.screen.blit(pg.surfarray.make_surface(self.screen_array2), (450, 0))    # Черно-белый шум.
        self.app.screen.blit(pg.surfarray.make_surface(self.screen_array3), (250, 100))  # Рендеринг изображения.
        

        
