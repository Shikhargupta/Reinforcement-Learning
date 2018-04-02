## Markov Decision Processes

- Markov property states that state and rewards at a particular instant depends only upon the previous state and action only.
- Although, the assumption is not limited to the immediate previous state and action only. 

### Policy

- It is the algorithm used by agent to take an action (eg. epsilon greedy).
- Policy along with value function forms the solution.
- Optimal policy is th eone for which V(s) is max for all s.
- Optimal policies are not unique. More than 1 policy can result in max value function.

### Discount Factor

- Return, G(t), is the sum of all the future rewards.
- A discount factor is introduced to reduce the weight of rewards as we move further into the future so as to make it more realistic.

### Value Function

- Value function, V(s), is the expected value of Return given the state we are in.
- Action value function, Q(s,a), is the expected value of the future return given the current state and the action. 
- Value function of the immediate next state incorporates all the future rewards hence no need to go till the end to make a decision.


* It's more convinient to have Q(s,a) than V(s). In case of V(s) we have to iterate through all the actions to figure out which one gives the max V(s) but in Q(s,a) we just have to pick the action for which it is max.
