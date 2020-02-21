# header files
import numpy as np
import sys

class PuzzleSolver(object):
    """
    This is the class for the 8-puzzle game. The following are the attributes:
    
    Attributes:
        graph: the numpy array for storing the puzzle
        goalGraph: the numpy array denoting the goal state of the puzzle
        leftMove: constant for left move
        upMove: constant for up move
        rightMove: constant for right move
        downMove: constant for down move
    """
    
    # init method for the class
    def __init__(self, graph):
        self.nodesFile = open("Nodes.txt", "w")
        self.nodePathFile = open("nodePath.txt", "w")
        self.nodesInfoFile = open("NodesInfo.txt", "w")
        self.graph = graph
        self.goalGraph = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
        self.leftMove = 1
        self.upMove = 2
        self.rightMove = 3
        self.downMove = 4
        
    # write to a nodes.txt
    def WriteToFile(self, array):
        text = ""
        for col in range(0, array.shape[1]):
            for row in range(0, array.shape[0]):
                text = text + str(array[row][col]) + " "
        text = text + "\n"
        self.nodesFile.write(text)
        
    # write to a nodePath.txt
    def WriteToPathFile(self, array):
        text = ""
        for col in range(0, array.shape[1]):
            for row in range(0, array.shape[0]):
                text = text + str(array[row][col]) + " "
        text = text + "\n"
        self.nodePathFile.write(text)
        
    # get string equivalent of the graph
    def GraphToString(self, array):
        text = str("")
        for col in range(0, array.shape[1]):
            for row in range(0, array.shape[0]):
                text = text + str(array[row][col]) + " "
        return text
        
    # get blank tile location (blank tile denoted by 0)
    def BlankTileLocation(self):
        blankTileRow, blankTileCol = np.where(self.graph == 0)
        if(len(blankTileRow) > 0 and len(blankTileCol) > 0):
            return (blankTileRow[0], blankTileCol[0])
        else:
            return (-1, -1)
    
    # check valid move or not
    def ValidMove(self, blankTileRow, blankTileCol, numRows, numCols):
        if((blankTileRow >= 0 and blankTileRow < numRows) and (blankTileCol >= 0 and blankTileCol < numCols)):
            return True
        else:
            return False
    
    # move blank tile left
    def ActionMoveLeft(self, blankTileRow, blankTileCol):
        newGraph = self.graph.copy()
    
        # move left
        temp = newGraph[blankTileRow][blankTileCol]
        newGraph[blankTileRow][blankTileCol] = newGraph[blankTileRow][blankTileCol - 1]
        newGraph[blankTileRow][blankTileCol - 1] = temp
        return newGraph
    
    # move blank tile right
    def ActionMoveRight(self, blankTileRow, blankTileCol):
        newGraph = self.graph.copy()
    
        # move right 
        temp = newGraph[blankTileRow][blankTileCol]
        newGraph[blankTileRow][blankTileCol] = newGraph[blankTileRow][blankTileCol + 1]
        newGraph[blankTileRow][blankTileCol + 1] = temp
        return newGraph
    
    # move blank tile up
    def ActionMoveUp(self, blankTileRow, blankTileCol):
        newGraph = self.graph.copy()
    
        # move up 
        temp = newGraph[blankTileRow][blankTileCol]
        newGraph[blankTileRow][blankTileCol] = newGraph[blankTileRow - 1][blankTileCol]
        newGraph[blankTileRow - 1][blankTileCol] = temp
        return newGraph
    
    # move blank tile down
    def ActionMoveDown(self, blankTileRow, blankTileCol):
        newGraph = self.graph.copy()
    
        # move down
        temp = newGraph[blankTileRow][blankTileCol]
        newGraph[blankTileRow][blankTileCol] = newGraph[blankTileRow + 1][blankTileCol]
        newGraph[blankTileRow + 1][blankTileCol] = temp
        return newGraph
    
    # check goal state function
    def CheckGoalState(self):
        return ((self.graph == self.goalGraph).all() and (self.graph.shape == self.goalGraph.shape))
    
    # compare graphs
    def CompareGraphs(self, graph1, graph2):
        return ((graph1 == graph2).all() and (graph1.shape == graph2.shape))
    
    # update graph
    def UpdateGraph(self, newGraph):
        self.graph = newGraph
    
    # backtrack to find the path to reach from initial to goal
    def GeneratePath(self, movesArray, numberOfMoves, lastMove):
        answerGraphs = []
        self.UpdateGraph(self.goalGraph)
        answerGraphs.append((self.goalGraph, -1))
        
        if(lastMove == self.leftMove):
            newGraph = self.ActionMoveRight(2, 2)
        elif(lastMove == self.upMove):
            newGraph = self.ActionMoveDown(2, 2)
        elif(lastMove == self.rightMove):
            newGraph = self.ActionMoveLeft(2, 2)
        else:
            newGraph = self.ActionMoveUp(2, 2)
            
        numberOfMoves = numberOfMoves - 1
        while(len(movesArray[numberOfMoves]) > 0):
            for index in range(0, len(movesArray[numberOfMoves])):
                if(self.CompareGraphs(newGraph, movesArray[numberOfMoves][index][0])):
                    answerGraphs.append((newGraph, lastMove))
                    self.UpdateGraph(newGraph)
                    (currBlankTileRow, currBlankTileCol) = self.BlankTileLocation()
                    lastMove = movesArray[numberOfMoves][index][1]
                    
                    # update graph
                    if(lastMove == self.leftMove):
                        newGraph = self.ActionMoveRight(currBlankTileRow, currBlankTileCol)
                    elif(lastMove == self.upMove):
                        newGraph = self.ActionMoveDown(currBlankTileRow, currBlankTileCol)
                    elif(lastMove == self.rightMove):
                        newGraph = self.ActionMoveLeft(currBlankTileRow, currBlankTileCol)
                    else:
                        newGraph = self.ActionMoveUp(currBlankTileRow, currBlankTileCol)
                    numberOfMoves = numberOfMoves - 1
                    break
                    
        # reverse graph paths
        answerGraphs = answerGraphs[::-1]
        return answerGraphs
    
    # solve the puzzle using bfs
    def solve(self):
        queue = []
        queue.append((self.graph, -1, 0, 0))
        visitedGraph = {}
        movesArray = {}
        moves = []
        prevLevel = -1
        lastMove = -1
        flag = -1
        startIndex = 1
    
        while(len(queue) > 0):
            (currGraph, prevMove, currLevel, parentIndex) = queue[0]
            self.UpdateGraph(currGraph)
            stringGraph = self.GraphToString(currGraph)
            queue.pop(0)
            
            # write to nodesInfo.txt and nodes.txt
            text = "" + str(startIndex) + " " + str(parentIndex) + "\n"
            self.nodesInfoFile.write(text)
            self.WriteToFile(currGraph)
            
            # max number of steps
            if(currLevel > 1000):
                lastMove = -1
                break
            
            # update movesArray
            if(prevLevel != currLevel):
                movesArray[prevLevel] = moves
                moves = []
                moves.append((currGraph, prevMove))
                prevLevel = currLevel
            else:
                moves.append((currGraph, prevMove))
                
        
            # check if goal state reached or not
            if(self.CheckGoalState()):
                flag = currLevel
                lastMove = prevMove
                break
                
            # new graph visited
            if(visitedGraph.get(str(stringGraph)) is None):
                #update graph as visited
                visitedGraph[str(stringGraph)] = 1
                
                # find blank tile location
                (currBlankTileRow, currBlankTileCol) = self.BlankTileLocation()
        
                # move left
                if(prevMove != self.rightMove and self.ValidMove(currBlankTileRow, currBlankTileCol - 1, 3, 3)):
                    leftMoveGraph = self.ActionMoveLeft(currBlankTileRow, currBlankTileCol)
                    
                    # check graph visited or not
                    if(visitedGraph.get(str(leftMoveGraph)) is None):
                        visitedGraph[str(leftMoveGraph)] = 1
                        queue.append((leftMoveGraph, self.leftMove, currLevel + 1, startIndex))
            
                # move up
                if(prevMove != self.downMove and self.ValidMove(currBlankTileRow - 1, currBlankTileCol, 3, 3)):
                    upMoveGraph = self.ActionMoveUp(currBlankTileRow, currBlankTileCol)
                    
                    # check graph visited or not
                    if(visitedGraph.get(str(upMoveGraph)) is None):
                        visitedGraph[str(upMoveGraph)] = 1
                        queue.append((upMoveGraph, self.upMove, currLevel + 1, startIndex))
                    
                # move right
                if(prevMove != self.leftMove and self.ValidMove(currBlankTileRow, currBlankTileCol + 1, 3, 3)):
                    rightMoveGraph = self.ActionMoveRight(currBlankTileRow, currBlankTileCol)
                    
                    # check graph visited or not
                    if(visitedGraph.get(str(rightMoveGraph)) is None):
                        visitedGraph[str(rightMoveGraph)] = 1
                        queue.append((rightMoveGraph, self.rightMove, currLevel + 1, startIndex))
                    
                # move down
                if(prevMove != self.upMove and self.ValidMove(currBlankTileRow + 1, currBlankTileCol, 3, 3)):
                    downMoveGraph = self.ActionMoveDown(currBlankTileRow, currBlankTileCol)
                    
                    # check graph visited or not
                    if(visitedGraph.get(str(downMoveGraph)) is None):
                        visitedGraph[str(downMoveGraph)] = 1
                        queue.append((downMoveGraph, self.downMove, currLevel + 1, startIndex)) 
            startIndex = startIndex + 1
                        
        
        # backtrack to find the solution
        numberOfMoves = flag
        lastMoveToReachGoal = lastMove
        if(flag == -1):
            self.nodesFile.close()
            self.nodePathFile.close()
            self.nodesInfoFile.close()
            return ([], -1)
        else:
            answerGraphs = self.GeneratePath(movesArray, numberOfMoves, lastMove)
            
            # write to nodePath file
            for array in answerGraphs:
                self.WriteToPathFile(array[0])
            
            self.nodesFile.close()
            self.nodePathFile.close()
            self.nodesInfoFile.close()
            return (answerGraphs, numberOfMoves)



# set data path
args = sys.argv
if(len(args) > 1 and len(args[1]) > 8):
    inputMatrix = str(args[1])
    userMatrix = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    userMatrix[0][0] = int(inputMatrix[0])
    userMatrix[1][0] = int(inputMatrix[1])
    userMatrix[2][0] = int(inputMatrix[2])
    userMatrix[0][1] = int(inputMatrix[3])
    userMatrix[1][1] = int(inputMatrix[4])
    userMatrix[2][1] = int(inputMatrix[5])
    userMatrix[0][2] = int(inputMatrix[6])
    userMatrix[1][2] = int(inputMatrix[7])
    userMatrix[2][2] = int(inputMatrix[8])

    # solve graph
    puzzle = PuzzleSolver(userMatrix)
    (array, moves) = puzzle.solve()
    if(moves > -1):
        print("Puzzle solved with moves: " + str(moves))
    else:
        print("Puzzle not solved!")
else:
    print("Check README.md for running bfs.py")
