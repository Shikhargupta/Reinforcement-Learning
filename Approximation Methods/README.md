### Approximation Methods

- State space could be huge or it even might be a non-episodic task and hence determining the value for each state could be very expensive.

- Therefore we approximate V[s] and Q[s,a] using neural networks.

#### Monte Carlo Evaluation Using Approximation
Here we use linear regression to determine theta which gives minimum error for:

                   `V_hat = theta.x`

where V_hat is the prediction for value function given a state and x is the feature vector representing that state.

We apply stochastic gradient descent to calculate the gradient and change the parameter (theta):

          `theta = theta + alpha*(G - V_hat)*x`

![This](approx_mc_prediction.py) file contains the implementation.

<p align="center">
  <img src="approx_mc_prediction.JPG" width="300"/>
</p>

#### TD(0) Prediction Using Approximation
Approximation method could be applied to TD(0) prediction as well but it would be a semi-gradient as the target used here is itself a value function.

          `theta = theta + alpha*(r + V'[s] - V[s])`

![This](approx_td0_prediction.py) file contains the implementation.

<p align="center">
  <img src="approx_td0_prediction.JPG" width="300"/>
</p>

#### Semi-Gradient SARSA
Whatever we did for TD(0), same this is done here for SARSA.

![This](approx_sarsa.py) file contains the implementation.

<p align="center">
  <img src="approx_sarsa.JPG" width="300"/>
</p>
