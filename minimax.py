import math

def minimax_policy(depth, h):
    def fxn(pos):
        value, move = minimax(pos, depth, h)
        return move
    return fxn


def minimax(pos, depth, h):
    ''' Returns the minimax value of the given position, with the given heuristic function
        applied at the given depth.

        pos -- a game position
        depth -- a nonnegative integer
        h -- a heuristic function that can be applied to pos and all its successors
    '''
    # print("Minimax called with depth", depth, "on following position:")
    # print(pos)
    # print("Position is terminal:", pos.is_terminal())
    # print("Current actor is:", pos.actor())
    if pos.is_terminal() or depth == 0:
        # print("Position is terminal or depth is 0, returning heuristic value")
        return (pos.heuristic(), None)
    else:
        if pos.actor() == 0:
            # max player
            best_value = -math.inf
            best_move = None
            moves = pos.get_actions()
            # if moves:
            #     print("Available moves:", moves)
            # else:
            #     print("No moves available")
            for move in moves:
                # print("Evaluating move", move, "for the following position:")
                # print(pos)
                child = pos.successor(move)
                # print("Successor is the following position:")
                # print(child)
                mm, _ = minimax(child, depth - 1, h)
                if mm > best_value:
                    best_value = mm
                    best_move = move
            return (best_value, best_move)
        else:
            # min player
            best_value = math.inf
            best_move = None
            moves = pos.get_actions()
            # if moves:
            #     print("Available moves:", moves)
            # else:
            #     print("No moves available")
            for move in moves:
                # print("Evaluating move", move, "for the following position:")
                # print(pos)
                child = pos.successor(move)
                # print("Successor is the following position:")
                # print(child)
                mm, _ = minimax(child, depth - 1, h)
                if mm < best_value:
                    best_value = mm
                    best_move = move
            return (best_value, best_move)
