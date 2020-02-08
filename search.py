# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    from util import Stack
    ####   variables
    startState = problem.getStartState()
    goal = None
    stack = Stack() #basically keeps track of our depth first search
    parentDict = {} #our dictionary adds successor states as keys, each mapping to their parent states
    actions = [] #RETURN THIS
    currentState = None #this will be set to goal, and then updated by a loop until it becomes start. so when
                        #   currentState = (startState, None, None) then we have successfully reached start from
                        #   goal and we are almost done

    explored = set() #the 'explored' set variable prevents infinite loop by preventing us from appending (to stack) successor
                     #   states of a state whose successor states are already in stack. in other words, prevents us from
                     #   re-exploring previously explored branches
    explored.add(startState)

    #this loop is executed once. our dictionary adds each successor of startState as a key mapping to startState
    for successor in problem.getSuccessors(startState):
        parentDict[successor] = (startState, None, None)
        stack.push(successor)

    #this while loop and its contained for loop allow us to move through with our depth first search
    while not stack.isEmpty():
        popped = stack.pop()
        if popped[0] in explored:
            continue #exits the current iteration
        if problem.isGoalState(popped[0]):
            goal = popped
            break #exits entire while loop
        explored.add(popped[0])
        for successor in problem.getSuccessors(popped[0]): #similar to the above for loop
            parentDict[successor] = popped
            stack.push(successor)
    currentState = goal
    #print("goal: ")
    #print(goal)

    #from all the above code we've been able to assemble a dictionary mapping successor states as keys to their
    #   parent states. now our currentState variable will use a while loop to move through this dictionary from
    #   goal to start and append the direction values to our 'actions' list. the reverse of this list is our answer
    while currentState != (startState, None, None):
        actions.append(currentState[1])
        currentState = parentDict[currentState]
    actions.reverse()
    return actions


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #the first attempt didn't work for problem 5
    """
    from util import Queue
    ####   variables
    startState = problem.getStartState()
    goal = None
    q = Queue()
    parentDict = {}
    actions = []
    currentState = None
    explored = set()
    explored.add(startState)

    #this loop is executed once. our dictionary adds each successor of startState as a key mapping to startState
    for successor in problem.getSuccessors(startState):
        parentDict[successor] = (startState, None, None)
        q.push(successor)

    #this while loop and its contained for loop allow us to move through with our depth first search
    while not q.isEmpty():
        popped = q.pop()
        if popped[0] in explored:
            continue #exits the current iteration
        if problem.isGoalState(popped[0]):
            goal = popped
            break #exits entire while loop
        explored.add(popped[0])
        for successor in problem.getSuccessors(popped[0]): #similar to the above for loop
            parentDict[successor] = popped
            q.push(successor)
    currentState = goal

    #from all the above code we've been able to assemble a dictionary mapping successor states as keys to their
    #   parent states. now our currentState variable will use a while loop to move through this dictionary from
    #   goal to start and append the direction values to our 'actions' list. the reverse of this list is our answer
    while currentState != (startState, None, None):
        actions.append(currentState[1])
        currentState = parentDict[currentState]
    actions.reverse()
    return actions
    """
    #cleaned up version that works with problem 5
    from util import Queue
    q = Queue()
    explored = set()
    q.push((problem.getStartState(), [], 0))
    while not q.isEmpty():
        popped = q.pop()
        if popped[0] in explored:
            continue
        explored.add(popped[0])
        if problem.isGoalState(popped[0]):
            return popped[1]
        for successor in problem.getSuccessors(popped[0]):
            if successor[0] not in explored:
                #push successor, where actions and cost are cumulative on its parent (popped)
                q.push((successor[0], popped[1] + [successor[1]], popped[2] + successor[2]))
    return popped[1]


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    ####   variables
    pq = PriorityQueue() #basically keeps track of our uniform cost search
    startState = problem.getStartState()
    explored = [] #this list will stop us from revisiting states unnecessarily. But it will let us revisit
                  ##a state if we have found a way to get there in lower cost

    pq.push([startState, [], 0], 0)
    current = pq.pop()
    while not problem.isGoalState(current[0]):
        exploreThis = True
        totalCost = problem.getCostOfActions(current[1])
        for e in explored:
            if current[0] == e[0] and totalCost >= e[1]:
                #if current's state has already been explored and the cost is not being lowered:
                exploreThis = False
        if exploreThis:
            explored.append([current[0], totalCost])
            for successor in problem.getSuccessors(current[0]):
                (state, action, cost) = successor
                pq.push([state, current[1] + [action], problem.getCostOfActions(current[1] + [action])],
                    problem.getCostOfActions(current[1] + [action]))
        current = pq.pop()
    return current[1]


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    ####   variables
    pq = PriorityQueue() #basically keeps track of our uniform cost search
    startState = problem.getStartState()
    explored = [] #this list will stop us from revisiting states unnecessarily. But it will let us revisit
                  ##a state if we have found a way to get there in lower cost

    pq.push([startState, [], 0], 0)
    current = pq.pop()
    while not problem.isGoalState(current[0]):
        exploreThis = True
        totalCost = problem.getCostOfActions(current[1]) + heuristic(current[0], problem)
        for e in explored:
            if current[0] == e[0] and totalCost >= e[1]:
                #if current's state has already been explored and the cost is not being lowered:
                exploreThis = False
        if exploreThis:
            explored.append([current[0], totalCost])
            for successor in problem.getSuccessors(current[0]):
                (state, action, cost) = successor
                ucsDistance = problem.getCostOfActions(current[1] + [action])
                heur = heuristic(state, problem)
                pq.push([state, current[1] + [action], ucsDistance + heur], ucsDistance + heur)
        current = pq.pop()
    return current[1]


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
