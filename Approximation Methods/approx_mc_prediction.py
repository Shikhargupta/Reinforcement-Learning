import numpy as np

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

def s2x(state):
    x1 = state[0]
    x2 = state[1]
    return np.array([x1-1, x2-1.5, x1*x2-3, 1])

def random_action(a,eps=0.1):
    draw = np.random.uniform()
    if draw < (1-eps):
        return a
    else:
        tmp = ['U','D','L','R']
        tmp.remove(a)
        action = np.random.choice(tmp)
        return action

def play_game(grid, policy, gamma):
    s = (2,0)
    grid.set_state(s)
    state_and_reward = [(s,0.0)]
    while not grid.game_over():
        action = policy[s]
        a = random_action(action)
        reward = grid.take_action(a)
        s = grid.current_state()
        state_and_reward.append((s,reward))
    G = 0.0
    state_and_total = [(s,G)]
    first = True
    for s,r in reversed(state_and_reward):
        if first:
            reward = r
            first = False
            continue
        G = reward + gamma*G
        state_and_total.append((s,G))
        reward = r
    state_and_total.reverse()
    return state_and_total[:-1]

if __name__ == '__main__':
    gamma = 0.9
    SMALL_ENOUGH = 1e-4 # threshold for convergence
    grid = grid_world()
    V = {}
    policy = {
        (2,0): 'U',
        (1,0): 'U',
        (0,0): 'R',
        (0,1): 'R',
        (0,2): 'R',
        (1,2): 'U',
        (2,1): 'L',
        (2,2): 'U',
        (2,3): 'L'
    }
    learning_rate = 0.001

    states = grid.all_states()
    for s in states:
        if s not in grid.actions.keys():
            V[s] = 0
    theta = np.random.randn(4)/2
    t = 1
    for it in range(20000):
        if it%100 == 0:
            t += 0.001
        alpha = learning_rate/t
        results = play_game(grid,policy,gamma)
        seen_states = []
        for s,G in results:
            if s not in seen_states:
                seen_states.append(s)
                x = s2x(s)
                V_hat = np.dot(theta, x)
                theta += alpha*(G - V_hat)*x

    for s in grid.actions.keys():
        V[s] = np.dot(theta, s2x(s))

    print "Values:"
    print_values(V,grid)

    print "Policy:"
    print_policy(policy,grid)
