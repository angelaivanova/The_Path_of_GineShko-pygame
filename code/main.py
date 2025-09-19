# main.py
import pygame, random
from player import Player
from bullet import Bullet
from room import Room
from power import PowerUp

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Binding of Isaac clone")
        self.running = True
        self.clock = pygame.time.Clock()

        self.all_sprites = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.player = Player((WINDOW_WIDTH//2, WINDOW_HEIGHT//2), self.all_sprites, self.bullet_group)

        num_rooms = random.randint(6, 10)
        self.rooms = self.generate_rooms(num_rooms)
        self.current_room = self.rooms[(0,0)]
        self.current_room.visited = True

        # spawn enemies and powerups for every room
        for room in self.rooms.values():   
            room.spawn_enemies(self.player, self.bullet_group)
            room.spawn_powerups()

    def generate_rooms(self, max_rooms):
        rooms = {(0,0): Room((100,100,100), (0,0))}
        poz = [(0,0)]

        while len(rooms) < max_rooms and poz:
            cx, cy = random.choice(poz)
            directions = [(1,0),(-1,0),(0,1),(0,-1)]
            dx, dy = random.choice(directions)
            new_pos = (cx+dx, cy+dy)
            if new_pos not in rooms:
                color = (random.randint(50,200), random.randint(50,200), random.randint(50,200))
                rooms[new_pos] = Room(color, new_pos)
                poz.append(new_pos)
            if len(poz) > max_rooms:
                poz.pop(0)

        for room in rooms.values():
            room.update_doors(rooms)

        return rooms

    def draw_health(self):
        heart = pygame.image.load("images/heart.png").convert_alpha()
        s_heart = pygame.transform.scale(heart, (32,32))
        for i in range(self.player.health):
            self.screen.blit(s_heart, (20 + i * 40, 20))

    def draw_minimap(self, screen, offset_y=60):
        xs = [pos[0] for pos in self.rooms.keys()]
        ys = [pos[1] for pos in self.rooms.keys()]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        cell_size = 15
        spacing = 20

        for (x, y), room in self.rooms.items():
            draw_x = 20 + (x - min_x) * spacing
            draw_y = 20 + (y - min_y) * spacing + offset_y
            color = (100, 100, 100) if not room.visited else (255, 255, 255)
            rect = pygame.Rect(draw_x, draw_y, cell_size, cell_size)
            pygame.draw.rect(screen, color, rect)

        cx, cy = self.current_room.pos
        draw_x = 20 + (cx - min_x) * spacing
        draw_y = 20 + (cy - min_y) * spacing + offset_y
        rect = pygame.Rect(draw_x, draw_y, cell_size, cell_size)
        pygame.draw.rect(screen, (0, 255, 0), rect)

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update groups (player is in all_sprites; enemies are in room.sprites)
            self.all_sprites.update(dt)
            self.bullet_group.update(dt)
            self.current_room.sprites.update(dt)

            # check room transitions
            new_room, new_pos = self.current_room.check_doors(self.player, self.rooms)
            if new_room:
                self.current_room = new_room
                # clamp new_pos inside screen
                nx = max(0, min(WINDOW_WIDTH, new_pos[0]))
                ny = max(0, min(WINDOW_HEIGHT, new_pos[1]))
                self.player.rect.center = (nx, ny)

            # collect powerups (iterate over a copy to avoid modification during iteration)
            for spr in list(self.current_room.sprites):
                if isinstance(spr, PowerUp) and self.player.rect.colliderect(spr.rect):
                    spr.apply(self.player)

            # draw
            self.current_room.draw(self.screen)
            self.all_sprites.draw(self.screen)
            self.bullet_group.draw(self.screen)
            self.current_room.sprites.draw(self.screen)

            self.draw_minimap(self.screen, offset_y=60)
            self.draw_health()
            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    igra = Game()
    igra.run()
