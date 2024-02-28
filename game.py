import pygame
from sprites import Background, Player

WIDTH = 1720
HEIGHT = 950

BACKGROUNDS_STACKED = 4
MAX_BACKGROUND_SPEED = 2

MAX_PLAYER_SPEED = 5
SPEED_INC = 1.04

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Scavenge')
        self.clock = pygame.time.Clock()
        self.bgs = []

    def set_backgrounds(self):
        # static image
        self.bgs.append(Background('backgrounds/1.png', 0, 0))
        # number of layers

        for i in range(1, BACKGROUNDS_STACKED):
            # each background needs 2 copies for parallax
            b = Background(f'backgrounds/{i + 1}.png', 0 , i)

            self.bgs.append(b)
            self.bgs.append(Background(f'backgrounds/{i + 1}.png', b.width, i))


    def set_animation_frame(self, entity, l_update) -> int:
        """Sets the current animation frame for the entity, returns the last time updated

        Args:
            entity (Player): _description_
            l_p_update (int): _description_

        Returns:
            c_time (int): last update time, if updated.
            l_update (int): previous update time

        """
        c_time = pygame.time.get_ticks()

        if c_time - l_update >= entity.animation_cooldown:
            entity.frame += 1

            if entity.frame >= entity.a_count:
                entity.frame = 0

            return c_time
        
        return l_update


    def update_background_parallax(self):
        # place the backgrounds parallax effect
        for i in range(2, BACKGROUNDS_STACKED * 2, 2):
            # parallax right
            if self.bgs[i].speed >= 0:
                if self.bgs[i-1].rect.right < WIDTH + self.bgs[i].speed: # width + parallax speed so that the image does not blip in
                    self.bgs[i].set_position(self.bgs[i-1].rect.right)

                if self.bgs[i].rect.right < WIDTH + self.bgs[i].speed:
                    self.bgs[i-1].set_position(self.bgs[i].rect.right)
            else:
                if self.bgs[i-1].rect.left > 1:
                    self.bgs[i].set_position(self.bgs[i-1].rect.left - self.bgs[i-1].width)

                if self.bgs[i].rect.left > 1:
                    self.bgs[i-1].set_position(self.bgs[i].rect.left - self.bgs[i].width)
                    
            self.bgs[i-1].update()
            self.bgs[i].update()


    def run(self):
        """Handles game logic
        """
        
        self.set_backgrounds()

        hero = Player(WIDTH // 2 - 400)

        last_player_update = self.clock.tick()

        while True:

            # calculate the right animation sprite
            last_player_update = self.set_animation_frame(hero, last_player_update)

            # handle events that need to happen when a key is once pressed
            events = pygame.event.get()
            # handle events that happens when a key is getting pressed
            pressed = pygame.key.get_pressed()

            # handle key inputs for entities
            for bg in self.bgs:
                bg.handle_keys(events, pressed)

            hero.handle_keys(events, pressed)

            self.update_background_parallax()
            hero.update(WIDTH)
        
            # Draw the objects on the screen
            for b in self.bgs:
                b.draw(self.screen)
            
            hero.draw(self.screen)
            # update player

            pygame.display.update()

            # limit FPS to 30
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()
