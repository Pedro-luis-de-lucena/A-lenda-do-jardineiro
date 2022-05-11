import pygame 
from support import import_folder

class Player(pygame.sprite.Sprite):
    	
	def __init__(self,pos,groups,obstacle_sprites,create_attack, destroy_attack, network):
		super().__init__(groups)
		#base
		self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,-26)
    	#network
		self.pos2 = pygame.math.Vector2()
		self.net = network
		
  		#graphics setup
		self.import_player_assets()
		self.status = 'down'
		self.frame_index = 0
		self.animation_speed = 0.15

		# movement 
		self.direction = pygame.math.Vector2()
		self.speed = 5
		self.attacking = False
		self.attack_cooldown = 400
		self.attack_time = None

		self.obstacle_sprites = obstacle_sprites

		#ataque
		self.create_attack = create_attack
		self.destroy_attack = destroy_attack
		self.weapon_index = 0
		self.can_switch_weapon = True
		self.weapon_switch_time = None
		self.switch_duration_cooldown = 200
	# sounds
		pygame.mixer.init()
		pygame.mixer.music.load('audio/sword.wav')
		pygame.mixer.music.set_volume(0.1)

	def import_player_assets(self):
		character_path = 'graphics/player/'
		self.animations = {'up': [],'down': [],'left': [],'right': [],
			'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
			'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[]}

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)

	def input(self):
		if not self.attacking:
			keys = pygame.key.get_pressed()

			# movement input
			if keys[pygame.K_UP]:
				self.direction.y = -1
				self.status = 'up'
			elif keys[pygame.K_DOWN]:
				self.direction.y = 1
				self.status = 'down'
			else:
				self.direction.y = 0

			if keys[pygame.K_RIGHT]:
				self.direction.x = 1
				self.status = 'right'
			elif keys[pygame.K_LEFT]:
				self.direction.x = -1
				self.status = 'left'
			else:
				self.direction.x = 0

			# attack input 
			if keys[pygame.K_SPACE]:
				self.attacking = True
				self.attack_time = pygame.time.get_ticks()
				pygame.mixer.music.play()
				self.create_attack()			


			# magic input 
			
	def get_status(self):
    
		# idle status
		if self.direction.x == 0 and self.direction.y == 0:
			if not 'idle' in self.status and not 'attack' in self.status:
				self.status = self.status + '_idle'

		if self.attacking:
			self.direction.x = 0
			self.direction.y = 0
			if not 'attack' in self.status:
				if 'idle' in self.status:
					self.status = self.status.replace('_idle','_attack')
				else:
					self.status = self.status + '_attack'
		else:
			if 'attack' in self.status:
				self.status = self.status.replace('_attack','')
    
	def move(self,speed):
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

		self.hitbox.x += self.direction.x * speed
		self.collision('horizontal')
		self.hitbox.y += self.direction.y * speed
		self.collision('vertical')
		self.rect.center = self.hitbox.center
		

	def collision(self,direction):
		if direction == 'horizontal':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.x > 0: # moving right
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0: # moving left
						self.hitbox.left = sprite.hitbox.right

		if direction == 'vertical':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.y > 0: # moving down
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0: # moving up
						self.hitbox.top = sprite.hitbox.bottom
	def cooldowns(self):
		current_time = pygame.time.get_ticks()

		if self.attacking:
			if current_time - self.attack_time >= self.attack_cooldown:
				self.attacking = False
				self.destroy_attack()

			

	def animate(self):
		animation = self.animations[self.status]

		# loop over the frame index 
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		# set the image
		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)

	def update(self):
		self.input()
		self.cooldowns()
		self.get_status()
		self.animate()
		self.move(self.speed)
		
	def send_data(self):
		data = Data(self.status,self.hitbox)
		self.reply = self.net.send(data)
		if isinstance(self.reply,Data):
			#data
			(x,y) = (self.reply.position)
			self.pos2.x = x
			self.pos2.y = y 
			return self.reply
		return None
	

class Data:
	def __init__(self,status,hitbox):
		self.status = status
		self.position = (hitbox.x, hitbox.y)