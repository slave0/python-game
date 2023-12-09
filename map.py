from clouds import Clouds
from utils import rand_bool
from utils import rand_cell
from utils import rand_rive_cell
from utils import get_moves
from utils import check_bounds

CELL_TYPES = '🟩🌳🌊🏥🏬🔥'
TREE_BONUS = 100
UPGRADE_COST = 5000
LIFE_COST = 100

class Map():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[0 for i in range(width)] for j in range(height)]
        print(self.rand_cell())
        self.generate_forest(5, 10)
        self.generate_rive(10)
        self.generate_rive(10)
        self.set_with_condition(self.rand_cell(),1, 5)
        self.set_with_condition(self.rand_cell(),1, 5)
        self.set_with_condition(self.rand_cell(),1, 5)
        self.simple_set_cell_value(self.rand_cell(), 4)
        self.generate_hospital()
        self.clouds = Clouds(width, height)

    def update_clouds(self):
        self.clouds.update()

    def get_value_cell(self, cell):
        return self.cells[cell[1]][cell[0]]

    def rand_cell(self):
        return rand_cell(self.width, self.height)

    def print_map(self, helico):
        print("⬛" * (self.width + 2))
        for rowI in range(self.height):
            print("⬛", end="")
            for cellI in range(self.width):
                cell = self.cells[rowI][cellI]
                if (self.clouds.cells[rowI][cellI] == 1):
                    print("💭", end="")
                elif (self.clouds.cells[rowI][cellI] == 2):
                    print("⚡", end="")
                elif (helico.y == rowI and helico.x == cellI):
                    print("🚁", end="")
                elif (cell >= 0 and cell < len(CELL_TYPES)):
                    print(CELL_TYPES[cell], end="")
            print("⬛")
        print("⬛" * (self.width + 2))

    def check_bounds(self, x, y):
        return check_bounds(x, y, self.width, self.height)    

    def generate_forest(self, r, mxr):
        for rowI in range(self.height):
            for cellI in range(self.width):
                if rand_bool(r, mxr):
                    self.cells[rowI][cellI] = 1

    def generate_rive(self, lenght):
        riveCell = rand_cell(self.width, self.height)
        x, y = riveCell[0], riveCell[1]
        self.cells[y][x] = 2
        while lenght > 0:
            moves = get_moves(x, y, self.cells)
            if (len(moves) == 0):
                break
            coordinate = rand_rive_cell(x, y, moves)
            coordinateX, coordinateY = coordinate[0], coordinate[1]
            if (self.check_bounds(coordinateX, coordinateY)):
                self.cells[coordinateY][coordinateX] = 2
                x, y = coordinateX, coordinateY
                lenght -= 1

    def generate_hospital(self):
        cell = self.rand_cell()
        if (self.get_value_cell(cell) == 4):
            self.generate_hospital
        else:
            self.simple_set_cell_value(cell, 3)

    def simple_set_cell_value(self, cell, value):
        cellX, cellY = cell[0], cell[1]
        self.cells[cellY][cellX] = value    

    def set_with_condition(self, cell, cellValue, value):
        cellX, cellY = cell[0], cell[1]
        if (self.cells[cellY][cellX] == cellValue):
            self.cells[cellY][cellX] = value
    
    def update_fires(self, helico):
        for rowI in range(self.height):
            for cellI in range(self.width):
                if (self.cells[rowI][cellI] == 5):
                    self.cells[rowI][cellI] = 0
                    newScore = helico.score - 50
                    if (newScore < 0):
                        newScore = 0
                    helico.score = newScore
                    
        for i in range(10):
            self.set_with_condition(self.rand_cell(), 1, 5)
    
    def process_helicopter(self, helico):
        cell = self.cells[helico.y][helico.x]
        cellCloud = self.clouds.cells[helico.y][helico.x]

        if (cell == 2):
            helico.tank = helico.maxTank
        elif (cell == 5 and helico.tank > 0):
            helico.tank -= 1
            helico.score += TREE_BONUS
            self.cells[helico.y][helico.x] = 1
        elif (cell == 4 and helico.score >= UPGRADE_COST):
            helico.maxTank += 1
            helico.score -= UPGRADE_COST
        elif (cell == 3 and helico.score >=LIFE_COST):
            helico.lives += 10
            helico.score -= LIFE_COST
        elif (cellCloud == 2):
            helico.lives -= 1
            if (helico.lives == 0):
                helico.game_over()

    def export_data(self):
        return {"cells": self.cells}

    def import_data(self, data):
        self.cells = data["cells"] or [[0 for i in range(self.width)] for j in range(self.height)]