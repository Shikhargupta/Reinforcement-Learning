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
            print "Cannot perform this action"
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

        assert(self.current_state in self.all_states)

    def game_over(self):
        return (self.state not in self.actions.keys())

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

if __name__ == '__main__':
    SMALL_ENOUGH = 1e-4 # threshold for convergence
    grid = grid_world()
    V = {}
    states = grid.all_states()
    for s in states:
        V[s] = 0
    gamma = 1
    while True:
        for s in states:

            if s in grid.actions.keys():
                biggest_change = 0
                no_of_actions = len(grid.actions[s])
                p_s = (1.0/no_of_actions)
                new_v = 0
                old_v = V[s]
                for a in grid.actions[s]:
                    grid.set_state(s)
                    reward = grid.take_action(a)
                    new_v += p_s*(reward + gamma*V[grid.current_state()])
                V[s] = new_v
                biggest_change = max(biggest_change, np.abs(old_v - new_v))
        if biggest_change < SMALL_ENOUGH:
            break
    print "values for uniformly distributed actions"
    print_values(V, grid)
    print "\n\n"


    actions = {(2,0):['U'],
               (0,0):['R'],
               (0,1):['R'],
               (0,2):['R'],
               (1,0):['U'],
               (1,2):['R'],
               (2,1):['R'],
               (2,2):['R'],
               (2,3):['U']}

    print_policy(actions,grid)
    gamma = 0.9

    for s in states:
        V[s] = 0
    grid.actions.update(actions)
    epochs = 0
    while True:
        for s in states:
            if s in grid.actions.keys():
                biggest_change = 0
                # print s
                no_of_actions = len(grid.actions[s])
                p_s = (1.0/no_of_actions)
                new_v = 0
                old_v = V[s]
                for a in grid.actions[s]:
                    grid.set_state(s)
                    # print p_s
                    reward = grid.take_action(a)
                    new_v += p_s*(reward + gamma*V[grid.current_state()])
                V[s] = new_v
                biggest_change = max(biggest_change, np.abs(old_v - new_v))
            epochs += 1
        # if biggest_change < SMALL_ENOUGH:
        if epochs > 1000:
            break
    print "values for fixed policy actions"
    print_values(V, grid)
