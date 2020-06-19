import pygame
import sys
import math
import os.path
from os import path
from random import randint
import tkinter as tk
from tkinter import messagebox

SIZE = 45
OFFSET = 60
VOLUME_ON = True

class Canvas():
	def __init__(self, snake, size, width, height, offset):
		self.offset = offset
		self.width = width 
		self.height = height - self.offset 
		self.size = size
		self.square_width = self.square_height = self.width // self.size
		self.coords = snake.GetCoords()


	def DrawCanvas(self, canvas, background_color, gradient_color, snake_color, food_color, offset, food_coords, font, snake_length, highscore):
		global VOLUME_ON
		canvas.fill(background_color)
		start_button = pygame.Rect((canvas.get_width() // 2 - 40, 10), (80, 40))
		pygame.draw.rect(canvas, gradient_color, start_button)
		start_button_textsurface = pygame.font.SysFont("Arial", 25).render("Start", False, (255, 255, 255))
		canvas.blit(start_button_textsurface, (canvas.get_width() // 2 - 27, 15))
		mute_button = pygame.Rect((canvas.get_width() // 2 + 22 * self.square_width - 50, 7), (40, 40))
		if VOLUME_ON:
			mute_button_image = pygame.image.load("sound_on.png")
		else:
			mute_button_image = pygame.image.load("sound_off.png")
		canvas.blit(mute_button_image, mute_button)
		score_textsurface = font.render("Score: " + str(snake_length - 1), False, (255, 255, 255))
		canvas.blit(score_textsurface, (canvas.get_width() // 2 - self.width // 2 + 15, 10))
		if highscore >= snake_length - 1:
			highscore_textsurface = font.render('Highscore: ' + str(highscore), False, (255, 255, 255))
		else:
			highscore_textsurface = font.render('Highscore: ' + str(snake_length - 1), False, (255, 255, 255))

		canvas.blit(highscore_textsurface, (canvas.get_width() // 2 - self.width // 2 + 15, 30))
		pygame.draw.rect(canvas, gradient_color, pygame.Rect((canvas.get_width() // 2 - self.width // 2, offset), (self.width, self.height)), 5)
		for coord in self.coords:
			pygame.draw.rect(canvas, snake_color, pygame.Rect((canvas.get_width() // 2 - self.width // 2 + coord[0] * self.square_width + 5, coord[1] * self.square_height + self.offset + 5), (self.square_width, self.square_height)))
		pygame.draw.rect(canvas, food_color, pygame.Rect((canvas.get_width() // 2 - self.width // 2 + food_coords[0] * self.square_width + 5, food_coords[1] * self.square_height + self.offset + 5), (self.square_width, self.square_height)))
		pygame.display.update()

	def GetSquareWidth(self):
		return self.square_width

class Snake():
	def __init__(self, size, offset, highscore):
		self.size = size
		self.highscore = highscore
		self.offset = offset
		self.matrix = [ [0 for i in range(self.size)] for j in range(self.size)]
		self.snake = []
		self.snake_i = randint(0, self.size - 1) 
		self.snake_j = randint(0, self.size - 1) 
		self.head = self.tail = [self.snake_i, self.snake_j]
		self.snake.append([self.snake_i, self.snake_j])
		self.matrix[self.snake[0][0]][self.snake[0][1]] = 1

	def GetFoodCoords(self):
		return [self.food_i, self.food_j]

	def SpawnFood(self):
		while True:	
			self.food_i = randint(0, self.size - 1) 
			self.food_j = randint(0, self.size - 1) 	
			if self.matrix[self.food_i][self.food_j] == 0:
				self.matrix[self.food_i][self.food_j] = 2
				break

	def GetCoords(self):
		return self.snake

	def UpdateSnakeCoords(self, way):
		global running
		global again
		if way == 1:
			if self.head[1] == self.size - 1:
				self.snake.insert(0, [self.head[0], 0])
			else:
				self.snake.insert(0, [self.head[0], self.head[1] + 1])	

		if way == -1:
			if self.head[1] == 0:
				self.snake.insert(0, [self.head[0], self.size - 1])
			else:
				self.snake.insert(0, [self.head[0], self.head[1] - 1])

		if way == -2:
			if self.head[0] == 0:
				self.snake.insert(0, [self.size - 1, self.head[1]])
			else:
				self.snake.insert(0, [self.head[0] - 1, self.head[1]])

		if way == 2:
			if self.head[0] == self.size - 1:
				self.snake.insert(0, [0, self.head[1]])
			else:
				self.snake.insert(0, [self.head[0] + 1, self.head[1]])

		self.head = self.snake[0]
		self.tail = self.snake[len(self.snake) - 2]
		self.matrix[self.head[0]][self.head[1]] = 1
		self.matrix[self.snake[len(self.snake) - 1][0]][self.snake[len(self.snake) - 1][1]] = 0

		if self.head == [self.food_i, self.food_j]:
			self.Eat([self.food_i, self.food_j])

		del self.snake[-1]

		if len(self.snake) != 1:
			for x in range(1, len(self.snake)):
				if self.head == self.snake[x]:
					if VOLUME_ON:
						pygame.mixer.music.stop()
						pygame.mixer.music.set_volume(1)
						pygame.mixer.music.load("you_dead.ogg")
						pygame.mixer.music.play(1000000)
					root = tk.Tk()
					root.withdraw()
					running = False
					msg = messagebox.askyesno("Game Over", "Score: " + str(len(self.snake) - 1) + "\nHighscore: " + (str(self.highscore) if self.highscore > len(self.snake) - 1 else str(len(self.snake) - 1)) + "\nWanna play again?")
					if msg:
						again = True
					else:
						again = False
					root.destroy()
					break

	def GetSnakeLength(self):
		return len(self.snake)

	def Eat(self, food_coords):
		self.snake.append(food_coords)
		self.matrix[food_coords[0]][food_coords[1]] = 1
		self.tail = self.snake[len(self.snake) - 1]
		self.SpawnFood()

running = True
again = True

def LoadMusic():
	pygame.mixer.music.stop()
	pygame.mixer.music.set_volume(0.7)
	pygame.mixer.music.load("music.ogg")
	pygame.mixer.music.play(1000000)

def ToggleMusic():
	global VOLUME_ON
	if VOLUME_ON:
		VOLUME_ON = False
		pygame.mixer.music.pause()
	else:
		VOLUME_ON = True
		pygame.mixer.music.unpause()
	
if __name__ == "__main__":
	pygame.init()
	infoObject = pygame.display.Info()
	pygame.font.init()
	font = pygame.font.SysFont("Arial", 20)
	canvas = pygame.display.set_mode(((infoObject.current_h - OFFSET) // SIZE * SIZE - 80, (infoObject.current_h - OFFSET) // SIZE * SIZE + OFFSET - 80), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
	pygame.display.set_caption("Snake")
	initial_width = width = canvas.get_width()
	initial_height = height = canvas.get_height()
	direction = 1
	hold_time = 30
	while again:
		ok = False
		pygame.key.set_repeat(hold_time)
		if not(path.exists("highscore.txt")):
			highscore_file_w = open("highscore.txt", "w+")
			highscore = 0
			highscore_file_w.write(str(highscore))
		else:
			highscore_file_r = open("highscore.txt", "r")
			highscore = int(highscore_file_r.read()) // 410591994621847176085029512873
			highscore_file_r.close()
		if VOLUME_ON:
			LoadMusic()
		running = True
		time = 100
		length = 0
		snake = Snake(SIZE, OFFSET, highscore)
		snake.SpawnFood()
		cnv = Canvas(snake, SIZE, initial_width, initial_height, OFFSET)
		while running:
			cnv.DrawCanvas(canvas, (0, 0, 0), (200, 0, 0), (0, 255, 0), (102, 0, 102), OFFSET, snake.GetFoodCoords(), font, snake.GetSnakeLength(), highscore)
			for event in pygame.event.get():
				if not(ok) and (event. type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN):
					if (pygame.mouse.get_pos()[0] >= canvas.get_width() // 2 - 30 and pygame.mouse.get_pos()[0] <= canvas.get_width() // 2 + 30 and pygame.mouse.get_pos()[1] >= 10 and pygame.mouse.get_pos()[1] <= 50) or (event.type != pygame.MOUSEBUTTONDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_w or event.key == pygame.K_a or event.key == pygame.K_s or event.key == pygame.K_d)):
						ok = True
				if ok:
					if event.type == pygame.KEYDOWN:
						if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and (direction != -1 or snake.GetSnakeLength() == 1):
							direction = 1
							snake.UpdateSnakeCoords(direction)
							cnv.DrawCanvas(canvas, (0, 0, 0), (200, 0, 0), (0, 255, 0), (102, 0, 102), OFFSET, snake.GetFoodCoords(), font, snake.GetSnakeLength(), highscore)
						if (event.key == pygame.K_UP or event.key == pygame.K_w) and (direction != 1 or snake.GetSnakeLength() == 1):
							direction = -1
							snake.UpdateSnakeCoords(direction)
							cnv.DrawCanvas(canvas, (0, 0, 0), (200, 0, 0), (0, 255, 0), (102, 0, 102), OFFSET, snake.GetFoodCoords(), font, snake.GetSnakeLength(), highscore)
						if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and (direction != 2 or snake.GetSnakeLength() == 1):
							direction = -2
							snake.UpdateSnakeCoords(direction)
							cnv.DrawCanvas(canvas, (0, 0, 0), (200, 0, 0), (0, 255, 0), (102, 0, 102), OFFSET, snake.GetFoodCoords(), font, snake.GetSnakeLength(), highscore)
						if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and (direction != -2 or snake.GetSnakeLength() == 1):
							direction = 2
							snake.UpdateSnakeCoords(direction)
							cnv.DrawCanvas(canvas, (0, 0, 0), (200, 0, 0), (0, 255, 0), (102, 0, 102), OFFSET, snake.GetFoodCoords(), font, snake.GetSnakeLength(), highscore)
				if event.type == pygame.MOUSEBUTTONDOWN:
					if pygame.mouse.get_pos()[0] >= canvas.get_width() // 2 + 22 * cnv.GetSquareWidth() - 50 and pygame.mouse.get_pos()[0] <= canvas.get_width() // 2 + 22 * cnv.GetSquareWidth() and pygame.mouse.get_pos()[1] >= 10 and pygame.mouse.get_pos()[1] <= 50:
						ToggleMusic() 
				if event.type == pygame.QUIT:
					running = False
					again = False
				elif event.type == pygame.VIDEORESIZE:
					width, height = event.size
					if width < 600:
						width = 600
					if height < 400:
						height = 400
					canvas = pygame.display.set_mode((width, height), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)

			if ok:
				if (snake.GetSnakeLength() - 1) % 10 == 0 and length < snake.GetSnakeLength() and time > hold_time:
					length = snake.GetSnakeLength() 
					time -= 10
				if event.type == pygame.KEYDOWN and (event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_w or event.key == pygame.K_a or event.key == pygame.K_s or event.key == pygame.K_d):
					pygame.time.wait(hold_time)
				else:
					pygame.time.wait(time)
				snake.UpdateSnakeCoords(direction)
				cnv.DrawCanvas(canvas, (0, 0, 0), (200, 0, 0), (0, 255, 0), (102, 0, 102), OFFSET, snake.GetFoodCoords(), font, snake.GetSnakeLength(), highscore)	
		
		if snake.GetSnakeLength() - 1 > highscore:
			highscore_file_w = open("highscore.txt", "w")
			highscore_file_w.write(str((snake.GetSnakeLength() - 1) * 410591994621847176085029512873))
			highscore_file_w.close()
