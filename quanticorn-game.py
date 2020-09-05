from tkinter import *
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk

import quantumrandom
import qiskit as q

# running a quantum simulator locally
# Aer is simulator framework for qiskit
from qiskit import Aer
from qiskit import IBMQ

# IBMQ.save_account(open("keypath.txt","r").read())
# IBMQ.load_account()
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

        # graphics
        self.tiles_on_screen = {}
        self.answer_key = {}
        self.unopenedTile = None
        self.openedTile = None
        # self.lockedTile = None
        # self.lockedTile = Button(frame, image = dict_of_images['tile_locked'],command=None, text='')
        # self.lockedTile["bg"] = "white"
        # self.lockedTile["border"] = "0"


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

        # create GUI with opened tiles
        for r in range(self.tiles):
            for c in range(self.tiles):
                self.openedTile = Button(frame, image = dict_of_images['tile_opened'],command=None, text='')
                self.openedTile["bg"] = "white"
                self.openedTile["border"] = "0"
                self.openedTile.grid(row=r, column=c)
                self.answer_key[(r, c)] = self.openedTile

        # put all tiles i.e. qubits in superposition
        for tile_number, tile in self.dict_of_mappings.items():
            # tile_number is assumed to be equal to qubit index in this case
            # puts the qubit in superposition by applying the hadamard gate
            self.circuit.h(tile_number)

        # generate a random position using the quantumrandom python module
        pos_x = int(quantumrandom.randint(0, self.tiles))  # position along the row x
        pos_y = int(quantumrandom.randint(0, self.tiles))  # position along the column y
        self.grid[pos_x][pos_y] = 'U'                      # assign unicorn a random position
        self.answer_key[(pos_x, pos_y)].configure(image = dict_of_images['unicorn'])

        # place lightning_bolts randomly
        lightning_bolts_placed = 0
        while (lightning_bolts_placed < self.lightning_bolts):

            pos_x = int(quantumrandom.randint(0, self.tiles))
            pos_y = int(quantumrandom.randint(0, self.tiles))
            # print(pos_x, pos_y)

            if (self.grid[pos_x][pos_y] != 'X' and self.grid[pos_x][pos_y] != 'U'):
                self.grid[pos_x][pos_y] = 'X'
                self.answer_key[(pos_x, pos_y)].configure(image = dict_of_images['lightning'])

                # index tiles around the lightning_bolts
                # Make this part of the code more efficient ***
                if (pos_x <= self.tiles-2):
                     if (self.grid[pos_x+1][pos_y] != 'X' and self.grid[pos_x+1][pos_y] != 'U'):
                        self.grid[pos_x+1][pos_y] += 1  # the row after the lightning_bolt
                        self.answer_key[(pos_x+1, pos_y)].configure(text=str(self.grid[pos_x+1][pos_y]),
                                                                    compound="center",
                                                                    font=('Helvetica', 18, 'bold'))

                if (pos_x >= 1):
                    if (self.grid[pos_x-1][pos_y] != 'X' and self.grid[pos_x-1][pos_y] != 'U'):
                        self.grid[pos_x-1][pos_y] += 1 # the row before the lightning_bolt
                        self.answer_key[(pos_x-1, pos_y)].configure(text=str(self.grid[pos_x-1][pos_y]),
                                                                    compound="center",
                                                                    font=('Helvetica', 18, 'bold'))

                if (pos_y >= 1):
                    if (self.grid[pos_x][pos_y-1] != 'X' and self.grid[pos_x][pos_y-1] != 'U'):
                        self.grid[pos_x][pos_y-1] += 1 # the col before the lightning_bolt
                        self.answer_key[(pos_x, pos_y-1)].configure(text=str(self.grid[pos_x][pos_y-1]),
                                                                    compound="center",
                                                                    font=('Helvetica', 18, 'bold'))

                if (pos_y <= self.tiles-2):
                    if (self.grid[pos_x][pos_y+1] != 'X' and self.grid[pos_x][pos_y+1] != 'U'):
                        self.grid[pos_x][pos_y+1] += 1 # the col after the lightning_bolt
                        self.answer_key[(pos_x, pos_y+1)].configure(text=str(self.grid[pos_x][pos_y+1]),
                                                                    compound="center",
                                                                    font=('Helvetica', 18, 'bold'))

                if (pos_y <= self.tiles-2 and pos_x <= self.tiles-2):
                    if (self.grid[pos_x+1][pos_y+1] != 'X' and self.grid[pos_x+1][pos_y+1] != 'U'):
                        self.grid[pos_x+1][pos_y+1] += 1 # diagonally to the bottom right
                        self.answer_key[(pos_x+1, pos_y+1)].configure(text=str(self.grid[pos_x+1][pos_y+1]),
                                                                    compound="center",
                                                                    font=('Helvetica', 18, 'bold'))

                if (pos_y <= self.tiles-2 and pos_x >= 1):
                    if (self.grid[pos_x-1][pos_y+1] != 'X' and self.grid[pos_x-1][pos_y+1] != 'U'):
                        self.grid[pos_x-1][pos_y+1] += 1 # diagonally to the bottom left
                        self.answer_key[(pos_x-1, pos_y+1)].configure(text=str(self.grid[pos_x-1][pos_y+1]),
                                                                    compound="center",
                                                                    font=('Helvetica', 18, 'bold'))

                if (pos_y >= 1 and pos_x >= 1):
                    if (self.grid[pos_x-1][pos_y-1] != 'X' and self.grid[pos_x-1][pos_y-1] != 'U'):
                        self.grid[pos_x-1][pos_y-1] += 1 # diagonally to the top left
                        self.answer_key[(pos_x-1, pos_y-1)].configure(text=str(self.grid[pos_x-1][pos_y-1]),
                                                                    compound="center",
                                                                    font=('Helvetica', 18, 'bold'))

                if (pos_y >= 1 and pos_x <= self.tiles-2):
                     if (self.grid[pos_x+1][pos_y-1] != 'X' and self.grid[pos_x+1][pos_y-1] != 'U'):
                        self.grid[pos_x+1][pos_y-1] += 1 # diagonally to the top right
                        self.answer_key[(pos_x+1, pos_y-1)].configure(text=str(self.grid[pos_x+1][pos_y-1]),
                                                                    compound="center",
                                                                    font=('Helvetica', 18, 'bold'))

                lightning_bolts_placed += 1

        return(self.grid)


    """This function creates a grid for the user with tiles that have not yet been
    flipped."""
    def initialise_player_grid(self):
        self.player_grid = [['-' for row in range(self.tiles)] for col in range(self.tiles)]

        # create GUI with unopened tiles
        for r in range(self.tiles):
            for c in range(self.tiles):
                self.unopenedTile = Button(frame, image = dict_of_images['tile'],
                                            command = lambda row=r, column=c: self.flip_tile(row, column),
                                            text='')
                self.unopenedTile["bg"] = "white"
                self.unopenedTile["border"] = "0"
                self.unopenedTile.grid(row=r, column=c)
                # self.unopenedTile.configure()
                self.tiles_on_screen[(r, c)] = self.unopenedTile

        return self.player_grid


    # Make this function more efficent *******
    def flip_tile(self, r, c):
        global avaliable_flips, lightning_bolt_found, score, score_display, unicorn_found
        avaliable_flips -= 1

        # Check if the tile has a Unicorn
        if self.grid[r][c] == 'U':
            unicorn_found = True
            self.tiles_on_screen[(r, c)].destroy()
            self.tiles_on_screen[(r, c)] = self.answer_key[(r, c)]
            self.game_status()
            # output = won(score, unicorn_found, check_game)
            # game_status(output)

        # Check if the tile has a lightning_bolt
        elif self.grid[r][c] == 'X':

            self.tiles_on_screen[(r, c)].destroy()
            self.tiles_on_screen[(r, c)] = self.answer_key[(r, c)]

            # measure the value of the lightning_bolt which was initially put into superposition
            self.circuit.measure([0], [0])
            job = q.execute(self.circuit, backend=backend, shots=500)
            # counts is a dictionary
            counts = job.result().get_counts(self.circuit)
            # print("Counts ", counts)
            # print(round(max_val))

            max_val = max(counts, key=counts.get)

            # 50 percent chance
            if max_val != 1:
                game.display_grid(grid)
                lightning_bolt_found = True
                self.game_status()
                # output = game_finished(player_grid, avaliable_flips, lightning_bolt_found)
                # game_status(output)

            else:
                messagebox.showinfo('Feeling Lucky', 'The Quantum World is in your favour! Continue Playing')
                print("The Quantum World is in your favour!")
                print("Continue playing...")
                self.player_grid[r][c] = self.grid[r][c]
                self.display_grid(self.player_grid)


        # else if the tile is neither a unicorn nor a lightning bolt
        else:
            # Choose to reveal the value on the tile is random
            self.circuit.measure([0], [0])
            job = q.execute(self.circuit, backend=backend, shots=500)
            counts = job.result().get_counts(self.circuit)
            max_val = max(counts, key=counts.get)
            # print(round(max_val))
            if max_val != 1:
                # reveal the cell
                self.player_grid[r][c] = self.grid[r][c]
                self.tiles_on_screen[(r, c)].destroy()
                self.tiles_on_screen[(r, c)] = self.answer_key[(r, c)]
            else:
                self.tiles_on_screen[(r,c)].destroy()
                self.tiles_on_screen[(r,c)].configure(image=dict_of_images['tile_locked'])
                messagebox.showinfo('Oops', 'The Quantum World is not in your favour. The tile is locked.')
                print("The Quantum World is not in your favour!")
                game.player_grid[r][c] = '$'  # blank cell

            self.display_grid(self.player_grid)
            score += 1
            score_output = "SCORE  " + str(score)
            canvas.itemconfigure(score_display, text=score_output)


    """This function takes in player grid or grid as its input and prints the
    grid on the screen."""
    def display_grid(self, grid):
        for row in grid:
            print(row)


    """This function checks if the game is over/ the player has lost."""
    def game_finished(self, player_grid, avaliable_flips, lightning_bolt_found):
        if avaliable_flips < 0:
            messagebox.showinfo('You Lost', 'Maximum limit of flips reached!', icon='error')
            print("Maximum limit of flips reached!")
            return True

        if (lightning_bolt_found == True):
            print("Oops, you accidentally clicked on the lightning bolt!")
            messagebox.showinfo('You Lost', 'Oops, you accidentally clicked on the lightning bolt!', icon='error')
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
            messagebox.showinfo('You Won', 'You were successful in finding the lightning bolts!')

            return True
        # The unicorn has been found - game won
        elif (unicorn_found == True):
            print("Congrats, you found the unicorn!")
            messagebox.showinfo('You Won', 'Congrats, you found the unicorn!')
            return True
        else:
            return False


    def game_status(self):
        while True:
            game_won = self.won(score, unicorn_found, check_game)
            if(game_won == True):
                print("YOU WON")
                break

            game_over = self.game_finished(player_grid, avaliable_flips, lightning_bolt_found)
            if(game_over == True):
                print("YOU LOST")
                print("Your Score: ", score)
                break


def create_window(width_of_window, height_of_window):
    global width_of_screen, height_of_screen, x_position, y_position
    window = Tk()
    window.title("Quanticorn")
    width_of_screen = window.winfo_screenwidth()
    height_of_screen = window.winfo_screenheight()
    x_position = int((width_of_screen/2) - (width_of_window/2))
    y_position = int((height_of_screen/2) - (height_of_window/2))-35  # remove -35
    window.geometry("{}x{}+{}+{}".format(width_of_window, height_of_window,
                                         x_position, y_position))
    window.resizable(False, False)
    return window


if __name__ == "__main__":

    # Setting up the tkinter GUI environment
    width, height = 650, 650
    window = create_window(width, height) # calls the create_window function.

    # loading graphics for the GUI
    dict_of_images = {}
    dict_of_images['logo'] = PhotoImage(file="../../static/graphics/quanticorn.png")
    dict_of_images['lightning'] = PhotoImage(file="../../static/graphics/lightning.png")
    dict_of_images['tile'] = PhotoImage(file="../../static/graphics/tile-unopened.png")
    dict_of_images['tile_locked'] = PhotoImage(file="../../static/graphics/tile-locked.png")
    dict_of_images['tile_opened'] = PhotoImage(file="../../static/graphics/tile-opened.png")
    dict_of_images['unicorn'] = PhotoImage(file="../../static/graphics/unicorn.png")

    canvas = Canvas(window, width=width, height=25, bg="#191618")
    canvas.pack(side='top', fill='y', expand=True)
    frame = Frame(window, width=width, height=height-25, bg='white', padx=5, pady=5)
    frame.pack(side="bottom", fill="y", expand=False)
    frame.grid_rowconfigure(10, weight=1)
    frame.grid_columnconfigure(10, weight=1)

    game = Quanticorn(10, 10)  # create an instance of the game

    # game variables
    score = 0                  # inital score of the user
    avaliable_flips = (game.tiles*game.tiles - 4)  # limit the number of avaliable flips
    lightning_bolt_found = False
    unicorn_found = False
    check_game = False # Not implemented !!! ******

    header_image = canvas.create_image(70, 22, image=dict_of_images['logo'])
    score_output = "SCORE  " + str(score)
    score_display = canvas.create_text(550, 25, fill="white", text=score_output, font="Arial 16 bold")

    grid = game.initialise_grid()
    game.display_grid(grid)  # for testing purposes

    player_grid = game.initialise_player_grid()
    game.display_grid(player_grid)

    # game.game_status()

window.mainloop()

# NOTE - Check game button needs to be created
