import pygame
from player import Player
from bullet import Bullet
from room import Room

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

        
        self.rooms = [
            Room((100, 0, 0), (0,0)),
            Room((0, 100, 0), (1,0)),
            Room((0, 0, 100), (0,1)),
            Room((100, 100, 0), (1,1)),
        ]
        self.current_room = self.rooms[0]
        self.current_room.visited = True

    def draw_minimap(self):
        for room in self.rooms:
            color = (200,200,200) if room.visited else (50,50,50)
            x, y = room.pos
            pygame.draw.rect(self.screen, color, pygame.Rect(1100 + x*40, 50 + y*40, 30, 30))

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.all_sprites.update(dt)
            self.bullet_group.update(dt)

            
            new_room, new_pos = self.current_room.check_doors(self.player, self.rooms)
            if new_room:
                self.current_room = new_room
                self.player.rect.center = new_pos

            
            self.current_room.draw(self.screen)
            self.all_sprites.draw(self.screen)
            self.bullet_group.draw(self.screen)
            self.draw_minimap()
            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    igra = Game()
    igra.run()
