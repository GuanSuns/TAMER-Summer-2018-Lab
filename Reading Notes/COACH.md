# COACH

## COACH: Interactive Learning from Policy-Dependent Human Feedback

### Motivation: human feedback exhibits properties that are inconsistent with a traditional reward signal.


### Advantage Function: evaluate how recent behavior is different from the trainer's desired policy
- Advantage function can successfully represent threee different kinds of feedback schemes
	- Diminishing Feedback
	- Differential Feedback 
	- Policy Shaping


### Comparison to TAMER:
- TAMER might have the forgetting of learned behavior issue

### Properties:
- it's impossible for human trainer to provide feedback on each time step (spare human feedback): use eligibility traces


## Deep COACH: Deep Reinforcement Learning from Policy-Dependent Human Feedback
### Motivation: adjust COACH to making use of the higher dimensional data

### Properties:
- maximize expected sum of rewards using **policy gradient**
- In favor of an **eligibility Q-Networks**, deep COACH extends this idea using a replaybuffer where the atomic elements stored are **whole windows of experience**, rather than individual transitions.
- using replay buffer creates a discrepancy between the policy being optimized at current timestep and the policy under which data sampled from the buffer was generated: use off-policy learning with **importance sampling**.
- Use **unsupervised pre-training**
- For robustness, restrict to relatively small policy network architectures

### Experiment results:
- **COACH**: not enough generalization; get locked into a sub-optimal policy
- **Deep TAMER**: demonstrate a certain degree of unstability
- **Deep COACH**: the vast majority of trainer feedback consists of negative signals discouraging incorrect behavior at the start of learning whereas a relatively smaller number of positive signals are actually needed to guide the agent towards good behavior. (also needs less feedbacks)
- Catastrophic **forgetting** exhibited in both TAMER and Deep-COACH, but COACH was able to fix it while TAMER's was irreversible.
