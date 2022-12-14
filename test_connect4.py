from connect4 import Connect4
from random_policy import random_policy

if __name__ == '__main__':

    num_games = 100000
    p0_wins = 0
    p0_policy = random_policy()
    p1_wins = 0
    p1_policy = random_policy()

    for _ in range(num_games):
        board = Connect4()
        pos = board.initial_state()
        turn = pos.actor()

        while not pos.is_terminal():
            pos = pos.successor(p0_policy(pos) if turn == 0 else p1_policy(pos))
            turn = 1 - turn
        
        if pos.payoff() == 0:
            p0_wins += 0.5
            p1_wins += 0.5
        elif pos.payoff() == 1:
            p0_wins += 1
        elif pos.payoff() == -1:
            p1_wins += 1
    
    print(p0_wins / (p0_wins + p1_wins))
