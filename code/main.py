import pygame, random
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

       
        num_rooms = random.randint(6, 10)
        self.rooms = self.generate_rooms(num_rooms)
        self.current_room = self.rooms[(0,0)]
        self.current_room.visited = True

    def generate_rooms(self, max_rooms):
        
        rooms = {(0,0): Room((100,100,100), (0,0))}  # pocetna soba
        poz = [(0,0)]  

        # se zima random soba i se prosiruva od tamo
        while len(rooms) < max_rooms and poz:
           
            cx, cy = random.choice(poz)

            
            directions = [(1,0),(-1,0),(0,1),(0,-1)]
            dx, dy = random.choice(directions)
            new_pos = (cx+dx, cy+dy)

            # ako nema soba, naprae se
            if new_pos not in rooms:
                color = (random.randint(50,200), random.randint(50,200), random.randint(50,200))
                rooms[new_pos] = Room(color, new_pos)
                poz.append(new_pos)  

            
            if len(poz) > max_rooms:
                poz.pop(0)

        
        for room in rooms.values():
            room.update_doors(rooms)

        return rooms

    def draw_minimap(self):
        
        for pos, room in self.rooms.items():
            color = (200,200,200) if room.visited else (50,50,50)
            x, y = pos
            pygame.draw.rect(self.screen, color, pygame.Rect(1100 + x*40, 50 + y*40, 30, 30))

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            
            self.all_sprites.update(dt)
            self.bullet_group.update(dt)

            # dali igraco minal niz soba
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
