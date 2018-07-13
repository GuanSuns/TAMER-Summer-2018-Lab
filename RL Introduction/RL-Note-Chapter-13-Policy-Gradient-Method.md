# Chapter 13 Policy Gradient Methods

## 1. Big Picture
### 1.1. Motivation
So far in RL Introduction, all the methods are action-value methods. However, in fact, the agent can learn a parameterized policy that can select actions without consulting a value function (A value function may still be used to learn the policy parameter, but it's not required for action selections)

- Formula: $\pi(a|s, \theta) = Pr\{A_t=a | S_t=s, \theta _ t = \theta\}$

### Update Rules
- **Performance measure**: $J(\theta)$
- **Objective**: maximize performance using gradient ascent in J 
- **Formula**: $\theta _{t+1} = \theta _t + \alpha \widehat{\triangledown J(\theta _t)}$






