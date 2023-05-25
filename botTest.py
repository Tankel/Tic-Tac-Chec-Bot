from round_robin import RoundRobin

from player_random import TTCPlayer as RandomTTCPlayer
from player import TTCPlayer as NormalTTCPlayer
from player2 import TTCPlayer as Normal2TTCPlayer
from player3 import TTCPlayer as Normal3TTCPlayer
from evaluator import PlayerWrapper

player = Normal3TTCPlayer("Nacho")
player.setColor(1)
# player3 = TTCPlayer("juan3")
# player4 = TTCPlayer("juan4")



if __name__ == '__main__':
    board1 = [[-1, 0, 1, 0],
              [0, 0, -2, 0],
              [0, 4, 0, 0],
              [3, 0, 2, 0]]
    
    for n,i in enumerate(board1):
        print(i)

    newBoard = player.play(board1)
    n=0
    for i in newBoard:
        if n<4:
            print(i)
        n+=1