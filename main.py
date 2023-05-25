from round_robin import RoundRobin

from player_random import TTCPlayer as RandomTTCPlayer
from player import TTCPlayer as NormalTTCPlayer
from player2 import TTCPlayer as Normal2TTCPlayer
from player3 import TTCPlayer as Normal3TTCPlayer
from player4 import TTCPlayer as Normal4TTCPlayer

player1 = RandomTTCPlayer("brandon")
player2 = Normal4TTCPlayer("Nacho")
#player3 = Normal2TTCPlayer("Nacho")
#player4 = Normal3TTCPlayer("Brandon")

if __name__ == '__main__':
    tournament = RoundRobin([player2, player1], 20, 7, 70)
    tournament.start()
