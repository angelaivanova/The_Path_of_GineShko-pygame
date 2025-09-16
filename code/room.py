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

        self.doors = {
            "up": pygame.Rect(self.width//2 - DOOR_SIZE//2, 0, DOOR_SIZE, DOOR_SIZE),
            "down": pygame.Rect(self.width//2 - DOOR_SIZE//2, self.height - DOOR_SIZE, DOOR_SIZE, DOOR_SIZE),
            "left": pygame.Rect(0, self.height//2 - DOOR_SIZE//2, DOOR_SIZE, DOOR_SIZE),
            "right": pygame.Rect(self.width - DOOR_SIZE, self.height//2 - DOOR_SIZE//2, DOOR_SIZE, DOOR_SIZE)
        }

    def draw(self, screen):
        screen.fill(self.color)
        for door in self.doors.values():
            pygame.draw.rect(screen, (120,120,120), door)
        self.sprites.draw(screen)

    def check_doors(self, player, rooms):
        
        x, y = player.rect.center
        new_room = None
        new_pos = None

        if x < 0:  # left door
            new_room = self.get_room_at_offset(rooms, (-1, 0))
            if new_room:
                new_pos = (WINDOW_WIDTH - 50, y)
        elif x > self.width:  # right door
            new_room = self.get_room_at_offset(rooms, (1, 0))
            if new_room:
                new_pos = (50, y)
        elif y < 0:  # up door
            new_room = self.get_room_at_offset(rooms, (0, -1))
            if new_room:
                new_pos = (x, WINDOW_HEIGHT - 50)
        elif y > self.height:  # down door
            new_room = self.get_room_at_offset(rooms, (0, 1))
            if new_room:
                new_pos = (x, 50)

        if new_room:
            new_room.visited = True
        return new_room, new_pos

    def get_room_at_offset(self, rooms, offset):
        cx, cy = self.pos
        for room in rooms:
            if room.pos == (cx + offset[0], cy + offset[1]):
                return room
        return None
