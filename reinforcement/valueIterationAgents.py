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
        #stores info about best action leading to a state
        self.actionAtState = {state: None for state in self.mdp.getStates()}
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        for i in range(self.iterations):
            buffer = util.Counter()
            for currState in self.mdp.getStates():
                maxQValue = float('-inf')
                possible_actions = self.mdp.getPossibleActions(currState)
                for action in possible_actions:
                    # maxQValue = max(maxQValue, self.getQValue(currState, action))
                    # buffer[currState] = maxQValue
                    # self.actionAtState[currState] = action 
                    newQvalue = self.getQValue(currState, action)
                    if maxQValue <  newQvalue:
                        maxQValue = newQvalue
                        buffer[currState] = maxQValue
                        self.actionAtState[currState] = action 
            self.values = buffer
            #update state
                
                
            



    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        #self.values : state -> valeu
        return self.values[state]

    
    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        """
        Q(s, a) = Sum (Transition(s, a, s') [Reward(s, a, s') + discount*V*])
        """
        "*** YOUR CODE HERE ***"
            # mdp.getStates()
            
            #   mdp.getPossibleActions(state)
            #   mdp.getTransitionStatesAndProbs(state, action)
            #   mdp.getReward(state, action, nextState)
            #   mdp.isTerminal(state)
        #getTransitionStatesAndProbs : (nextState, prob) pairs reachable from action
        
        #map a state t        if mdp.isTerminalState(state):
        total = 0
        if self.mdp.isTerminal(state):
            print("TERMINAL OEFNJWOFIGJWOGIJ")
            return total
        for item in self.mdp.getTransitionStatesAndProbs(state, action):
            nextState, probability = item[0], item[1]
            total += probability * (self.mdp.getReward(state, action,nextState) + self.discount*self.getValue(nextState))
        return total
        #sum over all transition
        # nextState, probability = mdp.getTransitionStatesAndProbs[0]
        # qValue = probability*(mdp.getReward(state, action,nextState)+ self.discount*mdp.getValue(nextState))
        #max over q values -> v k + 1

    
    
    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        # if mdp.isTerminalState(state):
        #     return None
        # nextStates = mdp.getPossibleActions(state)
        # return .getValue(state)
        #keeps track of most recent value
        # startActions = self.mdp.getPossibleActions(state)
        # best_action = None
        # qValue = -1000
        # for action in startActions:
        #     currQValue = self.computeQValueFromValues(state, action)
        #     if (qValue < currQValue):
        #         qValue = currQValue
        #         best_action = action
        # # print("computeaction total", qValue, best_action)
        # return best_action
        
        return self.actionAtState[state]

        


    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)[0]

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)


class PrioritizedSweepingValueIterationAgent(ValueIterationAgent):
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
        # mdp = self.mdp
        # values = self.values
        # discount = self.discount
        # iterations = self.iterations
        # theta = self.theta
        # states = mdp.getStates()
        

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        