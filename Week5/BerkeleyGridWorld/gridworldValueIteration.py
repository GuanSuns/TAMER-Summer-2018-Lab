# gridworldValueIteration.py
# ------------
# Run Value Iteration on gridworld

import gridworld
import sys
import math


def isQValuesConverged(m_environment, old_qValues, new_qValues, delta=0.02):
    """
        check if the qValues have converged
    """
    states = m_environment.getGridWorld().getNonTerminalStates()
    # iterate through all the non-terminal states
    for state in states:
        for action in m_environment.getPossibleActions(state):
            diff = math.fabs(float(old_qValues[(state, action)]) - float(new_qValues[(state, action)]))
            print(str((state, action)) + ', value diff: ' + str(diff))
            if diff > delta:
                return False
    return True


def runEpoch(agent, m_environment, f_display, f_message, f_pause
             , i_epoch, global_step=0, delta=0.02):
    m_environment.reset()

    # save old qValues
    old_qValues = agent.getQValuesCopy()

    if 'startEpoch' in dir(agent):
        agent.startEpisode()
    f_message("BEGINNING EPOCH: " + str(i_epoch) + "\n")

    # iterate through all the possible state-action pairs
    for state in m_environment.getGridWorld().getNonTerminalStates():
        for action in m_environment.getPossibleActions(state):
            # set current state
            if 'startEpisode' in dir(agent):
                agent.startEpisode()
            m_environment.setCurrentState(state)
            # DISPLAY CURRENT STATE
            f_display(state)
            f_pause()

            # EXECUTE ACTION
            nextState, reward = m_environment.doAction(action)
            f_message("Step: " + str(global_step) +
                      ", S: " + str(state) +
                      ", A: " + str(action) +
                      ", S': " + str(nextState) +
                      ", R: " + str(reward) + "\n")

            # use temporal-difference update in q-learning agent
            if 'observeTransition' in dir(agent):
                agent.observeTransition(state, action, nextState, reward)
            # update global step
            global_step += 1

    # check if the qValue is converged
    is_converged = isQValuesConverged(m_environment, old_qValues, agent.getQValues(), delta)
    return (global_step, is_converged)


class GridworldValueIterationExperiment():
    # noinspection PyUnresolvedReferences
    def __init__(self, grid_name='DiscountGrid', discount=0.9, learning_rate=0.5, living_reward=0.0
                 , noise=0, epsilon=0.3, display_speed=0.5
                 , grid_size=150, text_only=False
                 , save_optimal_policy_file=None
                 , delta=0.02):

        ###########################
        # GENERAL CONTROL
        ###########################

        self.text_only = text_only
        self.display_speed = display_speed
        self.discount = discount
        self.delta = delta
        self.save_optimal_policy_file = save_optimal_policy_file

        ###########################
        # GET THE GRIDWORLD
        ###########################

        # noinspection PyUnresolvedReferences
        import gridworld
        mdp_function = getattr(gridworld, "get" + grid_name)
        self.mdp = mdp_function()
        self.mdp.setLivingReward(living_reward)
        self.mdp.setNoise(noise)
        self.env = gridworld.GridworldEnvironment(self.mdp)

        ###########################
        # GET THE DISPLAY ADAPTER
        ###########################

        import textGridworldDisplay
        self.display = textGridworldDisplay.TextGridworldDisplay(self.mdp)
        if not text_only:
            import graphicsGridworldDisplay
            self.display = graphicsGridworldDisplay.GraphicsGridworldDisplay(self.mdp, grid_size, display_speed)
        try:
            self.display.start()
        except KeyboardInterrupt:
            sys.exit(0)

        ###########################
        # GET THE TAMER AGENT
        ###########################

        import qlearningAgents
        # env.getPossibleActions, opts.discount, opts.learningRate, opts.epsilon
        # simulationFn = lambda agent, state: simulation.GridworldSimulation(agent,state,mdp)
        self.gridWorldEnv = gridworld.GridworldEnvironment(self.mdp)
        action_function = lambda state: self.mdp.getPossibleActions(state)
        q_learn_opts = {
            'gamma': discount,
            'alpha': learning_rate,
            'epsilon': epsilon,
            'actionFn': action_function
        }

        self.agent = qlearningAgents.QLearningAgent(**q_learn_opts)

    def start(self):
        ###########################
        # RUN EPISODES
        ###########################
        display_callback = lambda x: None
        if not self.text_only:
            display_callback = lambda state: self.display.displayQValues(self.agent, state, "CURRENT Q-VALUES")

        message_callback = lambda x: gridworld.printString(x)
        if self.text_only:
            message_callback = lambda x: None

        # FIGURE OUT WHETHER TO WAIT FOR A KEY PRESS AFTER EACH TIME STEP
        pause_callback = lambda: None

        total_steps = 0
        i_epoch = 0
        is_converged = False

        while not is_converged:
            (global_step, is_converged) = runEpoch(self.agent, self.env, display_callback, message_callback, pause_callback
                                                   , i_epoch, total_steps, self.delta)
            i_epoch += 1

        # DISPLAY POST-LEARNING VALUES / Q-VALUES
        try:
            self.display.displayQValues(self.agent, message="Q-VALUES AFTER " + str(i_epoch) + " EPOCHS")
            self.display.pause()
            self.display.displayValues(self.agent, message="VALUES AFTER " + str(i_epoch) + " EPOCHS")
            self.display.pause()
        except KeyboardInterrupt:
            sys.exit(0)
