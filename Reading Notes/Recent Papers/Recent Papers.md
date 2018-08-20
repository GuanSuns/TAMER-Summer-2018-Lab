
# Papers read recently

## Label Ranking by Learning Pairwise Preferences **
- Learning **piarwise preference** (pairwise classification) $\rightarrow$ comnining predicted preferences into a ranking (can be voting, several algorithms could be used)
- $\clubsuit$ Pairwise comparison
![Pairwise comparison
](https://lh3.googleusercontent.com/DuEdIMDiCmUgvvjLv4Ij6c6DN59EEfvrIPSE6gUZ7_fJp6kBJfcXvNETqjam6_pEm_VrmmAtPE4 "Pairwise comparison")

## Preference-Based Policy Iteration: Leveraging Preference Learning for Reinforcement Learning
- Use ROLLOUT to estimate state-action value: might be not efficient enough
- Use Q values to elicit preferences (train a label ranker)


## Preference-based Evolutionary Direct Policy Search
- The goal of PBR algorithm is to find the k best random variables with respect to the surrogate decision model
- Extension of the evolutionary direct policy search algorithm

## Model-Free Preference-based Reinforcement Learning *
- Use trajectory preferences (leverage trajectory utility function)
- $\clubsuit$ Use preferences to update w (features weights vector):
 ![
](https://lh3.googleusercontent.com/qUJtwUCQzwtTI0zcK7FDJ7ZBqGQGuKCjG-mqv_4buedQPChvWNt4dRCaRUExuKdH54x7wXmXeG8 "figure0")
- The policy update of actor critic REPS is inspired by the episodic REPS algorithm (Daniel et al., 2012).
- Based on the Relative Entropy Policy Search (REPS) algorithm (Peters et al., 2010): Actor Critic relative Entropy Policy Search
- Reweighting Old Preferences.

## A policy Iteration Algorithm for Learning from Preference-Based Feedback **
- Use feedback based on **complete trajectories**
- $\clubsuit$ $Pr(a|s)$ follows the estimation in "Pairwise Neural Network Classifiers with Probabilistic Outputs":
$$Pr(a|s) = \frac{1}{\sum_{a' \in A(s), a' \neq a}{\frac{1}{Pr(a \succ a' |s )}}  - (|A(s)| - 2) }$$
- $\clubsuit$ Use simple boosting update to improve $Pr(a \succ a' |s)$
- Definition of preference: $Pr(T_1 \succ T_2 | m=p) = \frac{p}{n}$, where m is the number of **decisive states**
- $Pr(s \in M) = \frac{1}{2}$, $Pr(a \succ a' |s, T_1 \succ T_2) = \frac{n+1}{2n}$, where n is the number of **overlapping states** 
- Use algorithms like EXP3 to solve exploration/exploitation dilemma

## Preference-based Policy Learning *
- $\clubsuit$ **Process**: the robot demonstrates a new policy $\rightarrow$ the expert ranks the policies (human's preferences will be added to the constraints set C) 88 $\rightarrow$ **learn a policy return estimate J built from all constraints in C** $\rightarrow$ generate new policy based on policy return estimate
- Use BvR to map policy into real valued vector $\mu$
- $\clubsuit$ Use a standard constrained convex optimization formula to learn **policy return estimation**
- Can't use gradient-like methods since the policy return estimate is not defined on the parametric representation space of the policy: use $1+\lambda - ES$ algorithm instead.
- Need to think about parametric representation of policies and the behavioral representation of policies.

## Thoughts
- How to reuse past preferences (replay buffer): Reweighting Old Preferences.
- How to handle conflicting preferences
- How to understand human feedback: 
	- "$$a_t > a_{t-1}$$" might be more reasonable but hard to implement.
	- "$a_t$ better than any other", need to handle confiction in replay buffer.
- Under TAMER settings, no need to worry about how to elicit trajectories for comparison, but need to think about what to compare (current trajectory vs what) and the length of clips to be evaluated.
- Current preference learning frameworks do not intend to handle the case that human preferences might change. They only compare two specific trajectories.
- How to convert preferences to policy
	- pairwise model or something else? (pairwise might be more efficient and precise)