import math
import random
import os
from time import sleep
import networkx as nx
from collections import deque


class Game:
    def __init__(self, map, pacman, ghost1, ghost2, scores):
        self.map = map
        self.pacman = pacman
        self.ghost1 = ghost1
        self.ghost2 = ghost2
        self.scores = scores

    def printGame(self):

        print("Scores:%d" % self.scores)
        print("******************************************************************")
        for i in range(self.map.height):
            for j in range(self.map.width):

                if i == ghost1.x and j == ghost1.y or i == ghost2.x and j == ghost2.y:
                    if i == ghost1.x and j == ghost1.y:
                        print("G", end=" ")
                    else:
                        print("g", end=" ")
                elif i == self.pacman.x and j == self.pacman.y:

                    print("p", end=" ")
                else:
                    print(self.map.boardArray[i][j], end=" ")
            print(" ")
        print("******************************************************************")

    # minimax algorithm
    def minimax2(self, currDepth, targetDepth, alpha, beta, isMaximizing):
        # base case
        if currDepth == targetDepth:
            return self.calculate_score()

        if isMaximizing == 0:  # Pacman's turn
            bestMove = 0
            for i in range(4):
                if isValid(self.map.boardArray, self.pacman.x, self.pacman.y, i) != -1:
                    possiblex, possibley = isValid(self.map.boardArray, self.pacman.x, self.pacman.y, i)
                    xcurr, ycurr = self.pacman.x, self.pacman.y
                    dot = self.map.boardArray[possiblex][possibley]
                    self.pacman.x, self.pacman.y = possiblex, possibley

                    point = self.minimax2(currDepth, targetDepth, alpha, beta, 1)

                    self.pacman.x = xcurr
                    self.pacman.y = ycurr
                    self.map.boardArray[possiblex][possibley] = dot

                    if point > alpha:
                        alpha = point
                        bestMove = i

                    if alpha >= beta:
                        break  # Beta cut-off

            if currDepth == 0:
                # updating scores
                tempx, tempy = isValid(self.map.boardArray, self.pacman.x, self.pacman.y, bestMove)
                if self.map.boardArray[tempx][tempy] == '+':
                    self.scores += 9
                else:
                    self.scores -= 1
                self.map.boardArray[tempx][tempy] = " "
                return isValid(self.map.boardArray, self.pacman.x, self.pacman.y, bestMove)
            else:
                return alpha

        elif isMaximizing == 1:  # Ghost one's turn
            bestPoint = float('inf')
            for i in range(4):
                if isValid(self.map.boardArray, self.ghost1.x, self.ghost1.y, i) != -1:
                    possiblex, possibley = isValid(self.map.boardArray, self.ghost1.x, self.ghost1.y, i)
                    xcurr, ycurr = self.ghost1.x, self.ghost1.y

                    self.ghost1.x, self.ghost1.y = possiblex, possibley

                    point = self.minimax2(currDepth, targetDepth, alpha, beta, 2)
                    self.ghost1.x = xcurr
                    self.ghost1.y = ycurr

                    if point < bestPoint:
                        bestPoint = point

                    if beta <= alpha:
                        break  # Alpha cut-off

            return bestPoint

        elif isMaximizing == 2:  # Ghost two's turn
            bestPoint = float('inf')
            for i in range(4):
                if isValid(self.map.boardArray, self.ghost2.x, self.ghost2.y, i) != -1:
                    possiblex, possibley = isValid(self.map.boardArray, self.ghost2.x, self.ghost2.y, i)
                    xcurr, ycurr = self.ghost2.x, self.ghost2.y
                    self.ghost2.x, self.ghost2.y = possiblex, possibley

                    point = self.minimax2(currDepth + 1, targetDepth, alpha, beta, 0)
                    self.ghost2.x = xcurr
                    self.ghost2.y = ycurr

                    if point < bestPoint:
                        bestPoint = point

                    if beta <= alpha:
                        break  # Alpha cut-off

            return bestPoint

    # utility function

    def calculate_score(self):

        graph = nx.Graph()
        # creating graph
        for i in range(11):
            for j in range(20):
                if self.map.boardArray[i][j] != "#":
                    graph.add_node((i, j))

                    # Add edges based on valid moves
                    if i > 0 and self.map.boardArray[i - 1][j] != "#":
                        graph.add_edge((i, j), (i - 1, j))
                    if i < self.map.height - 1 and self.map.boardArray[i + 1][j] != "#":
                        graph.add_edge((i, j), (i + 1, j))
                    if j > 0 and self.map.boardArray[i][j - 1] != "#":
                        graph.add_edge((i, j), (i, j - 1))
                    if j < self.map.width - 1 and self.map.boardArray[i][j + 1] != "#":
                        graph.add_edge((i, j), (i, j + 1))

        visited = set()
        none = float('inf')

        def bfs(graph, start):
            queue = deque([(start, 0)])
            while queue:
                current_node, distance = queue.popleft()
                x, y = current_node
                visited.add(current_node)
                if self.map.boardArray[x][y] == "+":
                    return distance

                for neighbor in graph.neighbors(current_node):
                    if neighbor not in visited:
                        queue.append((neighbor, distance + 1))
                        visited.add(neighbor)
            return none

        disOne = nx.shortest_path_length(graph, (self.pacman.x, self.pacman.y), (self.ghost1.x, self.ghost1.y))
        disTwo = nx.shortest_path_length(graph, (self.pacman.x, self.pacman.y), (self.ghost2.x, self.ghost2.y))

        closestDot = bfs(graph, (self.pacman.x, self.pacman.y))

        sc = math.sqrt((self.map.height - 2) ** 2 + (self.map.width - 2) ** 2)

        score = ((sc - closestDot) / sc) * 9

        if min(disOne, disTwo) < 2:
            score = score * -1
        return score


class Board:
    def __init__(self, boardArray, height, width):
        self.width = width
        self.height = height
        self.boardArray = boardArray

    def fill(self):
        self.boardArray = [['#' if i == 0 or i == height - 1 or j == 0 or j == width - 1
                            else '+' for j in range(width)] for i in range(height)]
        self.boardArray[1][5] = '#'
        self.boardArray[1][14] = '#'
        self.boardArray[2][2] = '#'
        self.boardArray[2][3] = '#'
        self.boardArray[2][5] = '#'
        self.boardArray[2][7] = '#'
        self.boardArray[2][8] = '#'
        self.boardArray[2][9] = '#'
        self.boardArray[2][10] = '#'
        self.boardArray[2][11] = '#'
        self.boardArray[2][12] = '#'
        self.boardArray[2][14] = '#'
        self.boardArray[2][16] = '#'
        self.boardArray[2][17] = '#'
        self.boardArray[3][2] = '#'
        self.boardArray[3][17] = '#'
        self.boardArray[4][2] = '#'
        self.boardArray[4][4] = '#'
        self.boardArray[4][5] = '#'
        self.boardArray[4][7] = '#'
        self.boardArray[4][8] = '#'
        self.boardArray[4][11] = '#'
        self.boardArray[4][12] = '#'
        self.boardArray[4][14] = '#'
        self.boardArray[4][15] = '#'
        self.boardArray[4][17] = '#'
        self.boardArray[5][7] = '#'
        self.boardArray[5][12] = '#'
        self.boardArray[9][5] = '#'
        self.boardArray[9][14] = '#'
        self.boardArray[8][2] = '#'
        self.boardArray[8][3] = '#'
        self.boardArray[8][5] = '#'
        self.boardArray[8][7] = '#'
        self.boardArray[8][8] = '#'
        self.boardArray[8][9] = '#'
        self.boardArray[8][10] = '#'
        self.boardArray[8][11] = '#'
        self.boardArray[8][12] = '#'
        self.boardArray[8][14] = '#'
        self.boardArray[8][16] = '#'
        self.boardArray[8][17] = '#'
        self.boardArray[7][2] = '#'
        self.boardArray[7][17] = '#'
        self.boardArray[6][2] = '#'
        self.boardArray[6][4] = '#'
        self.boardArray[6][5] = '#'
        self.boardArray[6][7] = '#'
        self.boardArray[6][8] = '#'
        self.boardArray[6][11] = '#'
        self.boardArray[6][12] = '#'
        self.boardArray[6][14] = '#'
        self.boardArray[6][15] = '#'
        self.boardArray[6][17] = '#'
        self.boardArray[6][9] = '#'
        self.boardArray[6][10] = '#'

    def printBoard(self):
        for i in range(self.height):
            for j in range(self.width):
                print(self.boardArray[i][j], end=" ")
            print("")


class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Ghosts:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def randomGhost():
    rnd = random.randint(0, 3)
    return rnd


def isValid(map, x, y, dir):
    if dir == 0:
        x -= 1
    if dir == 1:
        x += 1
    if dir == 2:
        y += 1
    if dir == 3:
        y -= 1
    if map[x][y] != '#':
        return x, y
    else:
        return -1


def finishGame(game):
    if game.pacman.x == game.ghost1.x and game.pacman.y == game.ghost1.y:
        return -1
    if game.pacman.x == game.ghost2.x and game.pacman.y == game.ghost2.y:
        return -1
    for i in range(11):
        for j in range(20):
            if game.map.boardArray[i][j] == '+':
                return 0

    return 1


height = 11
width = 20
arr = [[0] * width] * height
map = Board(arr, height, width)
map.fill()
alpha = float('-inf')
beta = float('inf')
# creating objects
pacman = Pacman(8, 8)
ghost1 = Ghosts(1, 1)
ghost2 = Ghosts(1, 2)

game = Game(map, pacman, ghost1, ghost2, 0)
# starting game with starting from pacman turn
turn = 0

while True:
    if finishGame(game) == -1:
        print("Game Over")
        break
    elif finishGame(game) == 1:
        print("WIN")
        break

    game.printGame()
    game.pacman.x, game.pacman.y = game.minimax2(0, 1, alpha, beta, 0)
    randMove = randomGhost()
    if isValid(map.boardArray, ghost1.x, ghost1.y, randMove) != -1:
        ghost1.x, ghost1.y = isValid(map.boardArray, ghost1.x, ghost1.y, randMove)
    randMove = randomGhost()
    if isValid(map.boardArray, ghost2.x, ghost2.y, randMove) != -1:
        ghost2.x, ghost2.y = isValid(map.boardArray, ghost2.x, ghost2.y, randMove)

    # for running in cmd
    sleep(0.1)
    os.system("cls")
