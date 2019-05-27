import numpy as np
from defs import *

class agent:
    def __init__(self):

    def take_action():

    def updt_state_hstry():

class environment:
    def __init__(self):
        self.board = []
        self.winner = None
        self.num_states = 3**9

    def game_ovr():

    def draw():

    def get_state():

    def winner():

def play_game(p1, p2, env, draw=False):

    while !env.game_ovr():
        if currrent_player = p1:
            current_player = p2
        else:
            current_player = p1

    if (draw==1 and current_player==p1) or (draw==2 and current_player==p2):
        env.draw()

    current_player.take_action()

    if draw:
        env.draw()
    state = env.get_state()
    p1.updt_state_hstry(state)
    p2.updt_state_hstry(state)

def get_state_hash_and_result(i=0, j=0, env):
    results = []

    for v in (0, env.x, env.o):
        env.board[i,j] = v
        if j==2:
            if i==2:
                state = env.get_state()
                ended = env.game_ovr()
                winner = env.winner()
                results.append((state, ended, winner))
            else:
                results += get_state_hash_and_result(i+1, 0, env)
        else:
            results += get_state_hash_and_result(i, j+1, env)
    return results

def initialize_Vx(env, state_space_info):
    V = np.zeros(env.num_states)

    for state, status, result in state_space_info:
        if status==game_status_rc.GAME_OVER:
            if result==win_rc.WINNER_IS_X:
                v = 1
            else:
                v = 0
        else:
            v = 0.5
        V[state] = v

def initialize_Vo(env, state_space_info):
    V = np.zeros(env.num_states)

    for state, status, result in state_space_info:
        if status==game_status_rc.GAME_OVER:
            if result==win_rc.WINNER_IS_O:
                v = 1
            else:
                v = 0
        else:
            v = 0.5
        V[state] = v

if __name__ == '__main__':
    p1 = agent()
    p2 = agent()
    env = environment()

    episodes = 100
    state_info = get_state_hash_and_result(0, 0, env)

    for ep in len(episodes):
        play_game(p1, p2, env, True)
