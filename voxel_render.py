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
                    height_on_screen = int((player_height - height_map[x, y][0]) / depth * scale_height + player_pitch)
                    
                    if not first_contact:
                        y_buffer[num_ray] = min(height_on_screen, screen_height)
                        first_contact = True
                        
                    if height_on_screen < 0:
                        height_on_screen = 0
                        
                    if height_on_screen < y_buffer[num_ray]:
                        for screen_y in range(height_on_screen, y_buffer[num_ray]):
                            screen_array[num_ray, screen_y] = color_map[x, y]
                        y_buffer[num_ray] = height_on_screen    
        
        
        ray_angle = ray_angle + delta_angle
    return screen_array
    '''
    for y in range(0, screen_height - 1):
        for x in range(0, screen_width - 1):
            screen_array[x, y] = color_map[x, y]
    
    return screen_array
    '''


@njit(fastmath=True) # Увеличивает скорость выполнения многократно.
def ray_casting_object(screen_array, object_pos, player_pos, player_angle, player_height, player_pitch, screen_width, screen_height, delta_angle, ray_distance, h_fov, scale_height):
    
    # object_to_screen_1 = np.array([0, 0], dtype = float)
    # screen_array[:] = np.array([0, 0, 0])
    # y_buffer = np.full(screen_width, screen_height)
    ray_angle = player_angle - h_fov
    
    flagBreak = False
    numRayRet = -1000
    deltaRet = -1000
    
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
                    # height_on_screen = int((player_height - height_map[x, y][0]) / depth * scale_height + player_pitch)
                    if((int(object_pos[0]) == int(x)) and (int(object_pos[1]) == int(y))):
                        # object_to_screen_1[0] = num_ray
                        # object_to_screen_1[1] = screen_height // 2
                        '''
                        for screen_x in range(int((num_ray - 50) / depth), int((num_ray + 50) / depth)):
                            for screen_y in range(screen_height // 2 - 5, screen_height // 2 + 5):
                                screen_array[screen_x, screen_y] = (100, 200, 255)
                        '''        
                        flagBreak = True
                        deltaRet = depth
                        break
                    '''
                    if not first_contact:
                        y_buffer[num_ray] = min(height_on_screen, screen_height)
                        first_contact = True
                        
                    if height_on_screen < 0:
                        height_on_screen = 0
                        
                    if height_on_screen < y_buffer[num_ray]:
                        for screen_y in range(height_on_screen, y_buffer[num_ray]):
                            screen_array[num_ray, screen_y] = color_map[x, y]
                        y_buffer[num_ray] = height_on_screen    
                    '''
        if flagBreak == True:
            numRayRet = num_ray
            break
        ray_angle = ray_angle + delta_angle
    # return object_to_screen
    # return screen_array
    return numRayRet, deltaRet
    



class VoxelRender:
    def __init__(self, app):
        self.app = app
        self.player = app.player
        self.fov = math.pi / 3
        self.h_fov = self.fov / 2
        self.num_rays = app.width
        self.delta_angle = self.fov / self.num_rays
        self.ray_distance = 2000
        self.scale_height = 620
        self.screen_array = np.full((app.width, app.height, 3), (0, 0, 0))
        # self.screen_array2 = np.full((300, 200, 3), (110, 110, 110))
        self.screen_array2 = np.full((app.width, app.height, 3), (110, 110, 110))
        # self.screen_array3 = np.full((app.width, app.height, 3), (0, 0, 0))
        
        self.object_1 = np.array([0, 0], dtype = float)
        self.object_1[0] = 0
        self.object_1[1] = 0
        self.x_o = 150
        self.y_o = 50
        
        self.dx = 1.2
        self.dy = 1.2
        
        self.x_object = 0
        self.deltaToObject = 0
        
        
        
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
        # self.screen_array = np.random.randint(0, 255, size = self.screen_array.shape)
        
        
        showBackScreen = 0;
        if random.randint(0, 2000) < 200:
            # Имитируем помехи на экране заднего вида
            showBackScreen = 0
            # Черно-белый шум  FPS = 40
            self.screen_array2 = np.random.randint(0, 255, size = self.screen_array2.shape)
            
            # Быстрый способ преобразования. Цветные значения превращаем в черно-белые значения
            self.screen_array2[:, :, 0] = (self.screen_array2[:, :, 2] + self.screen_array2[:, :, 1] + self.screen_array2[:, :, 0]) // 3
            self.screen_array2[:, :, 1] = self.screen_array2[:, :, 0]
            self.screen_array2[:, :, 2] = self.screen_array2[:, :, 0]
        else:
            # Показываем экран заднего вида без помех
            showBackScreen = 1
            
        
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
        
        # Камера заднего вида
        if showBackScreen == 1:
            self.screen_array2 = ray_casting(self.screen_array2, self.player.pos, self.player.angle - math.pi, self.player.height, self.player.pitch, self.app.width, self.app.height, self.delta_angle, self.ray_distance, self.h_fov, self.scale_height)
        
        
        
        print('self.player.pos: x = ' + str(self.player.pos[0]) + '  y = ' + str(self.player.pos[1]) + '  angle = ' + str(self.player.angle))
        print('  self.object_1: x = ' + str(self.object_1[0]) + '  y = ' + str(self.object_1[1]))
        print('  ==self.x_object_to_screen: x = ' + str(self.x_object))
        print('  ==self.deltaToObject = ' + str(self.deltaToObject))
        
        # Рисуем движущийся объект
        # self.object_1[0] = int(self.x_o)
        # self.object_1[1] = int(self.y_o)
        self.object_1[0] = int(self.x_o)
        self.object_1[1] = int(self.y_o)
        
        if self.x_o > self.app.width:
            self.dx = -self.dx
        if self.x_o < 0:
            self.dx = -self.dx
            
        self.x_o = self.x_o + self.dx
            
        
        if self.y_o > 400:
            self.dy = -self.dy
        if self.y_o < 0:
            self.dy = -self.dy

        self.y_o = self.y_o + self.dy
        
        self.x_object, self.deltaToObject = ray_casting_object(self.screen_array, self.object_1, self.player.pos, self.player.angle, self.player.height, self.player.pitch, self.app.width, self.app.height, self.delta_angle, self.ray_distance, self.h_fov, self.scale_height)
        
    def draw(self):
        self.app.screen.blit(pg.surfarray.make_surface(self.screen_array), (0, 0))       # Цветной шум. Кординаты вывода x = 0 y = 0
        back_screen = pg.surfarray.make_surface(self.screen_array2)
        back_screen = pg.transform.scale(back_screen, (200, 150))
        # self.app.screen.blit(pg.surfarray.make_surface(self.screen_array2), (0, 250))    # Черно-белый шум.
        self.app.screen.blit(back_screen, (50, 250))    # Черно-белый шум.
        
        # Вывод объекта
        if self.deltaToObject > 0:
            pg.draw.circle(self.app.screen,(255, 255, 0), (self.x_object, 250), self.app.width // 3 - self.deltaToObject)
        
        # self.app.screen.blit(pg.surfarray.make_surface(self.screen_array3), (250, 100))  # Рендеринг изображения.
        

        
