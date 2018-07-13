# Chapter 12 Eligibility Traces Note

## 1. Big Picture
### 1.1. Motivation
Update can be done not just toward any n-step return, but toward any average of n-step returns.

### 1.2. Some concepts:
- **Compund update**: average simpler component updates like average of simple n-step returns (lambda formula 12.2)
- Understanding lambda return: lambda=1: reduces to Monte Carlo (large variance), lambda=0: one step TD method
- Understanding lambda return: parameter lambda characterizes how fast the exponential weighting falls off

### 1.3. Off-line lambda-return algorithm
- **Update**: formula 12.4
- Udpate at the end of the episode: can be modified to **n-step Truncated lambda-return method (TTD)**

### 1.4. => Computationally congenial implementation of lambda-return: TD(lambda)
- **Improvements over off-line lambda-return algorithm**:
    - update the weight vectors on every step
    - its computations are equally distributed instead of all at the end
    - can be applied to continuing problems
- Eligibility trace: short-term memory (weight vector is a long-term memory, accumulating over the lifetime of the system)
- Properties:
    - Each update depends on the current TD error combined with the current eligibility traces of past events
	- At each moment we look at the current TD error and assign it backward to each prior state according to how much that state contributed to the current eligibility trace at that time.
	- TD(1) is way of implementing MC algorithm that is more general

### 1.5. Instead of using truncation parameter n, we can redoing updates: The online lambda-return algorithm
- It's the best performing TD algorithm currently 
- But needs lots of computation resource

### 1.6. => Computationally congenial implementation of the online lambda-return algorithm: True Online TD(lambda)
- Pay attention to how it updtae the eligibility trace in the case of using function approximation (formula 12.11)


### 1.7. Sarsa(lambda): use eligibility traces for control


