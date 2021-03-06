import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
from math import cos, sin, pi, atan2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (136,136,136)
BACKGROUND = (0, 255, 255)
ZCOLOR = (255, 216, 160)

background=pygame.image.load('welcome.png')
winnerimg =pygame.image.load('winner.png')
goimg =pygame.image.load('gameover.png')

colors = {
  "1": (255, 0, 0),
  "2": (0, 255, 0),
  "3": (0, 0, 255)
}


hand = pygame.image.load('./player.png')

texturesM = {
	"1": pygame.image.load('./wallM1.png'),
	"2": pygame.image.load('./wallM2.png'),
	"3": pygame.image.load('./wallM3.png'),
	"4": pygame.image.load('./wallM4.png'),
	"5": pygame.image.load('./wallM5.png'),
}

texturesZ = {
	"1": pygame.image.load('./wallZ1.png'),
	"2": pygame.image.load('./wallZ2.png'),
	"3": pygame.image.load('./wallZ3.png'),
	"4": pygame.image.load('./wallZ4.png'),
	"5": pygame.image.load('./wallZ5.png'),
	"6": pygame.image.load('./wallZ6.png'),
	"7": pygame.image.load('./wallZ7.png'),
}

texturesP = {
	"1": pygame.image.load('./wallP1.png'),
	"2": pygame.image.load('./wallP2.png'),
	"3": pygame.image.load('./wallP3.png'),
	"4": pygame.image.load('./wallP1.png'),
	"5": pygame.image.load('./wallP1.png'),
	"6": pygame.image.load('./wallP1.png'),
	"7": pygame.image.load('./wallP1.png'),
}

enemiesM = [
	{
		"x": 80,
		"y": 150,
		"texture": pygame.image.load('./jump.png')
	},
	{
		"x": 500,
		"y": 80,
		"texture": pygame.image.load('./castleM.png')
	},
	{
		"x": 500,
		"y": 600,
		"texture": pygame.image.load('./coinM.png')
	},
	{
		"x": 208,
		"y": 174,
		"texture": pygame.image.load('./coinM.png')
	},
	{
		"x": 344,
		"y": 262,
		"texture": pygame.image.load('./enemyM.png')
	}
]

enemiesZ = [
	{
		"x": 315,
		"y": 275,
		"texture": pygame.image.load('./linkZ.png')
	},
	{
		"x": 300,
		"y": 170,
		"texture": pygame.image.load('./keyZ.png')
	},
	{
		"x": 90,
		"y": 350,
		"texture": pygame.image.load('./enemyZ.png')
	}
]

enemiesP = [
	{
		"x": 100,
		"y": 300,
		"texture": pygame.image.load('./enemyP1.png')
	},
	{
		"x": 250,
		"y": 262,
		"texture": pygame.image.load('./enemyP2.png')
	},
	{
		"x": 400,
		"y": 167,
		"texture": pygame.image.load('./enemyP3.png')
	},
	{
		"x": 158,
		"y": 125,
		"texture": pygame.image.load('./enemyP4.png')
	},
	{
		"x": 320,
		"y": 360,
		"texture": pygame.image.load('./cherryP.png')
	}
]

class Raycaster:
	def __init__(self, screen):
		_, _, self.width, self.height = screen.get_rect()
		self.screen = screen
		self.blocksize = 50
		self.map = []
		self.tema = ''
		self.zbuffer = [-float('inf') for z in range(0, 500)]
		self.player = {
		"x": self.blocksize + 20,
		"y": self.blocksize + 20,
		"a": 0,
		"fov": pi/3
		}
		
		
	def point(self, x, y, c = None):
		#se dibuja un punto en x,y con el color c
		screen.set_at((x, y), c)

	def draw_rectangle(self, x, y, texture):
		for cx in range(x, x + 50):
			for cy in range(y, y + 50):
				#texture size 128x128
				tx = int((cx - x) * 128/50)
				ty = int((cy - y) * 128/50)
				c = texture.get_at((tx,ty))
				self.point(cx, cy, c)


	def draw_player(self, xi, yi, w = 256, h = 256):
	    for x in range(xi, xi + w):
	      for y in range(yi, yi + h):
	        tx = int((x - xi) * 32/w)
	        ty = int((y - yi) * 32/h)
	        c = hand.get_at((tx, ty))
	        if c != (152, 0, 136, 255):
	          self.point(x, y, c)

	def load_map(self, filename):
		#se cargan mapas de archivos .txt
		with open(filename) as f:
			for line in f.readlines():
				self.map.append(list(line))

	def cast_ray(self, a):
		d = 0
		while True:
			x = int(self.player["x"] + d*cos(a))
			y = int(self.player["y"] + d*sin(a))

			i = int(x/self.blocksize)
			j = int(y/self.blocksize)

			if self.map[j][i] != ' ':
				hitx = x - i*50
				hity = y - j*50
				if 1 < hitx < 49:
					maxhit = hitx
				else: 
					maxhit = hity
				tx = int(maxhit * 128/50)
				return d, self.map[j][i], tx
			self.point(x, y, WHITE)
			d += 1

	def draw_stake(self, x, h, tx, texture):
		start = int(250 - h/2)
		end = int(250 + h/2)
		for y in range(start, end):
			ty =  int((y - start) * (128 / (end - start)))
			c = texture.get_at((tx, ty))
			self.point(x, y, c)


	def draw_sprite(self, sprite):
		sprite_a = atan2((sprite["y"] - self.player["y"]), (sprite["x"] - self.player["x"]))
		sprite_d = ((self.player["x"] - sprite["x"])**2 +\
	      (self.player["y"] - sprite["y"])**2)**0.5
		sprite_size = int(500/sprite_d * 70)
		sprite_x = int(500 + (sprite_a - self.player["a"]) * 500/self.player["fov"] +\
	       250 - sprite_size/2)
		sprite_y = int(250 - sprite_size/2)

		for x in range(sprite_x, sprite_x + sprite_size):
			for y in range(sprite_y, sprite_y + sprite_size):
				if 500 < x < 1000 and self.zbuffer[x - 500] >= sprite_d:
					tx = int((x - sprite_x) * 128/sprite_size)
					ty = int((y - sprite_y) * 128/sprite_size)
					c = sprite["texture"].get_at((tx, ty))
					if c != (152, 0, 136, 255):
						self.point(x, y, c)
						self.zbuffer[x - 500] = sprite_d


	"""def render(self):
		for x in range(0, self.width, self.blocksize):
			for y in range(0, self.height, self.blocksize):
				i = int(x/self.blocksize)
				j = int(y/self.blocksize)
				if self.map[j][i] != ' ':
					self.draw_rectangle(x, y, (255, 0, 0))"""

	def render(self):
		#dibuja la vista desde arriba
		if self.tema == "mario":
			textures = texturesM
			enemies = enemiesM
		if self.tema == "zelda":
			textures = texturesZ
			enemies = enemiesZ
		if self.tema == "pacman":
			textures = texturesP
			enemies = enemiesP

		for x in range(0, int(self.width / 2), self.blocksize):
			for y in range(0, self.height, self.blocksize):
				i = int(x/self.blocksize)
				j = int(y/self.blocksize)
				if self.map[j][i] != ' ':
					self.draw_rectangle(x, y, textures[self.map[j][i]])

		self.point(self.player["x"], self.player["y"], WHITE)

		# dibuja la vista de primera persona
		for i in range(0, 500):
			a =  self.player["a"] - self.player["fov"]/2 + (i * self.player["fov"] / 500)
			d, m, tx = self.cast_ray(a)
			self.zbuffer[i] = d
			x = 500 + i
			h = (500 /(d * cos(a - self.player["a"]))) * 50
			self.draw_stake(x, h, tx, textures[m])

		for i in range(0, 500):
			self.point(499, i, (0,0,0))
			self.point(500, i, (0,0,0))
			self.point(501, i, (0,0,0))

		for enemy in enemies:
			self.point(enemy["x"], enemy["y"], BLACK)
			self.draw_sprite(enemy)

		self.draw_player(1000 - 256 - 128, 500 - 256)

	
	def text_objects(self, text, font):
	    textSurface = font.render(text, True, BLACK)
	    return textSurface, textSurface.get_rect()

	def updateFPS(self, color):
		font = pygame.font.Font(None, 25)
		fps = "FPS: " + str(int(clock.get_fps()))
		fps = font.render(fps, 1, color)
		return fps

	def winner_sound(self):
		pygame.mixer.music.load('./tada.mp3')
		pygame.mixer.music.set_volume(0.8)
		pygame.mixer.music.play(0)

	def loser_sound(self):
		pygame.mixer.music.load('./loser.mp3')
		pygame.mixer.music.set_volume(0.8)
		pygame.mixer.music.play(0)

	def game_music(self):
		pygame.mixer.music.load('./never.mp3')
		pygame.mixer.music.set_volume(0.8)
		pygame.mixer.music.play(0)

	def game_intro(self):
	    intro = True
	    r.game_music()
	    while intro:
	        for event in pygame.event.get():
	            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
	                exit(0)
	            if event.type == pygame.KEYDOWN:
	            	if event.key == pygame.K_1:
	            		intro = False
	            		self.tema = "mario"
	            		self.game_start_mario()
	            	if event.key == pygame.K_2:
	            		intro = False
	            		self.tema = "zelda"
	            		self.game_start_zelda()
	            	if event.key == pygame.K_3:
	            		intro = False
	            		self.tema = "pacman"
	            		self.game_start_pacman()
	             
	        screen.blit(background, (0,0))
	        pygame.display.update()
	        clock.tick(15)

	def game_over(self):
	    intro = True
	    r.loser_sound()
	    while intro:
	        for event in pygame.event.get():
	            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
	                exit(0)
	            if event.type == pygame.KEYDOWN:
	            	if event.key == pygame.K_0:
	            		intro =False
	            		self.game_intro()
	                
	        screen.blit(goimg, (0,0))
	        pygame.display.update()
	        clock.tick(15)

	def game_win(self):
	    intro = True
	    r.winner_sound()
	    while intro:
	        for e in pygame.event.get():
	            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
	                exit(0)
	            if e.type == pygame.KEYDOWN:
	            	if e.key == pygame.K_0:
	            		intro = False
	            		self.game_intro()
	                
	        screen.blit(winnerimg, (0,0))
	        pygame.display.update()
	        clock.tick(15)

	def game_start_mario(self):
		self.load_map('./mapMario.txt')
		reloj = pygame.time.Clock()
 
		# Esta es la fuente que usaremos para el textoo que aparecerá en pantalla (tamaño 25)
		fuente = pygame.font.Font(None, 25)
		fuentep = pygame.font.Font(None, 100)
		numero_de_fotogramas = 0
		tasa_fotogramas = 60
		instante_de_partida = 5

		paused  = False
		running = True
		while running:
			screen.fill((0,0,0))
			d = 10
			for e in pygame.event.get():
				if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
					running = False
					exit(0)
				if e.type == pygame.KEYDOWN:
					if e.key == pygame.K_LEFT:
						r.player["a"] -= pi/20
					if e.key == pygame.K_RIGHT:
						r.player["a"] += pi/20
					if e.key == pygame.K_UP:
						r.player["x"] += int(d * cos(r.player["a"]))
						r.player["y"] += int(d * sin(r.player["a"]))
					if e.key == pygame.K_DOWN:
						r.player["x"] -= int(d * cos(r.player["a"]))
						r.player["y"] -= int(d * sin(r.player["a"]))
					if e.key == pygame.K_p:
						paused = not paused
						texto_paused = "Paused"
						textoPp = fuentep.render(texto_paused, True, WHITE)
						screen.blit(textoPp, [375,int(500/2)])
						pygame.display.update()
						clock.tick(15)
					if (r.player["x"] > 318) and (r.player["y"] > 380):
						r.player["x"] = 70
						r.player["y"] = 70
						self.game_win()
					print(r.player["x"],r.player["y"])
				if e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.MOUSEBUTTONUP:
					if not paused:
						if e.button == 4:
							r.player["a"] -= pi/20
						if e.button == 5:
							r.player["a"] += pi/20
			if not paused:
				segundos_totales = numero_de_fotogramas // tasa_fotogramas
				minutos = segundos_totales // 60
				segundos = segundos_totales % 60
				texto_de_salida = "Time: {0:02}:{1:02}".format(minutos, segundos)
				texto = fuente.render(texto_de_salida, True, WHITE)
				segundos_totales = instante_de_partida - (numero_de_fotogramas // tasa_fotogramas)
				if segundos_totales < 0:
					segundos_totales = 0
				minutos = segundos_totales // 60
				segundos = segundos_totales % 60
				if segundos == 0:
					self.game_over()
				texto_de_salida = "Time left: {0:02}:{1:02}".format(minutos, segundos)
				texto = fuente.render(texto_de_salida, True, WHITE)
				screen.blit(texto, [300, 420])
				texto_de_pausa = "Press P to pause"
				textoP = fuente.render(texto_de_pausa, True, WHITE)
				screen.blit(textoP, [800, 50])
				screen.blit(self.updateFPS(WHITE), (300, 390)) #el FPS del juego
				r.render()
				numero_de_fotogramas += 1
				reloj.tick(20)
				pygame.display.flip()
			"""screen.blit(counting_text, counting_rect)
			pygame.display.update()
			clock.tick(25)
			r.render()
			pygame.display.flip()"""

	def game_start_zelda(self):
		self.load_map('./mapZelda.txt')
		reloj = pygame.time.Clock()
		r.player["x"] = 80
		r.player["y"] = 176

		fuente = pygame.font.Font(None, 25)
		fuentep = pygame.font.Font(None, 100)
		numero_de_fotogramas = 0
		tasa_fotogramas = 60
		instante_de_partida = 5

		paused  = False
		running = True
		while running:
			screen.fill(ZCOLOR)
			d = 10
			for e in pygame.event.get():
				if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
					running = False
					exit(0)
				if e.type == pygame.KEYDOWN:
					if e.key == pygame.K_LEFT:
						r.player["a"] -= pi/20
					if e.key == pygame.K_RIGHT:
						r.player["a"] += pi/20
					if e.key == pygame.K_UP:
						r.player["x"] += int(d * cos(r.player["a"]))
						r.player["y"] += int(d * sin(r.player["a"]))
					if e.key == pygame.K_DOWN:
						r.player["x"] -= int(d * cos(r.player["a"]))
						r.player["y"] -= int(d * sin(r.player["a"]))
					if e.key == pygame.K_p:
						paused = not paused
						texto_paused = "Paused"
						textoPp = fuentep.render(texto_paused, True, WHITE)
						screen.blit(textoPp, [375,int(500/2)])
						pygame.display.update()
						clock.tick(15)
					if (r.player["x"] > 317) and (r.player["y"] > 210):
						r.player["x"] = 70
						r.player["y"] = 70
						self.game_win()
					print(r.player["x"],r.player["y"])
				if e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.MOUSEBUTTONUP:
					if not paused:
						if e.button == 4:
							r.player["a"] -= pi/20
						if e.button == 5:
							r.player["a"] += pi/20
			if not paused:
				segundos_totales = numero_de_fotogramas // tasa_fotogramas
				minutos = segundos_totales // 60
				segundos = segundos_totales % 60
				texto_de_salida = "Time: {0:02}:{1:02}".format(minutos, segundos)
				texto = fuente.render(texto_de_salida, True, WHITE)
				segundos_totales = instante_de_partida - (numero_de_fotogramas // tasa_fotogramas)
				if segundos_totales < 0:
					segundos_totales = 0
				minutos = segundos_totales // 60
				segundos = segundos_totales % 60
				if segundos == 0:
					r.player["x"] = 80
					r.player["y"] = 176
					self.game_over()
				texto_de_salida = "Time left: {0:02}:{1:02}".format(minutos, segundos)
				texto = fuente.render(texto_de_salida, True, BLACK)
				screen.blit(texto, [270, 370])
				texto_de_pausa = "Press P to pause"
				textoP = fuente.render(texto_de_pausa, True, BLACK)
				screen.blit(textoP, [800, 50])
				screen.blit(self.updateFPS(BLACK), (270, 350)) #el FPS del juego
				r.render()
				numero_de_fotogramas += 1
				reloj.tick(20)
				pygame.display.flip()
			"""screen.blit(counting_text, counting_rect)
			pygame.display.update()
			clock.tick(25)
			r.render()
			pygame.display.flip()"""

	def game_start_pacman(self):
		self.load_map('./mapPacman.txt')
		reloj = pygame.time.Clock()
		r.player["x"] = 70
		r.player["y"] = 70

		fuente = pygame.font.Font(None, 25)
		fuentep = pygame.font.Font(None, 100)
		numero_de_fotogramas = 0
		tasa_fotogramas = 60
		instante_de_partida = 5

		paused  = False
		running = True
		while running:
			screen.fill(BLACK)
			d = 10
			for e in pygame.event.get():
				if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
					running = False
					exit(0)
				if e.type == pygame.KEYDOWN:
					if e.key == pygame.K_LEFT:
						r.player["a"] -= pi/20
					if e.key == pygame.K_RIGHT:
						r.player["a"] += pi/20
					if e.key == pygame.K_UP:
						r.player["x"] += int(d * cos(r.player["a"]))
						r.player["y"] += int(d * sin(r.player["a"]))
					if e.key == pygame.K_DOWN:
						r.player["x"] -= int(d * cos(r.player["a"]))
						r.player["y"] -= int(d * sin(r.player["a"]))
					if e.key == pygame.K_p:
						paused = not paused
						texto_paused = "Paused"
						textoPp = fuentep.render(texto_paused, True, WHITE)
						screen.blit(textoPp, [375,int(500/2)])
						pygame.display.update()
						clock.tick(15)
					if (r.player["x"] > 310) and (r.player["y"] > 360):
						r.player["x"] = 70
						r.player["y"] = 70
						self.game_win()
					print(r.player["x"],r.player["y"])
				if e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.MOUSEBUTTONUP:
					if not paused:
						if e.button == 4:
							r.player["a"] -= pi/20
						if e.button == 5:
							r.player["a"] += pi/20
			if not paused:
				segundos_totales = numero_de_fotogramas // tasa_fotogramas
				minutos = segundos_totales // 60
				segundos = segundos_totales % 60
				texto_de_salida = "Time: {0:02}:{1:02}".format(minutos, segundos)
				texto = fuente.render(texto_de_salida, True, WHITE)
				segundos_totales = instante_de_partida - (numero_de_fotogramas // tasa_fotogramas)
				if segundos_totales < 0:
					segundos_totales = 0
				minutos = segundos_totales // 60
				segundos = segundos_totales % 60
				if segundos == 0:
					r.player["x"] = 70
					r.player["y"] = 70
					self.game_over()
				texto_de_salida = "Time left: {0:02}:{1:02}".format(minutos, segundos)
				texto = fuente.render(texto_de_salida, True, WHITE)
				screen.blit(texto, [270, 360])
				texto_de_pausa = "Press P to pause"
				textoP = fuente.render(texto_de_pausa, True, WHITE)
				screen.blit(textoP, [800, 50])
				screen.blit(self.updateFPS(WHITE), (270, 380)) #el FPS del juego
				r.render()
				numero_de_fotogramas += 1
				reloj.tick(20)
				pygame.display.flip()
			"""screen.blit(counting_text, counting_rect)
			pygame.display.update()
			clock.tick(25)
			r.render()
			pygame.display.flip()"""

pygame.init()
screen = pygame.display.set_mode((1000, 500))
screen.set_alpha(None)
r = Raycaster(screen)
gameDisplay = pygame.display.set_mode((1000,500))
pygame.display.set_caption('Camila')
clock = pygame.time.Clock()
r.game_intro()
#render loop
"""while True:
	screen.fill((0,0,0))
	d = 10
	for e in pygame.event.get():
		if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
			exit(0)
		if e.type == pygame.KEYDOWN:
			if e.key == pygame.K_LEFT:
				r.player["a"] -= pi/20
			if e.key == pygame.K_RIGHT:
				r.player["a"] += pi/20
			if e.key == pygame.K_UP:
				r.player["x"] += int(d * cos(r.player["a"]))
				r.player["y"] += int(d * sin(r.player["a"]))
			if e.key == pygame.K_DOWN:
				r.player["x"] -= int(d * cos(r.player["a"]))
				r.player["y"] -= int(d * sin(r.player["a"]))
	r.render()
	pygame.display.flip()"""

