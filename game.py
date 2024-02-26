import pygame
from sprites import Background, Player

WIDTH = 1720
HEIGHT = 950

PARALLAX_SPEED = 3
MAX_BACKGROUND_SPEED = 2

MAX_PLAYER_SPEED = 5
PLAYER_SPEED_INC = 1.04

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Scavenge')
        self.clock = pygame.time.Clock()
        self.objects = pygame.sprite.Group()

    def run(self):
        """Handles game logic
        """
        # static cloud image
        self.objects.add(Background('backgrounds/1.png', 0))
        # number of layers
        backgrounds_stacked = 4

        for i in range(1, backgrounds_stacked):
            b = Background(f'backgrounds/{i+ 1}.png', 0)
            self.objects.add(b)
            self.objects.add(Background(f'backgrounds/{i+ 1}.png', b.width-1))
        
        player_speed = 0
        background_speed = 0
        last_player_update = self.clock.tick()
        hero = Player(WIDTH//2 - 400)

        while True:

            # calculate the right animation sprite
            current_time = pygame.time.get_ticks()
            if current_time - last_player_update >= hero.animation_cooldown:
                hero.frame += 1
                if hero.frame >= hero.a_count:
                    hero.frame = 0
                last_player_update = current_time

            # handle events that need to happen when a key is once pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                elif event.type == pygame.KEYDOWN:

                    hero.frame = 0
                    if event.key == pygame.K_d:
                        player_speed = 1
                        background_speed = 1

                    elif event.key == pygame.K_a:
                        player_speed = -1
                        background_speed = -1
                    
                    elif event.key == pygame.K_SPACE and not hero.is_jumping:
                        hero.is_jumping = True
            
            # handle events that happens when a key is getting pressed
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_d]:

                # handle background speed
                if background_speed < MAX_BACKGROUND_SPEED:
                    background_speed *= PLAYER_SPEED_INC

                # running
                if pressed[pygame.K_LSHIFT]:
                    if player_speed < MAX_PLAYER_SPEED:
                        player_speed = player_speed * PLAYER_SPEED_INC
                else:
                    player_speed = PLAYER_SPEED_INC

            elif pressed[pygame.K_a]:
                # if pressed[pygame.K_LSHIFT]:
                # handle background speed
                if background_speed > -MAX_BACKGROUND_SPEED:
                    background_speed *= PLAYER_SPEED_INC
                
                # running
                if pressed[pygame.K_LSHIFT]:
                    if player_speed > -MAX_PLAYER_SPEED:
                        player_speed = player_speed * PLAYER_SPEED_INC
                else:
                    player_speed = -PLAYER_SPEED_INC
            else:
                # handle background speed
                player_speed = 0
                background_speed = 0
            
            if not hero.is_jumping and pressed[pygame.K_SPACE]:
                hero.is_jumping = True
        
            # bounding box for hero movement
            if hero.x >= WIDTH // 2 + 150:
                hero.x = WIDTH // 2 + 150
            if hero.x <= 400 - hero.dimensions // 2:
                hero.x = 400 - hero.dimensions // 2
            
            # update player
            hero.update(player_speed)

            # place the backgrounds parallax effect
            for i in range(2, backgrounds_stacked * 2, 2):
                # parallax right
                if background_speed >= 0:
                    if self.objects.sprites()[i-1].rect.right < WIDTH + background_speed: # width + parallax speed so that the image does not blip in
                        self.objects.sprites()[i].set_position(self.objects.sprites()[i-1].rect.right)

                    if self.objects.sprites()[i].rect.right < WIDTH + background_speed:
                        self.objects.sprites()[i-1].set_position(self.objects.sprites()[i].rect.right)
                else:
                    if self.objects.sprites()[i-1].rect.left > 1:
                        self.objects.sprites()[i].set_position(self.objects.sprites()[i-1].rect.left - self.objects.sprites()[i-1].width)

                    if self.objects.sprites()[i].rect.left > 1:
                        self.objects.sprites()[i-1].set_position(self.objects.sprites()[i].rect.left - self.objects.sprites()[i].width)
                # update each sprite
                self.objects.sprites()[i-1].update(background_speed * i)
                self.objects.sprites()[i].update(background_speed * i)
        
            
            # Draw the objects on the screen
            self.objects.draw(self.screen)

            # draw player, set which sprites to draw

            if player_speed < 0:
                phase = 'jump' if hero.is_jumping else 'run'
                flip = True

            elif player_speed > 0:
                phase = 'jump' if hero.is_jumping else 'run'
                flip = False
            else:
                phase = 'jump' if hero.is_jumping else 'idle'
                flip = False
            
            hero.draw(self.screen, phase, flip)

            pygame.display.update()

            # limit FPS to 30
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()
