import pygame
from pygame.locals import *
import math
import random
import copy


class HillClimb:
    indexList = ["a", "b", "c", "d", "e", "f", "g", "h"]
    indexNumbersList = [0, 1, 2, 3, 4, 5, 6, 7]
    coordinateList = {}
    valueMatrix = []
    trainsPoints = []
    listOfSolutions = []

    def __init__(self,
                 name,
                 display,
                 local,
                 size,
                 border_width,
                 color=(255, 255, 255)):
        self.name = name
        self.display = display
        self.color = color
        self.local = color
        self.height = size[0]
        self.width = size[1]
        self.border_width = border_width

    def validate(self, condition, data):
        x1, y1 = condition["init"][0], condition["init"][1]
        x2, y2 = x1 + condition["form"][0], y1
        y3 = y2 + condition["form"][1]

        x, y = data[0], data[1]

        if x1 <= x <= x2 and y1 <= y <= y3:
            return True
        else:
            return False

    def separate_blocks(self, string):
        string = string[1:-1]
        return [
            "          " + string[i:i + 52] for i in range(0, len(string), 52)
        ]

    def show_environment(self):
        text = '||     ||  a ||  b ||  c ||  d ||  e ||  f ||  g ||  h ||'
        texts = []
        baseBar = ""

        for i in range(len(text) - 25):
            baseBar += "_"

        texts.append(baseBar)
        texts.append(text)
        texts.append(baseBar)

        for i in range(len(self.valueMatrix)):
            text = "||  " + self.indexList[i] + " "
            for e in self.valueMatrix[i]:
                nullSpace = ""
                for i in range(3 - len(str(e))):
                    nullSpace += " "
                text += "||" + nullSpace + str(e) + " "

            text += "||"

            texts.append(text)
            texts.append(baseBar)

        formatCoordinateList = []

        formatCoordinateList.append("Lista de Coordenadas Iniciais: {")
        formatCoordinateList = formatCoordinateList + self.separate_blocks(
            str(self.coordinateList))
        formatCoordinateList.append("}")

        count = 0
        for text in formatCoordinateList:
            self.display.add_surface(
                self.name + "-coordinateList-" + str(count),
                pygame.font.SysFont(None, 23).render(text, True, self.color))

            count += 1

        count = 0
        for i in range(len(formatCoordinateList)):
            self.display.render_surface(
                self.name + "-coordinateList-" + str(i),
                (self.local[0] + 40, (self.border_width * 2) + count),
            )

            count += 23.5

        nextLineY = count - 1

        self.display.add_surface(
            'valueMatrix',
            pygame.font.SysFont(None, 23).render('Matris de distancias', True,
                                                 self.color))

        self.display.render_surface('valueMatrix',
                                    (self.local[0] + 40,
                                     (self.border_width * 2) + nextLineY))

        nextLineY -= 1

        count = 0
        for text in texts:
            self.display.add_surface(
                self.name + str(count),
                pygame.font.SysFont(None, 23).render(text, True, self.color))

            count += 1

        count = nextLineY
        for i in range(len(texts)):
            self.display.render_surface(
                self.name + str(i),
                (self.local[0] + 40, (self.border_width * 4) + count),
            )
            if i % 2 == 0:
                count += 23 * 0.655

        nextLineY = count + 23
        self.display.add_surface(
            'trains',
            pygame.font.SysFont(None, 23).render('Numero de Trens: 4', True,
                                                 self.color))

        self.display.render_surface('trains',
                                    (self.local[0] + 40,
                                     (self.border_width * 2) + nextLineY))

    def show_response(self):

        formatCoordinateList = []

        formatCoordinateList.append("Solução para caminhos dos Trens: ")

        count = 0
        for trainPoint in self.trainsPoints:
            text = "Tren no ponto " + self.indexList[
                trainPoint] + " -> Solução final: "
            solution = [
                self.indexList[i] for i in self.listOfSolutions[count][0]
            ]
            text += str(solution) + " -> " + str(
                self.listOfSolutions[count][1])
            formatCoordinateList.append(text)
            count += 1

        count = 0
        for text in formatCoordinateList:
            self.display.add_surface(
                self.name + "-coordinateList-" + str(count),
                pygame.font.SysFont(None, 23).render(text, True, self.color))

            count += 1

        count = 305
        for i in range(len(formatCoordinateList)):
            self.display.render_surface(
                self.name + "-coordinateList-" + str(i),
                (self.local[0] + 40, (self.border_width * 2) + count),
            )

            count += 17

    def ignite(self):
        print(self.name + " ativado")

        self.create_environment()

        self.hill_climb()

        self.show_environment()

        self.show_response()

    # Cria um ambiente com dados aleatórios.
    def create_environment(self):
        min_x, max_x = 0, 10
        min_y, max_y = 0, 10

        for i in self.indexList:
            x = round(random.uniform(min_x, max_x))
            y = round(random.uniform(min_y, max_y))

            self.coordinateList[i] = [x, y]

        for i in self.coordinateList:
            coordinateRow = []
            x1, y1 = self.coordinateList[i][0], self.coordinateList[i][1]
            for e in self.coordinateList:
                x2, y2 = self.coordinateList[e][0], self.coordinateList[e][1]

                coordinateRow.append(
                    round(math.sqrt((x2 - x1)**2 + (y2 - y1)**2)))

            self.valueMatrix.append(coordinateRow)

        self.trainsPoints = random.sample(self.indexNumbersList, 4)

    # Retorna um array contendo uma solução inicial gerada aleatoriamente.
    def init_solution(self, lockedPositions):
        numberOfIndexes = len(self.indexNumbersList)
        numberOfLockedPositions = len(lockedPositions)

        indexNumbersList = list(
            set(self.indexNumbersList) - set(lockedPositions))

        return (lockedPositions +
                random.sample(indexNumbersList,
                              (numberOfIndexes - numberOfLockedPositions)))

    # Avalia a solução.
    def evaluate_solution(self, solution):
        travelValue = 0

        for i in range(len(solution) - 1):
            travelValue += self.valueMatrix[solution[i]][solution[i + 1]]

        return travelValue

    # Implementa o algoritmo de subida de encosta.
    def slope(self, solution, lockedPosition=0):
        travelValue = self.evaluate_solution(solution)

        newTravelValue = travelValue
        newSolution = copy.deepcopy(solution)

        while True:
            try:
                i = random.randint(lockedPosition + 1, len(solution) - 1)

                for e in range(lockedPosition + 1, len(solution) - 1):
                    auxSolution = copy.deepcopy(solution)
                    auxSolution[e] = solution[i]
                    auxSolution[i] = solution[e]

                    auxTravelValue = self.evaluate_solution(auxSolution)

                    if auxTravelValue < newTravelValue:
                        newTravelValue = auxTravelValue
                        newSolution = copy.deepcopy(auxSolution)

                if newTravelValue < travelValue:
                    travelValue = newTravelValue
                    solution = copy.deepcopy(newSolution)
                else:
                    return [solution, travelValue]
            except:
                return [solution, travelValue]

    # Verifica se há conflitos no caminho percorrido e corrige-os, se necessário.
    def solve_oblique_paths(self, solution, otherSolutions, init=0):
        for i in range(init, len(solution) - 1):
            e = i + 1
            pointStart = solution[i]
            pointEnd = solution[e]
            for otherSolution in otherSolutions:
                if pointStart == otherSolution[
                        i] and pointEnd == otherSolution[e]:
                    return self.solve_oblique_paths(self.slope(solution, i),
                                                    otherSolutions, i)

        return solution

    # Inicia a base de operações para o algoritmo
    def hill_climb(self):
        listOfSolutions = []
        count = 0
        for trainPoint in self.trainsPoints:

            solution = self.slope(self.init_solution([trainPoint]),
                                  self.trainsPoints[0])

            if len(listOfSolutions) > 0:
                solution = self.solve_oblique_paths(solution, listOfSolutions)

            listOfSolutions.append(solution)
            count += 1

        self.listOfSolutions = listOfSolutions
