# from qiskit import QuantumCircuit
import qiskit as q
import quantumrandom
import math

class Quanticorn:
    def __init__(self, n_tiles, n_lightning_bolts):
        self.tiles = n_tiles
        self.lightning_bolts = n_lightning_bolts
        self.grid = None
        self.dict_of_mappings = {}
        # create a quantum circuit with equal number of qubits and bits
        self.circuit = q.QuantumCircuit(self.tiles*self.tiles, self.tiles*self.tiles)


    def assign_tile_numbers(self):
        list_of_tiles = []
        x = 0
        for i in range(self.tiles):
            list_of_tiles.append([])
            for j in range(self.tiles):
                list_of_tiles[i].append(x)
                self.dict_of_mappings[list_of_tiles[i][j]] = [i, j]
                x += 1

    # create an empty self.grid
    def initialise_grid(self):
        self.grid = [[0 for row in range(self.tiles)] for column in range(self.tiles)]

        # assign numbers to these tiles
        self.assign_tile_numbers()

        # place lightning_bolts randomly
        lightning_bolts_placed = False
        lightning_bolts_to_place = self.lightning_bolts

        while (not lightning_bolts_placed):

            if (lightning_bolts_to_place <= 1):
                # complete last iteration through the loop after the local variable is set to true
                lightning_bolts_placed = True

            # generate a random position using the quantumrandom python module
            pos_x = int(quantumrandom.randint(0, self.tiles))  # position along the row x
            pos_y = int(quantumrandom.randint(0, self.tiles))  # position along the column y
            # print(pos_x, pos_y)


            if (self.grid[pos_x][pos_y] != 'X'):
                self.grid[pos_x][pos_y] = 'X'
                lightning_bolts_to_place -= 1

                # make this part of the code more efficient ***
                for tile_number, tile in self.dict_of_mappings.items():
                    if tile == [pos_x, pos_y]:
                        # print(tile_number)
                        # tile_number is assumed to be equal to tile in this case
                        # put the qubit in superposition by applying the hadamard gate
                        self.circuit.h(tile_number)


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


    def initialise_player_grid(self):
        player_grid = [['-' for row in range(self.tiles)] for col in range(self.tiles)]
        return player_grid


    def display_grid(self, grid):
        for row in grid:
            print(row)


# create an instance of the game
if __name__ == "__main__":

    score = 0

    game = Quanticorn(3, 3)

    player_grid = game.initialise_player_grid()
    game.display_grid(player_grid)

    grid = game.initialise_grid()
    game.display_grid(grid)
