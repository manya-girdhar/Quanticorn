# Quantum Computing Game
This is my hackathon submission Quanticorn, a python-based game that uses a Quantum Computing Library. Quanticorn takes inspiration from Minesweepers to introduce its users to some of the bizarre concepts in Quantum Computing with the help of a gamified environment. 

# How it works?
- Each tile in the game is mapped to a qubit (tile --> qubit). 
- The tiles with lightning bolts are placed randomly using a [quantum random number generators](https://qrng.anu.edu.au/). 
- Clicking on the tile reveals a number representing the count of the lightning bolts surrounding the tile. 
- One tile is assigned to a Unicorn. Clicking on the tile with a unicorn makes you win the game.
- If you click on a tile with a lightning bolt, there is a 50 percent chance of losing the game. This is because a Hadamard gate is applied to each tile (i.e. the qubit) in the game.

# Explanation
- A Hadamard gate is a logical gate which when applied to a qubit puts the qubit into superposition - which means the qubit is both a 0 and a 1 at the same time. Although, it collapses to one value when the qubit is measured. Once the player clicks on a tile, the value of the qubit is measured and it collapses into one of the two states (0 or 1). It has a 50 per cent chance of collapsing to a 1 and if the output is 1, clicking on the tile with a lightning bolt will not affect your progress of the game and you can continue playing.
- A Hadamard gate is also applied to the other tiles which means that depending on the value of the qubits when they are measured, some tiles will be locked and will not reveal the number of lightning bolts surrounding the tile.

# Technical Details
- The game is written in Python and uses the Tkinter GUI toolkit.
- It makes use of qiskit, a python framework for Quantum Computing.
- A python interface - quantumrandom is used access the [ANU Quantum Random Number Generator](https://qrng.anu.edu.au/)

# Trivia
The game was tested on Quantum Computer Simulator and runs on an IBM Quantum Computer. 

# Demo
Find out more about Quanticorn and watch the project demo on [Devpost](https://devpost.com/software/quanticorn).

# Future Developments
- In the future, I hope to add a feature in the game which mimics quantum entanglement by entangling random tiles with each other, where revealing one tile would reveal its pair as well.
- Furthermore, I plan on making the game multiplayer by adding a realtime functionality, using a pusher such as Vue.

# Mentions
The idea of creating an Quantum game originally came about from https://github.com/desireevl
