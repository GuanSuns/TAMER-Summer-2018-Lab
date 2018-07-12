# RL Reading Note: COACH

## 1. COACH: Interactive Learning from Policy-Dependent Human Feedback

### 1.1. Motivation: human feedback exhibits properties that are inconsistent with a traditional reward signal. (Much previous work has made the assumption that people are providing policy-independent feedback, while experiments show that it should be policy-dependent)

### 1.2. Huamn-Centered Reinforcement Learning
- Interpretion of huamn feedback
	- Reward function: bad way, often induces positive reward cycles that leads to unintended behaviors.
	- Comment on the agent's behavior: better interpretation


### 1.3. Advantage Function: evaluate how recent behavior is different from the trainer's desired policy
- Advantage function can successfully represent threee different kinds of feedback schemes
	- **Diminishing Feedback**: basic TAMER can't catch the change with time, it has to keep giving positive feedback on good behaviors; On the contrary, COACH requires the user stops giving positive feedback after the agent learns desirable policy. 
	- **Differential Feedback** 
	- **Policy Shaping**
- $f_{t} =A^{\pi}(s, a)= Q^{\pi}(s_t, a_t) - V^{\pi}(s_t)$


### 1.4. Comparison to TAMER:
- TAMER might have the **forgetting** of learned behavior issue

### 1.5. Properties:
- it's impossible for human trainer to provide feedback on each time step (spare human feedback): use eligibility traces
- Due to reaction time, human feedback is typically delayed by about 0.2 to 0.8 seconds

### 1.6. Implementation
- Environment:
	- Fast decison cycle: 33ms
	- Numeric feedback: +1,+4, -1
	- Data pre-processing (RGB images): see details in the paper
- COACH agent:
	- Maintains multiple eligibility traces with different temporal decay rates: $\lambda = 0.95$ for feedback +1 and -1, $\lambda = 0.9999$ for feedback +4 
	- feedback-action delay d=6, which is 0.198 seconds
	- use an actor-critic parameter-update rather than using the gradient of the policy

