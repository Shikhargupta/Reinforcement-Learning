## Build an Intelligent Tic-Tac-Toe

- In this module a walkthrough is provided to built a RL-based agent to play tic-tac-toe

- Components of a RL System
	- Agent: One who plays the game.
	- Environment: Agent interacts with it 
	- State: It represents a particular configuration or setup of the environment that an agent can sense. Any action of the agent may change the state of the environment.
	- Rewards: It is given to the agent depending upon his action which brings a change in the state of the environment.
	- Episode: One run of a game. 
	- Terminal State: State from where no further action can be taken.


- Rewards are not the measure of correct or incorrect action. It tells how good the action was. 


### Value Function

- AI needs to have the ability of planning and foresight. It shoukd see how present actions will result in *Delayed Rewards*.
- Hence each state is assigned a *Value* depending upon the future rewards it yields.
- Rewards are immediate while value is a measure of future rewards.
- Value function of a state is the expected value of all future rewards possible when if we are in that state.
- Initialization:
	- V(s) = 1 (if s is winning state)
	- V(s) = 0 (if s is losing or drawing state)
	- V(s) = 0.5 (otherwise)
- Update Equation: V(s) = V(s) + learning_rate*(V(s`) - V(s)) : We would want the value of a state to be closer to the value of next state. Suppose for a winning state (reward=1) all the preceding visited states should be moved closer to 1 as they eventually lead to a win.
- Explore-Exploit condition hence greedy-epsilon method will be implemented.
- Using the update equation we are moving V(s) closer to V(s`) hence V(s`) should me more accurate. Therefore update starts backwards, i.e from terminal states.


### Designing an Environment and an Agent.

#### Agent
- It interacts with the environment and takes action in order to gain maximum rewards.
- Each agent has its own history of states and the corresponding value function
- After each episode the agent updates its value functions according to the reward received.

#### Environment
- Environment class provides agent with rewards.
- It monitors the state of the game and notifies who has won the game or if the game is drawn. 


The value function incorporates intelligence into an agent. After each episode the agent updates the value function and becomes better. The states are enumerated using a hash function which translates each state into a decimal number. Also, to address the explore-exploit dilemma epsilon greedy method is used. With a probability epsilon the agent takes a random action and otherwise chooses the action with maximum value function.