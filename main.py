# Imports
import pygame
from os.path import join
import random 

#general setup
pygame.init()
window_width, window_height = 1280, 720
screen = pygame.display.set_mode((window_width, window_height))
#Change the title of Window
pygame.display.set_caption('Space Shooter')
clock = pygame.time.Clock()

# Variables
running = True
star_distance = 0




# Sprites Groups
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
Laser_sprites = pygame.sprite.Group()


#Class
class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(midbottom = (640,700))
        self.direction = pygame.Vector2()
        self.speed = 450

        #Cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400
    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True
    def update(self, dt):
        self.laser_timer()
        #Input 
        keys= pygame.key.get_pressed()

        #Movement
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT]) #Works because its a boolean values and the int makes true become 1 and False become 0
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed *dt

        # Shoot Lasers
        recent_keys = pygame.key.get_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop,(all_sprites, Laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (random.randint(0,window_width + star_distance),random.randint(0,window_height + star_distance)))
class Laser(pygame.sprite.Sprite):
    def __init__(self,surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
    def update(self,dt):
        self.rect.centery -= 650 *dt
        if self.rect.bottom < 0:
            self.kill()
class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midtop = pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime= 3000
        if random.random() < 0.3:
            self.direction = pygame.Vector2(0,1)
        else:
            self.direction = pygame.Vector2(random.uniform(-0.5, 0.5), 1)
        self.speed = random.randint(400,600)
        self.pos = pygame.math.Vector2(self.rect.center)
    def update(self, dt):
        self.pos.x += self.direction.x  * self.speed * dt
        self.pos.y += self.direction.y  * self.speed * dt
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()
        
def collsions():
    global running
    collison_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True)
    if collison_sprites:
        running = False

    for laser in Laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprites:
            laser.kill()
def display_score():
    current_time = pygame.time.get_ticks() // 100
    text_surf = font.render(str(current_time),True, (240,240,240))
    text_rec = text_surf.get_frect(midbottom = (window_width / 2, window_height - 50))
    screen.blit(text_surf, text_rec)
    pygame.draw.rect(screen, (240,240,240) , text_rec.inflate(20,20).move(0,-5)  , 5, 10)


#Sprites
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
for i in range(40):
    Stars = Star(all_sprites, star_surf)
    star_distance + 50
player = Player(all_sprites)


# importing an image
Icon = pygame.image.load(join('images', 'player.png')).convert_alpha()
meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
laser_surf = pygame.image.load(join('images','laser.png')).convert_alpha()
font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 40)

#Change Icon
pygame.display.set_icon(Icon)


# Custom Events -> Meteor Event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 300) #Half a second


while running:
    dt = clock.tick() / 1000 # dt = Deta Time

    #event loopS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            Meteor(meteor_surf,(random.randint(0,1280), 0), (all_sprites, meteor_sprites))
    
    # Update
    all_sprites.update(dt)
    collsions()


    #draw the game
    screen.fill('#3a2e3f')
      
    


    all_sprites.draw(screen)



    display_score()
    pygame.display.update()
pygame.quit()