import pygame
from player import Data
from support import import_folder
from player import Player

class P(Player):
	def __init__(self,groups,obstacle_sprites, create_attack, destroy_attack, destroy_attack_p, create_attack_p,network):
		super().__init__((2000,1430),groups,obstacle_sprites, create_attack, destroy_attack,network)
		
		self.create_attack_p = create_attack_p
		self.destroy_attack_p = destroy_attack_p
		self.timer_attack = False
  
	def recv_data(self,data:Data):
		#imported information
		(x,y) = data.position
		self.pos2.x = x
		self.pos2.y = y  
		self.status = data.status
 
	def update(self):
		self.hitbox.x = self.pos2.x
		self.hitbox.y = self.pos2.y
		self.rect.center = self.hitbox.center
		self.animate()
		self.timer()
		if 'attack' in self.status:
			self.create_attack_p()
			self.timer_attack = True
	
	def timer (self):
		start_ticks = pygame.time.get_ticks()
		if self.timer_attack:
			while True: # mainloop
				seconds = (pygame.time.get_ticks()-start_ticks)/1000 #calculate how many seconds
				if seconds>0.15: # if more than 10 seconds close the game
					self.destroy_attack_p()
					break
 