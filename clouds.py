from utils import rand_bool

class Clouds:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.cells = [[0 for i in range(width)] for j in range(height)]

    def update(self, r = 1, mxr = 20, g = 1, mxg = 10):
        for i in range(self.height):
            for j in range(self.width):
                if rand_bool(r, mxr):
                    self.cells[i][j] = 1
                    if rand_bool(g, mxg):
                        self.cells[i][j] = 2
                else:
                    self.cells[i][j] = 0
    
    def export_data(self):
        return {"cells":self.cells}
    
    def import_data(self, data):
        self.cells = data["cells"] or [[0 for i in range(self.width)] for j in range(self.height)]