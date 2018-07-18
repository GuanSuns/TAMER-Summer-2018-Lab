# RL Reading Note: Deep COACH

## 1. Deep COACH: Deep Reinforcement Learning from Policy-Dependent Human Feedback

### 1.1. Motivation
Adjust COACH to making use of the higher dimensional data

### 1.2. Update Rules
- Policy gradient:
$$\triangledown _{\theta _t} J(\theta _t) = E _ {a \sim \pi_ {\theta_t}(\cdot |s)} [ \triangledown _{\theta_{t}} log \pi_{\theta_t} (a|s) A^{\pi_{\theta_t}} (s, a)]$$ 
$$A^{\pi_{\theta_t}} (s, a) = Q^{\pi_{\theta_t}} (s, a)  - V^{\pi_{\theta_t}} (s)$$
- Eligibility traces with importance sampling:
$$e_{\lambda} = \lambda e_{\lambda} +  \frac{\pi_{\theta_t}(a_{t'}|s_{t'})}{\pi_{\theta_{t'}}(a_{t'}|s_{t'})}  \bigtriangledown _ {\theta_{t}} log \pi_{\theta_{t}} (a_{t'}|s_{t'})$$


### 1.3. How COACH got adjusted to DQN:
- In favor of an **eligibility Q-Networks**, deep COACH extends this idea using a replay
buffer where the atomic elements stored are **whole windows of experience**, rather than individual transitions.
- Eligibility traces are averaged over the entire minibatch and the mean eligibility trace is applied as a single updtate
- Using replay buffer creates a discrepancy between the policy being optimized at current timestep (simply use greedy selection) and the policy under which data sampled from the buffer was generated: use off-policy learning with **importance sampling**.
- Use **unsupervised pre-training**
- For robustness, restrict to relatively small policy network architectures
- To prevent the learned policy $\pi$ assigning all the probability to a single action at some state, employ the **entropy regularization**
- Limit the number of units in hidden layer (two fully-connected layers) to no more than 30


### 1.4. Implementation
- **Pre-training parameters**:
	- optimizer: Adam
	- learning rate: 0.001
	- mini-batch size: 32
	- 10,000 images
- **Policy network paramters**:
	- observation representation: 84 * 84
	- optimizer: RMSProp
	- human delay factor d: 1
	- learning rate: 0.00025
	- eligibility decay $\lambda$: 0.35
	- window size L: 10
	- mini-batch size m: 16
	- entropy regularization coefficient $\beta$: 1.5


### 1.5. Experiment results:
- **COACH**: not enough generalization; get locked into a sub-optimal policy
- **Deep TAMER**: demonstrate a certain degree of unstability
- **Deep COACH**: the vast majority of trainer feedback consists of negative signals discouraging incorrect behavior at the start of learning whereas a relatively smaller number of positive signals are actually needed to guide the agent towards good behavior. (also needs less feedbacks)
- Catastrophic **forgetting** exhibited in both TAMER and Deep-COACH, but COACH was able to fix it while TAMER's was irreversible.
