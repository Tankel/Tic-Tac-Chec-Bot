# Project README

## Project Name: "Nacho" - Final Report for BOT

Authors: Luis Ángel Reyes Frausto, Samuel Iván Sánchez Salazar (@SamuelSanchez03)

### Introduction
Final Project for Data structures and algorithms III class, top 3 of the contest. Bot that plays Tic Tac Chec, a combination of Tic Tac Toc and Chess, here's a short video that explain the game: https://www.youtube.com/watch?v=P7U7cB-pf2c. The project specifications and the tempalte the project can be found on my teacher repository: [https://github.com/manuel-rdz/tic-tac-chec](https://github.com/manuel-rdz/tic-tac-chec) 

For the development of this bot, we decided to implement the minimax algorithm as it is ideal for this type of game. The different implementations of the bot can be found in this repository, where the final version is `playerNacho.py`.

### Documentation
The main class contains the following attributes, initialized and distributed in the `__init__` and `setColor` methods:
- `name`: The name of the player.
- `pawnDirection`: The movement direction of the pawn for the player (-1 for forward, 1 for backward).
- `currentTurn`: The current turn of the player.
- `piecesOnBoard`: A list indicating which pieces of the player are on the board.
- `enemyPiecesOnBoard`: A list indicating which pieces of the opponent are on the board.
- `piecesCode`: A list containing the value codes of the player's pieces, where passing a piece index returns its actual color.

##### Functions
- `__init__(self, name)`: Initializes the class attributes.
- `setColor(self, piecesColor)`: Sets the color of the player's pieces (-1 for black, 1 for white).
- `__updatePawnDirection(self, board)`: Updates the player's pawn direction based on its position on the board.
- `__sameSign(self, a, b)`: Checks if two pieces have the same color.
- `__isInsideBoard(self, row, col)`: Checks if a position is inside the board.
- `__wasPieceMovement(self, oldBoard, newBoard)`: Checks if a movement was a valid move or a capture.
- `__getPawnValidMovements(self, position, board, pawnDirection)`: Returns the valid movements for a pawn in a given position.
- `__getBishopValidMovements(self, position, board)`: Returns the valid movements for a bishop in a given position.
- `__getKnightValidMovements(self, position, board)`: Returns the valid movements for a knight in a given position.
- `__getRookValidMovements(self, position, board)`: Returns the valid movements for a rook in a given position.
- `__getValidMovements(self, pieceCode, position, board)`: Returns the valid movements for a piece in a given position.
- `__updatePiecesOnBoard(self, board)`: Updates the list of pieces for both players based on the board.
- `__moveRandomPiece(self, board)`: Moves a random piece of the player on the board.
- `__putRandomPiece(self, board)`: 
  - Blocks the opponent by placing a piece in their missing cell if they are about to win.
  - In the first 4 turns, follows the previously described strategy for piece placement.
  - In subsequent turns, places a piece on the line that has the most pieces.
  - If none of the above conditions are met, places a piece randomly in an available position.
- `__getBestMove(self, board, depth, isMaximizingPlayer)`: Implements the minimax algorithm to make the best move according to the heuristic function `__evaluateBoard`.
- `__blockOpponent(self, board, myMissingPieces, oppMissingPositions, oppAlignedPositions)`: Prevents the opponent from winning by placing one of our pieces in the opponent's missing cell or capturing their piece.
- `__checkVictory(self, board, piecesColor)`: Checks if the given player has won.
- `__evaluateBoard(self, board)`: Evaluates the board using the heuristic function, considering if either player has won and the maximum number of aligned pieces.
- `__maxAlignedValue(self, board, piecesColor)`: Retrieves:
  - The maximum number of aligned pieces for the player.
  - A list of aligned pieces.
  - A list of non-aligned pieces.
  - Coordinates of the missing cells for alignment.
  - Coordinates of the already aligned pieces.
- `play(self, board)`: The main method that represents the overall strategy of the bot. It takes the current board, the number of available captures, and the maximum number of allowed turns as input. The method returns the updated board after the bot has made its move.
- `reset(self)`: Resets the necessary attributes to start another game.
