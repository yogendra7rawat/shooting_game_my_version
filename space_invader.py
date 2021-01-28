import pygame
import os
import random
import time
import math

pygame.init()
WIDTH = 700
HEIGHT = 700
FPS = 60
screen = pygame.display.set_mode((WIDTH,HEIGHT))

blue_ship = pygame.image.load(os.path.join("assets","pixel_ship_blue_small.png"))
red_ship = pygame.image.load(os.path.join("assets","pixel_ship_red_small.png"))
yellow_ship = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))
green_ship = pygame.image.load(os.path.join("assets","pixel_ship_green_small.png"))



blue_laser = pygame.image.load(os.path.join("assets","pixel_laser_blue.png"))
green_laser = pygame.image.load(os.path.join("assets","pixel_laser_green.png"))
red_laser =  pygame.image.load(os.path.join("assets","pixel_laser_red.png"))
yellow_laser =  pygame.image.load(os.path.join("assets","pixel_laser_yellow.png"))


background = pygame.transform.scale(pygame.image.load(os.path.join("assets","background-black.png")),(WIDTH,HEIGHT))




bullets = []
Enemies = []

class Player():
	def __init__(self,x,y,heal):
		self.x = x
		self.y = y
		self.ship_img = yellow_ship
		self.laser_img = yellow_laser
		self.heal = heal
		self.mask = pygame.mask.from_surface(self.ship_img)
		
		
		
	def draw(self,screen):
		screen.blit(self.ship_img,(self.x,self.y))
		self.health(screen)
		
	def health(self,screen):
		pygame.draw.rect(screen,(255,0,0),(self.x,self.y+self.ship_img.get_height()//2+50,self.ship_img.get_width(),10))
		pygame.draw.rect(screen,(0,210,0),(self.x,self.y+self.ship_img.get_height()//2+50,self.ship_img.get_width()-5*(100-self.heal),10))
		
		
	def bullet(self,screen):
		screen.blit(self.laser_img,(self.x,self.y-self.ship_img.get_height()//2))
	

	
class Enemy():
	COLOR_MAP = {
                "red": (red_ship, red_laser),
                "green": (green_ship,green_laser),
                "blue": (blue_ship, blue_laser)
                }
	def __init__(self,x,y,color,vel):
		self.x = x
		self.y = y
		self.vel = vel
		self.color = color
		self.ship_img, self.laser_img = self.COLOR_MAP[color]
		self.mask = pygame.mask.from_surface(self.ship_img)
		
	def draw(self,screen):
		screen.blit(self.ship_img,(self.x,self.y))
		
		
	def move(self):
		self.y +=3
		
	def shoot(self):
		self.vel +=0.1
		screen.blit(self.laser_img,(self.x-15,self.y+self.vel))
			
	


def collide(obj1, obj2):
	offset_x = obj2.x-obj1.x
	offset_y = obj2.y-obj1.y
	return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None
	
main_font = pygame.font.Font("freesansbold.ttf", 32)
lost_font = pygame.font.Font("freesansbold.ttf", 50)




def draw_win(x,y,lives,heal):
	screen.fill((0,0,0))
	
	screen.blit(background,(0,0))
	#Space_ship
	space_ship = Player(x,y,heal)
	space_ship.draw(screen)
	# health 
	# ~ Health = Laser(x,y,yellow_ship.get_height(),heal)
	# ~ Health.draw(screen)
	
	for enemy in Enemies:
		enemy.draw(screen)
		if random.randrange(0, 2*60) == 1:
			enemy.shoot()
		
	#laser 
	for bullet in bullets:
		bullet.bullet(screen)
		
	
	if(lives<0):
		lost_label = lost_font.render("You Lost!!", 1, (255,255,255))
		screen.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))
	
	lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
	screen.blit(lives_label,(10,10))
	pygame.display.update()

def main(screen):
	x =200
	y=350
	lives=5
	length =5
	run  = True
	total_bullet =0
	heal = 100
	space_ship = Player(x,y,heal)
	enemy = Enemy(random.randrange(50, WIDTH-100),random.randrange(-1500, -100),random.choice(["red","blue","green"]),-10)
	clock = pygame.time.Clock()
	flag=0
	while run:
		clock.tick(FPS)
		for enemy in Enemies:
			if enemy.y>HEIGHT:
				lives-=1
				heal-=1
				Enemies.pop(Enemies.index(enemy))
		
		if total_bullet>0:
			total_bullet +=1
		if total_bullet>5:
			total_bullet =0
		for bullet in bullets:
			if collide(enemy,bullet):
				bullets.remove(bullet)
				Enemies.remove(enemy)
			if bullet.y<HEIGHT and bullet.y>0:
				bullet.y-=4
			else:
				bullets.remove(bullet)
				
				
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run  = False
			
		keys = pygame.key.get_pressed()
		
		if keys[pygame.K_a]:
			x -=2
		if keys[pygame.K_d]:
			x+=2
		if keys[pygame.K_w]:
			y-=2
		if keys[pygame.K_s]:
			y+=2
		
		if keys[pygame.K_SPACE] and total_bullet==0:
			print(x,y)
			if(len(bullets)<5):
				Bullet = Player(x,y,heal)
				bullets.append(Bullet)
			
			total_bullet = 1
			
		
		if len(Enemies)==0:
			length+=5
			for i in range(length):
				enemy_x = random.randrange(50, WIDTH-100)
				enemy_y  = random.randrange(-1500, -100)
				enemy = Enemy(enemy_x, enemy_y,random.choice(["red","blue","green"]),-10)
				Enemies.append(enemy)
				
		

					
		draw_win(x,y,lives,heal)
		
		for enemy in Enemies[:]:
			enemy.move()
			enemy.shoot()
							
			if(collide(enemy,space_ship)):
				print("HIT")
				heal-=1
				Enemies.pop(Enemies.index(enemy))

		
		
		
		if(x+yellow_ship.get_width()<WIDTH and y+yellow_ship.get_height()<HEIGHT and (x>0 and y>0)):
			continue
			
		if(x+yellow_ship.get_width()>= WIDTH):
			x = WIDTH - yellow_ship.get_width()
		if(x<=0):
			x=0			
		if(y+yellow_ship.get_height() >= HEIGHT):
			y = WIDTH - yellow_ship.get_height()
		
		if(y<=0):
			y=0
		
		
		
		
			
	pygame.quit()
	
	
main(screen)
