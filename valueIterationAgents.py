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

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        # calculating Vk+1
        # in range of V iterations
        for i in range(self.iterations):
            # for each state in grid
            valCopy = self.values.copy()
            
            for s in self.mdp.getStates():
                #stateVal = self.values[s]
                # for each legal action from current state

                #if not terminal state
                if self.mdp.isTerminal(s) == False:
                    #keep track of highest VK1 value 
                    maxVK1 = float ("-inf")
                    #for a in self.mdp.getLegalActions(s):
                    
                    for a in self.mdp.getPossibleActions(s):
                        vk1 = 0
                        for t in mdp.getTransitionStatesAndProbs(s,a):
                            vk1 += t[1]*(self.mdp.getReward(s,a,t[0])+self.discount*self.values[t[0]])
                            #if(self.values[t[1]] <= vk1):
                                #self.values[t[1]] = vk1

                        #update maxVK1  
                        if vk1 > maxVK1:
                            maxVK1 = vk1 

                        valCopy[s] = maxVK1      
                #is a terminal state 
                else:           
                    #for a in self.mdp.getLegalActions(s):
                    
                    for a in self.mdp.getPossibleActions(s):
                        vk1 = 0
                        for t in mdp.getTransitionStatesAndProbs(s,a):
                            vk1 += t[1]*(self.mdp.getReward(s,a,t[0])+self.discount*self.values[t[0]]) 

                        valCopy[s] = vk1                

            self.values = valCopy               
                           
                           
                            


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
        sum = 0
        for t in self.mdp.getTransitionStatesAndProbs(state, action):
            sum += t[1] * (self.mdp.getReward(state, action, t[0]) + self.discount * self.values[t[0]])

        return sum    
        
        #util.raiseNotDefined()

    #def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        actionsToCheck = self.mdp.getPossibleActions(state)
        if self.mdp.isTerminal(state) == False:
            besta = actionsToCheck[0]
            bestq = self.getQValue(state, besta)
            for a in actionsToCheck:
                if self.getQValue(state, a) > bestq:
                    bestq = self.getQValue(state, a)
                    besta = a
            return besta

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
