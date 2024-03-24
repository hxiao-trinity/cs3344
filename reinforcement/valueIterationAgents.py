# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        values = util.Counter()
        for state in states:
            values[(state, 0)] = 0
        for k in range(1, self.iterations + 1):
            for state in states:
                actions = self.mdp.getPossibleActions(state)
                maxVal = float('-infinity')
                for action in actions:
                    value = 0
                    nextStateInfos = self.mdp.getTransitionStatesAndProbs(state, action)
                    for nextStateInfo in nextStateInfos:
                        nextState = nextStateInfo[0]
                        prob = nextStateInfo[1]
                        reward = self.mdp.getReward(state, action, nextState)
                        v = values[(nextState, k-1)]
                        value += prob * (reward + self.discount * v)
                    maxVal = max(maxVal, value)
                if maxVal > float('-infinity'):
                    values[(state, k)] = maxVal
                else:
                    values[(state, k)] = 0
        for state in states:
            self.values[state] = values[(state, self.iterations)]


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        q = 0
        for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
            reward = self.mdp.getReward(state, action, nextState)
            v = self.values[nextState]
            q += prob * (reward + self.discount * v)
        return q

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        actions = self.mdp.getPossibleActions(state)
        bestQ = float('-inf')
        bestAction = None
        for action in actions:
            if self.getQValue(state,action) > bestQ:
                bestQ = self.getQValue(state,action)
                bestAction = action
        return bestAction
        

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        this_iteration_values = self.values.copy()

        num_state = len(self.mdp.getStates())

        for i in range(self.iterations):

            state = self.mdp.getStates()[i % num_state]

            maxQ = -sys.maxsize - 1

            if not self.mdp.isTerminal(state):
                for action in self.mdp.getPossibleActions(state):
                    qsum = 0
                    for nextstate, prob in self.mdp.getTransitionStatesAndProbs(state, action):    
                        nextstateV = self.values[nextstate]
                        qsum += prob * (self.mdp.getReward(state, action, nextstate) + (self.discount * nextstateV))
                    if qsum > maxQ:
                        maxQ = qsum
                this_iteration_values[state] = maxQ 

            if (i % num_state) == num_state - 1:
                for state, v in this_iteration_values.items():
                    self.values[state] = v

        
        for state, v in this_iteration_values.items():
            self.values[state] = v

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        predecessors = {}
        for state in states:
            predecessors[state] = set()
        for state in states:
            for action in self.mdp.getPossibleActions(state):
                nextStateInfos = self.mdp.getTransitionStatesAndProbs(state, action)
                for (nextState, _) in nextStateInfos:
                    predecessors[nextState].add(state)

        prioQ = util.PriorityQueue()

        for s in states:
            if self.mdp.isTerminal(s):
                continue
            bestAction = self.computeActionFromValues(s)
            highestQValue = self.computeQValueFromValues(s, bestAction)
            diff = abs(highestQValue - self.values[s])
            prioQ.push(s, -diff)

        for _ in range(self.iterations):
            if prioQ.isEmpty():
                return
            s = prioQ.pop()

            if not self.mdp.isTerminal(s):
                actions = self.mdp.getPossibleActions(s)
                maxVal = float('-infinity')
                for action in actions:
                    value = 0
                    nextStateInfos = self.mdp.getTransitionStatesAndProbs(s, action)
                    for (nextState, prob) in nextStateInfos:
                        reward = self.mdp.getReward(s, action, nextState)
                        v = self.values[nextState]
                        value += prob * (reward + self.discount * v)
                    maxVal = max(maxVal, value)
                if maxVal > float('-infinity'):
                    self.values[s] = maxVal
                else:
                    self.values[s] = 0

            for p in predecessors[s]:
                bestAction = self.computeActionFromValues(p)
                if bestAction == None:
                    continue
                maxQ = self.computeQValueFromValues(p, bestAction)
                diff = abs(maxQ - self.values[p])

                if diff > self.theta:
                    prioQ.update(p, -diff)

