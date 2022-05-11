import pygame, sys
from level import Level
from network import Network
class Game:
	def __init__(self):
		self.net = Network()
		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((1280	,720))
		pygame.display.set_caption('legend of warrior')
		self.clock = pygame.time.Clock()
		#music
		music = pygame.mixer.Sound('audio/mushroom_dance.ogg')
		music.set_volume(0.5)
		music.play(-1)
		
		self.level = Level(self.net) 
	
	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			self.screen.fill('#71DDEE')
			self.level.run()
			pygame.display.update()
			self.clock.tick(60)

if __name__ == '__main__':
	game = Game()
	game.run()