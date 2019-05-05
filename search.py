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


def nodeselection(problem, fringe):

    visited = []

    # initialisation of the Tree-search function, insertion of the initial state node (pacman's position)
    # + the action to be done (empty list)
    
    fringe.push( (problem.getStartState(), []) )

    while not fringe.isEmpty():
        # We remove the last element placed in the fringe, which is the last node we've expanded
        node , actions = fringe.pop() 
        
        # node : (x,y)
        # actions : list of every actions taken from the beggining
        # visited : list of every visited nodes
    
        if (not node in visited):
            visited.append(node)
            # If the node we just removed from the fringe is the Goal State, end of the problem, we return the path  
            if problem.isGoalState(node):
                return actions

            # Else we have to replace the last visited node by its children, and expand the new deepest node
            # child is all the legal next positions, nextaction are the actions required to get there and steps are the cost
            for child, nextaction, cost in problem.getSuccessors(node):
                # We place in the fringe the node that we expand: the child node of the node that we previously have expanded        
                newaction = actions + [nextaction]
                visited = visited + [node]
                
                fringe.push((child, newaction ))
    return []



def depthFirstSearch(problem):
    """
    To test, try any of the following commands:
    python pacman.py -l tinyMaze -p SearchAgent
    python pacman.py -l mediumMaze -p SearchAgent --frameTime 0
    python pacman.py -l bigMaze -z .5 -p SearchAgent --frameTime 0
    """
    # implementation of a LIFO stack
    fringe = util.Stack()
    result = nodeselection(problem,fringe)  
    return result


def breadthFirstSearch(problem):

    """
    python pacman.py -l bigMaze -p SearchAgent -a fn=bfs -z .5
    """

    fringe = util.Queue()
    result = nodeselection(problem,fringe)
    return result



def uniformCostSearch(problem):
    """Search the node of least total cost first.
    python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs --frameTime 0
    python pacman.py -l mediumDottedMaze -p StayEastSearchAgent --frameTime 0
    python pacman.py -l mediumScaryMaze -p StayWestSearchAgent --frameTime 0
    """

    fringe = util.PriorityQueue()
    # dernier élément : priorité, on mettra le coût en tant que priorité car on
    # étant toujours la node avec la plus petite priorité, donc le plus petit coût

    fringe.push( (problem.getStartState(), [], 0), 0 ) 
    expanded = []

    while not fringe.isEmpty():
        node, actions, curCost = fringe.pop()

        if(not node in expanded):
            expanded.append(node)

            if problem.isGoalState(node):
                return actions

            for child, direction, cost in problem.getSuccessors(node):
                fringe.push((child, actions+[direction], curCost + cost), curCost + cost)

    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0
"""
def uniformP(problem):
    
    heuristic = 0
    result = heuristicSearch(problem, heuristic)

    return result

def AstarP(problem):

    heuristic = nullHeuristic
    result = heuristicSearch(problem, heuristic)

    return result
"""
    
"""
def heuristicSearch(problem, heuristic):

    #python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
    fringe = util.PriorityQueue()
    try: 
        h = heuristic(problem.getStartState(), problem)
    except:
        h = 0

    fringe.push( (problem.getStartState(), [], 0), h )
    expanded = []

    while not fringe.isEmpty():
        node, actions, curCost = fringe.pop()

        if(not node in expanded):
            expanded.append(node)

            if problem.isGoalState(node):
                return actions

            for child, direction, cost in problem.getSuccessors(node):
                g = curCost + cost
                try:
                    h = heuristic(child,problem)
                except:
                    h=0
                fringe.push((child, actions+[direction], curCost + cost), g + h)

    return []

"""

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first.
    python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
    """

    fringe = util.PriorityQueue()
    fringe.push( (problem.getStartState(), [], 0), heuristic(problem.getStartState(), problem) )
    expanded = []

    while not fringe.isEmpty():
        node, actions, curCost = fringe.pop()

        if(not node in expanded):
            expanded.append(node)

            if problem.isGoalState(node):
                return actions

            for child, direction, cost in problem.getSuccessors(node):
                g = curCost + cost
                fringe.push((child, actions+[direction], curCost + cost), g + heuristic(child, problem))

    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
