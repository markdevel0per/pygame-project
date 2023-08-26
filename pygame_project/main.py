import pygame
from random import randint, choice

pygame.init()

# music
music = pygame.mixer.Sound("audio/music.wav")
music.set_volume(.4)
music.play(loops=(-1))


class Hero(pygame.sprite.Sprite):
    """Hero in the main game loop"""
    
    
    def __init__(self):
        super().__init__()
        self.frames = [pygame.image.load("graphics/hero/hero1.png").convert_alpha(),
                        pygame.image.load("graphics/hero/hero2.png").convert_alpha(),
                        pygame.image.load("graphics/hero/hero3.png").convert_alpha(),
                        pygame.image.load("graphics/hero/hero4.png").convert_alpha(),
                        pygame.image.load("graphics/hero/hero5.png").convert_alpha(),
                        pygame.image.load("graphics/hero/hero6.png").convert_alpha(),
                        pygame.image.load("graphics/hero/hero7.png").convert_alpha(),
                        pygame.image.load("graphics/hero/hero8.png").convert_alpha()]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.jump_image = pygame.image.load("graphics/hero/jump.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound("audio/jump.mp3")
        self.jump_sound.set_volume(.4)


    def jump(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == 300:
            self.gravity = -20.5
            self.jump_sound.play()


    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        # always on the ground
        if self.rect.bottom > 300:
            self.rect.bottom = 300


    def animation(self):
        # if on the ground
        if self.rect.bottom == 300:
            self.current_frame += .12
            if self.current_frame >= len(self.frames):
                self.current_frame = 0
            self.image = self.frames[int(self.current_frame)]
        # jump hero frame
        else:
            self.image = self.jump_image


    def update(self):
        # all functions
        self.jump()
        self.apply_gravity()
        self.animation()


class Enemy(pygame.sprite.Sprite):
    """Flies and snails in the main game loop"""
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            self.frames = [pygame.image.load("graphics/fly/fly1.png").convert_alpha(),
                           pygame.image.load("graphics/fly/fly2.png").convert_alpha(),
                           pygame.image.load("graphics/fly/fly3.png").convert_alpha(),
                           pygame.image.load("graphics/fly/fly4.png").convert_alpha(),
                           pygame.image.load("graphics/fly/fly5.png").convert_alpha()]
            y_pos = randint(170, 180)
        else:
            self.frames = [pygame.image.load("graphics/snail/snail1.png").convert_alpha(),
                           pygame.image.load("graphics/snail/snail2.png").convert_alpha(),
                           pygame.image.load("graphics/snail/snail3.png").convert_alpha(),
                           pygame.image.load("graphics/snail/snail4.png").convert_alpha(),
                           pygame.image.load("graphics/snail/snail5.png").convert_alpha()]
            y_pos = 300
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(midbottom=(randint(800, 1000), y_pos))
    
    
    def animation(self):
        self.current_frame += .1
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.image = self.frames[int(self.current_frame)]


    def destroy(self):
        # if the enemy is behind left border, then he dies
        if self.rect.right <= 0:
            self.kill()


    def update(self):
        self.animation()
        # movement
        self.rect.x -= 6
        self.destroy()


score = 0
start_time = 0


def display_score():
    game_time = int(pygame.time.get_ticks() / 1000) - start_time
    # text
    score_surf = font.render(f'Score: {game_time}', False, (255, 255, 255))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return game_time


def collision_between_sprites():
    if pygame.sprite.spritecollide(hero.sprite, enemy_group, False):
        enemy_group.empty()
        return False
    return True


# window and clock
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Sunset runner")
icon = pygame.image.load("graphics/icon.jpg").convert_alpha()
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
# background surface
bg_surf = pygame.image.load("graphics/bg.png").convert_alpha()
# font
font = pygame.font.Font("font/pixeltype.ttf", 100)
# class instances
hero = pygame.sprite.GroupSingle()
hero.add(Hero())
enemy_group = pygame.sprite.Group()
# intro screen:
# background 
non_game_bg = pygame.image.load("graphics/non_game_bg.jpg").convert_alpha()
# hero
hero_stand = pygame.image.load("graphics/hero/stand.png").convert_alpha()
hero_stand = pygame.transform.rotozoom(hero_stand, 0, 1.75) # zoomed
hero_stand_rect = hero_stand.get_rect(center=(400, 200))
# text
game_name = font.render('Sunset runner', False, (111, 0, 169))
game_name_rect = game_name.get_rect(center=(400, 80))
game_message = font.render('Press space to run', False, (111, 0, 169))
game_message_rect = game_message.get_rect(center=(400, 340))
# timer of spawning enemies
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1500)
# main loop
game_active = False
loop = True
while loop:
    if game_active == True:
        screen.blit(bg_surf, (0, 0))
        score = display_score()
        hero.draw(screen)
        hero.update()
        enemy_group.draw(screen)
        enemy_group.update()
        game_active = collision_between_sprites()
    # not the game
    else:
        screen.blit(non_game_bg, (0, 0))
        screen.blit(hero_stand, hero_stand_rect)
        screen.blit(game_name, game_name_rect)
        if score > 0:
            game_message = font.render(f'Your score: {score}', False, (111, 0, 169))
            game_message_rect = game_message.get_rect(center=(400 ,330))
        screen.blit(game_message, game_message_rect)
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # exit the game
            loop = False
        if game_active == True:
            # spawning enemies
            if event.type == enemy_timer:
                enemy_group.add(Enemy(choice(['fly', 'snail', 'snail', 'snail'])))
        else:
            # starting a new game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = int(pygame.time.get_ticks() / 1000)

    # other trash
    pygame.display.update()
    clock.tick(60)
