import pygame

class Background(pygame.sprite.Sprite):
    def __init__(self, image, x):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, -100))
        self.width = self.rect.width

    def update(self, speed):
        self.rect.x -= speed

        

    def set_position(self, x):
        self.rect.x = x

PLAYER_SPEED_INC = 1.04
HEIGHT = 950

class Player:

    # 162 x 160 sprite dimensions
    
    def __init__(self, x):
        self.dimensions = 300
        self.animation_cooldown = 120
        self.scale = 3
        self.frame = 0
        self.speed = 1
        self.jump_speed = 6
        self.jump_duration = 0
        self.x = x
        self.y = HEIGHT - self.dimensions
        self.jump_start_y = self.y
        self.gravity = 1
        self.jump_height = self.dimensions * 3
        self.idle_image = pygame.image.load('player/Idle.png').convert_alpha()
        self.idle_sprite = SpriteSheet(self.idle_image)
        self.idle_animations = []
        self.a_count = 8

        for i in range(self.a_count):
            self.idle_animations.append(self.idle_sprite.get_image(i, 150, 150, self.scale, (0, 0, 0)))

        self.running_image = pygame.image.load('player/Run.png').convert_alpha()
        self.run_sprite = SpriteSheet(self.running_image)
        self.run_animations = []

        for i in range(self.a_count):
            self.run_animations.append(self.run_sprite.get_image(i, 150, 150, self.scale, (0, 0, 0)))

        self.is_jumping = False

        self.jumping_image = pygame.image.load('player/Jump.png').convert_alpha()
        self.jump_sprite = SpriteSheet(self.jumping_image)
        self.jump_animations = []
        self.j_count = 20

        for i in range(self.j_count):
            self.jump_animations.append(self.jump_sprite.get_image(i, 150, 150, self.scale, (0, 0, 0)))

    def update(self, speed):
        self.x = self.x + speed

        if self.is_jumping:
            if self.j_count >= -20:
                self.y -= int((self.j_count * abs(self.j_count)) * 0.1)
                self.j_count -= 1
            else:
                self.j_count = 20
                self.is_jumping = False

    


    def draw(self, screen, a_type, flipped=None):

        if a_type == 'idle':
            image = self.idle_animations[self.frame]
            
        elif a_type == 'run':
            image = self.run_animations[self.frame]
        
        elif a_type == 'jump':
            image = self.jump_animations[self.frame % 2]

        if flipped:
            flipped_image = pygame.transform.flip(image, True, False)
            flipped_image.set_colorkey((0, 0, 0))
            screen.blit(flipped_image, (self.x, self.y))

        else:
            screen.blit(image, (self.x, self.y))


class SpriteSheet:
    def __init__(self, image):
        self.sheet = image
    
    def get_image(self, frame, width, height, scale, color):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)

        return image
