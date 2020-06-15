import pygame
import sys
import math
import os.path
from os import path
from random import randint
import tkinter as tk
from tkinter import messagebox

WIDTH = 910
HEIGHT = 970
SIZE = 45
OFFSET = 60

class Canvas():
	def __init__(self, snake, size, width, height, offset):
		self.offset = offset
		self.width = width 
		self.height = height - self.offset 
		self.size = size
		self.square_width = self.square_height = self.width // self.size
		self.coords = snake.GetCoords()


	def DrawCanvas(self, canvas, background_color, gradient_color, snake_color, food_color, offset, food_coords, font, snake_length, highscore):
		canvas.fill(background_color)
		button = pygame.Rect((self.width // 2 - 40, 10), (80, 40))
		pygame.draw.rect(canvas, gradient_color, button)
		button_textsurface = pygame.font.SysFont("Arial", 25).render("Start", False, (255, 255, 255))
		canvas.blit(button_textsurface, (self.width // 2 - 27, 15))
		score_textsurface = font.render("Score: " + str(snake_length - 1), False, (255, 255, 255))
		canvas.blit(score_textsurface, (800, 20))
		if highscore >= snake_length - 1:
			highscore_textsurface = font.render('Highscore: ' + str(highscore), False, (255, 255, 255))
		else:
			highscore_textsurface = font.render('Highscore: ' + str(snake_length - 1), False, (255, 255, 255))

		canvas.blit(highscore_textsurface, (20, 20))
		pygame.draw.rect(canvas, gradient_color, pygame.Rect((0, offset), (self.width, self.height)), 5)
		for coord in self.coords:
			pygame.draw.rect(canvas, snake_color, pygame.Rect((coord[0] * self.square_width + 5, coord[1] * self.square_height + self.offset + 5), (self.square_width, self.square_height)))
		pygame.draw.rect(canvas, food_color, pygame.Rect((food_coords[0] * self.square_width + 5, food_coords[1] * self.square_height + self.offset + 5), (self.square_width, self.square_height)))
		pygame.display.update()


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
		if way == 1:
			if self.head[1] == self.size - 1:
				self.snake.insert(0, [self.head[0], 0])
			else:
				self.snake.insert(0, [self.head[0], self.head[1] + 1])	
			self.head = self.snake[0]			
			self.tail = self.snake[len(self.snake) - 2]
			self.matrix[self.head[0]][self.head[1]] = 1
			self.matrix[self.snake[len(self.snake) - 1][0]][self.snake[len(self.snake) - 1][1]] = 0

		if way == -1:
			if self.head[1] == 0:
				self.snake.insert(0, [self.head[0], self.size - 1])
			else:
				self.snake.insert(0, [self.head[0], self.head[1] - 1])
			self.head = self.snake[0]
			self.tail = self.snake[len(self.snake) - 2]
			self.matrix[self.head[0]][self.head[1]] = 1
			self.matrix[self.snake[len(self.snake) - 1][0]][self.snake[len(self.snake) - 1][1]] = 0

		if way == -2:
			if self.head[0] == 0:
				self.snake.insert(0, [self.size - 1, self.head[1]])
			else:
				self.snake.insert(0, [self.head[0] - 1, self.head[1]])
			self.head = self.snake[0]
			self.tail = self.snake[len(self.snake) - 2]
			self.matrix[self.head[0]][self.head[1]] = 1
			self.matrix[self.snake[len(self.snake) - 1][0]][self.snake[len(self.snake) - 1][1]] = 0

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
					running = False
					root = tk.Tk()
					root.withdraw()
					messagebox.showinfo("Game Over", "Score: " + str(len(self.snake) - 1) + "\nHighscore: " + (str(self.highscore) if self.highscore > len(self.snake) - 1 else str(len(self.snake) - 1)))
					print("Game Over")
					break

	def GetSnakeLength(self):
		return len(self.snake)

	def Eat(self, food_coords):
		self.snake.append(food_coords)
		self.matrix[food_coords[0]][food_coords[1]] = 1
		self.tail = self.snake[len(self.snake) - 1]
		self.SpawnFood()

running = True

if __name__ == "__main__":
	ok = False
	if not(path.exists("highscore.txt")):
		highscore_file_w = open("highscore.txt", "w+")
		highscore = 0
	else:
		highscore_file_r = open("highscore.txt", "r")
		highscore = int(highscore_file_r.read())
	snake = Snake(SIZE, OFFSET, highscore)
	cnv = Canvas(snake, SIZE, WIDTH, HEIGHT, OFFSET)
	snake.SpawnFood()
	pygame.init()
	canvas = pygame.display.set_mode((WIDTH, HEIGHT))
	direction = 1
	time = 100
	hold_time = 30
	length = 0
	pygame.key.set_repeat(hold_time)
	pygame.font.init()
	font = pygame.font.SysFont("Comic Sans MS", 30)
	while running:
		cnv.DrawCanvas(canvas, (0, 0, 0), (200, 0, 0), (0, 255, 0), (102, 0, 102), OFFSET, snake.GetFoodCoords(), font, snake.GetSnakeLength(), highscore)
		for event in pygame.event.get():
			if not(ok) and (event. type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN):
				if (pygame.mouse.get_pos()[0] >= WIDTH // 2 - 30 and pygame.mouse.get_pos()[0] <= WIDTH // 2 + 30 and pygame.mouse.get_pos()[1] >= 10 and pygame.mouse.get_pos()[1] <= 50) or event.key == pygame.K_RETURN:
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
			if event.type == pygame.QUIT:
				running = False

		if ok:
			if (snake.GetSnakeLength() - 1) % 10 == 0 and length < snake.GetSnakeLength() and time > hold_time:
				length = snake.GetSnakeLength() 
				time -= 10
			if event.type == pygame.KEYDOWN:
				pygame.time.wait(hold_time)
			else:
				pygame.time.wait(time)
			snake.UpdateSnakeCoords(direction)
			cnv.DrawCanvas(canvas, (0, 0, 0), (200, 0, 0), (0, 255, 0), (102, 0, 102), OFFSET, snake.GetFoodCoords(), font, snake.GetSnakeLength(), highscore)	
	
	if snake.GetSnakeLength() - 1 > highscore:
		highscore_file_w = open("highscore.txt", "w")
		highscore_file_w.write(str(snake.GetSnakeLength() - 1))
