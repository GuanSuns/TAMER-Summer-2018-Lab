## Week 3
- **Berkeley Grid World**
	- Setup TAMER on berkely gridworld
	- Make it able to save Tamer (Q table, log) on every trial
- **Experiment Creater and Resumer**
	- Modify the original experiment launcher and resumer
	- Redirect all the output (print) to log files and make a copy of related files


## Week 4
- **Reading Note**
	- RL Reading Note - Chapter 4 DP: https://guansuns.github.io/blog/09/RL-Note-Chapter-4-DP/
- **Berkeley Grid World**
	- Add Evaluation metric: number of episode/step to reach optimal policy
	- Add instant feedback: pause and wait until human feedback
	- Random starting initial starting position
	- Softmax action selection for exploration with overflow protection

## Week 5
- **Reading Note**
	- RL Reading Note - Chapter 12 Eligibility Traces: https://guansuns.github.io/blog/08/RL-Note-Chapter-12-Eligibility-Traces/
- **Berkeley Grid World**
	- Make environment deterministic
	- Value Iteration Experiment: use value iteration to find the optimal (converged) values (Q-Values) in the Gridworld
	- QValue Saver and Loader: save the computed q-values to json files, as well as read q-values from json files
	- Record and display policy agreement ratio
	- Add temperature control into Softmax action selection
	- Visualize last state and action
	- Statistics Module: visualize and compare experiment results

## Week 6
- **Reading Note**
	- RL Reading Note - Covergent Actor-Critic by Humans (COACH): https://guansuns.github.io/blog/10/RL-Reading-Note-Covergent-Actor-Critic-by-Humans-COACH/
	- RL Reading Note - Deep COACH: https://guansuns.github.io/blog/11/RL-Reading-Note-Deep-COACH/
- **Berkeley Grid World**
	- Use distinct color to display 'STAY' move
	- Add flags to control how many details printed on the screen as log during the experiment
	- Experiment on TAMER with epsilon-greedy
	- Evaluate TAMER's performance in noise environment

## Week 7
- **Reading Note**
	- Double DQN: https://guansuns.github.io/blog/21/RL-Reading-Note-Double-DQN/
	- Deep RL from Human Preferences: https://guansuns.github.io/blog/22/Deep-RL-from-Human-Preferences/
- **Berkeley Grid World**
	- Use VDBE as epsilon annealing policy 
	- Use both global-wise epsilon annealing and episode-wise epsilon annealing

## Week 8
- **Reading Note**
	-  Preference-Based RL Relevant Paper: https://guansuns.github.io/blog/23/Relevant-Papers/
- **Berkeley Grid World**
	- Record and visualize VDBE values

## Week 9
- **Reading Note**
	-  Relevant Papers: learning through human feedback: https://guansuns.github.io/blog/02/Papers-RL-with-Human-Feedback/
- **Berkeley Grid World**
	- Add supports for preferences-based agents

## Week 10
- **Berkeley Grid World**
	- Add supports for preferences-based agents

