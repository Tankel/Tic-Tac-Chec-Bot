"""
Value code for each piece is as follows:
    - pawn = 1 for white, -1 for black
    - bishop =  2 for white, -2 for black
    - knight =  3 for white, -3 for black
    - rook =  4 for white, -4 for black

* It is recommended to store the direction of movement of both your pawn and opponent's pawn.

"""
import math
import copy
import random
import time

#HACER FUNCION QUE CHECQUE SI LA PIECE FALTANTE PUEDE LLEGAR AL LUGAR

class TTCPlayer:
    # valuesCode is a list containing the value code that you must use to represent your pieces over the board. 
    # The sign of the value code will tell you if you are playing as white or black pieces.
    # The values are in the order: pawn, bishop, knight, rook
    def __init__(self, name):
        self.name = name
        self.pawnDirection = -1
        self.currentTurn = -1

        self.piecesOnBoard = [0] * 5

    def print_matrix_mirror(self, matrix):
        for row in reversed(matrix):
            print(row[::-1])

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
        return ((a < 0 and b < 0) or (a > 0  and b > 0))
    
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
        
        row, col = position

        newRow = row + pawnDirection
        if self.__isInsideBoard(newRow, col) and board[newRow][col] == 0:
            validMovements.append((newRow, col))

        for offset in [-1, 1]:
            newCol = col + offset
            if self.__isInsideBoard(newRow, newCol) and board[newRow][newCol] != 0 and not self.__sameSign(board[newRow][newCol], board[row][col]):
                validMovements.append((newRow, newCol))

        return validMovements
    
    def __getBishopValidMovements(self, position, board):
        validMovements = []

        row, col = position

        # Define the four diagonal directions
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for direction in directions:
            deltaRow, deltaCol = direction
            newRow, newCol = row + deltaRow, col + deltaCol

            while self.__isInsideBoard(newRow, newCol):
                if board[newRow][newCol] == 0:
                    validMovements.append((newRow, newCol))
                elif not self.__sameSign(board[newRow][newCol], board[row][col]):
                    validMovements.append((newRow, newCol))
                    break
                else:
                    break

                newRow += deltaRow
                newCol += deltaCol

        return validMovements


    def __getKnightValidMovements(self, position, board):
        validMovements = []

        row, col = position

        movements = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

        for movement in movements:
            deltaRow, deltaCol = movement
            newRow, newCol = row + deltaRow, col + deltaCol
            if self.__isInsideBoard(newRow, newCol) and (board[newRow][newCol] == 0 or not self.__sameSign(board[newRow][newCol], board[row][col])):
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

    def __getCurrentValidMovements(self, board, piecesColor):
        pieces = [1, 2, 3, 4] if piecesColor == 1 else [-1, -2, -3, -4]
        validMovements = []
        
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j]-1 in pieces:
                    pieceCode = pieces[board[i][j]-1]
                    #piecesOnBoard.append(board[i][j])
                    validMovements.append((self.__getValidMovements(pieceCode, (i, j), board), pieceCode))

        return validMovements
    def __moveRandomPiece(self, board):
        #print(self.name, "::moveRandomPiece")
        piece = 0

        while(self.piecesOnBoard[piece] != 1): 
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
        
        newRow, newCol = validMovements[random.randint(0, len(validMovements)-1)]

        board[row][col] = 0
        board[newRow][newCol] = pieceCode

        return board
    
    def __movePiece(self, currentBoard):
        #print(self.name, "::moveRandomPiece")
        row = -1
        col = -1

        #Copy the board
        board = [row[:] for row in currentBoard]
        #Set bestScore to a very small value
        bestScore = -math.inf

        move = None
        bestPiece = None
        #For every possible move
        pieces = self.getMissingPieces(board, self.piecesColor)
        
        for i in range(len(board)):
            for j in range(len(board[0])):
                # si es una casilla vacia probamos con las piezas que no estan en el tablero
                if board[i][j] == 0:
                    for k in pieces:
                        #Put 'O' in the available position
                        board[i][j] = k

                        #Call minimax to see how good the move is
                        #isMaximizing is false because it would be the human's turn
                        #Set alpha to a very small value and beta to a very large one
                        score = self.minimaxAB(board, 0, -math.inf, math.inf, True)

                        #Undo the change to the board
                        board[i][j] = 0

                        #If the score is bigger than the current best score
                        if score > bestScore:
                            #Set bestScore to score and save the move
                            bestScore = score
                            lastPosition = [i, j]
                            move = [i, j]
                            bestPiece = k
                # si es una de mis piezas
                elif board[i][j] in self.piecesCode:
                    kValidMoves = self.__getValidMovements(board[i][j], (i,j), board)
                    for coor in kValidMoves:
                        #print(coor)
                        a, b = coor

                        #guardamos cual es la pieza
                        pastPiece = board[a][b]
                        #ponemos la pieza en la nueva posición 
                        board[a][b] = board[i][j]

                        #Call minimax to see how good the move is
                        #isMaxismizing is false because it would be the human's turn
                        #Set alpha to a very small value and beta to a very large one
                        score = self.minimaxAB(board, 0, -math.inf, math.inf, True)

                        #Undo the change to the board
                        board[a][b] = pastPiece

                        #If the score is bigger than the current best score
                        if score > bestScore:
                            #Set bestScore to score and save the move
                            bestScore = score
                            lastPosition = [i, j]
                            move = [a, b]
                            bestPiece = board[i][j]


        #After we checked every move, return the best one
        #print("a", move)

        #if move is not None:
        newRow, newCol = move
        row, col = lastPosition

        board[row][col] = 0
        board[newRow][newCol] = bestPiece

        return board
        
        #return self.__moveRandomPiece(currentBoard)

    def __updatePiecesOnBoard(self, board):
        self.piecesOnBoard = [0] * 5

        for i in range(len(board)):
            for j in range(len(board[0])):
                if self.__sameSign(board[i][j], self.piecesColor):
                    self.piecesOnBoard[abs(board[i][j])] = 1

    def __putRandomPiece(self, currentBoard):
        #Copy the board
        board = [row[:] for row in currentBoard]

        if (self.currentTurn<2):
            available_squares = [(1, 1), (1, 2), (2, 1), (2, 2)]

            for square in available_squares:
                row, col = square
                if board[row][col] == 0:
                    #print("aaaa", self.currentTurn, board[row][col] )
                    if(self.currentTurn==0):
                        board[row][col] = self.piecesCode[3]
                        return board
                    elif(self.currentTurn==1):
                        board[row][col] = self.piecesCode[2]
                        return board
        else:
            #myAlignedValue, myAlignedPieces, myMissingPieces, myMissingPositions= self.maxAlignedValue(board, self.piecesColor)
            pieces = self.getMissingPieces(board, self.piecesColor)
            
            row = -1
            col = -1
            #Set bestScore to a very small value
            bestScore = -math.inf

            move = None
            bestPiece = None

            for i in range(len(board)):
                for j in range(len(board[0])):
                    if board[i][j] == 0:
                        for k in pieces:
                            #Put 'O' in the available position
                            board[i][j] = k

                            #Call minimax to see how good the move is
                            #isMaximizing is false because it would be the human's turn
                            #Set alpha to a very small value and beta to a very large one
                            score = self.minimaxAB(board, 0, -math.inf, math.inf, True)

                            #Undo the change to the board
                            board[i][j] = 0

                            #If the score is bigger than the current best score
                            if score > bestScore:
                                #Set bestScore to score and save the move
                                bestScore = score
                                lastPosition = [i, j]
                                #move = [i, j]
                                bestPiece = k

            #newRow, newCol = move
            row, col = lastPosition

            board[row][col] = bestPiece
            #board[newRow][newCol] = bestPiece

        return board

    def play(self, board):
        start = time.time()
        self.currentTurn += 1
        self.__updatePiecesOnBoard(board)

        originalBoard = copy.deepcopy(board)

        # We put a limit since there can be a really rare case when the only valid movement is a capture
        # And if in that moment it happens that you can no longer make any capture, it will cicle. That's why we put a limit.
        for n,_ in enumerate(range(100)):
            if n<5 and (time.time() - start)<3:
                #print("heuristic")
                if self.currentTurn < 3: # or sum(self.piecesOnBoard) == 0:
                    newBoard = self.__putRandomPiece(board)
                else: # All the pieces are on the board
                    newBoard = self.__movePiece(board)
            else:
                #print("random")
                newBoard = self.__moveRandomPiece(board)

            _, wasCapture = self.__wasPieceMovement(originalBoard, newBoard)
            
            if wasCapture:
                if self.availableCaptures > 0:
                    self.availableCaptures -= 1
                else:
                    board = copy.deepcopy(originalBoard)
                    continue

            if newBoard != originalBoard:
                break
        
        self.__updatePawnDirection(newBoard)
        print("Time taken: ", time.time() - start)
        
        #self.print_matrix_mirror(newBoard)
        #print(newBoard, flush=True)

        #return utils.updateSyncBoard(syncBoard, newBoard)
        return newBoard

    #Minimax with Alpha-Beta pruning
    def minimaxAB(self, currentBoard, depth, alpha, beta, isMaximizing):
        #Copy the board
        board = [row[:] for row in currentBoard]

        #Evaluate the current position
        result = self.evaluatePosition(board)

        #If someone won
        if result == 10 or result == -10 or depth == 3:
            #Set eval to the value of the result in the dictionary
            
            #If the bot won, return the evaluation minus the depth, we want the fastest way to win
            #If the human won, return the evaluation plus the depth, the human would want the fastest win
            return result - depth if result > 0 else result + depth

        #Truno de nuestro bot
        if isMaximizing:
            #Set maxEval to a very small value
            maxEval = -math.inf

            #For every possible position in the board
            validMovements = self.__getCurrentValidMovements(board, self.piecesColor)  
            for coorx, piece in validMovements:
                #Put 'O' in the position
                for coor in coorx:
                    #print(coor)
                    i,j = coor
                    board[i][j] = piece

                    #New call to the minimax function with the new position
                    #Add one to the depth to know how many moves have been done
                    #isMaximizing is false because it would be the human's turn   
                    eval = self.minimaxAB(board, depth + 1, alpha, beta, False)

                    #Undo the move
                    board[i][j] = 0

                    #Set maxEval to the maximum between the current maxEval and the eval minimax returned
                    maxEval = max(maxEval, eval)
                    #Set alpha to the maximum between the current alpha and the eval minimax returned
                    alpha = max(alpha, eval)
                    #If beta is less or equal to alpha, we dont need to continue trying moves, so we break the loop
                    if beta <= alpha:
                        break

            #After all the moves, return the maxEval
            return maxEval    

        # turno del bot contrincante
        else:
            #Set minEval to a very large value
            minEval = math.inf

            #For every possible position in the board
            validMovements = self.__getCurrentValidMovements(board, self.piecesColor*-1)  
            for coorx, piece in validMovements:
                #Put 'O' in the position
                for coor in coorx:
                    i,j = coor
                    board[i][j] = piece

                    #New call to the minimax function with the new position
                    #Add one to the depth to know how many moves have been done
                    #isMaximizing is true because it would be the bot's turn    
                    eval = self.minimaxAB(board, depth + 1, alpha, beta, True)

                    #Undo the move
                    board[i][j] = 0

                    #Set minEval to the minimum between the current minEval and the eval minimax returned
                    minEval = min(minEval, eval)
                    #Set beta to the minimum between the current beta and the eval minimax returned
                    beta = min(beta, eval)
                    #If beta is less or equal to alpha, we dont need to continue trying moves, so we break the loop
                    if beta <= alpha:
                        break

            #After all the moves, return the minEval
            return minEval
    
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


    def evaluatePosition(self, board):
        
        '''
        if self.checkVictory(board, self.piecesColor):
            return 10
        elif self.checkVictory(board, self.piecesColor*-1):
            return -10
        '''
            
        myAlignedValue, myAlignedPieces, myMissingPieces, myMissingPositions= self.maxAlignedValue(board, self.piecesColor)
        oppAlignedValue, oppAlignedPieces, oppMissingPieces, oppMissingPositions = self.maxAlignedValue(board, self.piecesColor*-1)
    

        '''
        if myAlignedValue == 3:
            if self.isValidMove(board, myMissingPieces, myMissingPositions):
                return 8
            return 7
        elif(oppAlignedValue == 3): 
            if (self.isValidMove(board, oppMissingPieces, oppMissingPositions)):
                return -8
            return -7
        elif myAlignedValue == oppAlignedPieces:
            if(self.piecesColor in myAlignedPieces and self.piecesColor*2 in myAlignedPieces):
                return 6
            elif (self.piecesColor in myAlignedPieces or self.piecesColor*2 in myAlignedPieces):
                return 3
            elif(self.piecesColor*-1 in myAlignedPieces and self.piecesColor*-2 in myAlignedPieces):
                return -6
            elif (self.piecesColor*-1 in myAlignedPieces or self.piecesColor*-2 in myAlignedPieces):
                return -3
            myAlignedValue = self.countCenterPieces(board, self.piecesColor)
            oppAlignedValue = self.countCenterPieces(board, self.piecesColor*-1)
            '''
        if myAlignedValue > oppAlignedValue:
            return 10
        elif myAlignedValue < oppAlignedValue:
            return -10

            #return -1
        return 0


    def checkVictory(self, board, piecesColor):
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

        reverse_diagonal_values = [board[i][len(board)-1-i] for i in range(len(board))]
        if set(reverse_diagonal_values) - {0} == target_numbers:
            return True

        return False

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

    def maxAlignedValue(self, board, number_sign):
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

        return max_value, aligned_numbers, missing_numbers, missing_positions


    def can_pawn_move_vertically(self, board, current_position, target_position):
        current_row, current_col = current_position
        target_row, target_col = target_position

        if abs(target_row-current_row) == abs(target_col-current_col) == 1 and board[target_row][target_col] != 0 and self.currentTurn>0:
            return True

        if current_col != target_col:
            return False  # Pawns can only move vertically, not horizontally

        if current_row < target_row:
            # Check if there are any pieces blocking the pawn's vertical movement
            for row in range(current_row + 1, target_row):
                if board[row][current_col] != 0:
                    return False  # There is a piece blocking the pawn's path

        else:  # current_row > target_row
            # Check if there are any pieces blocking the pawn's vertical movement
            for row in range(target_row + 1, current_row):
                if board[row][current_col] != 0:
                    return False  # There is a piece blocking the pawn's path

        return True  # The pawn can move vertically to the target position

    def isValidMove(self, board, piece, target_position):
        # Check if the piece is already aligned or missing
        if piece == 0:
            return True


        for piece, position in zip(piece, target_position):
            x, y = position

            if(board[x][y] != 0 and self.currentTurn>0):
                if piece == 1 or piece == -1:
                    row = -1
                    col = -1
                    for i in range(4):
                        for j in range(4):
                            if board[i][j] == piece:
                                row = i
                                col = j
                                break
                    if(self.can_pawn_move_vertically(board, (row,col), (x,y))): 
                        return True
                    
                elif piece == 2 or piece == -2:
                    row = -1
                    col = -1
                    for i in range(4):
                        for j in range(4):
                            if board[i][j] == piece:
                                row = i
                                col = j
                                break
                    # Bishop can go to cells with the same parity as the initial position
                    if (x + y) % 2 == (row + col) % 2:
                        return True

                elif piece == 3 or piece == -3:
                    # Knight can go to any cell, no restrictions
                    return True

                elif piece == 4 or piece == -4:
                    # Rook can go to any cell, no restrictions
                    return True

                # Invalid piece value
                return False
            
            return False


    def reset(self):
        self.pawnDirection = -1
        self.piecesOnBoard = [0] * 5
        self.currentTurn = -1
        self.availableCaptures = 5