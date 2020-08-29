# from qiskit import QuantumCircuit
import qiskit
import quantumrandom
import math

class Quanticorn:
    def __init__(self, n_tiles, n_lightning_bolts):
        self.tiles = n_tiles
        self.lightning_bolts = n_lightning_bolts
        self.grid = None


    # create an empty self.grid
    def initialise_grid(self):
        self.grid = [[0 for row in range(self.tiles)] for column in range(self.tiles)]
        # place_lightning_bolts()


    #
    # # place lightning_bolts randomly
    # def place_lightning_bolts(self):
        lightning_bolts_placed = False
        lightning_bolts_to_place = self.lightning_bolts

        while (not lightning_bolts_placed):

            if (lightning_bolts_to_place <= 1):
                # complete last iteration through the loop after the local variable is set to true
                lightning_bolts_placed = True

            # generate a random position using the quantumrandom python module
            pos_x = int(quantumrandom.randint(0, self.tiles-1))  # position along the row x
            pos_y = int(quantumrandom.randint(0, self.tiles-1))  # position along the column y
            print(pos_x, pos_y)

            if (self.grid[pos_x][pos_y] != 'X'):
                self.grid[pos_x][pos_y] = 'X'
                lightning_bolts_to_place -= 1

                # index tiles around the lightning_bolts
                # Make this part of the code more efficient ***
                if (pos_x <= self.tiles-2):
                    if (self.grid[pos_x+1][pos_y] != 'X'):
                        self.grid[pos_x+1][pos_y] += 1  # the row after the lightning_bolt

                if (pos_x >= 1):
                    if (self.grid[pos_x-1][pos_y] != 'X'):
                        self.grid[pos_x-1][pos_y] += 1 # the row before the lightning_bolt

                if (pos_y >= 1):
                    if (self.grid[pos_x][pos_y-1] != 'X'):
                        self.grid[pos_x][pos_y-1] += 1 # the col before the lightning_bolt

                if (pos_y <= self.tiles-2):
                    if (self.grid[pos_x][pos_y+1] != 'X'):
                        self.grid[pos_x][pos_y+1] += 1 # the col after the lightning_bolt

                if (pos_y <= self.tiles-2 and pos_x <= self.tiles-2):
                    if (self.grid[pos_x+1][pos_y+1] != 'X'):
                        self.grid[pos_x+1][pos_y+1] += 1 # diagonally to the bottom right

                if (pos_y <= self.tiles-2 and pos_x >= 1):
                    if (self.grid[pos_x-1][pos_y+1] != 'X'):
                        self.grid[pos_x-1][pos_y+1] += 1 # diagonally to the bottom left

                if (pos_y >= 1 and pos_x >= 1):
                    if (self.grid[pos_x-1][pos_y-1] != 'X'):
                        self.grid[pos_x-1][pos_y-1] += 1 # diagonally to the top left

                if (pos_y >= 1 and pos_x <= self.tiles-2):
                    if (self.grid[pos_x+1][pos_y-1] != 'X'):
                        self.grid[pos_x+1][pos_y-1] += 1 # diagonally to the top right

        return(self.grid)

# create an instance of the game
if __name__ == "__main__":
    score = 0
    beginners_game = Quanticorn(5, 3)
    # beginner_game.initialise_self.grid()
    grid = beginners_game.initialise_grid()
    for row in grid:
        print(row)
