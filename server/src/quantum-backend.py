import qiskit as q
import quantumrandom
import math

# running a quantum simulator locally aka without internet
from qiskit import Aer    # simulator framework for qiskit
from qiskit import IBMQ

class Quanticorn:
    def __init__(self, n_tiles, n_lightning_bolts):
        self.tiles = n_tiles
        self.lightning_bolts = n_lightning_bolts
        self.grid = None
        self.player_grid = None
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
        lightning_bolts_placed = 0
        while (lightning_bolts_placed < self.lightning_bolts):

            # generate a random position using the quantumrandom python module
            pos_x = int(quantumrandom.randint(0, self.tiles))  # position along the row x
            pos_y = int(quantumrandom.randint(0, self.tiles))  # position along the column y
            # print(pos_x, pos_y)

            if (self.grid[pos_x][pos_y] != 'X'):
                self.grid[pos_x][pos_y] = 'X'

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

                lightning_bolts_placed += 1

        return(self.grid)


    def initialise_player_grid(self):
        self.player_grid = [['-' for row in range(self.tiles)] for col in range(self.tiles)]
        return self.player_grid


    def display_grid(self, grid):
        for row in grid:
            print(row)

    def status(self, player_grid):
        #########################
        # redo this code to check for if all tiles other than lightning_bolts have been found
        for row in player_grid:
            for tile in row:
                if tile == '-':
                    return False
        return True

    def game_won(self, grid):
        pass
        #########################
        # two scenarios - a lightning_bolt was clicked on or a unicorn was found


# create an instance of the game
if __name__ == "__main__":
    IBMQ.save_account(open("keypath.txt","r").read())
    # IBMQ.save_account('', overwrite=True)
    IBMQ.load_account()
    # provider = IBMQ.get_provider("ibm-q")
    # Running jobs on the simulator
    backend = Aer.get_backend("qasm_simulator")

    score = 0
    game = Quanticorn(3, 3)

    grid = game.initialise_grid()
    game.display_grid(grid)  # for testing purposes

    player_grid = game.initialise_player_grid()
    game.display_grid(player_grid)

    while game.status(player_grid) == False:

        print("Open a tile")
        x = input("Row position 1, 2 or 3 :")
        y = input("Column position 1, 2 or 3 :")
        x = int(x) - 1 # 0 based indexing
        y = int(y) - 1 # 0 based indexing

        # check if the player opened a tile with a lightning_bolt
        if grid[x][y] == 'X':
            # measure the value of the lightning_bolt which was initially put into superposition
            game.circuit.measure([0, 1], [0, 1])
            job = q.execute(game.circuit, backend=backend, shots=500)
            result = job.result()
            counts = result.get_counts(game.circuit)
            max_val = max(counts, key=counts.get)
            if max_val == 1:
                game.display_grid(grid)
                print("Game Over")
                print("Your Score: ", score)
            else:
                print("You just got lucky!")
                print("The unicorn is safe. Continue playing...")
                game.player_grid[x][y] = game.grid[x][y]
                game.display_grid(player_grid)

        else:
            # reveal the cell
            game.player_grid[x][y] = game.grid[x][y]
            game.display_grid(player_grid)
            score += 1
