import quantumrandom
import qiskit as q

# running a quantum simulator locally
# Aer is simulator framework for qiskit
from qiskit import Aer
from qiskit import IBMQ

IBMQ.save_account(open("keypath.txt","r").read())
IBMQ.load_account()
backend = Aer.get_backend("qasm_simulator") # Running jobs on the simulator locally


class Quanticorn:
    def __init__(self, n_tiles, n_lightning_bolts):
        self.tiles = n_tiles
        self.lightning_bolts = n_lightning_bolts
        self.grid = None
        self.player_grid = None
        self.dict_of_mappings = {}  # dictionary for tile to number mappings

        # creates a quantum circuit with equal number of qubits and bits
        # Note there are self.tiles*self.tiles number of tiles on board
        # The circuit is created with equal number of qubits and bits
        self.circuit = q.QuantumCircuit((self.tiles*self.tiles), (self.tiles*self.tiles))


    """This function assigns a unique number to each tile in the grid
    The mappings between is the tile position and the unique number is stored
    in a dictionary - self.dict_of_mappings. """
    def assign_tile_numbers(self):
        list_of_tiles = []
        x = 0
        for i in range(self.tiles):
            list_of_tiles.append([])
            for j in range(self.tiles):
                list_of_tiles[i].append(x)
                self.dict_of_mappings[list_of_tiles[i][j]] = [i, j]
                x += 1


    """This function creates a grid of tiles. It also assumes the tiles behaves
    like qubits and places the qubits (i.e. tiles) in superposition.
    The function uses the quantumrandom module to place lightning bolts in random
    places on the grid. It also maps tile around each lightning bolt with a number
    indicating how many lightning bolts are present around it. """
    def initialise_grid(self):
        # create an empty grid
        self.grid = [[0 for row in range(self.tiles)] for column in range(self.tiles)]

        # calls the function that assigns unique numbers to each tile
        self.assign_tile_numbers()

        # put all tiles in superposition
        for tile_number, tile in self.dict_of_mappings.items():
            # tile_number is assumed to be equal to qubit index in this case
            # puts the qubit in superposition by applying the hadamard gate
            self.circuit.h(tile_number)

        # generate a random position using the quantumrandom python module
        pos_x = int(quantumrandom.randint(0, self.tiles))  # position along the row x
        pos_y = int(quantumrandom.randint(0, self.tiles))  # position along the column y
        self.grid[pos_x][pos_y] = 'U'                      # assign unicorn a random position

        # place lightning_bolts randomly
        lightning_bolts_placed = 0
        while (lightning_bolts_placed < self.lightning_bolts):

            pos_x = int(quantumrandom.randint(0, self.tiles))
            pos_y = int(quantumrandom.randint(0, self.tiles))
            # print(pos_x, pos_y)

            if (self.grid[pos_x][pos_y] != 'X' and self.grid[pos_x][pos_y] != 'U'):
                self.grid[pos_x][pos_y] = 'X'

                # index tiles around the lightning_bolts
                # Make this part of the code more efficient ***
                if (pos_x <= self.tiles-2):
                     if (self.grid[pos_x+1][pos_y] != 'X' and self.grid[pos_x+1][pos_y] != 'U'):
                        self.grid[pos_x+1][pos_y] += 1  # the row after the lightning_bolt

                if (pos_x >= 1):
                    if (self.grid[pos_x-1][pos_y] != 'X' and self.grid[pos_x-1][pos_y] != 'U'):
                        self.grid[pos_x-1][pos_y] += 1 # the row before the lightning_bolt

                if (pos_y >= 1):
                    if (self.grid[pos_x][pos_y-1] != 'X' and self.grid[pos_x][pos_y-1] != 'U'):
                        self.grid[pos_x][pos_y-1] += 1 # the col before the lightning_bolt

                if (pos_y <= self.tiles-2):
                    if (self.grid[pos_x][pos_y+1] != 'X' and self.grid[pos_x][pos_y+1] != 'U'):
                        self.grid[pos_x][pos_y+1] += 1 # the col after the lightning_bolt

                if (pos_y <= self.tiles-2 and pos_x <= self.tiles-2):
                    if (self.grid[pos_x+1][pos_y+1] != 'X' and self.grid[pos_x+1][pos_y+1] != 'U'):
                        self.grid[pos_x+1][pos_y+1] += 1 # diagonally to the bottom right

                if (pos_y <= self.tiles-2 and pos_x >= 1):
                    if (self.grid[pos_x-1][pos_y+1] != 'X' and self.grid[pos_x-1][pos_y+1] != 'U'):
                        self.grid[pos_x-1][pos_y+1] += 1 # diagonally to the bottom left

                if (pos_y >= 1 and pos_x >= 1):
                    if (self.grid[pos_x-1][pos_y-1] != 'X' and self.grid[pos_x-1][pos_y-1] != 'U'):
                        self.grid[pos_x-1][pos_y-1] += 1 # diagonally to the top left

                if (pos_y >= 1 and pos_x <= self.tiles-2):
                     if (self.grid[pos_x+1][pos_y-1] != 'X' and self.grid[pos_x+1][pos_y-1] != 'U'):
                        self.grid[pos_x+1][pos_y-1] += 1 # diagonally to the top right

                lightning_bolts_placed += 1

        return(self.grid)


    """This function creates a grid for the user with tiles that have not yet been
    flipped."""
    def initialise_player_grid(self):
        self.player_grid = [['-' for row in range(self.tiles)] for col in range(self.tiles)]
        return self.player_grid


    """This function takes in player grid or grid as its input and prints the
    grid on the screen."""
    def display_grid(self, grid):
        for row in grid:
            print(row)


    """This function checks if the game is over/ the player has lost."""
    def game_finished(self, player_grid, avaliable_flips, lightning_bolt_found):
        if avaliable_flips < 0:
            print("Maximum limit of flips reached!")
            return True

        if (lightning_bolt_found == True):
            print("Oops, you accidentally clicked on the lightning bolt!")
            return True

        for row in player_grid:
            for tile in row:
                if tile == '-':
                    return False
        return False


    """This function checks if the game has finished - either when the unicorn has been
    found or the score of the player indicates that all tiles other than the tiles
    with lightning bolts have been flipped."""
    def won(self, score, unicorn_found, check_game):
        # all tiles other than the lightning bolts were opened
        # Note - find a better method to check for this *****
        if (check_game == True and score == (self.tiles*self.tiles - self.lightning_bolts - 1)):
            print("You were successful in finding the lightning bolts!")
            return True
        # The unicorn has been found - game won
        elif (unicorn_found == True):
            print("Congrats, you found the unicorn!")
            return True
        else:
            return False



if __name__ == "__main__":
    game = Quanticorn(3, 4)  # create an instance of the game
    score = 0                # inital score of the user

    grid = game.initialise_grid()
    game.display_grid(grid)  # for testing purposes

    player_grid = game.initialise_player_grid()
    game.display_grid(player_grid)

    avaliable_flips = (game.tiles*game.tiles - 4)  # limit the number of avaliable flips
    lightning_bolt_found = False
    unicorn_found = False
    check_game = False

    while True:
        game_over = game.game_finished(player_grid, avaliable_flips, lightning_bolt_found)
        game_won = game.won(score, unicorn_found, check_game)

        if(game_won == True):
            print("YOU WON")
            break

        elif (game_over == True):
            print("YOU LOST")
            print("Your Score: ", score)
            break

        # Ask for user input
        print("Open a tile")
        # EDIT THIS *****************
        # Error checking needs to be added to avoid opening the same tile ****
        check = str(input("y to check the game:"))
        if (check == 'y'):
            game_won = game.won(score, unicorn_found, check_game)
            continue
        "Choose a tile to begin"
        x = input("Row position 1, 2 or 3 :")
        y = input("Column position 1, 2 or 3 :")
        x = int(x) - 1 # 0 based indexing
        y = int(y) - 1 # 0 based indexing
        # while tiles in list of opened tiles try again

        avaliable_flips -= 1

        # Check if the tile has a Unicorn
        if grid[x][y] == 'U':
            unicorn_found = True
            continue

        # Check if the tile has a lightning_bolt
        elif grid[x][y] == 'X':

            # measure the value of the lightning_bolt which was initially put into superposition
            game.circuit.measure([0], [0])
            job = q.execute(game.circuit, backend=backend, shots=500)
            # counts is a dictionary
            counts = job.result().get_counts(game.circuit)
            print("Counts ", counts)

            max_val = max(counts, key=counts.get)

            # 50 percent chance
            if max_val != 1:
                game.display_grid(grid)
                lightning_bolt_found = True
                continue

            else:
                print("The Quantum World is in your favour!")
                print("Continue playing...")
                game.player_grid[x][y] = game.grid[x][y]
                game.display_grid(player_grid)

        # else if the tile is neither a unicorn nor a lightning bolt
        else:
            # Choose to reveal the value on the tile is random
            game.circuit.measure([0], [0])
            job = q.execute(game.circuit, backend=backend, shots=500)
            counts = job.result().get_counts(game.circuit)
            max_val = max(counts, key=counts.get)

            if max_val != 1:
                # reveal the cell
                game.player_grid[x][y] = game.grid[x][y]
            else:
                print("The Quantum World is not in your favour!")
                game.player_grid[x][y] = '$'  # blank cell

            game.display_grid(player_grid)
            score += 1
