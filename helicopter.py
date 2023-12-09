from utils import rand_cell

class Helicopter:
    def __init__(self, width, height):
        cell = rand_cell(width, height)
        self.width, self.height = width, height
        self.x, self.y = cell[0], cell[1]
        self.tank = 0
        self.maxTank = 1
        self.score = 0
        self.lives = 20

    def move(self, x, y):
        newX, newY = x + self.x, y + self.y
        if (newX >= 0 and newY >= 0 and newX < self.width and newY < self.height):
            self.x, self.y = newX, newY

    def print_stats(self):
        print("🪣  ", self.tank, "/", self.maxTank, sep="", end= " | ")
        print("🏆 ", self.score, end="|")
        print("💛", self.lives)
        
    def game_over(self):
        text = "X   GAME OVER, YOUR SCORE IS " + str(self.score) + "   X"
        textLen = len(text)

        print("X" * textLen)
        print("X", " " * (textLen - 4), "X")
        print(text)
        print("X", " " * (textLen - 4), "X")
        print("X" * textLen)
        exit(0)    
    
    def export_data(self):
        return {"score": self.score,
                "lives": self.lives,
                "x": self.x, 
                "y": self.y,
                "tank": self.tank,
                "maxTank": self.maxTank}
    
    def import_data(self, data):
        self.x = data["x"] or 0
        self.y = data["y"] or 0
        self.score = data["score"] or 0
        self.lives = data["lives"] or 20
        self.tank = data["tank"] or 1
        self.maxTank = data["maxTank"] or 1