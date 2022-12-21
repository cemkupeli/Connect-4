import math
import time
import random

def q_learn(board, time_limit):
    # Parameters that will be used in the q-learning algorithm
    epsilon = 1
    epsilon_max = 1
    epsilon_min = 0.01
    epsilon_decay = 0.00005
    learning_rate = 0.0001
    learning_rate_decay = 0.99999
    gamma = 0.95

    # An n-tuple network will be used as a function approximator for the q-learning algorithm
    # Source: https://link.springer.com/content/pdf/10.1007/978-3-642-32937-1.pdf?pdf=button
    # Page 187 explains how the algorithm works and provides insight into how q-values are stored and accessed

    # Creates an n-tuple by performing a random walk and returns a list of the selected indices
    def get_n_tuple(n):
        indices = [random.randint(0, board.nrows * board.ncols - 1)] # initialize list with a random index
        for _ in range(n - 1):
            candidates = [] # Allow duplicates, as they could be a better fit for the tuple than singly-adjacent tiles
            for index in indices:
                # Check lower bound
                if index % board.nrows != 0 and index - 1 not in indices:
                    candidates.append(index - 1)
                # Check upper bound
                if (index + 1) % board.nrows != 0 and index + 1 not in indices:
                    candidates.append(index + 1)
                # Check left bound
                if index >= board.nrows and index - board.nrows not in indices:
                    candidates.append(index - board.nrows)
                # Check right bound
                if index + board.nrows <= board.nrows * board.ncols - 1 and index + board.nrows not in indices:
                    candidates.append(index + board.nrows)
            # Pick a candidate randomly and add it to the n-tuple
            indices.append(random.choice(candidates))
        return indices
    
    # Create a list of n-tuples
    NUM_N_TUPLES = 80
    TUPLE_LEN = 8
    n_tuples = [get_n_tuple(TUPLE_LEN) for _ in range(NUM_N_TUPLES)]
    # print(n_tuples)

    # Create two q-tables that store q(s, a) for every state s of every n-tuple paired with each possible action, one per player
    MAX_INDEX_ENCODING = 2 # each board location has a value of 0 for empty, 1 for player 0, 2 for player 1
    TUPLE_STATE_SPACE = (MAX_INDEX_ENCODING + 1) ** (TUPLE_LEN - 1) * TUPLE_LEN
    q_table0 = [[[0 for _ in range(TUPLE_STATE_SPACE)]
                 for _ in range(NUM_N_TUPLES)]
                 for _ in range(board.ncols)]
    q_table1 = [[[0 for _ in range(TUPLE_STATE_SPACE)]
                 for _ in range(NUM_N_TUPLES)]
                 for _ in range(board.ncols)]

    # List of learning rates for every state of every n-tuple, one per player
    lr_table0 = [[learning_rate for _ in range(TUPLE_STATE_SPACE)]
                 for _ in range(NUM_N_TUPLES)]
    lr_table1 = [[learning_rate for _ in range(TUPLE_STATE_SPACE)]
                 for _ in range(NUM_N_TUPLES)]

    ## Function approximator mapping the state space to the n-tuple network
    # Returns a list where every element is the current state for the corresponding n-tuple, in order
    def get_mapping(curr_pos):
        states = []
        for i in range(NUM_N_TUPLES):
            state = 0
            for j in range(TUPLE_LEN):
                index = n_tuples[i][j]
                value = curr_pos._cols[index]
                state += value * (MAX_INDEX_ENCODING + 1) ** j
            states.append(state)
        return states

    # Returns the q(s, a) value for the given position-action pair by summing the q-values across all n-tuples
    # Mapping calculated in advance by call to get_mapping and passed by reference to avoid recalculating for each action
    def get_q_value(mapping, action, player):
        value = 0
        for i in range(NUM_N_TUPLES):
            value += q_table0[action][i][mapping[i]] if player == 0 else q_table1[action][i][mapping[i]]
        return value

    # Update q(s, a) values and corresponding learning rates
    def update_table(mapping, action, reward, future_reward, player):
        for i in range(NUM_N_TUPLES):
            if player == 0:
                q_table0[action][i][mapping[i]] = q_table0[action][i][mapping[i]] + lr_table0[i][mapping[i]] * (
                    reward + gamma * future_reward - q_table0[action][i][mapping[i]])
                # Learning rate decay
                lr_table0[i][mapping[i]] *= learning_rate_decay
            else:
                q_table1[action][i][mapping[i]] = q_table1[action][i][mapping[i]] + lr_table1[i][mapping[i]] * (
                    reward + gamma * future_reward - q_table1[action][i][mapping[i]])
                # Learning rate decay
                lr_table1[i][mapping[i]] *= learning_rate_decay


    # Run q-learning until the time limit is reached
    num_iterations = 0
    start_time = time.time()
    while time.time() - time_limit < start_time:
        pos = board.initial_state()
        while not pos.is_terminal():
            # Pick action using epsilon-greedy
            mapping = []
            action = 0
            if random.random() < epsilon:
                action = random.choice(pos.get_actions())
            else:
                mapping = get_mapping(pos)
                action = max(pos.get_actions(), key = lambda a: get_q_value(mapping, a, pos.actor()))

            # Get next state based on action and reward for action
            next_pos = pos.successor(action)
            reward = 0
            end_reached = False
            if next_pos.is_terminal():
                reward = next_pos.payoff() if pos.actor() == 0 else -next_pos.payoff()
                end_reached = True
                
                
            # Update q(s, a) in q_table
            if not mapping:
                mapping = get_mapping(pos)
            if end_reached:
                update_table(mapping, action, reward, 0, pos.actor()) # no future reward if next state is a terminal position
            else:    
                next_mapping = get_mapping(next_pos)
                next_action = max(next_pos.get_actions(), key = lambda a: get_q_value(next_mapping, a, next_pos.actor()))
                max_future_reward = -get_q_value(next_mapping, next_action, next_pos.actor())
                update_table(mapping, action, reward, max_future_reward, pos.actor())

            # Update current position
            pos = next_pos

        # Epsilon decay
        epsilon = epsilon_min + (epsilon_max - epsilon_min) * math.exp(-epsilon_decay * num_iterations)

        # Update number of iterations
        num_iterations += 1
    
    print(q_table0)
    print(q_table1)
    print("Number of games:", num_iterations)
    def fxn(position):
        mapping = get_mapping(position)
        action = max(position.get_actions(), key = lambda a: get_q_value(mapping, a, position.actor()))
        # print(action) # FOR TESTING
        return action
    return fxn