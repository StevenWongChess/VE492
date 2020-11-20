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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

        WeightFood = 2.0
        WeightGhost = 1.0
        value = successorGameState.getScore()

        distanceToGhost = manhattanDistance(newPos, newGhostStates[0].getPosition())
        if distanceToGhost > 0:
            value -= WeightGhost / distanceToGhost
        distancesToFood = list()
        for x in newFood.asList():
            distancesToFood.append(manhattanDistance(newPos, x))
        if len(distancesToFood):
            value += WeightFood / min(distancesToFood)
        return value       
        # since the consideration of food and ghost is enough for 1000 pts,
        # we do not need to take advantage of the scaretime anymore

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def helper(state, depth, agent):
            NumAgents = state.getNumAgents()
            if agent == NumAgents: # pacman            
                if depth == self.depth:
                    return self.evaluationFunction(state)
                else:
                    return helper(state, depth + 1, 0)
            else:
                actions = state.getLegalActions(agent)
                if len(actions) == 0:
                    return self.evaluationFunction(state)
                successor = list()
                for action in actions:
                    successor.append(helper(state.generateSuccessor(agent, action),
                    depth, agent + 1))
                if agent == 0:
                    return max(successor)                    
                else:
                    return min(successor)                    
        return max(gameState.getLegalActions(0),
            key = lambda x: helper(gameState.generateSuccessor(0, x), 1, 1))

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        answer = self.value(gameState, 0, float("-inf"), float("inf"))
        return answer[0]

    def value(self, gameState, depth, alpha, beta):
        if depth == self.depth * gameState.getNumAgents() or gameState.isWin() or gameState.isLose():
            return (None, self.evaluationFunction(gameState))
        if depth % gameState.getNumAgents() == 0:
            return self.maxValue(gameState, depth, alpha, beta)
        else:
            return self.minValue(gameState, depth, alpha, beta)

    def minValue(self, gameState, depth, alpha, beta):
        actions = gameState.getLegalActions(depth % gameState.getNumAgents())
        v = (None, float("inf"))
        for action in actions:
            succ = gameState.generateSuccessor(depth % gameState.getNumAgents(), action)
            child = self.value(succ, depth+1, alpha, beta)
            if child[1] < v[1]:
                v = (action, child[1])
            if v[1] < alpha:
                return v
            beta = min(beta, v[1])
        return v

    def maxValue(self, gameState, depth, alpha, beta):
        actions = gameState.getLegalActions(0)
        v = (None, float("-inf"))
        for action in actions:
            successor = gameState.generateSuccessor(0, action)
            child = self.value(successor, depth+1, alpha, beta)
            if child[1] > v[1]:
                v = (action, child[1])
            if v[1] > beta:
                return v
            alpha = max(alpha, v[1])
        return v

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
        answer = self.value(gameState, 0)
        return answer[0]

    def value(self, gameState, depth):
        if depth == self.depth * gameState.getNumAgents() or gameState.isWin() or gameState.isLose():
            return (None, self.evaluationFunction(gameState))
        if depth % gameState.getNumAgents() == 0:
            return self.maxValue(gameState, depth)
        else:
            return self.expValue(gameState, depth)

    def expValue(self, gameState, depth):
        actions = gameState.getLegalActions(depth % gameState.getNumAgents())
        v = 0
        for action in actions:
            succ = gameState.generateSuccessor(depth % gameState.getNumAgents(), action)
            child = self.value(succ, depth+1)
            v += child[1] * 1./len(actions)
        return (None, v)

    def maxValue(self, gameState, depth):
        actions = gameState.getLegalActions(0)
        v = (None, float("-inf"))
        for action in actions:
            succ = gameState.generateSuccessor(0, action)
            child = self.value(succ, depth+1)
            if child[1] > v[1]:
                v = (action, child[1])
        return v

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    position = currentGameState.getPacmanPosition()
    foodList = currentGameState.getFood().asList()
    value = currentGameState.getScore()
    GhostStates = currentGameState.getGhostStates()
    ScaredTimes = list()
    for ghostState in GhostStates:
        ScaredTimes.append(ghostState.scaredTimer)
    
    Wfood = 1
    Wbadghost = -1
    Wgoodghost = 8

    for ghost in GhostStates:
        distance = manhattanDistance(position, GhostStates[0].getPosition())
        if distance > 0:
            if ghost.scaredTimer > 0:  # if ghost is scared -> go for him
                value += Wgoodghost / distance
            else: 
                value += Wbadghost / distance

    minFood = float("inf")
    if len(foodList):
        for food in foodList:
            minFood = min(manhattanDistance(position, food), minFood)
        value += Wfood / minFood

    return value

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
