# Chapter 4 Dynamic Programming Reading Note

## Big Picture
### Assumption: finite MDP

### Applications
- Application 1: Policy Evaluation (prediction problem)
	- Method **iterative policy evaluation**: iterative methods using a sequence of approximated values
	- Key concepts: expected update

- Application 2: Policy Improvement
	- Theorem: policy improvement therem, **inequality 4.7 and 4.8**

- Application 3: Policy Iteration (iterative policy eval and policy improvement)
	- Features: fast converge
	- Cons:  Policy evaluation requires mltiple sweeps through the entire state space

- Improvement 1: Value Iteration (synchronous)
	- Features: faster converge becasue one sweep combines one sweep of policy eval and one sweep of policy improvement

- Improvement 2: Asynchronous DP
	- Features: not necessary to perform DP methods in complete sweeps through the entire state set. **in-place** iterative methods
	- converge as long as keep visiting all the states
	- preferred for large state space

### Generalization
- GPI (generalizaed policy iteration): **evaluation &larr;&rarr; policy improvement (greedy)**
- Optimal when stable (no change)

### Problems of DP
- may not be practical for very large problems though it's efficient (much faster than search algorithm)

