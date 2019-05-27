import numpy as np
from defs import *

#Agent class.
#This will interact with the environment and take actions.
class Agent:
    def __init__(self):
        self.eps = 0.1           #Exploring probability
        self.state_history = []  #History of all the states seen by the agent
        self.alpha = 0.5         #Learning rate
        self.verbose = False

    def reset_history(self):
        self.state_history = []

    def set_verbose(self, v):
        self.verbose = v

    #take action under the explore-exploit dilemma
    def take_action(self, env):
        possible_moves = []
        for i in xrange(params.LENGTH):
            for j in xrange(params.LENGTH):
                if env.is_cell_empty(i,j):
                    possible_moves.append((i,j))
        r = np.random.rand()
        if r < self.eps:
            if self.verbose:
                print "Exploring"
            idx = np.random.randint(low=0, high=len(possible_moves))
            next_move = possible_moves[idx]
        else:
            pos2value = {}
            Vmax = 0
            for moves in possible_moves:
                i = moves[0]
                j = moves[1]
                env.board[i,j] = self.sym
                state = env.get_state()
                env.board[i,j] = 0
                pos2value[(i,j)] = self.V[state]
                if self.V[state] > Vmax:
                    Vmax = self.V[state]
                    best_state = state
                    next_move = (i,j)
            if self.verbose:
                print "Exploiting"
                print "------------------"
                for i in range(params.LENGTH):

                    for j in range(params.LENGTH):
                        if env.is_cell_empty(i, j):
                            # print the value
                            print " %.2f|" % pos2value[(i,j)],
                        else:
                            print "  ",
                            if env.board[i,j] == env.x:
                                print "x  |",
                            elif env.board[i,j] == env.o:
                                print "o  |",
                            else:
                                print "   |",
                        print "",
                    print "\n------------------"

        env.board[next_move[0], next_move[1]] = self.sym

    def updt_state_hstry(self, state):
        self.state_history.append(state)

    def update_sym(self, sym):
        self.sym = sym

    #value function update routine
    def update(self, env):
        reward = env.reward(self.sym)
        target = reward
        for state in reversed(self.state_history):
            self.V[state] += self.alpha*(target - self.V[state])
            target = self.V[state]
        self.reset_history()

    def setV(self, V):
        self.V = V

#Environment class.
#It is the surrounding of an agent and acts upon the actions and give rewards.
class Environment:
    def __init__(self):
        self.board = np.zeros((params.LENGTH,params.LENGTH))
        self.winner = None
        self.num_states = 3**(params.LENGTH**2)
        self.x = 1
        self.o = -1
        self.status = game_status_rc.GAME_IN_PROGRESS

    def is_cell_empty(self, i, j):
        return self.board[i, j] == 0

    def reward(self, sym):
        if self.status == game_status_rc.GAME_IN_PROGRESS:
            return 0
        return self.winner == sym

    #routine to check if game is over (win, draw)
    def game_ovr(self, force=False):
        for i in range(params.LENGTH):
            if np.sum(self.board[i,:]) == params.LENGTH*self.x:
                self.winner = self.x
                self.status = game_status_rc.GAME_OVER
                return self.status
            elif np.sum(self.board[i,:]) == params.LENGTH*self.o:
                self.winner = self.o
                self.status = game_status_rc.GAME_OVER
                return self.status
            elif np.sum(self.board[:,i]) ==  params.LENGTH*self.o:
                self.winner = self.o
                self.status = game_status_rc.GAME_OVER
                return self.status
            elif np.sum(self.board[:,i]) == params.LENGTH*self.x:
                self.winner = self.x
                self.status = game_status_rc.GAME_OVER
                return self.status

        if np.trace(self.board) == params.LENGTH*self.x:
            self.winner = self.x
            self.status = game_status_rc.GAME_OVER
            return self.status
        elif np.trace(self.board) == params.LENGTH*self.o:
            self.winner = self.o
            self.status = game_status_rc.GAME_OVER
            return self.status
        elif np.fliplr(self.board).trace == params.LENGTH*self.x:
            self.winner = self.x
            self.status = game_status_rc.GAME_OVER
            return self.status
        elif np.fliplr(self.board).trace == params.LENGTH*self.o:
            self.winner = self.o
            self.status = game_status_rc.GAME_OVER
            return self.status

        for row in self.board:
            for cell in row:
                if cell == 0:
                    self.winner = None
                    self.status = game_status_rc.GAME_IN_PROGRESS
                    return self.status
        self.winner = None
        self.status = game_status_rc.GAME_DRAW
        return self.status

    def draw(self):
        print "-------------"
        for i in range(params.LENGTH):
            for j in range(params.LENGTH):
                if self.is_cell_empty(i, j):
                    print "0 |",
                else:
                    if self.board[i,j] == self.x:
                        print "x |",
                    elif self.board[i,j] == self.o:
                        print "o |",
            print ""
            print "-------------"

    def get_state(self):
        bitlist = ""
        for row in self.board:
            for cell in row:
                if cell == 0:
                    bitlist += "0"
                elif cell == env.x:
                    bitlist += "1"
                elif cell == env.o:
                    bitlist += "2"
        return int(bitlist, 3)

#main game playing routine
def play_game(p1, p2, env, draw=False):
    current_player = None
    while env.game_ovr() != game_status_rc.GAME_OVER and env.game_ovr() != game_status_rc.GAME_DRAW:
        if current_player == p1:
            current_player = p2
        else:
            current_player = p1

        if (draw==1 and current_player==p1) or (draw==2 and current_player==p2):
            env.draw()

        current_player.take_action(env)
        state = env.get_state()
        p1.updt_state_hstry(state)
        p2.updt_state_hstry(state)

    p1.update(env)
    p2.update(env)

def get_state_hash_and_result(env, i=0, j=0):
    results = []

    for v in [0, env.x, env.o]:
        env.board[i,j] = v
        if j==2:
            if i==2:
                state = env.get_state()
                status = env.game_ovr()
                winner = env.winner
                results.append((state, status, winner))
            else:
                results += get_state_hash_and_result(env, i+1, 0)
        else:
            results += get_state_hash_and_result(env, i, j+1)
    return results

def initialize_Vx(env, state_space_info):
    V = np.zeros(env.num_states)

    for state, status, winner in state_space_info:
        if status==game_status_rc.GAME_OVER:
            if winner==env.x:
                v = 1
            else:
                v = 0
        else:
            v = 0.5
        V[state] = v
    return V

def initialize_Vo(env, state_space_info):
    V = np.zeros(env.num_states)

    for state, status, winner in state_space_info:
        if status==game_status_rc.GAME_OVER:
            if winner==env.o:
                v = 1
            else:
                v = 0
        else:
            v = 0.5
        V[state] = v
    return V

class Human:
    def __init__(self):
        pass

    def set_symbol(self, sym):
        self.sym = sym

    def take_action(self, env):
        while True:
      # break if we make a legal move
            move = raw_input("Enter coordinates i,j for your next move (i,j=0..2): ")
            i, j = move.split(',')
            i = int(i)
            j = int(j)
            if env.is_cell_empty(i, j):
                env.board[i,j] = self.sym
                break

    def update(self, env):
        pass

    def updt_state_hstry(self, s):
        pass


if __name__ == '__main__':
    # train the agent
    p1 = Agent()
    p2 = Agent()

    # set initial V for p1 and p2
    env = Environment()
    state_winner_triples = get_state_hash_and_result(env)
    # for state, status, winner in state_winner_triples:
        # if status == game_status_rc.GAME_OVER:
            # print state, winner

    Vx = initialize_Vx(env, state_winner_triples)
    p1.setV(Vx)
    Vo = initialize_Vo(env, state_winner_triples)
    p2.setV(Vo)

    # give each player their symbol
    p1.update_sym(env.x)
    p2.update_sym(env.o)

    T = 10000
    for t in range(T):
        if t % 200 == 0:
            print t
        play_game(p1, p2, Environment())

    # play human vs. agent
    # do you think the agent learned to play the game well?
    human = Human()
    human.set_symbol(env.o)
    while True:
        p1.set_verbose(True)
        play_game(p1, human, Environment(), draw=2)
    # I made the agent player 1 because I wanted to see if it would
    # select the center as its starting move. If you want the agent
    # to go second you can switch the human and AI.
        answer = raw_input("Play again? [Y/n]: ")
        if answer and answer.lower()[0] == 'n':
            break
