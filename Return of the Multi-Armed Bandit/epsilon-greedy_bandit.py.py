import numpy as np
from matplotlib import pyplot as plt

#Defining class for Bandit Machine
class banditMachine:
    def __init__(self, m):
        self.m = m          #Actual mean of machine
        self.mean = 0       #Initial estimated mean assumed
        self.N = 0          #Number of samples collected

#Function pull() that returns the resulting sample value for bandit machine
    def pull(self):
        self.N = self.N + 1
        return (np.random.randn() + self.m)

#Function update() updates the estimated mean of a particular bandit machine after a pull
    def update(self, x):
        self.mean = (1-1.0/self.N)*self.mean + x/self.N

def run_experiment(m1, m2, m3, N, eps):
    #Instantiating 3 objects of class banditMachine() and initializing with actual means
    bandit = [banditMachine(m1), banditMachine(m2), banditMachine(m3)]
    data = np.empty(N)      #For storing sample values

    #Running loop for epsilon-greedy method
    for i in range(N):
        rand_num = np.random.random()
        if eps<rand_num:
            bandit_num = np.argmax([b.mean for b in bandit])
        else:
            bandit_num = np.random.choice(3)

        #Pulling the chosen machine and updating its mean
        x = bandit[bandit_num].pull()
        bandit[bandit_num].update(x)
        data[i] = x

    #Plotting cumulative average during the experimentation
    cumulative_average = np.cumsum(data)/(np.arange(N) + 1)
    plt.plot(cumulative_average)
    plt.show()

if __name__=='__main__':
    run_experiment(1,2,8,10000,0.01)
