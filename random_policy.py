import random

def random_policy():
    def fxn(pos):
        move = random_move(pos)
        return move
    return fxn


def random_move(pos):
    return random.choice(pos.get_actions())
