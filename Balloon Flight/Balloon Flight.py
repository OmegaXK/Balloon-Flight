#Balloon Flight

import pygame, sys, random
from pygame.locals import *

pygame.init()

#Create the window
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Balloon Flight')

FPSCLOCK = pygame.time.Clock()

#Set up the variables for the obstacles
housex = random.randint(800, 1600)
treex = random.randint(800, 1600)
bup = True
birdx = random.randint(800, 1600)
birdy = random.randint(10, 200)
birdframe = 0

#Load assets
bgimg = pygame.image.load(r"images/background.png")
bgimg = pygame.transform.scale(bgimg, (WINDOWWIDTH, WINDOWHEIGHT))

balloonimg = pygame.image.load(r"images/balloon.png")
balloonrect = balloonimg.get_rect()
balloonrect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)

houseimg = pygame.image.load(r"images/house.png")
houserect = houseimg.get_rect()
houserect.center = (housex, 460)

treeimg = pygame.image.load(r"images/tree.png")
treerect = treeimg.get_rect()
treerect.center = (treex, 450)

birdup = pygame.image.load(r"images/bird-up.png")
birddown = pygame.image.load(r"images/bird-down.png")
birdrect = birdup.get_rect()
birdrect.center = (birdx, birdy)
costume = ''

#Colors
BLACK = (0, 0, 0)

#Game constants
fps = 60
balloony = WINDOWHEIGHT / 2
BASICFONT = 'freesansbold.ttf'

def main():
	global balloony, up, score, costume, birdframe, game_over, housex, treex, birdx, birdy, birdframe, score

	#Game variables
	game_over = False
	score = 0
	bup = True
	birdx = random.randint(800, 1600)
	birdy = random.randint(10, 200)
	birdframe = 0
	balloony = WINDOWHEIGHT / 2
	up = False

	#Position tree
	treex = random.randint(800, 1600)
	treerect.center = (treex, 450)
	while treerect.colliderect(houserect):
		treex = random.randint(800, 1600)
		treerect.center = (treex, 450)

	#Position house
	housex = random.randint(800, 1600)
	houserect.center = (housex, 460)
	while houserect.colliderect(treerect):
		housex = random.randint(800, 1600)
		houserect.center = (housex, 460)

	#Game loop
	while True:
		if game_over == False:
			DISPLAYSURF.blit(bgimg, (0, 0))
			for event in pygame.event.get(): #Event handling loop
				if event.type == QUIT:
					terminate()
				if event.type == KEYUP:
					if event.key == K_ESCAPE:
						terminate()
					if event.key == K_SPACE:
						up = False

				if event.type == KEYDOWN:
					if event.key == K_SPACE:
						up = True
						balloony -= 50
				
				if event.type == MOUSEBUTTONDOWN:
					up = True
					balloony -= 50
				if event.type == MOUSEBUTTONUP:
					up = False

			#Position and display all sprites
			ballooncontrol()
			balloonrect.center = (WINDOWWIDTH / 2, balloony)
			DISPLAYSURF.blit(balloonimg, balloonrect)

			housecontrol()
			houserect.center = (housex, 460)
			DISPLAYSURF.blit(houseimg, houserect)

			treecontrol()
			treerect.center = (treex, 450)
			DISPLAYSURF.blit(treeimg, treerect)

			getcostume()
			birdcontrol()
			bcostume = costume
			birdrect = bcostume.get_rect()
			birdrect.center = (birdx, birdy)
			DISPLAYSURF.blit(bcostume, birdrect)

			#Add text to display the score
			drawtext('Score: ' + str(score), BASICFONT, 25, DISPLAYSURF, 700, 15, BLACK)

			pygame.display.update()
			FPSCLOCK.tick(fps)

		else:
			break

	return


def update_high_scores():
	#Adds your score to the leaderboard if it is a high score
	global score, scores
	filename = r"balloon flight high-scores.txt"
	scores = []
	with open(filename, "r") as file:
		line = file.readline()
		high_scores = line.split()
		for high_score in high_scores:
			if (score > int(high_score)):
				scores.append(str(score) + " ")
				score = int(high_score)
			else:
				scores.append(str(high_score) + " ")

	with open(filename, "w") as file:
		for high_score in scores:
			file.write(high_score)


def display_high_scores():
	global scores
	drawtext("HIGH SCORES", BASICFONT, 40, DISPLAYSURF, 400, 150, BLACK)
	y = 225
	position = 1
	#Draw the leaderboard
	for high_score in scores:
		drawtext(str(position) + ". " + high_score, BASICFONT, 40, DISPLAYSURF, 400, y, BLACK)
		#Increase y and position so the next score is displayed correctly
		y += 50
		position += 1


def getcostume():
	#Sets the bird's costume
	global costume
	if bup:
		costume = birdup
	else:
		costume = birddown


def birdcontrol():
	global score, birdx, birdy, birdframe

	#Bird flaps every 9 frames
	if birdx > 0:
		birdx -= 4
		if birdframe == 9:
			flap()
			birdframe = 0
		else:
			birdframe += 1
	else:
		#Bird flew offscreen
		birdx = random.randint(800, 1600)
		birdy = random.randint(10, 200)
		score += 1
		birdframe = 0


def flap():
	#Change the bird's costume to make it look like it's flapping it's wings
	global bup, costume, birdup, birddown
	if bup:
		costume = birddown
		bup = False
	else:
		costume = birdup
		bup = True


def ballooncontrol():
	global balloony, game_over

	#Move the bird down if up is false
	if not up:
		balloony += 1

	#Check if the balloon is offscreen
	if balloonrect.top < -65 or balloonrect.bottom > 560:
		balloony = 300
		game_over = True

	#Check if the balloon has collided with any obstacles
	if balloonrect.collidepoint(birdx, birdy) or \
	balloonrect.collidepoint(housex, houserect.y) or \
	balloonrect.collidepoint(treex, treerect.y):
		game_over = True

 
def housecontrol():
	global housex, score, houserect
	
	#If the house is on the screen, then move it left
	if houserect.right > 0:
		housex -= 2
	else:
		#House went offscreen
		housex = random.randint(800, 1600)
		houserect.center = (housex, 460)
		while houserect.colliderect(treerect):
			housex = random.randint(800, 1600)
			houserect.center = (housex, 460)
		score += 1


def treecontrol():
	global treex, score, treerect

	#If the tree is on the screen, then move it left
	if treerect.right > 0:
		treex -= 2
	else:
		#Tree went offscreen
		treex = random.randint(800, 1600)
		treerect.center = (treex, 450)
		while treerect.colliderect(houserect):
			treex = random.randint(800, 1600)
			treerect.center = (treex, 450)
		score += 1
		

def terminate():
	pygame.quit()
	sys.exit()


def drawtext(text, font, size, surface, x, y, color):
    fontobj = pygame.font.Font(font, size)
    textobj = fontobj.render(text, size, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)


def gameover():
	#Fill the screen black so you can't see the sprites, then add the background image
	DISPLAYSURF.fill(BLACK)
	DISPLAYSURF.blit(bgimg, (0, 0))
	update_high_scores()
	display_high_scores()
	drawtext('Game Over', BASICFONT, 60, DISPLAYSURF, 400, 40, BLACK)
	drawtext('Press "r" to restart, or press "q" to quit.', BASICFONT, 25, DISPLAYSURF, 400, 500, BLACK)
	target = ''
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
			if event.type == KEYUP:
				if event.key == K_ESCAPE or event.key == K_q: 
					terminate()
				if event.key == K_r:
					target = 'restart' #Set the target to "restart" so the function knows to stop
					break

		if target == 'restart':
			return

		pygame.display.update()
		FPSCLOCK.tick(fps)


def rungame():
	main()
	gameover()


if __name__ == '__main__':
	while True:
		rungame()