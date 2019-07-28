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

def negative_grid(step_cost = -0.1):
    grid = grid_world()
    grid.rewards.update({(0,0):step_cost,
                         (0,1):step_cost,
                         (0,2):step_cost,
                         (1,0):step_cost,
                         (1,2):step_cost,
                         (2,0):step_cost,
                         (2,1):step_cost,
                         (2,2):step_cost,
                         (2,3):step_cost})

    return grid

def random_action(a,eps=0.1):
    draw = np.random.uniform()
    if draw < (1-eps):
        return a
    else:
        tmp = ['U','D','L','R']
        tmp.remove(a)
        action = np.random.choice(tmp)
        return action

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
    ALPHA = 0.1
    grid = negative_grid()

    print "Grid Rewards"
    print_values(grid.rewards, grid)

    Q = {}
    V = {}
    policy = {}
    states = grid.all_states()
    for s in states:
        Q[s] = {}
        V[s] = 0
        for a in ALL_POSSIBLE_ACTIONS:
            Q[s][a] = 0

    update_count_sa = {}
    update_count = {}
    for s in states:
        update_count_sa[s] = {}
        for a in ALL_POSSIBLE_ACTIONS:
            update_count_sa[s][a] = 1.0
    for it in range(10000):
        s = (2,0)
        grid.set_state(s)
        while not grid.game_over():
            action = max_dict(Q[s])[0]
            a = random_action(action,0.5)
            r = grid.take_action(a)
            s2 = grid.current_state()
            a2 = max_dict(Q[s2])[0]

            # print s,a,s2,a2,r
            alpha = ALPHA/update_count_sa[s][a]
            update_count_sa[s][a] += 0.005
            Q[s][a] = Q[s][a] + alpha*(r + gamma*Q[s2][a2] - Q[s][a])

            s = s2

    for s in grid.actions.keys():
        policy[s], V[s] = max_dict(Q[s])

    print "Final Values:"
    print_values(V,grid)

    print "Final Policy"
    print_policy(policy,grid)
