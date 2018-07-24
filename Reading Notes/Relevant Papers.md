# Relevant Papers

## 1. Preference-Based RL

### 1.1. Motivation
we can directly learn from an expert’s preferences instead of a hand-designed numeric reward (agent’s performance can be very sensitive to the used numeric values)

### 1.2. Problems:
-   Do not explicit state the assumption
-   Lack coherent framework
-   How to express pairwise comparisons
-   Partial order: incomparable pairs (or difference can be infinitesimal)

### 1.3. Main approaches

#### 1.3.1. Types of preferences
- state
- action
- trajectory

#### 1.3.2. Approaches
- **Learn a utility functions**
	- surrogate function is not directly comparable to an approximated reward or return function because it may be subject to concept drift if the estimate of the expert’s optimality criterion can change over time. 
- **Learn a policy**: 
	- induce a distribution over a parametric policy space
	- compare and rank policies
- **Learn a preference model**
   
### 1.4. Action Preferences
#### 1.4.1. Notes
- feedback concerning the long-term return should be preferred: but this requires expert to be really familiar with the expected long-term outcome

#### 1.4.2. Papers
- J. Fürnkranz, E. Hüllermeier, W. Cheng, and S.-H. Park. **Preference-based reinforcement learning: A formal framework and a policy iteration algorithm**. Machine Learning, 89 (1-2):123–156, 2012. Special Issue of Selected Papers from ECML/PKDD-11
	- https://link.springer.com/content/pdf/10.1007%2Fs10994-012-5313-8.pdf
	- **Learn a preference model**
- W. B. Knox and P. Stone. **Reinforcement learning from simultaneous human and MDP reward**. In Proceedings of the 11th International Conference on Autonomous Agents and Multiagent Systems (AAMAS-12), pages 475–482. 2012.
	- https://pdfs.semanticscholar.org/4503/09925f91da287e7227c2034be1a119997e41.pdf
- E. Hüllermeier, J. Fürnkranz, W. Cheng, and K. Brinker. **Label ranking by learning pairwise preferences**. Artificial Intelligence, 172(16–17):1897–1916, 2008.
	- http://weiweicheng.com/research/papers/cheng-ai08.pdf
	- Combined classifiers via voting or weighted voting
	- **Learn a preference model**
- Wirth and J. Fürnkranz. **A policy iteration algorithm for learning from preference-based feedback**. In Advances in Intelligent Data Analysis XII: 12th International Symposium (IDA-13), volume 8207 of LNCS, pages 427–437. 2013a.
	- https://link.springer.com/chapter/10.1007/978-3-642-41398-8_37
	- Return a weighted vote for each action instead of a binary vote
	- **Learn a preference model**

### 1.5. State Preferences
#### 1.5.1. Notes
- more informative than action preferences because they define relations between parts of the global state space
- but also suffer from the **long-term/short-term optimality problem**
- State preferences are **slightly less demanding for the expert** as it is not required to compare actions for a given state. However, the expert still needs to estimate the future outcome of the policy for a given state.
- **Short-term optimality**: Short-term state preferences do not define a trade-off, because it is unclear whether visiting an undominated state once should be preferred over visiting a rarely dominated state multiple times.

#### 1.5.2. Papers
- **Long-term**: C. Wirth and J. Fürnkranz. **A policy iteration algorithm for learning from preference-based feedback**. In Advances in Intelligent Data Analysis XII: 12th International Symposium (IDA-13), volume 8207 of LNCS, pages 427–437. 2013a.
	- https://link.springer.com/content/pdf/10.1007%2F978-3-642-41398-8.pdf
- **Short-term**: (Optional, Robot Locomotion)M. Zucker, J. A. Bagnell, C. Atkeson, and J. Kuffner, Jr. **An optimization approach to rough terrain locomotion**. In Proceedings of the IEEE International Conference on Robotics and Automation (ICRA-10), pages 3589–3595. 2010.
	- http://www.cs.cmu.edu/~cga/papers/zucker-icra10.pdf
- C. Wirth and J. Fürnkranz. **First steps towards learning from game annotations**. In Proceedings of the ECAI Workshop on Preference Learning: Problems and Applications in AI, pages 53–58, 2012.
	- http://www.ke.tu-darmstadt.de/events/PL-12/papers/11-wirth.pdf
	- Use human annotations
	- **Learn value-based utility: state-preference**


### 1.6. Trajectory Preferences
#### 1.6.1. Notes
- The **least demanding** preferences type for the expert as she can directly evaluate the outcomes of full trajectories
- **Temporal credit assignment problem**: need to determine which states or actions are responsible for the encountered 
- In practice, almost no algorithm known to the authors (PbRL Survey) is capable of dealing with preferences between trajectories with different initial states. (**Deep RL from Human Preferences** uses trajectory segments with different initial states)

#### 1.6.2. Papers
- **A Bayesian Approach for Policy Learning from Trajectory Preference Queries**, NIPS 2012
	- http://papers.nips.cc/paper/4805-a-bayesian-approach-for-policy-learning-from-trajectory-preference-queries.pdf
	- **Induce a distribution over a parametric policy space**
	- Generate trajectories pair using ROLLOUT
- R. Busa-Fekete, B. Szörényi, P. Weng, W. Cheng, and E. Hüllermeier. **Preference-based evolutionary direct policy search**. In Proceedings of the ICRA Workshop on Autonomous Learning, 2013.
	- http://www.ecmlpkdd2013.org/wp-content/uploads/2013/09/PBRL_08-BusaFekete.pdf
	- **Compare and rank policies**
	- Generate trajectories pair using ROLLOUT
	- optimization can be performed with algorithms similar to *evolutionary direct policy search* (EDPS; Heidrich Meisner and Igel 2009)
- C. Wirth, J. Fürnkranz, and G. Neumann. **Model-Free Preference-based Reinforcement Learning** . In Proceedings of the 30th AAAI Conference on Artificial Intelligence (AAAI-16), pages 2222–2228, 2016.
	- https://ewrl.files.wordpress.com/2015/02/ewrl12_2015_submission_10.pdf
	- **Learn non-linear utility function**
- **Deep Reinforcement Learning from Human Preferences**, Paul F. Christiano, NIPS 2017
	- http://papers.nips.cc/paper/7017-deep-reinforcement-learning-from-human-preferences
	- **approximate a non-linear utility function**
	- **Learn Reward-Based utility**
- Kupcsik, D. Hsu, and W. S. Lee. **Learning dynamic robot-to-human object handover from human feedback**. In Proceedings of the 17th International Symposium on Robotics Research (ISRR-15), 2015.
	- https://arxiv.org/pdf/1603.06390.pdf
	- **Learn return-based utility**
- C. Wirth and J. Fürnkranz. **A policy iteration algorithm for learning from preference-based feedback**. In Advances in Intelligent Data Analysis XII: 12th International Symposium (IDA-13), volume 8207 of LNCS, pages 427–437. 2013a.
	- https://link.springer.com/chapter/10.1007/978-3-642-41398-8_37
	- Derive additional action preferences for intermediate states in trajectory preferences, defining an approximate solution to the temporal credit assignment problem.
