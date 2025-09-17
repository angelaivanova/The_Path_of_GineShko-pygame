import pygame

DOOR_SIZE = 60
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800

class Room:
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
                    rect = pygame.Rect(self.width//2 - DOOR_SIZE//2, 0, DOOR_SIZE, DOOR_SIZE)
                elif direction == "down":
                    rect = pygame.Rect(self.width//2 - DOOR_SIZE//2, self.height - DOOR_SIZE, DOOR_SIZE, DOOR_SIZE)
                elif direction == "left":
                    rect = pygame.Rect(0, self.height//2 - DOOR_SIZE//2, DOOR_SIZE, DOOR_SIZE)
                elif direction == "right":
                    rect = pygame.Rect(self.width - DOOR_SIZE, self.height//2 - DOOR_SIZE//2, DOOR_SIZE, DOOR_SIZE)
                self.doors[direction] = rect

    def draw(self, screen):
        screen.fill(self.color)
        for door in self.doors.values():
            pygame.draw.rect(screen, (120,120,120), door)
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
