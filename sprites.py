import pygame

SPEED_INC = 1.04
MAX_BACKGROUND_SPEED = 2
HEIGHT = 950
MAX_PLAYER_SPEED = 5

class Background():
    def __init__(self, image, x, speed_multiplier):
        
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, -100))
        self.width = self.rect.width
        self.speed = 0
        self.speed_mul = speed_multiplier


    def handle_keys(self, key_events, pressed):
        # keys clicked
        for event in key_events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.speed = self.speed_mul

                elif event.key == pygame.K_a:
                    self.speed = -self.speed_mul

        # keys holded
        if pressed[pygame.K_d]:
            if self.speed < MAX_BACKGROUND_SPEED:
                self.speed *= SPEED_INC

        elif pressed[pygame.K_a]:
            if self.speed > -MAX_BACKGROUND_SPEED:
                self.speed *= SPEED_INC
        else:
            self.speed = 0


    def update(self,speed):

        self.rect.x -= speed * self.speed_mul

        
    def set_position(self, x):
        self.rect.x = x


    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, -100))



class Player:
    def __init__(self, x):
        self.dimensions = 300
        self.animation_cooldown = 120
        self.scale = 3
        self.frame = 0
        self.speed = 1
        self.x = x
        self.y = HEIGHT - self.dimensions


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


    def update(self, width):

        self.x = self.x + self.speed

        if self.is_jumping:
            if self.j_count >= -20:
                self.y -= int((self.j_count * abs(self.j_count)) * 0.1)
                self.j_count -= 1

            else:
                self.j_count = 20
                self.is_jumping = False
        
        # bounding box for hero movement
        if self.x >= width // 2 + 150:
            self.x = width // 2 + 150
        if self.x <= 400 - self.dimensions // 2:
            self.x = 400 - self.dimensions // 2

    
    def handle_keys(self, key_events, pressed):
        # handle single presses
        for event in key_events:
            if event.type == pygame.QUIT:
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.speed = 1

                elif event.key == pygame.K_a:
                    self.speed = -1

                elif event.key == pygame.K_SPACE and not self.is_jumping:
                    self.is_jumping = True
        
        # handle keys pressed
        if pressed[pygame.K_d]:
            # running
            if pressed[pygame.K_LSHIFT]:
                if self.speed < MAX_PLAYER_SPEED:
                    self.speed = self.speed * SPEED_INC

        elif pressed[pygame.K_a]:
            # running
            if pressed[pygame.K_LSHIFT]:
                if self.speed > -MAX_PLAYER_SPEED:

                    self.speed = self.speed * SPEED_INC

        else:
            # stand still
            self.speed = 0


    def draw(self, screen):
        flipped = None
        if self.is_jumping:
            image = self.jump_animations[self.frame % 2]
            if self.speed < 0:
                flipped = True
        
        else:
            if self.speed == 0:
                image = self.idle_animations[self.frame]

            else:
                image = self.run_animations[self.frame]
                if self.speed < 0:
                    flipped = True

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
