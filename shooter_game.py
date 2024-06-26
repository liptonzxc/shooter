from pygame import *
from random import randint
from time import time as timer

mixer.init()
mixer.music.load('Project_1.mp3')
mixer.music.play()
mixer.music.set_volume(0.1)

lost = 0
score = 0


class GameSprite(sprite.Sprite):
    def __init__(self, player_name, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_name), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 630:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 420:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(80, 620)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500
window = display.set_mode((700,500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (win_width,win_height))

font.init()
font = font.SysFont('Arial', 40)
win = font.render('YOU WIN', True, (255, 255, 255))
lose = font.render('YOU SUCK', True, (0, 255, 0))

ship = Player('rocket.png', 5, 405, 60, 80, 4)
bullets = sprite.Group()
monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(80, 620), -40, 80, 50, randint(1,3))
    monsters.add(monster)
asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png', randint(80, 620), -40, 80, 50, randint(1,3))
    asteroids.add(asteroid)

run = True
finish = False
fire_sound = mixer.Sound('fire.ogg')

rel_time = False
num_fire = 0
lyfe = 3

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <5 and rel_time != True:
                    fire_sound.play()
                    ship.fire()
                    num_fire += 1
                if num_fire >= 5 and rel_time != True:
                    rel_time = True 
                    last_time = timer()

    if not finish:
        window.blit(background, (0, 0))

        text = font.render(f'Счет:{score}', True,(255, 255, 255))
        window.blit(text,(10,20))

        text_lose = font.render(f'Пропущено:{lost}', True, (255, 255 ,255))
        window.blit(text_lose,(10,50))

        ship.reset()
        ship.update()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update( )
        asteroids.draw(window)
        asteroids.update()
        life_text = font.render(str(lyfe), True, (0, 255, 0))
        window.blit(life_text,(650, 10))
        collides = sprite.groupcollide(bullets, monsters, True, True)
        collides_m = sprite.groupcollide(bullets, asteroids, True, True)

        if rel_time:
            now_time = timer()
            if now_time - last_time <3:
                reload = font.render("Перезарядка", True, (100, 200, 100))
                window.blit(reload, (250, 450))
            else:
                num_fire = 0
                rel_time = False
        for i in collides:
            score += 1
            monster = Enemy('ufo.png', randint(80, 620), -40, 80, 50, randint(1,3))
            monsters.add(monster)
        for i in collides_m:
            score += 1
            asteroid = Enemy('asteroid.png', randint(80, 620), -40, 80, 50, randint(1,3))
            asteroids.add(asteroid)
        
        if sprite.spritecollide(ship, monsters, True):
            finish = True
            window.blit(lose, (200,200))
        if sprite.spritecollide(ship, asteroids, True):
            lyfe -= 1
    
        if score >= 10:
            window.blit(win, (200, 200))
            finish = True
        if lost >= 5:
            window.blit(lose, (200, 200))
            finish = True

    else:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()
        time.delay(3000)
        for i in range(5):
            monster = Enemy('ufo.png', randint(80, 620), -40, 80, 50, randint(1,3))
            monsters.add(monster)
        for i in range(3):
            asteroid = Enemy('asteroid.png', randint(80, 620), -40, 80, 50, randint(1,3))
            asteroids.add(asteroid)
        
    display.update()
    time.delay(20)