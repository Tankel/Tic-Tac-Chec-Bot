"""
Value code for each piece is as follows:
    - pawn = 1 for white, -1 for black
    - bishop =  2 for white, -2 for black
    - knight =  3 for white, -3 for black
    - rook =  4 for white, -4 for black

* It is recommended to store the direction of movement of both your pawn and opponent's pawn.

"""

import copy
import random
import time


class TTCPlayer:
    # valuesCode is a list containing the value code that you must use to represent your pieces over the board.
    # The sign of the value code will tell you if you are playing as white or black pieces.
    # The values are in the order: pawn, bishop, knight, rook
    def __init__(self, name):
        self.name = name
        self.pawnDirection = -1
        self.currentTurn = -1

        self.piecesOnBoard = [0] * 5
        self.enemyPiecesOnBoard = [0] * 5
        self.startTime = time.time()

    def setColor(self, piecesColor):
        self.piecesCode = [0, 1, 2, 3, 4]
        self.piecesCode = [x*piecesColor for x in self.piecesCode]
        self.piecesColor = piecesColor

    def __updatePawnDirection(self, board):
        # If the pawn is in the limit of the board, it should reverse
        if self.piecesColor in board[0]:
            self.pawnDirection = 1

        # If the pawn is in the start of the board, it should go forward
        if self.piecesColor in board[3]:
            self.pawnDirection = -1

    def __sameSign(self, a, b):
        return ((a < 0 and b < 0) or (a > 0 and b > 0))

    def __isInsideBoard(self, row, col):
        return (row >= 0 and row < 4 and col >= 0 and col < 4)

        # Function to check whether a movement was a movement or not
    # If it was a movement, it also checks if it was a capture or not.
    # For a movement to be classified as a capture, 2 conditions have to occur
    # 1. Only 2 squares changed value
    # 2. One square has to change from used to empty and the other from used to used with different color

    def __wasPieceMovement(self, oldBoard, newBoard):
        changedSquares = []

        for i in range(4):
            for j in range(4):
                if oldBoard[i][j] != newBoard[i][j]:
                    changedSquares.append((i, j))

        if len(changedSquares) != 2:
            return False, False

        def areChangesFromCapture(row1, col1, row2, col2):
            return (newBoard[row1][col1] == 0
                    and oldBoard[row2][col2] != 0
                    and newBoard[row2][col2] == oldBoard[row1][col1])

        def areChangesFromMovement(row1, col1, row2, col2):
            return (newBoard[row1][col1] == 0
                    and newBoard[row2][col2] == oldBoard[row1][col1])

        wasMovement = (areChangesFromMovement(changedSquares[0][0], changedSquares[0][1], changedSquares[1][0], changedSquares[1][1])
                       or areChangesFromMovement(changedSquares[1][0], changedSquares[1][1], changedSquares[0][0], changedSquares[0][1]))

        wasCapture = (areChangesFromCapture(changedSquares[0][0], changedSquares[0][1], changedSquares[1][0], changedSquares[1][1])
                      or areChangesFromCapture(changedSquares[1][0], changedSquares[1][1], changedSquares[0][0], changedSquares[0][1]))

        return (wasMovement, wasCapture)

    def __getPawnValidMovements(self, position, board, pawnDirection):
        validMovements = []

        row = position[0]
        col = position[1]

        # Move 1 to the front
        newRow = row + pawnDirection
        if self.__isInsideBoard(newRow, col) and board[newRow][col] == 0:
            validMovements.append((newRow, col))

        # Attack to the left
        newCol = col - 1
        if self.__isInsideBoard(newRow, newCol) and board[newRow][newCol] != 0 and not self.__sameSign(board[newRow][newCol], board[row][col]):
            validMovements.append((newRow, newCol))

        # Attack to the right
        newCol = col + 1
        if self.__isInsideBoard(newRow, newCol) and board[newRow][newCol] != 0 and not self.__sameSign(board[newRow][newCol], board[row][col]):
            validMovements.append((newRow, newCol))

        return validMovements

    def __getBishopValidMovements(self, position, board):
        validMovements = []

        row = position[0]
        col = position[1]

        # To check whether I already encountered a piece in this diagonal or not
        # 0 -> Up-Left Diagonal
        # 1 -> Up-Right Diagonal
        # 2 -> Down-Left Diagonal
        # 3 -> Down-Right Diagonal
        diagEncounteredPiece = [False] * 4

        # Describe the direction of the movement for the bishop in the same
        # order as described above
        movDirection = [[-1, -1],
                        [-1, 1],
                        [1, -1],
                        [1, 1]]

        # A bishop can move at most 3 squares
        for i in range(1, 4):
            # Check 4 directions of movement
            for j in range(4):
                newCol = col + i * movDirection[j][0]
                newRow = row + i * movDirection[j][1]

                # If I haven't found a piece yet in this direction and its inside the board
                if not diagEncounteredPiece[j] and self.__isInsideBoard(newRow, newCol):
                    # If the proposed square its occupied
                    if board[newRow][newCol] != 0:
                        # If the piece that occupies the square its from the opponent, then its a valid movement
                        if not self.__sameSign(board[row][col], board[newRow][newCol]):
                            validMovements.append((newRow, newCol))
                        diagEncounteredPiece[j] = True
                    else:  # If not, just append the movement
                        validMovements.append((newRow, newCol))

        return validMovements

    def __getKnightValidMovements(self, position, board):
        validMovements = []

        row = position[0]
        col = position[1]

        # Describe the movements of the knight
        movements = [[-2, 1],
                     [-1, 2],
                     [1, 2],
                     [2, 1],
                     [2, -1],
                     [1, -2],
                     [-1, -2],
                     [-2, -1]]

        # Loop through all possible movements
        for move in movements:
            newRow = row + move[0]
            newCol = col + move[1]

            # For the knight we just need to check if the new square is valid and it is not occupied by a piece of the same color
            if self.__isInsideBoard(newRow, newCol) and not self.__sameSign(board[row][col], board[newRow][newCol]):
                validMovements.append((newRow, newCol))

        return validMovements

    def __getRookValidMovements(self, position, board):
        validMovements = []

        row = position[0]
        col = position[1]

        # Checks whether or not I have found a piece in this direction
        # 0 - Up
        # 1 - Right
        # 2 - Down
        # 3 - Left
        dirPieceEncountered = [False] * 4

        # Describe the direction of movement for the rook
        # The order is the same as described above
        movDirection = [[-1, 0],
                        [0, 1],
                        [1, 0],
                        [0, -1]]

        # The rook can move maximum 3 squares
        for i in range(1, 4):
            # Loop through all possible movements
            for j in range(4):
                newRow = row + i * movDirection[j][0]
                newCol = col + i * movDirection[j][1]

                if not dirPieceEncountered[j] and self.__isInsideBoard(newRow, newCol):
                    if board[newRow][newCol] != 0:
                        if not self.__sameSign(board[newRow][newCol], board[row][col]):
                            validMovements.append((newRow, newCol))
                        dirPieceEncountered[j] = True
                    else:
                        validMovements.append((newRow, newCol))

        return validMovements

    def __getValidMovements(self, pieceCode, position, board):
        if abs(pieceCode) == 1:
            return self.__getPawnValidMovements(position, board, self.pawnDirection)
        elif abs(pieceCode) == 2:
            return self.__getBishopValidMovements(position, board)
        elif abs(pieceCode) == 3:
            return self.__getKnightValidMovements(position, board)
        elif abs(pieceCode) == 4:
            return self.__getRookValidMovements(position, board)
        else:
            print("Piece ", pieceCode, " not recognized")
            return []

    def __moveRandomPiece(self, board):
        # print(self.name, "::moveRandomPiece")
        piece = 0

        while (self.piecesOnBoard[piece] != 1):
            piece = random.randint(1, 4)

        pieceCode = self.piecesCode[piece]
        row = -1
        col = -1

        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == pieceCode:
                    row = i
                    col = j

                    i = len(board)
                    break

        validMovements = self.__getValidMovements(pieceCode, (row, col), board)
        if len(validMovements) == 0:
            return board

        newRow, newCol = validMovements[random.randint(
            0, len(validMovements)-1)]

        board[row][col] = 0
        board[newRow][newCol] = pieceCode

        return board

    def __updatePiecesOnBoard(self, board):
        self.piecesOnBoard = [0] * 5

        for i in range(len(board)):
            for j in range(len(board[0])):
                if self.__sameSign(board[i][j], self.piecesColor):
                    self.piecesOnBoard[abs(board[i][j])] = 1
                elif self.__sameSign(board[i][j], -self.piecesColor):
                    #print(board[i][j], i, j)
                    self.enemyPiecesOnBoard[abs(board[i][j])] = 1

    def __putRandomPiece(self, board):
        piece = -1

        
        # piecesInBoard = list({1, 2, 3, 4} - set(piecesNotInBoard))

        if self.currentTurn == 0:
            for i in range(4):
                if(board[3][i]==0):
                    board[3][i] = self.piecesCode[1]
                    return board
        elif self.currentTurn == 1 and self.piecesOnBoard[3] == 0:
            for i in range(4):
                if(board[3][i]==0):
                    board[3][i] = self.piecesCode[3]
                    return board
        elif self.currentTurn == 2  and self.piecesOnBoard[2] == 0:
            for i in range(4):
                if(board[3][i]==0):
                    board[3][i] = self.piecesCode[2]
                    return board
        elif self.currentTurn == 3:
            for i in range(4):
                if(board[3][i]==0  and self.piecesOnBoard[4] == 0):
                    board[3][i] = self.piecesCode[4]
                    return board
        myAlignedValue, myAlignedPieces, myMissingPieces, myMissingPositions = self.__maxAlignedValue(
            board, self.piecesColor)
        
        for i in myMissingPositions:
            #print(i)
            x, y = i
            if (board[x][y] == 0 and self.piecesOnBoard[myMissingPieces[0]] == 0):
                board[x][y] = myMissingPieces[0]
                return board

        if self.currentTurn < 2 or time.time() - self.startTime < 2:
            while (piece == -1 or self.piecesOnBoard[piece] != 0):
                piece = random.randint(1, 4)

            newRow = random.randint(0, 3)
            newCol = random.randint(0, 3)

            while (board[newRow][newCol] != 0):
                newRow = random.randint(0, 3)
                newCol = random.randint(0, 3)

            board[newRow][newCol] = piece * self.piecesColor

            # If a new pawn is put on the board, we should reset its direction.
            if piece == 1:
                self.pawnDirection = -1

            return board

        return board

    def play(self, board):
        start = time.time()
        self.currentTurn += 1
        self.__updatePiecesOnBoard(board)

        quienfue = 0

        print("My pieces: ",self.piecesOnBoard)
        print("Enemy pieces: ",self.enemyPiecesOnBoard)
        originalBoard = [row[:] for row in board]
        #originalBoard = copy.deepcopy(board)
        #newBoard = copy.deepcopy(board)
        newBoard = [row[:] for row in board]

        for n in range(1000):
            #print(n)
            if self.currentTurn < 4  or sum(self.piecesOnBoard) == 0:
                newBoard = self.__putRandomPiece(board)
                '''
                    quienfue = 1
                elif sum(self.piecesOnBoard) == 0:  # There are no pieces on the board
                    newBoard = self.__putRandomPiece(board)
                    quienfue = 2
                elif n > 2 or newBoard == None:  # All the pieces are on the board
                    newBoard = self.__moveRandomPiece(board)
                    quienfue = 3
                '''
            elif n > 500 and newBoard == None:  # All the pieces are on the board
                newBoard = self.__moveRandomPiece(board)

            else: 
                newBoard, _ = self.__getBestMove(board, 4, self.piecesColor)
                #print(newBoard)
                quienfue = 4
                
            if newBoard != None and newBoard != originalBoard:
                #print(newBoard)
                _, wasCapture = self.__wasPieceMovement(originalBoard, newBoard)
                if wasCapture:
                    if self.availableCaptures > 0:
                        self.availableCaptures -= 1
                    else:
                        newBoard = [row[:] for row in originalBoard]
                        #newBoard = copy.deepcopy(originalBoard)
                        continue

                if newBoard != originalBoard:
                    break
            ##else: 
                #newBoard = [row[:] for row in originalBoard]
                #newBoard = copy.deepcopy(originalBoard)
        #print(n, newBoard)
        #print("FUE", quienfue)
        self.__updatePawnDirection(newBoard)
        print("Time taken: ", time.time() - start)

        for row in newBoard:
            print(row)

        return newBoard

    def __checkVictory(self, board, piecesColor):
        target_numbers = {1, 2, 3, 4} if piecesColor == 1 else {-1, -2, -3, -4}

        # Check horizontally
        for row in board:
            if set(row) - {0} == target_numbers:
                return True

        # Check vertically
        for col in range(len(board[0])):
            column_values = [board[row][col] for row in range(len(board))]
            if set(column_values) - {0} == target_numbers:
                return True

        # Check diagonals
        diagonal_values = [board[i][i] for i in range(len(board))]
        if set(diagonal_values) - {0} == target_numbers:
            return True

        reverse_diagonal_values = [
            board[i][len(board)-1-i] for i in range(len(board))]
        if set(reverse_diagonal_values) - {0} == target_numbers:
            return True

        return False

    def __evaluateBoard(self, board):
        # Evaluation function for the minimax algorithm
        # It gives a value to a given board state
        # Positive values are good for the AI, negative for the opponent
        # The closer the value to 16 or -16, the better the state for each player

        if self.__checkVictory(board, self.piecesColor):
            return 16 
        elif self.__checkVictory(board, -self.piecesColor):
            return -16

        myAlignedValue, myAlignedPieces, myMissingPieces, myMissingPositions = self.__maxAlignedValue(
            board, self.piecesColor)

        oppAlignedValue, oppAlignedPieces, oppMissingPieces, oppMissingPositions = self.__maxAlignedValue(
            board, -self.piecesColor)
        
        #if myAlignedValue == oppAlignedValue:
            #return self.countCenterPieces(board, self.piecesColor) - self.countCenterPieces(board, self.piecesColor)
        #if(myAlignedValue > oppAlignedValue):
        return myAlignedValue - oppAlignedValue
        #elif (myAlignedValue < oppAlignedValue):
        #   return -10

        #return 0
        '''
        score = 0
        for row in board:
            for cell in row:
                score += cell

        return score
        '''

    def getMissingPieces(self, board, pieceColor):
        numbers = {1, 2, 3, 4} if pieceColor == 1 else {-1, -2, -3, -4}
        present_numbers = set()

        for row in board:
            for num in row:
                if num != 0:
                    if (num > 0 and pieceColor == 1) or (num < 0 and pieceColor == -1):
                        present_numbers.add(num)

        missing_numbers = list(numbers - present_numbers)
        return missing_numbers

    def __getBestMove(self, board, depth, piecesColor):
        bestMove = None
        bestScore = float('-inf') if piecesColor == self.piecesColor else float('inf')

        if depth == 0 or self.__checkVictory(board, 1) or self.__checkVictory(board, -1):
            return board, self.__evaluateBoard(board)

        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    for pieceCode in range(1, 5):
                        if (self.piecesOnBoard[pieceCode] == 0 and piecesColor == self.piecesColor) or (
                                self.enemyPiecesOnBoard[pieceCode] == 0 and piecesColor == -self.piecesColor):
                            newBoard = [row[:] for row in board]
                            newPiecesOnBoard = self.piecesOnBoard[:]
                            newEnemyPiecesOnBoard = self.enemyPiecesOnBoard[:]

                            if piecesColor == self.piecesColor:
                                newBoard[i][j] = pieceCode * self.piecesColor
                                newPiecesOnBoard[pieceCode] = 1
                            else:
                                newBoard[i][j] = pieceCode * -self.piecesColor
                                newEnemyPiecesOnBoard[pieceCode] = 1

                            if depth > 1:
                                _, score = self.__getBestMove(newBoard, depth - 1, -piecesColor)
                            else:
                                score = self.__evaluateBoard(newBoard)

                            if piecesColor == self.piecesColor:
                                if score > bestScore:
                                    bestScore = score
                                    bestMove = newBoard
                            else:
                                if score < bestScore:
                                    bestScore = score
                                    bestMove = newBoard

                elif (self.piecesOnBoard[board[i][j]] == 1 and piecesColor == self.piecesColor) or (
                        self.enemyPiecesOnBoard[board[i][j]] == 1 and piecesColor == -self.piecesColor):
                    validMovements = self.__getValidMovements(board[i][j], (i, j), board)
                    for move in validMovements:
                        newBoard = [row[:] for row in board]
                        newPiecesOnBoard = self.piecesOnBoard[:]
                        newEnemyPiecesOnBoard = self.enemyPiecesOnBoard[:]

                        if piecesColor == self.piecesColor:
                            newPiecesOnBoard[board[i][j]] = 0
                        else:
                            newEnemyPiecesOnBoard[board[i][j]] = 0

                        newBoard[i][j] = 0
                        newRow, newCol = move
                        newBoard[newRow][newCol] = board[i][j]

                        if depth > 1:
                            _, score = self.__getBestMove(newBoard, depth - 1, -piecesColor)
                        else:
                            score = self.__evaluateBoard(newBoard)

                        if piecesColor == self.piecesColor:
                            if score > bestScore:
                                bestScore = score
                                bestMove = newBoard
                        else:
                            if score < bestScore:
                                bestScore = score
                                bestMove = newBoard

        return bestMove, bestScore



    def __maxAlignedValue(self, board, number_sign):
        target_numbers = {1, 2, 3, 4} if number_sign == 1 else {-1, -2, -3, -4}
        max_value = 0
        aligned_numbers = set()
        missing_numbers = set(target_numbers)
        missing_positions = set()

        # Check horizontally
        for row in range(len(board)):
            aligned_values = [board[row][col] for col in range(len(board[row])) if board[row][col] != 0 and board[row][col] in target_numbers]
            if len(aligned_values) > max_value:
                max_value = len(aligned_values)
                aligned_numbers = set(aligned_values)
                missing_numbers = target_numbers - aligned_numbers
                missing_positions = {(row, col) for col in range(len(board[row])) if (board[row][col] == 0 or board[row][col] not in target_numbers)}

        # Check vertically
        for col in range(len(board[0])):
            aligned_values = [board[row][col] for row in range(len(board)) if board[row][col] != 0 and board[row][col] in target_numbers]
            if len(aligned_values) > max_value:
                max_value = len(aligned_values)
                aligned_numbers = set(aligned_values)
                missing_numbers = target_numbers - aligned_numbers
                missing_positions = {(row, col) for row in range(len(board)) if (board[row][col] == 0 or board[row][col] not in target_numbers)}

        # Check diagonals
        diagonal_values = [board[i][i] for i in range(len(board)) if board[i][i] != 0 and board[i][i] in target_numbers]
        #print(diagonal_values)
        if len(diagonal_values) > max_value:
            max_value = len(diagonal_values)
            aligned_numbers = set(diagonal_values)
            missing_numbers = target_numbers - aligned_numbers
            missing_positions = {(i, i) for i in range(len(board)) if (board[i][i] == 0 or board[i][i] not in target_numbers)}

        reverse_diagonal_values = [board[i][len(board)-1-i] for i in range(len(board)) if board[i][len(board)-1-i] != 0 and board[i][len(board)-1-i] in target_numbers]
        #print(reverse_diagonal_values)
        if len(reverse_diagonal_values) > max_value:
            max_value = len(reverse_diagonal_values)
            aligned_numbers = set(reverse_diagonal_values)
            missing_numbers = target_numbers - aligned_numbers
            missing_positions = {(i, len(board)-1-i) for i in range(len(board)) if (board[i][len(board)-1-i] == 0 or board[i][len(board)-1-i] not in target_numbers)}

        return max_value, aligned_numbers, list(missing_numbers), missing_positions

    def countCenterPieces(self, board, pieceColor):
        center = [(1, 1), (1, 2), (2, 1), (2, 2)]  # Coordinates of the center square

        count = 0  # Counter for the player's pieces

        for x, y in center:
            piece = board[x][y]
            if pieceColor == 1 and piece in [1, 2, 3, 4]:
                count += 1
            elif pieceColor == -1 and piece in [-1, -2, -3, -4]:
                count += 1

        return count

    def reset(self):
        self.pawnDirection = -1
        self.piecesOnBoard = [0] * 5
        self.enemyPiecesOnBoard = [0] * 5
        self.currentTurn = -1
        self.availableCaptures = 5
        self.startTime = time.time()

