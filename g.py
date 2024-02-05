# Import the pygame library
from pygame import mixer
import pygame, random

from sys import exit

# Necessary Step! Initiates all of the parts of the Pygame library.
pygame.init()

# Create Screen - a display surface
screen_width = 800
screen_height = 300
screen = pygame.display.set_mode((screen_width,screen_height))

# Add a label to the pygame window
pygame.display.set_caption("Intro to Pygame: Platform Game")

# Create Clock object - responsible for controlling the games frame rate
clock = pygame.time.Clock() # create a clock object


class Background(pygame.sprite.Sprite):
	def __init__(self, image_path, x, y, speed):
		super().__init__()
		self.x = x
		self.y = y
		self.speed = speed
		self.image = pygame.image.load(image_path)
		self.rect = self.image.get_rect(center = (self.x, self.y))

	def move_right(self):
		if self.rect.centerx > 1200:
			self.x = -400
			self.rect.centerx = self.x
		self.x += self.speed
		self.rect.centerx = self.x

	def move_left(self):
		if self.rect.centerx < -400:
			self.x = 1200
			self.rect.center = (self.x,self.y)
		self.x -= self.speed
		self.rect.center = (self.x,self.y)

class Player(pygame.sprite.Sprite):
	def __init__(self,x,y,anti):
		super(Player,self).__init__()
		self.anti=anti
		self.x = x
		self.y = y
		self.index = 0
		self.direction = "right"
		self.jump_count = 0
		self.fall_count = 0
		self.stans=pygame.image.load("graphics/player_stand.png").convert_alpha()
		self.jump_image = pygame.image.load("graphics/jump.png").convert_alpha()
		self.files = ["graphics/player_walk_1.png", "graphics/player_walk_2.png"]
		self.images = [pygame.image.load(filename).convert_alpha() for filename in self.files]
		self.pics = [[pygame.transform.flip(self.stans,False, self.anti)],[pygame.transform.flip(img, True, self.anti) for img in self.images],[pygame.transform.flip(self.jump_image,True,self.anti)], [pygame.transform.flip(img, False, self.anti) for img in self.images],[pygame.transform.flip(self.jump_image,False,self.anti)]]
		self.image = self.pics[0][0]
		self.rect = self.image.get_rect(center = (self.x, self.y))
	def move(self, deltax):
		if self.rect.left < 0 or self.rect.right>800:
			deltax *= -3
		self.rect.centerx += deltax
		if deltax>0:
			self.direction = "right"
			self.index = (self.index +1)%2
			self.image = self.pics[3][self.index]
		else:
			self.direction = "left"
			self.index = (self.index +1)%2
			self.image = self.pics[1][self.index]
	def stand(self):
		self.image = self.pics[0][0]
	
	def jump(self, group):
		if self.direction == "right":
			self.image = self.pics[4][0]
		else:
			self.image = self.pics[2][0]

		if self.jump_count < 20:
			self.y -= (20-(self.jump_count))
			self.rect.centery = self.y
		self.jump_count += 1

		
	def gravity(self): # this needs to be updated to stop on heads
		self.y += (self.fall_count/1.5)
		self.rect.centery = self.y
		if self.rect.centery > 300:
			self.kill()
			print("Death")
		self.fall_count+=1





class Ball(pygame.sprite.Sprite):
	def __init__(self,x,y,color):
		super(Ball,self).__init__()
		self.x = x
		self.y = y
		self.fall_count=0
		self.jump_count=0
		self.radius = 10
		self.color= color
		print("HEY")
		self.vx=0
		self.vy=0
		self.image = pygame.Surface((self.radius*2,self.radius*2),pygame.SRCALPHA,32)
		self.image = self.image.convert_alpha()
		pygame.draw.circle(self.image,self.color,(self.radius,self.radius),self.radius)
		self.rect = self.image.get_rect(center = (self.x, self.y))
	
	def jump(self,viy):
		while self.jump_count < 10:
			print("AAAAAH")
			self.x+=self.vx
			if self.vx<0:
				self.vx+=1
			elif self.vx>0:
				self.vx-=1
			self.vy=viy-self.jump_count
			self.y += self.vy
			self.rect.centery = self.y
			self.jump_count += 1

		
	def gravity(self): # this needs to be updated to stop on heads
		self.y += (self.fall_count/1.5)
		self.rect.centery = self.y
		if self.rect.centery > 300:
			self.kill()
			print("Death")
		self.fall_count+=1


'''
Groups
'''
background = pygame.sprite.Group() # Contains images of the blue sky and mountains
background.add(Background("graphics/Sky.png",-400,150, 4))
background.add(Background("graphics/Sky.png",400,150, 4))
background.add(Background("graphics/Sky.png",1200,150, 4))


land = pygame.sprite.Group() # Contains the platform images that the player run/walks on
land.add(Background("graphics/ground.png",325,325,8))
land.add(Background("graphics/short_ground.png",1100,325,8))

scenery = pygame.sprite.Group() # Contains both the background and platform images
scenery.add(background)
scenery.add(land)

player = Player(200,50,True)
p=Player(100,50,False)
b=Ball(300,50,(250,0,0,255))

all_sprites = pygame.sprite.Group() #contains all surfaces

all_sprites.add(scenery)
all_sprites.add(player)
all_sprites.add(p)
all_sprites.add(b)

while True:
	#Event loop - Looks for for user input which could include: key presses, mouse movement, mouse clicks, etc.
	for event in pygame.event.get():
		# Close game if the red square in the top left of the window is clicked
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		# Actions that the player takes when the user lifts finger from keys
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_RIGHT:
				player.stand()
			if event.key == pygame.K_LEFT:
				player.stand()
			if event.key == pygame.K_UP:
				player.stand()
			if event.key == pygame.K_d:
				p.stand()
			if event.key == pygame.K_a:
				p.stand()
			if event.key == pygame.K_w:
				p.stand()
	# Actions that the player and scenery take when the user presses particular keys	
	keys = pygame.key.get_pressed()
	if keys[pygame.K_RIGHT]:
		#for s in scenery:
		#	s.move_left()	
		player.move(5)	
	if keys[pygame.K_LEFT]:
		#for s in scenery:
		#	s.move_right()
		player.move(-5)
	if keys[pygame.K_UP]:
		#player.jump_count+=1
		player.jump(land)
	if keys[pygame.K_d]:
		#for s in scenery:
		#	s.move_left()
		p.move(5)	
	if keys[pygame.K_a]:
		#for s in scenery:
		#	s.move_right()
		p.move(-5)
	if keys[pygame.K_w]:
		# player.jump_count+=1
		p.jump(land)
	






	


	# The player falls if it is not touch a platform
	if not (pygame.sprite.spritecollide(player,land,False) or (player.rect.colliderect(p.rect))):
		player.gravity()
	else:
		player.jump_count = 0
		player.fall_count = 0
	if not (pygame.sprite.spritecollide(p,land,False) or (p.rect.colliderect(player.rect))):
		p.gravity()
	else:
		p.jump_count = 0
		p.fall_count = 0
	

	if pygame.sprite.spritecollide(b,land,False):
		b.jump_count=0
		b.fall_count=0
		b.jump(b.vy)
		print("gROUNd")
	if b.rect.colliderect(p.rect):
		if p.jump_count<20:
			b.jump_count=0
			b.fall_count=0
			b.vy+=20-p.jump_count
			b.jump(b.vy)
		else:
			b.jump_count=0
			b.fall_count=0
			b.jump(b.vy)
	if b.rect.colliderect(player.rect):
		if player.jump_count<20:
			b.jump_count=0
			b.fall_count=0
			b.vy+=20-player.jump_count
			b.jump(b.vy)
		else:
			b.jump_count=0
			b.fall_count=0
			b.jump(b.vy)
	else:
		b.gravity()
		print("AIR")
			
    # Blits all surfaces to screen
	all_sprites.draw(screen)

	# Updates all of the images and objects on the screen (display surface)
	pygame.display.update()

	#Setting the game's frame rate to 60 frames per second
	clock.tick(30)
