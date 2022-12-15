# SOURCE: Adapted from starter code for CPSC 474 Fall 2022 Project 4

from datetime import datetime
import random
import math

def alpha_beta_policy(depth, randomness):
    def fxn(pos):
        if randomness > 1:
            raise ValueError('randomness can not be more than 1')
        num = random.random()
        if num < randomness:
            moves = pos.get_actions()
            move = random.choice(moves)
            return move
        val, move = alpha_beta(pos, depth, -math.inf, math.inf)
        return move
    return fxn

def alpha_beta(pos, depth, alpha, beta):
    if pos.is_terminal() or depth == 0:
        return (pos.heuristic(), None)
    else:
        

        if pos.actor() == 0:
            # max player
            best_value = -math.inf
            best_move = None
            moves = pos.get_actions()
            for move in moves:
                child = pos.successor(move)
                mm, _ = alpha_beta(child, depth - 1, alpha, beta)
                if mm > best_value:
                    best_value = mm
                    best_move = move
                alpha = max(best_value, alpha)
                if alpha > beta:
                    break
            return (best_value, best_move)
        else:
            # min player
            best_value = math.inf
            best_move = None
            moves = pos.get_actions()
            for move in moves:
                child = pos.successor(move)
                mm, _ = alpha_beta(child, depth - 1, alpha, beta)
                if mm < best_value:
                    best_value = mm
                    best_move = move
                beta = min(beta, best_value)
                if alpha > beta:
                    break
            return (best_value, best_move)
