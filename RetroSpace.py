if __name__ == "__main__":
    # ** Import modules **
    import pygame, random
    pygame.init()
    pygame.font.init()

    # ** Create screen and clock **
    screen_size = screen_width, screen_height = 500, 800
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("RetroSpace v1")
    clock = pygame.time.Clock()
    FPS = 60

    # ** Color Definitions **
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE =  (0, 0, 255)

    # ** Classes **
    class Player(pygame.sprite.Sprite):
        def __init__(self, img, x, y):
            super().__init__()
            self.image = pygame.image.load(img).convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.mask = pygame.mask.from_surface(self.image)
            self.radius = 55
            self.speedx = 0
            
        def draw_radius(self):
            pygame.draw.circle(self.image, RED, (64, 64), self.radius)

        def update(self):
            if self.rect.x <= 0:
                self.rect.x = 0

            elif self.rect.x >= screen_width - 130:
                self.rect.x = screen_width - 130

            self.rect.x += self.speedy
                

    class Background(pygame.sprite.Sprite):
        def __init__(self, img, x, y):
            super().__init__()
            self.image = pygame.image.load(img).convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        def swipe_out(self):
            if self.rect.y >= -200:
                self.rect.y -= 5

    class Asteroid(pygame.sprite.Sprite):
        def __init__(self, img, x, y):
            super().__init__()
            self.image = pygame.image.load(img).convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.mask = pygame.mask.from_surface(self.image)
            self.radius = 28
            self.speedx = random.randrange(-1, 1)
            self.speedy = 1

        def draw_radius(self):
            pygame.draw.circle(self.image, RED, (32, 32), self.radius)

        def update(self):
            self.rect.y += (self.speedy + random.randrange(self.speedy, 3))
            self.rect.x += self.speedx
        

    class Bullet(pygame.sprite.Sprite):
        def __init__(self, img, x, y):
            super().__init__()
            self.image = pygame.image.load(img).convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.radius = 3
            self.speedy = -5

        def draw_radius(self):
            pygame.draw.circle(self.image, RED, (5, 7), self.radius)

        def update(self):
            self.rect.y += self.speedy

    class GameOver(pygame.sprite.Sprite):
        def __init__(self, img, x, y):
            super().__init__()
            self.image = pygame.image.load(img).convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.radius = 3

    class Explosion(pygame.sprite.Sprite):
        def __init__(self, img, x, y):
            super().__init__()
            self.image = pygame.image.load(img).convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.radius = 3
            
    # ** Create sprite groups **
    player_sprite_group = pygame.sprite.Group()
    asteroid_sprite_group = pygame.sprite.Group()
    background_sprite_group = pygame.sprite.Group()
    bullet_sprite_group = pygame.sprite.Group()
    gameover_sprite_group = pygame.sprite.Group()
    explosion_sprite_group = pygame.sprite.Group()

    # ** Create sprite objects **
    player = Player("img/player_ship.png", (screen_width / 2) - 60, screen_height - 130)
    background = Background("img/background_1.png", 0, 0)
    title = Background("img/title_screen.png", (screen_width / 2) - 141, 250)
    press_space = Background("img/press_space.png", (screen_width / 2) - 196, 300)
    controls_info = Background("img/controls.png", (screen_width / 2) - 77, 350)
    game_over = GameOver("img/game_over.png", (screen_width / 2) - 138, 200)
    #explosion = Explosion("img/explosion.png", (screen_width / 2) - 138, 200)

    # ** Add sprite objects to sprite groups **
    player_sprite_group.add(player)
    background_sprite_group.add(background)
    background_sprite_group.add(title)
    background_sprite_group.add(press_space)
    background_sprite_group.add(controls_info)
    gameover_sprite_group.add(game_over)
    #explosion_sprite_group.add(explosion)

    def start_screen():
        
        start_screen = True
        
        while start_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    start_screen = False
                    
            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE]:              
                game_loop()           
            
            background_sprite_group.draw(screen)
            player_sprite_group.draw(screen)
            
            pygame.display.update()

        pygame.quit()
        quit()

    def game_loop():
        pygame.time.wait(200)
        score = 0
        player_lives = 3
        
        shot_tick = 3
        asteroid_spawn_tick = 80
        explosion_tick = 30

        minimum_asteroid = 10
        running = True
        game_over_flag = False
        exploded = False
        
        game_font = pygame.font.SysFont("OCR A Extended", 24)
        
        while running:
            score_text = game_font.render("Score: " + str(score), False, WHITE)
            if asteroid_spawn_tick <= 0:
                for i in range(1, minimum_asteroid):
                    asteroid_critter = Asteroid("img/asteroid_1.png", random.randrange(0, screen_width), random.randint(0, 200) - 800)
                    asteroid_sprite_group.add(asteroid_critter)
                    asteroid_spawn_tick = 80

            #print("Minimum asteroid: " + str(minimum_asteroid))
            # ** Swipe out start screen **
            title.swipe_out()
            press_space.swipe_out()
            controls_info.swipe_out()
            
            # ** Ticks ** 
            clock.tick(FPS)
            shot_tick -= 1
            asteroid_spawn_tick -= 1
            if exploded:
                explosion_tick -= 1

            #print(explosion_tick)

            # ** Check events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # ** Check key events and update player object ** 
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_SPACE] and shot_tick <= 0:
                bullet1 = Bullet("img/player_laser.png", player.rect.x + 59, player.rect.y - 12)
                bullet_sprite_group.add(bullet1)
                shot_tick = 16

            elif keys[pygame.K_d]:
                player.speedy = 5
                            
            elif keys[pygame.K_a]:
                player.speedy = -5
                        
            else:
                player.speedy = 0

            player.update()

            # ** Spawns asteroid and bullet **
            for bullet in bullet_sprite_group:
                bullet.update()

                if bullet.rect.y <= 0:
                    bullet_sprite_group.remove(bullet)
            
            for asteroid in asteroid_sprite_group:
                asteroid.update()

                if asteroid.rect.x <= -64 or asteroid.rect.x >= screen_width + 64:
                    asteroid_sprite_group.remove(asteroid)

                if pygame.sprite.collide_mask(player, asteroid):
                    explosion = Explosion("img/explosion.png", asteroid.rect.x, asteroid.rect.y)
                    explosion_sprite_group.add(explosion)
                    exploded = True

                    player_lives -= 1
                    asteroid_sprite_group.remove(asteroid)

                    if player_lives <= 0:
                        game_over_flag = True
                    
                if explosion_tick <= 0:
                    print("test2")
                    explosion_sprite_group.remove(explosion)
                    exploded = False
                    explosion_tick = 30
        
    

            # ** Checks sprite collisions **

            if pygame.sprite.groupcollide(asteroid_sprite_group, bullet_sprite_group, True, True):
                score += 1

            # ** Draw sprite groups **
            lives_text = game_font.render("Lives: " + str(player_lives), False, WHITE)
            background_sprite_group.draw(screen)
            player_sprite_group.draw(screen)
            asteroid_sprite_group.draw(screen)
            bullet_sprite_group.draw(screen)
            explosion_sprite_group.draw(screen)          
            screen.blit(score_text,(0,0))
            screen.blit(lives_text,(0,30))
            
            if game_over_flag == True:
                gameover_sprite_group.draw(screen)
                pygame.display.update()
                pygame.time.wait(1000)
                running = False
            
            # ** Update screen **
            pygame.display.update()

        pygame.quit()
        quit()

    start_screen()


