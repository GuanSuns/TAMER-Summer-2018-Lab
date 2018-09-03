# Relevant Papers: learning through human feedback

## 1. Reward Shaping

### 1.1. Difficulties
- Human feedback signals may be infrequent, or occasionally inconsistent with the optimal policy.
- The ambiguity of translating a statement like "yes, that's right" or "no" into a reward.


## 1.2. Papers

#### C. L. Isbell, C. Shelton, M. Kearns, S. Singh, and P. Stone, “A social reinforcement learning agent,” in Proc. of the 5th Intl. Conf. on Autonomous Agents , pp. 377–384, 2001.

#### H. S. Chang, “Reinforcement learning with supervision by combining multiple learnings and expert advices,” in Proc. of the American Control Conference , 2006.

#### W. B. Knox and P. Stone, “Tamer: Training an agent manually via evaluative reinforcement,” in Proc. of the 7th IEEE ICDL , pp. 292–297, 2008.

#### A. Tenorio-Gonzalez, E.Morales, and L. Villaseor-Pineda, “Dynamic reward shaping: training a robot by voice,” in Advances in Artificial Intelligence–IBERAMIA , pp. 483–492, 2010.


#### P. M. Pilarski, M. R. Dawson, T. Degris, F. Fahimi, J. P. Carey, and R. S. Sutton, “Online human training of a myoelectric prosthesis controller via actor-critic reinforcement learning,” in Proc. of the IEEE ICORR , pp. 1–7, 2011.

#### A. L. Thomaz and C. Breazeal, “Teachable robots: Understanding human teaching behavior to build more effective robot learners,” Artificial Intelligence , vol. 172, no. 6-7, pp. 716–737, 2008.



## 2. Policy Shaping

### 2.1. Properties
- Related to work in **transfer learning**
- Recent papers have observed that a **more effective** use of human feedback is as direct information about policies


### 2.2. Papers
#### Shane Griffith, Kaushik Subramanian, Jonathan Scholz, Charles Isbell, and Andrea L Thomaz. Policy shaping: Integrating human feedback with reinforcement learning. In Advances in Neural Information Processing Systems, 2013. **
- Define human feedback as ADVICE, the probility (s,a) is optimal is:
$$\frac{C^{\Delta _{s,a}}}{C^{\Delta _{s,a}} + (1-C) ^ {\Delta _{s,a}}}$$
where $\Delta$ is the difference between the number of "right" and "wrong" labels, C is the probility that a human might make mistake.
- THe probability of performing s,a according to the feedback policy $\pi _ E$ is 
$$C^{\Delta _{s,a}} + (1-C) ^ {\sum_{j \neq a} \Delta _{s,j}}$$
- How to use ADVICE: BQL (a kind of Q value) + ADVICE
- ADVICE is **more robust to noisy signal** from human (inconsistent feedback)


#### R.Maclin and J.W. Shavlik, “Creating advice-taking reinforcement learners,” Machine Learning , vol. 22, no. 1-3, pp. 251–281, 1996. 
- Use KBANN to incorporate knowledge, in the form of simple propositional rules, into a neural network.
- Advice helps prevent converging to local optimal. Good advice helphelp the agent explore states that are useful in finding the optimal plan.


#### L. Torrey, J. Shavlik, T. Walker, and R. Maclin, “Transfer learning via advice taking,” in Advances in Machine Learning I, Studies in Computational Intelligence *
- All advice rules create constraints on problem solution (in the form of preference, Preference-KBKB)
- Use Inductive logic programming ILP to express first-order logic clauses (skills)
- Skill Trasfer: use RL to select training examples for skills ->human provides mapping between skills to target task -> apply advice and human advice in taget task.
- Robust to bad advice

## 3. Human Demonstration
### 3.1. Properties
- $\clubsuit$ The ability to acquire new behaviors through learning is fundamentally important for the development of generatl purpose agent platforms that can be used for a variety of tasks
- $\clubsuit$ Human teacher provide particularly noisy and suboptimal data due to differences in embodiment and limitations of human ability.

### 3.2. Papers

#### A. Y. Ng and S. Russell, “Algorithms for inverse reinforcement learning,” in Proc. of the 17th ICML, 2000.
- Algorithm 1: Find the function R that maximizes 
$$\sum_{s \in S} (Q^{\pi} (s, a_1) - max_{a \in A \setminus  a _1} Q^{\pi}(s, a))$$
- Algorithm 2 (Linear Function Approximation)
- Algorithm 3 (IRL from Sampled Trajectories)

#### P. Abbeel and A. Y. Ng, “Apprenticeship learning via inverse reinforcement learning,” in Proc. of the 21st ICML, 2004.
- Motivation: the difficulty of manually specifying a reward function in the tasks like driving.
- ? Biomechanics and cognitive science research have shown that the reward function, rather than the policy or the value function is the most succinct and robust definition of the task.
- Need Monte Carlo to **sample trajectories**.
- $\clubsuit$ The performance guarantees of this algorithm only depend on matching the feature expectations, not on recovering the true underlying reward function.


#### C. Atkeson and S. Schaal, “Learning tasks from a single demonstration,” in Proc. of the IEEE ICRA , pp. 1706–1712, 1997.


#### M. Taylor, H. B. Suay, and S. Chernova, “Integrating reinforcement learning with human demonstrations of varying ability,” in Proc. of the Intl. Conf. on AAMAS , pp. 617–624, 2011.
- In many domians, collecting training data may beslow, expensive, which motivates the need for ways of making RL algorithms **more sample-efficient**.
- Three ways to use human demonstration to improve independent learning: 
	- Value Bonus: when the agent reaches a state suggested by the summarized policy, then add a constant bonus to the Q-value
	- Extra Action: when reaching a state suggested by the summarized policy, execute the suggested action
	- Probabilistic Policy Reuse: $\pi$-reuse Exploration 

