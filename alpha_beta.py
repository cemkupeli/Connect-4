from datetime import datetime
import random
import math

def alpha_beta_policy(depth, h):
    def fxn(pos):
        #move = MCTS(pos, time_limit) # if MCTS was class
        #res =  move.till_end_time() # if run was function in class
        # h is heuristic class
        val, move = alpha_beta(pos, depth, -math.inf, math.inf, h)
        return move
    return fxn

def alpha_beta(pos, depth, alpha, beta, h):
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
                mm, _ = alpha_beta(child, depth - 1, alpha, beta, h)
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
                mm, _ = alpha_beta(child, depth - 1, alpha, beta, h)
                if mm < best_value:
                    best_value = mm
                    best_move = move
                beta = min(beta, best_value)
                if alpha > beta:
                    break
            return (best_value, best_move)
