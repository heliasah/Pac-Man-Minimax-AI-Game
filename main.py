import math
import random
import os
from time import sleep


class Game:
    def __init__(self, map, pacman, ghost1, ghost2, scores):
        self.map = map
        self.pacman = pacman
        self.ghost1 = ghost1
        self.ghost2 = ghost2
        self.scores = scores

    def printGame(self):
        print("Scores:%d" % self.scores)
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
    # minimax algorithm

    def minimax2(self, currDepth, targetDepth, isMaximizing):
        # base case
        if currDepth == targetDepth:
            return self.calculateScore2()
        # if pacman turn

        if isMaximizing == 0:
            bestPoint = float('-inf')
            bestMove = 0
            for i in range(0, 4):
                if isValid(self.map.boardArray, self.pacman.x, self.pacman.y, i) != -1:
                    possiblex, possibley = isValid(self.map.boardArray, self.pacman.x, self.pacman.y, i)
                    xcurr, ycurr = self.pacman.x, self.pacman.y
                    # back tracking

                    self.pacman.x, self.pacman.y = possiblex, possibley
                    dot = self.map.boardArray[possiblex][possibley]
                    currscore = game.scores

                    point = self.minimax2(currDepth, targetDepth, 1)

                    self.pacman.x = xcurr
                    self.pacman.y = ycurr
                    self.map.boardArray[possiblex][possibley] = dot

                    if bestPoint < point:
                        bestPoint = point
                        bestMove = i
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
                return bestPoint
        #     ghost one turn
        if isMaximizing == 1:
            bestPoint = float('inf')
            for i in range(0, 4):
                if isValid(self.map.boardArray, self.ghost1.x, self.ghost1.y, i) != -1:
                    possiblex, possibley = isValid(self.map.boardArray, self.ghost1.x, self.ghost1.y, i)
                    xcurr, ycurr = self.ghost1.x, self.ghost1.y

                    self.ghost1.x, self.ghost1.y = possiblex, possibley
                    currscore = self.scores

                    point = self.minimax2(currDepth, targetDepth, 2)
                    self.ghost1.x = xcurr
                    self.ghost1.y = ycurr

                    if bestPoint > point:
                        bestPoint = point

            return bestPoint
        # ghost two turn

        if isMaximizing == 2:
            bestPoint = float('inf')
            for i in range(0, 4):
                if isValid(self.map.boardArray, self.ghost2.x, self.ghost2.y, i) != -1:
                    possiblex, possibley = isValid(self.map.boardArray, self.ghost2.x, self.ghost2.y, i)
                    xcurr, ycurr = self.ghost2.x, self.ghost2.y
                    self.ghost2.x, self.ghost2.y = possiblex, possibley

                    currscore = self.scores

                    point = self.minimax2(currDepth + 1, targetDepth, 0)
                    self.ghost2.x = xcurr
                    self.ghost2.y = ycurr

                    if bestPoint > point:
                        bestPoint = point

            return bestPoint
    # utility function

    def calculateScore2(self):
        distance1 = math.sqrt(((self.pacman.x - self.ghost1.x) ** 2) + ((self.pacman.y - self.ghost1.y) ** 2))
        distance2 = math.sqrt(((self.pacman.x - self.ghost2.x) ** 2) + ((self.pacman.y - self.ghost2.y) ** 2))
        # print("adsfs", min(distance1, distance2))
        point = float('inf')
        for i in range(0, 11):
            for j in range(0, 20):
                if self.map.boardArray[i][j] == '+':
                    foodDistance = math.sqrt(((self.pacman.x - i) ** 2) + ((self.pacman.y - j) ** 2))
                    if foodDistance < point:
                        point = foodDistance
        score = point * -1
        if min(distance1, distance2) < 5:
            score -= 100
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
    for i in range(0, 11):
        for j in range(0, 20):
            if game.map.boardArray[i][j] == '+':
                return 0

    return 1


height = 11
width = 20
arr = [[0] * width] * height
map = Board(arr, height, width)
map.fill()
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
    game.pacman.x, game.pacman.y = game.minimax2(0, 1, 0)
    randMove = randomGhost()
    if isValid(map.boardArray, ghost1.x, ghost1.y, randMove) != -1:
        ghost1.x, ghost1.y = isValid(map.boardArray, ghost1.x, ghost1.y, randMove)
    randMove = randomGhost()
    if isValid(map.boardArray, ghost2.x, ghost2.y, randMove) != -1:
        ghost2.x, ghost2.y = isValid(map.boardArray, ghost2.x, ghost2.y, randMove)

    # for running in cmd
    sleep(0.1)
    os.system("cls")
