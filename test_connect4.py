from connect4 import Connect4
from random_policy import random_policy
from minimax import minimax_policy
from alpha_beta import alpha_beta_policy
from q_learn import q_learning_policy
import time
import sys

if __name__ == '__main__':

    if len(sys.argv) != 4:
        sys.exit("Usage: ./Connect4 {python3 | pypy3} agent {depth | training-time} games")

    parameter = None
    agent = sys.argv[1]
    if (agent == "alpha-beta" or agent == "q-learning"):
        try:
            parameter = int(sys.argv[2]) if agent == "alpha-beta" else float(sys.argv[2])
        except:
            sys.exit("Invalid parameter")
    else:
        sys.exit("Valid agents: alpha-beta, q-learning")
    
    num_games = 0
    try:
        num_games = int(sys.argv[3])
    except:
        sys.exit("Number of games must be an integer")

    print("\nFINAL PROJECT - CONNECT 4")
    print("Group members: Cem Kupeli, Jeffrey Zhou\n")
    print("Current test:", 
          "alpha-beta versus minimax runtime comparison" if agent == "alpha-beta" else "q-learning versus random",
          f"at depth {parameter}" if agent == "alpha-beta" else f"with {parameter} seconds of training time")
    
    if agent == "q-learning":
        print("Training agent...")

    randomness = 0.1
    p0_wins = 0
    p0_time = 0
    p0_policy = alpha_beta_policy(parameter, randomness) if agent == "alpha-beta" else q_learning_policy(Connect4(), parameter)
    p1_time = 0
    p1_wins = 0
    p1_policy = minimax_policy(parameter, randomness) if agent == "alpha-beta" else random_policy()

    print("Running", num_games, "games...\n")

    for _ in range(num_games):
        board = Connect4()
        pos = board.initial_state()
        turn = pos.actor()

        while not pos.is_terminal():
            move_start_time = time.time()
            pos = pos.successor(p0_policy(pos) if turn == 0 else p1_policy(pos))
            if turn == 0:
                p0_time += time.time() - move_start_time
            else:
                p1_time += time.time() - move_start_time
            turn = 1 - turn
        
        if pos.payoff() == 0:
            p0_wins += 0.5
            p1_wins += 0.5
        elif pos.payoff() == 1:
            p0_wins += 1
        elif pos.payoff() == -1:
            p1_wins += 1

    print("Player 0", "(alpha-beta)" if agent == "alpha-beta" else "(q-learning)", "win rate:", p0_wins / (p0_wins + p1_wins))
    if agent == "alpha-beta":
        print("Player 0 total runtime:", round(p0_time, 3), "seconds")
        print("Player 1 total runtime:", round(p1_time, 3), "seconds")
