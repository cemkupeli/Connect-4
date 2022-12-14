from datetime import datetime
import random
import math

# model is NFLstrategy class
# limit is time limit
def q_learn(model, limit):
    learning_rate = .2
    max_iteration = 1000
    discount_rate = .95
    exploration_rate = 1
    max_explor = 1
    min_explor = .01
    decay_rate = .00005
    gamma = 0.99
    learning_table = [0.1]* 9
    learning_rate_decy = 0.99999
    actions = model.offensive_playbook_size()
    q_table = [[0]*actions for i in range(9)]
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
                #action = max(q_table[cstate][:]) # fix later
                #for i in range(actions):
                 #   if action == (q_table[cstate][i]):
                  #      action = i
                   #     break

            else:
                actions = model.offensive_playbook_size()
                action = random.randint(0, actions -1)
            
            new_state, _ = model.result(state, action)
            reward = 0
            if (model.game_over(new_state)):
                if (model.win(new_state)):
                    reward = 8
                else:
                    reward = -8
            
            #yards to score/ time left
            cnew_state = classify(new_state)
            cstate = classify(state)


            q_table[cstate][action] = q_table[cstate][action] + learning_table[cstate] * (reward + gamma * max(q_table[cnew_state][:])
            - q_table[cstate][action])
            learning_table[cstate] *= learning_rate_decy
            state = new_state
            term = model.game_over(new_state)
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

def classify(new_state):
    #yards to score/ time left
    num1 = new_state[0] / (new_state[3] or 1)
    # distance / downs left
    num2 = new_state[2] / new_state[1]
    if num1 > 3.8:
        num1 = 0
    elif num1 > 1.8:
        num1 = 1
    else:
        num1 = 2
    
    if num2 > 4:
        num2 = 0
    elif num2 > 2:
        num2 = 1
    else:
        num2 = 2
    return num1*3 + num2   
