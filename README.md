## Week 3
- **Berkeley Grid World**
	- Setup TAMER on berkely gridworld
	- Make it able to save Tamer (Q table, log) on every trial
- **Experiment Creater and Resumer**
	- Modify the original experiment launcher and resumer
	- Redirect all the output (print) to log files and make a copy of related files


## Week 4
- **Berkeley Grid World**
	- Add Evaluation metric: number of episode/step to reach optimal policy
	- Add instant feedback: pause and wait until human feedback
	- Random starting initial starting position
	- Softmax action selection for exploration with overflow protection

## Week 5
- **Berkeley Grid World**
	- Make environment deterministic
	- Value Iteration Experiment: use value iteration to find the optimal (converged) values (Q-Values) in the Gridworld
	- QValue Saver and Loader: save the computed q-values to json files, as well as read q-values from json files
	- Record and display policy agreement ratio
	- Add temperature control into Softmax action selection
	- Visualize last state and action
	- Statistics Module: visualize and compare experiment results

## Week 6
- **Berkeley Grid World**
	- Use distinct color to display 'STAY' move
	- Add flags to control how many details printed on the screen as log during the experiment
	- Experiment on TAMER with epsilon-greedy
	- Evaluate TAMER's performance in noise environment
	