import pygame, sys, random #import thư viện
pygame.init()
clock = pygame.time.Clock()

ok = False

WIDTH = 400 #kích thước màn hình
HEIGHT = 600 #kích thước màn hình
FPS = 60 #FPS của trò chơi
BGSPEED = 1.5 #Di chuyển màn hình chơi

X_MARGIN = 80# kích thước lề đường trái
CARWIDTH = 40# Kích thước chiếc xe
CARHEIGHT = 60# kích thước chiếc xe 
CARSPEED = 3# tốc độ chiếc xe main

LANEWIDTH = 60#chiều dài lề đường
DISTANCE = 200
OBSTACLESSPEED = 2
CHANGESPEED = 0.001

screen = pygame.display.set_mode ((WIDTH, HEIGHT))
pygame.display.set_caption("RACING")

BGIMG = pygame.image.load('img/background.png')
CARIMG = pygame.image.load('img/car.png')
OBSTACLESIMG = pygame.image.load('img/obstacles.png')

class Background():
	def __init__(self):
		self.x = 0
		self.y = 0
		self.img = BGIMG
		self.speed = BGSPEED
		self.width = self.img.get_width()
		self.height = self.img.get_height()
	def draw(self):
		screen.blit(self.img, (int(self.x), int(self.y)))
		screen.blit(self.img, (int(self.x), int(self.y - self.height)))
	def update(self):
		self.y += self.speed
		if (self.y > self.height):
			self.y -= self.height

class Car():
	def __init__(self):
		self.img = CARIMG
		self.width = CARWIDTH
		self.height = CARHEIGHT
		self.x = (WIDTH - self.width)//2
		self.y = (HEIGHT - self.height)//2
		self.speed = CARSPEED
	def draw(self):
		screen.blit(self.img, (int(self.x), int(self.y)))
	def update(self, moveLeft, moveRight, moveUp, moveDown):
		if (moveLeft):
			self.x -= self.speed
		if (moveRight):
			self.x += self.speed
		if (moveUp):
			self.y -= self.speed
		if (moveDown):
			self.y += self.speed 
		if self.x < X_MARGIN:
			self.x = X_MARGIN					
		if self.x + self.width > WIDTH - X_MARGIN:	
			self.x = WIDTH - X_MARGIN - self.width
		if self.y < 0:
			self.y = 0
		if self.y + self.height > HEIGHT:
			self.y = HEIGHT - self.height

class Ob():
	def __init__(self):
		self.width = CARWIDTH
		self.height = CARHEIGHT
		self.distance = DISTANCE
		self.speed = OBSTACLESSPEED
		self.img = OBSTACLESIMG	
		self.changespeed = CHANGESPEED
		self.ds = []
		for i in range(5):
			y = -CARHEIGHT-i*self.distance
			lane = random.randint(0, 3)
			self.ds.append([lane, y])
	def draw(self):
		for i in range(5):
			x = int(X_MARGIN + self.ds[i][0]*LANEWIDTH + (LANEWIDTH-self.width)/2)
			y = int(self.ds[i][1])
			screen.blit(self.img, (x, y))
	def update(self):
		for i in range(5):
			self.ds[i][1] += self.speed
		self.speed += self.changespeed	
		if self.ds[0][1] > HEIGHT:
			self.ds.pop(0)
			y = self.ds[3][1] - self.distance
			lane = random.randint(0, 3)
			self.ds.append([lane, y])

class Score():
	def __init__(self):
		self.score = 0
	def draw(self):
		font = pygame.font.SysFont('consolas', 30)
		scoreSurface = font.render('Score: '+str(int(self.score)), True, (0, 0, 0))
		screen.blit(scoreSurface, (10, 10))
	def update(self):
		self.score += 0.02

def RectCollision(rect1, rect2):
	if rect1[0] <= rect2[0]+rect2[2] and rect2[0] <= rect1[0]+rect1[2] and rect1[1] <= rect2[1]+rect2[3] and rect2[1] <= rect1[1]+rect1[3]:
		return True
	return False
		
def isGameOver(car, ob):
	carRect = [car.x, car.y, car.width, car.height]
	for i in range(5):
		x = int(X_MARGIN + ob.ds[i][0]*LANEWIDTH + (LANEWIDTH-ob.width)/2)
		y = int(ob.ds[i][1])
		obRect = [x, y, ob.width, ob.height]
		if (RectCollision(carRect, obRect)):
			return True
	return False
			
def gameplay(bg, car, ob, score):
	global ok
	moveDown, moveUp, moveRight, moveLeft = False, False, False, False 
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					moveLeft = True
				if event.key == pygame.K_RIGHT:
					moveRight = True
				if event.key == pygame.K_UP:
					moveUp = True
				if event.key == pygame.K_DOWN:
					moveDown = True
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					moveLeft = False
				if event.key == pygame.K_RIGHT:
					moveRight = False
				if event.key == pygame.K_UP:
					moveUp = False
				if event.key == pygame.K_DOWN:
					moveDown = False						
		if isGameOver(car, ob):
			ok = True
			return
		bg.draw()
		bg.update()
		car.draw()
		car.update(moveLeft, moveRight, moveUp, moveDown)
		ob.draw()
		ob.update()
		score.draw()
		score.update()
		pygame.display.update()
		clock.tick(FPS)		

def gameOver(bg, car, obstacles, score):
    global ok
    font = pygame.font.SysFont('consolas', 60)
    headingSuface = font.render('GAMEOVER', True, (255, 0, 0))
    headingSize = headingSuface.get_size()
    font = pygame.font.SysFont('consolas', 20)
    commentSuface = font.render('Press "space" to replay', True, (0, 0, 0))
    commentSize = commentSuface.get_size()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    ok = False
                    return
        bg.draw()
        car.draw()
        obstacles.draw()
        score.draw()
        screen.blit(headingSuface, (int((WIDTH - headingSize[0])/2), 100))
        screen.blit(commentSuface, (int((WIDTH - commentSize[0])/2), 400))
        pygame.display.update()
        clock.tick(FPS)

def gameStart(bg):
    font = pygame.font.SysFont('consolas', 60)
    headingSuface = font.render('RACING', True, (255, 0, 0))
    headingSize = headingSuface.get_size()

    font = pygame.font.SysFont('consolas', 20)
    commentSuface = font.render('Press "space" to play', True, (0, 0, 0))
    commentSize = commentSuface.get_size()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    return
        bg.draw()
        screen.blit(headingSuface, (int((WIDTH - headingSize[0])/2), 100))
        screen.blit(commentSuface, (int((WIDTH - commentSize[0])/2), 400))
        pygame.display.update()
        clock.tick(FPS)

def main():
	bg = Background()
	car = Car()
	ob = Ob()
	score = Score()
	gameStart(bg)
	while True:
		gameplay(bg, car, ob, score)	
		if ok:
			gameOver(bg, car, ob, score)
			bg = Background()
			car = Car()
			ob = Ob()
			score = Score()

if __name__ == '__main__':
	main() 



