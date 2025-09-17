import pygame
from os.path import join
from os import walk
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, bullet_group):
        super().__init__(groups)
        self.load_images()
        self.state, self.frame_index = 'right', 0
        self.image = pygame.image.load(join("images", "player", "down", "0.png")).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.math.Vector2()
        self.speed = 500
        self.bullet_group = bullet_group
        self.shoot_cooldown = 0.25
        self.time_since_last_shot = 0

    def input(self):
        keys = pygame.key.get_pressed()
        
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        if self.direction.length_squared() > 0:
            self.direction = self.direction.normalize() # da ne ode dijagonalno pobrzo
        
        self.shoot(keys)



    def load_images(self):
        self.frames = {'left': [], 'right': [], 'up': [], 'down': []}

        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk(join('images', 'player', state)):
                if file_names:
                    for file_name in sorted(file_names, key= lambda name: int(name.split('.')[0])):
                        full_path = join(folder_path, file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surf)


    def animate(self, dt):
        # get state 
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'

        # animate
        self.frame_index = self.frame_index + 5 * dt if self.direction else 0
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]



    def shoot(self, keys):
        self.time_since_last_shot += self.dt
        if self.time_since_last_shot < self.shoot_cooldown:
            return

        direction = None
        if keys[pygame.K_UP]:
            direction = pygame.math.Vector2(0, -1)
        elif keys[pygame.K_DOWN]:
            direction = pygame.math.Vector2(0, 1)
        elif keys[pygame.K_LEFT]:
            direction = pygame.math.Vector2(-1, 0)
        elif keys[pygame.K_RIGHT]:
            direction = pygame.math.Vector2(1, 0)

        if direction:
            Bullet(self.rect.center, direction, self.bullet_group)
            self.time_since_last_shot = 0

    def move(self, dt):
        self.rect.center += self.direction * self.speed * dt

    def update(self, dt):
        self.dt = dt
        self.input()
        self.move(dt)
        self.animate(dt)
