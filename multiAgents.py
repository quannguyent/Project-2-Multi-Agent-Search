# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        foodList = newFood.asList()
        nearestFoodDistance = 1234
        nearestGhostDistance = 1234

        # Find nearest Ghost distance
        for ghosts in newGhostStates:
            if ghosts.scaredTimer == 0:
                nearestGhostDistance = min(nearestGhostDistance, manhattanDistance(ghosts.getPosition(), newPos))

        # Find nearest Food distance
        for food in foodList:
            nearestFoodDistance = min(nearestFoodDistance, manhattanDistance(newPos, food))
        if not foodList:
            nearestFoodDistance = 0

        return successorGameState.getScore() + 5.0 / (nearestFoodDistance + 1) - 15.0 / (nearestGhostDistance + 1)

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        def minimax(agentIndex, depth, gameState):

            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)

            # Calculate max value for Pacman
            if agentIndex == 0:
                nextAgent = agentIndex + 1

                actions = gameState.getLegalActions(agentIndex)
                maxValue = max(
                    minimax(nextAgent, depth, gameState.generateSuccessor(agentIndex, action)) for action in actions)

                return maxValue

            # Calculate min value for Ghost
            else:
                nextAgent = agentIndex + 1
                if gameState.getNumAgents() == nextAgent:
                    nextAgent = 0
                if nextAgent == 0:
                    depth += 1

                actions = gameState.getLegalActions(agentIndex)
                minValue = min(
                    minimax(nextAgent, depth, gameState.generateSuccessor(agentIndex, action)) for action in actions)

                return minValue

        maxScore = float("-inf")
        bestAction = Directions.STOP
        for action in gameState.getLegalActions(0):
            score = minimax(1, 0, gameState.generateSuccessor(0, action))
            if score > maxScore:
                maxScore = score
                bestAction = action

        return bestAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        # Pacman
        def maxValue(agentIndex, depth, gameState, a, b):
            nextAgent = agentIndex + 1

            v = float("-inf")
            for action in gameState.getLegalActions(agentIndex):
                v = max(v, alphabeta(nextAgent, depth, gameState.generateSuccessor(agentIndex, action), a, b))
                if v > b:
                    return v
                a = max(a, v)
            return v

        # Ghost
        def minValue(agentIndex, depth, gameState, a, b):
            nextAgent = agentIndex + 1
            if gameState.getNumAgents() == nextAgent:
                nextAgent = 0
            if nextAgent == 0:
                depth += 1

            v = float("inf")
            for action in gameState.getLegalActions(agentIndex):
                v = min(v, alphabeta(nextAgent, depth, gameState.generateSuccessor(agentIndex, action), a, b))
                if v < a:
                    return v
                b = min(b, v)
            return v

        def alphabeta(agentIndex, depth, gameState, a, b):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)

            if agentIndex == 0:
                return maxValue(agentIndex, depth, gameState, a, b)
            else:
                return minValue(agentIndex, depth, gameState, a, b)

        maxScore = float("-inf")
        bestAction = Directions.STOP
        alpha = float("-inf")
        beta = float("inf")

        for action in gameState.getLegalActions(0):
            score = alphabeta(1, 0, gameState.generateSuccessor(0, action), alpha, beta)
            if score > maxScore:
                maxScore = score
                bestAction = action

            alpha = max(alpha, maxScore)

        return bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        def expectimax(agentIndex, depth, gameState):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)

            if agentIndex == 0:
                nextAgent = agentIndex + 1
                score = float("-inf")
                for action in gameState.getLegalActions(agentIndex):
                    score = max(score, expectimax(nextAgent, depth, gameState.generateSuccessor(agentIndex, action)))
                return score

            else:
                nextAgent = agentIndex + 1
                if gameState.getNumAgents() == nextAgent:
                    nextAgent = 0
                if nextAgent == 0:
                    depth += 1
                score = 0.0
                for action in gameState.getLegalActions(agentIndex):
                    score += expectimax(nextAgent, depth, gameState.generateSuccessor(agentIndex, action))
                score /= len(gameState.getLegalActions(agentIndex))
                return score

        maxScore = float("-inf")
        bestAction = Directions.STOP
        for action in gameState.getLegalActions(0):
            score = expectimax(1, 0, gameState.generateSuccessor(0, action))
            if score > maxScore or maxScore == float("-inf"):
                maxScore = score
                bestAction = action

        return bestAction

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()

    foodList = newFood.asList()
    nearestFoodDistance = 1000
    nearestGhostDistance = 1000

    for ghosh in newGhostStates:
      if ghosh.scaredTimer == 0:
        nearestGhostDistance = min(nearestGhostDistance, manhattanDistance(ghosh.getPosition(), newPos))

    for food in foodList:
      nearestFoodDistance = min(nearestFoodDistance, manhattanDistance(newPos, food))
    if not foodList:
      nearestFoodDistance = 0

    return currentGameState.getScore() + 5.0 / (nearestFoodDistance + 1) - 15.0 / (nearestGhostDistance + 1)

# Abbreviation
better = betterEvaluationFunction

