## Week 4
- Berkeley Grid World
	- Add Evaluation metric: number of episode/step to reach optimal policy
	- Add instant feedback: pause and wait until human feedback
	- Random starting initial starting position
	- Softmax action selection for exploration with overflow protection

## Week 5
- Berkeley Grid World
	- Make environment deterministic
	- Value Iteration Experiment: use value iteration to find the optimal (converged) values (Q-Values) in the Gridworld
	- QValue Saver and Loader: save the computed q-values to json files, as well as read q-values from json files
	- Record and display policy agreement ratio