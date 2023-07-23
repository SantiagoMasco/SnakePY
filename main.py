import time

import pygame

snakePositionX = [23]
snakePositionY = [17]
direction = "RIGHT"
def draw_maze(maze, screen, screen_width, screen_height):
    block_size = 25

    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == 1:
                pygame.draw.rect(screen, (255, 255, 255), (col * block_size, row * block_size, block_size, block_size))
            elif maze[row][col] == 2:
                pygame.draw.rect(screen, (0, 0, 255), (col * block_size, row * block_size, block_size, block_size))
            elif maze[row][col] == 3:
                pygame.draw.rect(screen, (0, 255, 0), (col * block_size, row * block_size, block_size, block_size))
            else:
                pygame.draw.rect(screen, (0, 0, 0), (col * block_size, row * block_size, block_size, block_size))

    pygame.display.flip()


def start_game():
    global snakePositionX, snakePositionY, direction

    screen_width = 1200
    screen_height = 900

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("maze")

    with open("maze.txt", "r") as file:
        maze = [[int(cell) for cell in line.strip().split(",")] for line in file if line.strip()]

    running = True

    while running:
        maze[snakePositionY[0]][snakePositionX[0]] = 2
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    if(direction != "DOWN"):
                        direction = "UP"
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    if(direction != "UP"):
                        direction = "DOWN"
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    if(direction != "LEFT"):
                        direction = "RIGHT"
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    if(direction != "RIGHT"):
                        direction = "LEFT"
        move(maze)
        if(running == True):
            draw_maze(maze, screen, screen_width, screen_height)
        if maze[19][28] == 2:
            running = False


        time.sleep(0.1)

    pygame.quit()



def move(maze):
    global snakePositionX, snakePositionY
    if(direction == "UP"):
        maze[snakePositionY[0]][snakePositionX[0]] = 1
        snakePositionY[0] -= 1
        maze[snakePositionY[0]][snakePositionX[0]] = 2
    elif(direction == "DOWN"):
        maze[snakePositionY[0]][snakePositionX[0]] = 1
        snakePositionY[0] += 1
        maze[snakePositionY[0]][snakePositionX[0]] = 2
    elif(direction == "RIGHT"):
        maze[snakePositionY[0]][snakePositionX[0]] = 1
        snakePositionX[0] += 1
        maze[snakePositionY[0]][snakePositionX[0]] = 2
    else:
        maze[snakePositionY[0]][snakePositionX[0]] = 1
        snakePositionX[0] -= 1
        maze[snakePositionY[0]][snakePositionX[0]] = 2

start_game()
