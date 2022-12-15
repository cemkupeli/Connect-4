from datetime import datetime
import random
import math

# model is class
# limit is time limit


def q_learning(model, limit):
    learning_rate = .2
    max_iteration = 1000
    discount_rate = .95
    exploration_rate = 1
    max_explor = 1
    min_explor = .01
    decay_rate = .00005
    gamma = 0.99
    learning_table = [0.1]* 1000000
    learning_rate_decy = 0.999
    actions = model.get_actions()
    q_table = [[0]*actions for i in range(100000)]
    #print(q_table)
    count = 0
    start_time = datetime.now()

    while True:
        # run
        step = 0
        total_rewards = 0
        state = model.initial_position()

        for iter in range(max_iteration):
            num = random.random()
            if num > exploration_rate:
                cstate = classify(state)
                action = max(range(actions), key = lambda a: q_table[cstate][a])

            else:
                actions = model.get_actions()
                action = random.randint(0, actions -1)
            
            new_state, _ = model.result(state, action)
            reward = 0
            if (model.is_terminal(new_state)):
                if (model.win(new_state)):
                    reward = 8
                else:
                    reward = -8

            cnew_state = classify(new_state)
            cstate = classify(state)


            q_table[cstate][action] = q_table[cstate][action] + learning_table[cstate] * (reward + gamma * max(q_table[cnew_state][:])
            - q_table[cstate][action])
            learning_table[cstate] *= learning_rate_decy
            state = new_state
            term = model.is_terminal(new_state)
            if (term == True):
                break

        exploration_rate = min_explor + (max_explor - min_explor) * math.exp(-decay_rate*count)
        count += 1
        if (datetime.now() - start_time).total_seconds() > limit:
            break
    #state = classify(model.initial_position())
    #print(count)
    def returns(pos):
        pos = classify(pos)
        #print(max(range(actions), key = lambda a: q_table[pos][a]))
        return max(range(actions), key = lambda a: q_table[pos][a]) 


    return returns

def classify(state):
    num = 0
    power = 0
    for i in range(len(state)):
        num += state[i] * 7**power
        if state[i] == 0 and i < 6:
            num += 3 * 7**power
        elif state[i] == 0:
            if state[i-7] != 0:
                num += 3 * 7**power
    return num
