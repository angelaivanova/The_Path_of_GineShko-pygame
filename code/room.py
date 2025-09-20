# room.py
import pygame
from enemy import Enemy
import random
from power import PowerUp

DOOR_SIZE = 60
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800

class Room:

    DOOR_WIDTH = 20  # thickness of the door
    DOOR_HEIGHT = 100  # length of the door
    def __init__(self, color, pos):
        self.color = color
        self.pos = pos
        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT
        self.visited = False
        self.sprites = pygame.sprite.Group()
        self.doors = {}


    def update_doors(self, rooms_dict):
        cx, cy = self.pos
        self.doors = {}
        neighbors = {
            "up": (cx, cy - 1),
            "down": (cx, cy + 1),
            "left": (cx - 1, cy),
            "right": (cx + 1, cy)
        }
        for direction, npos in neighbors.items():
            if npos in rooms_dict:
                if direction == "up":
                    rect = pygame.Rect(self.width // 2 - self.DOOR_HEIGHT // 2, 0,
                                       self.DOOR_HEIGHT, self.DOOR_WIDTH)
                elif direction == "down":
                    rect = pygame.Rect(self.width // 2 - self.DOOR_HEIGHT // 2,
                                       self.height - self.DOOR_WIDTH, self.DOOR_HEIGHT,
                                       self.DOOR_WIDTH)
                elif direction == "left":
                    rect = pygame.Rect(0, self.height // 2 - self.DOOR_HEIGHT // 2,
                                       self.DOOR_WIDTH, self.DOOR_HEIGHT)
                elif direction == "right":
                    rect = pygame.Rect(self.width - self.DOOR_WIDTH,
                                       self.height // 2 - self.DOOR_HEIGHT // 2,
                                       self.DOOR_WIDTH, self.DOOR_HEIGHT)
                self.doors[direction] = rect

    def spawn_enemies(self, player, bullet_group):
        num_enemies = random.randint(3, 5)
        enemy_types = ["bat", "skeleton", "blob"]
        for _ in range(num_enemies):
            etype = random.choice(enemy_types)
            x = random.randint(100, self.width - 100)
            y = random.randint(100, self.height - 100)
            Enemy(etype, (x, y), self.sprites, bullet_group, player)

    def draw(self, screen):
        screen.fill(self.color)
        for door in self.doors.values():
            border_rect = door.inflate(4, 4)  # 2px extra on all sides
            pygame.draw.rect(screen, (100, 60, 20), border_rect, border_radius=5)  # dark border
            pygame.draw.rect(screen, (180, 120, 60), door,border_radius=5)
        self.sprites.draw(screen)

    def check_doors(self, player, rooms_dict):
        x, y = player.rect.center
        new_room = None
        new_pos = None

        if x < 0 and "left" in self.doors:
            new_room = rooms_dict.get((self.pos[0]-1, self.pos[1]))
            new_pos = (WINDOW_WIDTH - 50, y)
        elif x > self.width and "right" in self.doors:
            new_room = rooms_dict.get((self.pos[0]+1, self.pos[1]))
            new_pos = (50, y)
        elif y < 0 and "up" in self.doors:
            new_room = rooms_dict.get((self.pos[0], self.pos[1]-1))
            new_pos = (x, WINDOW_HEIGHT - 50)
        elif y > self.height and "down" in self.doors:
            new_room = rooms_dict.get((self.pos[0], self.pos[1]+1))
            new_pos = (x, 50)

        if new_room:
            new_room.visited = True
        return new_room, new_pos

    def spawn_powerups(self):
        if random.random() < 0.3:
            power_type = random.choice(["fast_shoot", "small", "damage"])
            x = random.randint(100, self.width - 100)
            y = random.randint(100, self.height - 100)
            # add to this room's sprite group
            PowerUp((x, y), [self.sprites], power_type)
