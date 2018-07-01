# gridworld.py
# ------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import random
import sys
import mdp
import environment
import util
import optparse
import qValueSaver
import matplotlib.pyplot as plt
import numpy as np

from input import user_input


class Gridworld(mdp.MarkovDecisionProcess):
    """
      Gridworld
    """

    def __init__(self, grid):
        # layout
        if isinstance(grid, list):
            grid = makeGrid(grid)
        self.grid = grid

        # parameters
        self.livingReward = 0.0
        self.noise = 0.2

    def setLivingReward(self, reward):
        """
        The (negative) reward for exiting "normal" states.

        Note that in the R+N text, this reward is on entering
        a state and therefore is not clearly part of the state's
        future rewards.
        """
        self.livingReward = reward

    def setNoise(self, noise):
        """
        The probability of moving in an unintended direction.
        """
        self.noise = noise

    def getPossibleActions(self, state):
        """
        Returns list of valid actions for 'state'.

        Note that you can request moves into walls and
        that "exit" states transition to the terminal
        state under the special action "done".
        """
        if state == self.grid.terminalState:
            return ()
        x, y = state
        if type(self.grid[x][y]) == int:
            return ('exit',)
        return ('north', 'west', 'south', 'east')

    def getStates(self):
        """
        Return list of all states.
        """
        # The true terminal state.
        states = [self.grid.terminalState]
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                if self.grid[x][y] != '#':
                    state = (x, y)
                    states.append(state)
        return states

    def getNonTerminalStates(self):
        """
        Return list of non-terminal states.
        """
        states = list()
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                if self.grid[x][y] != '#':
                    state = (x, y)
                    states.append(state)
        return states

    def getReward(self, state, action, nextState):
        """
        Get reward for state, action, nextState transition.

        Note that the reward depends only on the state being
        departed (as in the R+N book examples, which more or
        less use this convention).
        """
        if state == self.grid.terminalState:
            return 0.0
        x, y = state
        cell = self.grid[x][y]
        if type(cell) == int or type(cell) == float:
            return cell
        return self.livingReward

    def getStartState(self):
        start_states = list()
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                if self.grid[x][y] == 'S' or self.grid[x][y] == ' ':
                    start_states.append((x, y))
        if len(start_states) == 0:
            raise Exception('Grid has no start state')
        return random.choice(start_states)

    def isTerminal(self, state):
        """
        Only the TERMINAL_STATE state is *actually* a terminal state.
        The other "exit" states are technically non-terminals with
        a single action "exit" which leads to the true terminal state.
        This convention is to make the grids line up with the examples
        in the R+N textbook.
        """
        return state == self.grid.terminalState

    def getTransitionStatesAndProbs(self, state, action):
        """
        Returns list of (nextState, prob) pairs
        representing the states reachable
        from 'state' by taking 'action' along
        with their transition probabilities.
        """

        if action not in self.getPossibleActions(state):
            raise Exception("Illegal action!")

        if self.isTerminal(state):
            return []

        x, y = state

        if type(self.grid[x][y]) == int or type(self.grid[x][y]) == float:
            termState = self.grid.terminalState
            return [(termState, 1.0)]

        successors = []

        northState = (self.__isAllowed(y + 1, x) and (x, y + 1)) or state
        westState = (self.__isAllowed(y, x - 1) and (x - 1, y)) or state
        southState = (self.__isAllowed(y - 1, x) and (x, y - 1)) or state
        eastState = (self.__isAllowed(y, x + 1) and (x + 1, y)) or state

        if action == 'north' or action == 'south':
            if action == 'north':
                successors.append((northState, 1 - self.noise))
            else:
                successors.append((southState, 1 - self.noise))

            massLeft = self.noise
            successors.append((westState, massLeft / 2.0))
            successors.append((eastState, massLeft / 2.0))

        if action == 'west' or action == 'east':
            if action == 'west':
                successors.append((westState, 1 - self.noise))
            else:
                successors.append((eastState, 1 - self.noise))

            massLeft = self.noise
            successors.append((northState, massLeft / 2.0))
            successors.append((southState, massLeft / 2.0))

        successors = self.__aggregate(successors)

        return successors

    def __aggregate(self, statesAndProbs):
        counter = util.Counter()
        for state, prob in statesAndProbs:
            counter[state] += prob
        newStatesAndProbs = []
        for state, prob in counter.items():
            newStatesAndProbs.append((state, prob))
        return newStatesAndProbs

    def __isAllowed(self, y, x):
        if y < 0 or y >= self.grid.height:
            return False
        if x < 0 or x >= self.grid.width:
            return False
        return self.grid[x][y] != '#'


class GridworldEnvironment(environment.Environment):

    def __init__(self, gridWorld):
        self.gridWorld = gridWorld
        self.reset()
        self.state = None

    def getGridWorld(self):
        return self.gridWorld

    def getCurrentState(self):
        return self.state

    def setCurrentState(self, state):
        self.state = state

    def getPossibleActions(self, state):
        return self.gridWorld.getPossibleActions(state)

    def doAction(self, action):
        state = self.getCurrentState()
        (nextState, reward) = self.getRandomNextState(state, action)
        self.state = nextState
        return (nextState, reward)

    def getRandomNextState(self, state, action, randObj=None):
        rand = -1.0
        if randObj is None:
            rand = random.random()
        else:
            rand = randObj.random()
        sum_result = 0.0
        successors = self.gridWorld.getTransitionStatesAndProbs(state, action)
        for nextState, prob in successors:
            sum_result += prob
            if sum_result > 1.0:
                raise Exception('Total transition probability more than one; sample failure.')
            if rand < sum_result:
                reward = self.gridWorld.getReward(state, action, nextState)
                return (nextState, reward)
        raise Exception('Total transition probability less than one; sample failure.')

    def reset(self):
        self.state = self.gridWorld.getStartState()


class Grid:
    """
    A 2-dimensional array of immutables backed by a list of lists.  Data is accessed
    via grid[x][y] where (x,y) are cartesian coordinates with x horizontal,
    y vertical and the origin (0,0) in the bottom left corner.

    The __str__ method constructs an output that is oriented appropriately.
    """

    def __init__(self, width, height, initialValue=' '):
        self.width = width
        self.height = height
        self.data = [[initialValue for _ in range(height)] for _ in range(width)]
        self.terminalState = 'TERMINAL_STATE'

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, key, item):
        self.data[key] = item

    def __eq__(self, other):
        if other is None:
            return False
        return self.data == other.data

    def __hash__(self):
        return hash(self.data)

    def copy(self):
        g = Grid(self.width, self.height)
        g.data = [x[:] for x in self.data]
        return g

    def deepCopy(self):
        return self.copy()

    def shallowCopy(self):
        g = Grid(self.width, self.height)
        g.data = self.data
        return g

    def _getLegacyText(self):
        t = [[self.data[x][y] for x in range(self.width)] for y in range(self.height)]
        t.reverse()
        return t

    def __str__(self):
        return str(self._getLegacyText())


def makeGrid(gridString):
    width, height = len(gridString[0]), len(gridString)
    grid = Grid(width, height)
    for ybar, line in enumerate(gridString):
        y = height - ybar - 1
        for x, el in enumerate(line):
            grid[x][y] = el
    return grid


def getCliffGrid():
    grid = [[' ', ' ', ' ', ' ', ' '],
            ['S', ' ', ' ', ' ', 10],
            [-100, -100, -100, -100, -100]]
    return Gridworld(makeGrid(grid))


def getCliffGrid2():
    grid = [[' ', ' ', ' ', ' ', ' '],
            [8, 'S', ' ', ' ', 10],
            [-100, -100, -100, -100, -100]]
    return Gridworld(grid)


def getDiscountGrid():
    grid = [[' ', ' ', ' ', ' ', ' '],
            [' ', '#', ' ', ' ', ' '],
            [' ', '#', 1, '#', 10],
            ['S', ' ', ' ', ' ', ' '],
            [-10, -10, -10, -10, -10]]
    return Gridworld(grid)


def getBridgeGrid():
    grid = [['#', -100, -100, -100, -100, -100, '#'],
            [1, 'S', ' ', ' ', ' ', ' ', 10],
            ['#', -100, -100, -100, -100, -100, '#']]
    return Gridworld(grid)


def getBookGrid():
    grid = [[' ', ' ', ' ', +1],
            [' ', '#', ' ', -1],
            ['S', ' ', ' ', ' ']]
    return Gridworld(grid)


def getMazeGrid():
    grid = [[' ', ' ', ' ', +1],
            ['#', '#', ' ', '#'],
            [' ', '#', ' ', ' '],
            [' ', '#', '#', ' '],
            ['S', ' ', ' ', ' ']]
    return Gridworld(grid)


def getUserAction(state, actionFunction):
    """
    Get an action from the user (rather than the agent).

    Used for debugging and lecture demos.
    """
    import graphicsUtils
    action = None
    while True:
        keys = graphicsUtils.wait_for_keys()
        if 'Up' in keys:
            action = 'north'
        if 'Down' in keys:
            action = 'south'
        if 'Left' in keys:
            action = 'west'
        if 'Right' in keys:
            action = 'east'
        if 'q' in keys:
            sys.exit(0)
        if action is None:
            continue
        break
    actions = actionFunction(state)
    if action not in actions:
        action = actions[0]
    return action


def printString(x):
    print x


def parseOptions():
    optParser = optparse.OptionParser()
    optParser.add_option('-d', '--discount', action='store',
                         type='float', dest='discount', default=0.9,
                         help='Discount on future (default %default)')
    optParser.add_option('-r', '--livingReward', action='store',
                         type='float', dest='livingReward', default=0.0,
                         metavar="R", help='Reward for living for a time step (default %default)')
    optParser.add_option('-n', '--noise', action='store',
                         type='float', dest='noise', default=0.2,
                         metavar="P", help='How often action results in ' +
                                           'unintended direction (default %default)')
    optParser.add_option('-e', '--epsilon', action='store',
                         type='float', dest='epsilon', default=0.3,
                         metavar="E", help='Chance of taking a random action in q-learning (default %default)')
    optParser.add_option('-l', '--learningRate', action='store',
                         type='float', dest='learningRate', default=0.5,
                         metavar="P", help='TD learning rate (default %default)')
    optParser.add_option('-i', '--iterations', action='store',
                         type='int', dest='iters', default=10,
                         metavar="K", help='Number of rounds of value iteration (default %default)')
    optParser.add_option('-k', '--episodes', action='store',
                         type='int', dest='episodes', default=1,
                         metavar="K", help='Number of epsiodes of the MDP to run (default %default)')
    optParser.add_option('-g', '--grid', action='store',
                         metavar="G", type='string', dest='grid', default="BookGrid",
                         help='Grid to use (case sensitive; options are BookGrid, BridgeGrid, CliffGrid, MazeGrid, default %default)')
    optParser.add_option('-w', '--windowSize', metavar="X", type='int', dest='gridSize', default=150,
                         help='Request a window width of X pixels *per grid cell* (default %default)')
    optParser.add_option('-a', '--agent', action='store', metavar="A",
                         type='string', dest='agent', default="random",
                         help='Agent type (options are \'random\', \'value\' and \'q\', default %default)')
    optParser.add_option('-t', '--text', action='store_true',
                         dest='textDisplay', default=False,
                         help='Use text-only ASCII display')
    optParser.add_option('-p', '--pause', action='store_true',
                         dest='pause', default=False,
                         help='Pause GUI after each time step when running the MDP')
    optParser.add_option('-q', '--quiet', action='store_true',
                         dest='quiet', default=False,
                         help='Skip display of any learning episodes')
    optParser.add_option('-s', '--speed', action='store', metavar="S", type=float,
                         dest='speed', default=1.0,
                         help='Speed of animation, S > 1.0 is faster, 0.0 < S < 1.0 is slower (default %default)')
    optParser.add_option('-m', '--manual', action='store_true',
                         dest='manual', default=False,
                         help='Manually control agent')
    optParser.add_option('-v', '--valueSteps', action='store_true', default=False,
                         help='Display each step of value iteration')

    m_opts, args = optParser.parse_args()

    if m_opts.manual and m_opts.agent != 'q':
        print '## Disabling Agents in Manual Mode (-m) ##'
        m_opts.agent = None

    # MANAGE CONFLICTS
    if m_opts.textDisplay or m_opts.quiet:
        # if m_opts.quiet:
        m_opts.pause = False
        # m_opts.manual = False

    if m_opts.manual:
        m_opts.pause = True

    return m_opts


def getActionGreedilyFromQValues(m_environment, state, qValues):
    """ select action greedily according to the q-Values with tie breaking """
    possible_actions = m_environment.getPossibleActions(state)
    n_actions = len(possible_actions)
    action_qValues = [qValues[(state, possible_actions[j])] for j in range(0, n_actions)]
    # select action greedily with tie breaking
    action_index = np.random.choice(np.flatnonzero(action_qValues == np.max(action_qValues)))
    return possible_actions[action_index]


def getSelectedActions(m_environment, state, qValues):
    """ select action greedily according to the q-Values with no tie breaking """
    possible_actions = np.array(m_environment.getPossibleActions(state))
    n_actions = len(possible_actions)
    # round float to 4 decimal place
    action_qValues = [round(qValues[(state, possible_actions[j])], 4) for j in range(0, n_actions)]
    # select action greedily with tie breaking
    action_indices = np.flatnonzero(action_qValues == np.max(action_qValues))
    return possible_actions[action_indices]


def getPolicyAgreementRatio(m_environment, optimal_qValues, current_qValues, is_print_info):
    states = m_environment.getGridWorld().getNonTerminalStates()
    n_states = len(states)
    n_converged_states = 0

    # iterate through all the non-terminal state
    for state in states:
        optimal_actions = getSelectedActions(m_environment, state, optimal_qValues)
        current_actions = getSelectedActions(m_environment, state, current_qValues)
        is_optimal = True
        # treat current_actions as optimal if it's a subset of optimal_actions
        for current_action in current_actions:
            if current_action not in optimal_actions:
                if is_print_info:
                    print('Action \'' + current_action + '\' at state ' + str(state) + ' is not optimal')
                is_optimal = False
                break

        if is_optimal:
            if is_print_info:
                print('Policy at state ' + str(state) + ' is optimal')
            n_converged_states += 1

    return float(n_converged_states)/float(n_states)


def runEpisode(agent, m_environment, discount, f_decision
               , f_display, f_message, f_pause, i_episode
               , user_input_module=None, global_step=0
               , check_value_converge=False
               , old_qValues=None
               , check_policy_converge=False
               , policy_converge_ratio_logs=None
               , optimal_policy=None
               , delta=0.02):
    is_converge = False
    episode_rewards = 0
    episode_step = 0
    previous_state = None
    totalDiscount = 1.0
    m_environment.reset()

    if 'startEpisode' in dir(agent):
        agent.startEpisode()
    f_message("BEGINNING EPISODE: " + str(i_episode) + "\n")

    while True:
        # DISPLAY CURRENT STATE
        state = m_environment.getCurrentState()
        f_display(state, previous_state)
        f_pause()

        # get human feedback
        if episode_step != 0 and user_input_module is not None:
            human_signal = user_input_module.getInput()
            if human_signal is not None and human_signal == 'a':
                f_message("Receive Positive (+1) human signal\n")
                agent.receiveHumanSignal(human_signal=1)
            elif human_signal is not None and human_signal == 's':
                f_message("Receive Negative (-1) human signal\n")
                agent.receiveHumanSignal(human_signal=-1)

        # calculate policy convergence ratio
        policy_convergence_ratio = 0
        if optimal_policy is not None and policy_converge_ratio_logs is not None:
                policy_convergence_ratio = getPolicyAgreementRatio(m_environment
                                                                   , optimal_qValues=optimal_policy
                                                                   , current_qValues=agent.getQValues()
                                                                   , is_print_info=False)
                policy_converge_ratio_logs[global_step] = policy_convergence_ratio
                print("Current Policy Convergence Ratio: %f" % policy_convergence_ratio)

        # END IF IN A TERMINAL STATE
        actions = m_environment.getPossibleActions(state)
        if len(actions) == 0:
            f_message("--------------------------------")
            f_message("EPISODE " + str(i_episode) + " COMPLETE: RETURN WAS " + str(episode_rewards) + "\n")
            f_message("TOTAL STEPS: " + str(global_step) + ", EPISODE STEPS: " + str(episode_step))
            f_message("Learned QValue: " + str(agent.getQValues()) + "\n")
            f_message("--------------------------------\n")

            # calculate final policy convergence ratio
            if optimal_policy is not None:
                policy_convergence_ratio = getPolicyAgreementRatio(m_environment
                                                                   , optimal_qValues=optimal_policy
                                                                   , current_qValues=agent.getQValues()
                                                                   , is_print_info=True)
                f_message("################################")
                f_message("Current Policy Convergence Ratio: %f" % policy_convergence_ratio)
                f_message("################################\n")

            # Check if the policy has converged
            if check_policy_converge and optimal_policy is not None:
                # if the convergence ratio is 100%, means the policy has converged to the optimal policy
                if policy_convergence_ratio == 1.0:
                    is_converge = True
                    f_message("##################################")
                    f_message("The policy has converged\n")
                    f_message("TOTAL STEPS: " + str(global_step) + ", EPISODE STEPS: " + str(episode_step))
                    f_message("##################################")
                    f_message("Learned QValue: " + str(agent.getQValues()) + "\n")
                    f_message("##################################")

            return (episode_rewards, global_step, is_converge)

        # GET ACTION (USUALLY FROM AGENT)
        action = f_decision(state)
        if action is None:
            raise Exception('Error: Agent returned None action')

        # EXECUTE ACTION
        nextState, reward = m_environment.doAction(action)
        f_message("Step: " + str(episode_step) +
                  ", S: " + str(state) +
                  ", A: " + str(action) +
                  ", S': " + str(nextState) +
                  ", R: " + str(reward) + "\n")
        previous_state = state

        # UPDATE LEARNER
        if 'observeTransition' in dir(agent):
            agent.observeTransition(state, action, nextState, reward)

        episode_rewards += reward * totalDiscount
        totalDiscount *= discount
        episode_step += 1
        global_step += 1

    # noinspection PyUnreachableCode
    if 'stopEpisode' in dir(agent):
        agent.stopEpisode()


class TamerGridWorldExperiment():
    # noinspection PyUnresolvedReferences
    def __init__(self, grid_name='DiscountGrid', discount=0.9, learning_rate=0.5, living_reward=0.0
                 , noise=0, epsilon=0.3, display_speed=0.5
                 , grid_size=150, text_only=False, n_episodes=100
                 , agent_window_size=1, agent_max_n_experiences=1000
                 , check_value_converge=False
                 , check_policy_converge=False
                 , optimal_policy=None
                 , expr_log_dir=None
                 , delta=0.02
                 , is_use_q_agent=False
                 , init_temp=1024.0
                 , temp_decrease_rate=2.0
                 , is_asyn_input=True):

        ###########################
        # GENERAL CONTROL
        ###########################

        self.text_only = text_only
        self.display_speed = display_speed
        self.n_episodes = n_episodes
        self.discount = discount
        self.check_value_converge = check_value_converge
        self.check_policy_converge = check_policy_converge
        self.optimal_policy = optimal_policy
        self.expr_log_dir = expr_log_dir
        self.delta = delta

        ###########################
        # GET THE INPUT MODULE
        ###########################

        if is_use_q_agent:
            self.user_input_module = None
        else:
            self.user_input_module = user_input.UserInputModule(is_asyn=is_asyn_input)

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
        self.gridWorldEnv = GridworldEnvironment(self.mdp)
        action_function = lambda state: self.mdp.getPossibleActions(state)
        q_learn_opts = {
            'gamma': discount,
            'alpha': learning_rate,
            'epsilon': epsilon,
            'actionFn': action_function,
            'init_temp': init_temp,
            'temp_decrease_rate': temp_decrease_rate
        }

        if is_use_q_agent:
            self.agent = qlearningAgents.QLearningAgent(**q_learn_opts)
        else:
            self.agent = qlearningAgents.TamerQAgent(max_n_experiences=agent_max_n_experiences
                                                     , window_size=agent_window_size
                                                     , is_asyn_input=is_asyn_input
                                                     , **q_learn_opts)

    def run_episodes(self):
        ###########################
        # RUN EPISODES
        ###########################
        display_callback = lambda x: None
        if not self.text_only:
            display_callback = lambda state, previous_state: self.display.displayQValues(self.agent, state
                                                                                         , "CURRENT Q-VALUES"
                                                                                         , previousState=previous_state)

        message_callback = lambda x: printString(x)
        if self.text_only:
            message_callback = lambda x: None

        # FIGURE OUT WHETHER TO WAIT FOR A KEY PRESS AFTER EACH TIME STEP
        pause_callback = lambda: None

        # FIGURE OUT WHETHER THE USER WANTS MANUAL CONTROL (FOR DEBUGGING AND DEMOS)
        decision_callback = self.agent.getAction

        # RUN EPISODES
        if self.n_episodes > 0:
            print
            print "RUNNING", self.n_episodes, "EPISODES"
            print
        total_returns = 0
        total_episodes = 0
        total_steps = 0
        policy_converge_ratios = dict()

        for i_episode in range(1, self.n_episodes + 1):
            (episode_rewards, global_step, is_converge) = runEpisode(self.agent, self.env, self.discount
                                                                     , decision_callback, display_callback
                                                                     , message_callback, pause_callback, i_episode
                                                                     , user_input_module=self.user_input_module
                                                                     , global_step=total_steps
                                                                     , check_value_converge=self.check_value_converge
                                                                     , check_policy_converge=self.check_policy_converge
                                                                     , delta=self.delta
                                                                     , policy_converge_ratio_logs=policy_converge_ratios
                                                                     , optimal_policy=self.optimal_policy)
            total_returns += episode_rewards
            total_episodes += 1
            total_steps = global_step

            # terminate the experiment if the qValues have converged
            if is_converge:
                break

        if self.n_episodes > 0:
            print
            print "AVERAGE RETURNS FROM START STATE: " + str((total_returns + 0.0) / total_episodes)
            print
            print

        # save policy convergence ratio logs to file
        if self.expr_log_dir is not None:
            converge_log_file = self.expr_log_dir + '/' + 'policy_convergence_ratio.json'
            qValueSaver.saveDictToFile(converge_log_file, policy_converge_ratios)
        # plot policy convergence ratio
        # plotRatios(policy_converge_ratios)

        # DISPLAY POST-LEARNING VALUES / Q-VALUES
        try:
            self.display.displayQValues(self.agent, message="Q-VALUES AFTER "+str(total_episodes)+" EPISODES")
            raw_input('Press Enter to continue')
        except KeyboardInterrupt:
            sys.exit(0)


def plotRatios(ratio_dict):
    indices = ratio_dict.keys()
    min_index = np.min(indices)
    max_index = np.max(indices)
    ratio_list = list()
    for i in range(min_index, max_index+1):
        if i in ratio_dict:
            ratio_list.append(ratio_dict[i])
        else:
            ratio_list.append(0)
    # plot the ratio list
    plt.plot(ratio_list)
    plt.xlabel('steps')
    plt.ylabel('policy convergence ratios')
    plt.show()


if __name__ == '__main__':
    pass

