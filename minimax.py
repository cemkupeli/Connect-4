# SOURCE: Adapted from starter code for CPSC 474 Fall 2022 Project 4

import math
import random

def minimax_policy(depth, randomness):
    def fxn(pos):
        if randomness > 1:
            raise ValueError('randomness can not be more than 1')
        num = random.random()
        if num < randomness:
            moves = pos.get_actions()
            move = random.choice(moves)
            return move
        value, move = minimax(pos, depth)
        return move
    return fxn


def minimax(pos, depth):
    ''' Returns the minimax value of the given position, with the given heuristic function
        applied at the given depth.

        pos -- a game position
        depth -- a nonnegative integer
        h -- a heuristic function that can be applied to pos and all its successors
    '''
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
                mm, _ = minimax(child, depth - 1)
                moves = pos.get_actions()
                if mm > best_value:
                    best_value = mm
                    best_move = move  
            return (best_value, best_move)
        else:
            # min player
            best_value = math.inf
            best_move = None
            moves = pos.get_actions()
            for move in moves:
                child = pos.successor(move)
                mm, _ = minimax(child, depth - 1)
                if mm < best_value:
                    best_value = mm
                    best_move = move
            return (best_value, best_move)
