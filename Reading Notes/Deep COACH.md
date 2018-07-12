# RL Reading Note: Deep COACH

## 1. Deep COACH: Deep Reinforcement Learning from Policy-Dependent Human Feedback
### 1.1. Motivation: adjust COACH to making use of the higher dimensional data

### 1.2. Properties:
- maximize expected sum of rewards using **policy gradient**
- In favor of an **eligibility Q-Networks**, deep COACH extends this idea using a replay
buffer where the atomic elements stored are **whole windows of experience**, rather than individual transitions.
- using replay buffer creates a discrepancy between the policy being optimized at current timestep and the policy under which data sampled from the buffer was generated: use off-policy learning with **importance sampling**.
- Use **unsupervised pre-training**
- For robustness, restrict to relatively small policy network architectures

### 1.3. Experiment results:
- **COACH**: not enough generalization; get locked into a sub-optimal policy
- **Deep TAMER**: demonstrate a certain degree of unstability
- **Deep COACH**: the vast majority of trainer feedback consists of negative signals discouraging incorrect behavior at the start of learning whereas a relatively smaller number of positive signals are actually needed to guide the agent towards good behavior. (also needs less feedbacks)
- Catastrophic **forgetting** exhibited in both TAMER and Deep-COACH, but COACH was able to fix it while TAMER's was irreversible.
