import time

import pygame
import random
import mysql.connector

snakePositionX = [23]
snakePositionY = [17]
direction = "RIGHT"
running = True
score = 0

def connect_to_database():
    try:
      
        conn = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='',
            database='Snake'
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error al conectarse a la base de datos: {err}")
        return None

def top5():
    try:
        conn = connect_to_database()
        if conn is None:
            return

        cursor = conn.cursor()
        select_query = "SELECT mayorPuntaje, usuario FROM puntaje ORDER BY mayorPuntaje DESC LIMIT 5"
        cursor.execute(select_query)


        top_scores = cursor.fetchall()


        for rank, (score, user) in enumerate(top_scores, start=1):
            print(f"#{rank} - Puntaje: {score}, Usuario: {user}")

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"Error al obtener los mejores puntajes: {err}")

def insert_puntaje(mayor_puntaje, usuario):
    try:
        conn = connect_to_database()
        if conn is None:
            return

        cursor = conn.cursor()


        insert_query = "INSERT INTO puntaje (mayorPuntaje, usuario) VALUES (%s, %s)"
        data = (mayor_puntaje, usuario)
        cursor.execute(insert_query, data)
        conn.commit()

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"Error al insertar el puntaje: {err}")




def draw_maze(maze, screen):
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

conn = connect_to_database()
def start_game():
    global snakePositionX, snakePositionY, direction, running, score

    screen_width = 1200
    screen_height = 900

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("maze")

    with open("maze.txt", "r") as file:
        maze = [[int(cell) for cell in line.strip().split(",")] for line in file if line.strip()]
    addFood(maze)
    moved = False
    time.sleep(2.5)
    while running:
        maze[snakePositionY[0]][snakePositionX[0]] = 2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if moved == False:
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        if(direction != "DOWN"):
                            direction = "UP"
                            moved = True
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        if(direction != "UP"):
                            direction = "DOWN"
                            moved = True
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        if(direction != "LEFT"):
                            direction = "RIGHT"
                            moved = True
                    elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        if(direction != "RIGHT"):
                            direction = "LEFT"
                            moved = True
        move(maze)
        moved = False

        if(running == True):
            draw_maze(maze, screen)

        time.sleep(0.06)

    pygame.quit()

def addFood(maze):
    global score
    score += 1
    added = False
    while not added:
        foodY = random.randint(1, 34)
        foodX = random.randint(1, 46)
        if (maze[foodY][foodX] == 1):
            maze[foodY][foodX] = 3
            added = True
        #else:
            #Preguntar porque no sirve la recursividad.
            #addFood(maze)
            #maze[foodX+1][foodY+1] = 3


def move(maze):
    global snakePositionX, snakePositionY, direction, running

    if direction == "UP":
        if maze[snakePositionY[0] - 1][snakePositionX[0]] == 0 or maze[snakePositionY[0] - 1][snakePositionX[0]] == 2:
            running = False
        elif maze[snakePositionY[0] - 1][snakePositionX[0]] == 3:
            addFood(maze)
            snakePositionY.insert(0, snakePositionY[0] - 1)
            snakePositionX.insert(0, snakePositionX[0])
            maze[snakePositionY[0]][snakePositionX[0]] = 2
        else:
            maze[snakePositionY[-1]][snakePositionX[-1]] = 1
            moveSnakeBody(snakePositionX)
            moveSnakeBody(snakePositionY)
            snakePositionY[0] -= 1
            maze[snakePositionY[0]][snakePositionX[0]] = 2

    elif direction == "DOWN":
        if maze[snakePositionY[0] + 1][snakePositionX[0]] == 0 or maze[snakePositionY[0] + 1][snakePositionX[0]] == 2:
            running = False
        elif maze[snakePositionY[0] + 1][snakePositionX[0]] == 3:
            addFood(maze)
            snakePositionY.insert(0, snakePositionY[0] + 1)
            snakePositionX.insert(0, snakePositionX[0])
            maze[snakePositionY[0]][snakePositionX[0]] = 2
        else:
            maze[snakePositionY[-1]][snakePositionX[-1]] = 1
            moveSnakeBody(snakePositionX)
            moveSnakeBody(snakePositionY)
            snakePositionY[0] += 1
            maze[snakePositionY[0]][snakePositionX[0]] = 2

    elif direction == "RIGHT":
        if maze[snakePositionY[0]][snakePositionX[0] + 1] == 0 or maze[snakePositionY[0]][snakePositionX[0] + 1] == 2:
            running = False
        elif maze[snakePositionY[0]][snakePositionX[0] + 1] == 3:
            addFood(maze)
            snakePositionX.insert(0, snakePositionX[0] + 1)
            snakePositionY.insert(0, snakePositionY[0])
            maze[snakePositionY[0]][snakePositionX[0]] = 2
        else:
            maze[snakePositionY[-1]][snakePositionX[-1]] = 1
            moveSnakeBody(snakePositionX)
            moveSnakeBody(snakePositionY)
            snakePositionX[0] += 1
            maze[snakePositionY[0]][snakePositionX[0]] = 2

    elif direction == "LEFT":
        if maze[snakePositionY[0]][snakePositionX[0] - 1] == 0 or maze[snakePositionY[0]][snakePositionX[0] - 1] == 2:
            running = False
        elif maze[snakePositionY[0]][snakePositionX[0] - 1] == 3:
            addFood(maze)
            snakePositionX.insert(0, snakePositionX[0] - 1)
            snakePositionY.insert(0, snakePositionY[0])
            maze[snakePositionY[0]][snakePositionX[0]] = 2
        else:
            maze[snakePositionY[-1]][snakePositionX[-1]] = 1
            moveSnakeBody(snakePositionX)
            moveSnakeBody(snakePositionY)
            snakePositionX[0] -= 1
            maze[snakePositionY[0]][snakePositionX[0]] = 2


def moveSnakeBody(snakePosition):
    newSnakePosition = [snakePosition[0]]
    for i in range(1, len(snakePosition)):
        newSnakePosition.append(snakePosition[i - 1])
    snakePosition[:] = newSnakePosition

nombre = input("Ingresa tu nombre para empezar a jugar: ")

start_game()

insert_puntaje(score, nombre)

top5()
