import numpy as np

ALL_POSSIBLE_ACTIONS = ['D','U','L','R']

class Grid:
    def __init__(self, height, width, start):
        self.height = height
        self.width = width
        self.i = start[0]
        self.j = start[1]

    def set(self, rewards, actions):
        self.rewards = rewards
        self.actions = actions

    def set_state(self,state):
        self.i = state[0]
        self.j = state[1]

    def current_state(self):
        return (self.i, self.j)

    def is_terminal(self, state):
        if state not in self.actions.keys():
            return True
        return False

    def take_action(self,action):
        if action in self.actions[(self.i, self.j)]:
            if action == 'U':
                self.i -= 1
            elif action == 'D':
                self.i += 1
            elif action == 'L':
                self.j -= 1
            elif action == 'R':
                self.j += 1
        else:
            # print "Cannot perform this action"
            return 0
        return self.rewards[(self.i, self.j)]

    def undo_move(self, action):
        if action == 'U':
            self.i += 1
        elif action == 'D':
            self.i -= 1
        elif action == 'L':
            self.j += 1
        elif action == 'R':
            self.j -= 1

        assert(self.current_state() in self.all_states)

    def game_over(self):
        return (self.current_state() not in self.actions.keys())

    def all_states(self):
        return set(self.actions.keys() + self.rewards.keys())

def grid_world():
    grid = Grid(3,4,[2,0])
    rewards = {(0,0):0,
               (0,1):0,
               (0,2):0,
               (0,3):1,
               (1,0):0,
               (1,2):0,
               (1,3):-1,
               (2,0):0,
               (2,1):0,
               (2,2):0,
               (2,3):0}

    actions = {(0,0):['R','D'],
               (0,1):['R','L'],
               (0,2):['R','L','D'],
               (1,0):['U','D'],
               (1,2):['U','R','D'],
               (2,0):['U','R'],
               (2,1):['L','R'],
               (2,2):['L','R','U'],
               (2,3):['L','U']}

    grid.set(rewards, actions)
    return grid

def print_values(V, g):
    for i in range(g.height):
        print("---------------------------")
        for j in range(g.width):
            v = V.get((i,j), 0)
            if v >= 0:
                print " %.2f|" % v,
            else:
                print "%.2f|" % v, # -ve sign takes up an extra space
        print ""


def print_policy(P, g):
    for i in range(g.height):
        print("---------------------------")
        for j in range(g.width):
            a = P.get((i,j), ' ')
            print "  %s  |" % a[0],
        print "\n"

def play_game(grid, policy, gamma):
    possible_start_states = grid.actions.keys()
    random_start_state = np.random.choice(len(possible_start_states))

    s = possible_start_states[random_start_state]
    action = np.random.choice(ALL_POSSIBLE_ACTIONS)
    grid.set_state(s)
    state_action_reward = [(s,action,0)]
    seen_state = []
    num_steps = 0
    while True:
        reward = grid.take_action(action)
        num_steps += 1
        s = grid.current_state()
        if s in seen_state:
            reward = -10.0/num_steps
            state_action_reward.append((s,None,reward))
            break
        elif grid.game_over():
            state_action_reward.append((s,None,reward))
            break
        else:
            action = policy[s]
            state_action_reward.append((s,action,reward))
        seen_state.append(s)

    G = 0
    state_action_total = []
    first = True
    for s,a,r in reversed(state_action_reward):
        if first:
            reward = r
            first = False
            continue
        G = reward + gamma*G
        state_action_total.append((s,a,G))
        reward = r
    state_action_total.reverse()
    return state_action_total

def max_dict(d):
    # returns the argmax (key) and max (value) from a dictionary
    # put this into a function since we are using it so often
    max_key = None
    max_val = float('-inf')
    for k, v in d.items():
        if v > max_val:
            max_val = v
            max_key = k
    return max_key, max_val

if __name__ == '__main__':
    gamma = 0.9
    SMALL_ENOUGH = 1e-4 # threshold for convergence
    grid = grid_world()
    V = {}
    policy = {}
    for s in grid.actions.keys():
        policy[s] = np.random.choice(grid.actions[s])

    Q = {}
    states = grid.all_states()
    returns = {}
    for s in states:
        if s in grid.actions.keys():
            Q[s] = {}
            for a in ALL_POSSIBLE_ACTIONS:
                Q[s][a] = 0
                returns[(s,a)] = []
        else:
            V[s] = 0

    for t in range(2000):
        results = play_game(grid,policy,gamma)
        seen_state_action = []
        for s,a,G in results:
            sa = (s,a)
            if sa not in seen_state_action:
                seen_state_action.append(sa)
                returns[sa].append(G)
                Q[s][a] = np.mean(returns[sa])
        for s in policy.keys():
            policy[s] = max_dict(Q[s])[0]
            V[s] = max_dict(Q[s])[1]

    print "Final Values:"
    print_values(V,grid)

    print "Final Policy"
    print_policy(policy,grid)
