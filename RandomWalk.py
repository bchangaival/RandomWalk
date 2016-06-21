from networkx import *
import matplotlib.pyplot as plt
import random as ran
import math

# agent instance
class Agent(object):
    def __init__(self, position, agentID = 0):
        self.position = position
        self.agentID = agentID
    def getPosition(self):
        return self.position
    def setPosition(self, newPosition):
        self.position = newPosition
    #Move from the current node to the neighbor randomly
    def neighborMove(self, graph, agentList, visitList):
        overlap = True
        occupiedNeighbors = 0
        neighborList = graph.neighbors(self.position)
        #check if the neighbors are all occupied
        for neighbor in neighborList:
            for agent in agentList:
                if neighbor == agent.getPosition():
                    occupiedNeighbors += 1
        if occupiedNeighbors == len(neighborList):
            self.randomMove(agentList, visitList)
        else:
            #move to the random picked neighbour which is not occupied
            while overlap == True:
                overlapCount = 0
                target = ran.choice(neighborList)
                for agent in agentList:
                    if target == agent.getPosition():
                        overlapCount += 1
                if overlapCount == 0:
                    overlap = False
                    self.position = target
                    # if the node is visited, mark it as zero
                    visitList[target] = 0
    # Move randomly to prevent getting stuck in the surrounded node
    def randomMove(self, agentList, visitList):
        overlap = True
        #move to the random picked node which is not occupied
        while overlap == True:
            overlapCount = 0
            target = ran.randint(0, nodeNumber-1)
            for agent in agentList:
                if target == agent.getPosition():
                    overlapCount += 1
            if overlapCount == 0:
                overlap = False
                self.position = target
                # if the node is visited, mark it as zero
                visitList[target] = 0
                
def generateAgent(nodeNumber, agentList, agentNumber):
    duplicateCount = 0
    for i in range(agentNumber):
        duplicate = True
        while duplicate == True:
            duplicateCount = 0
            randomIndex = ran.randint(0, nodeNumber-1)
            for item in agentList:
                if randomIndex == item.getPosition():
                    duplicateCount += 1
            if duplicateCount == 0:
                agent = Agent(randomIndex)
                agentList.append(agent)
                duplicate = False
                    
def generateFromDominate(agentList, dominatingSet):
    for clusterID,dominatingNode in enumerate(dominatingSet):
        agent = Agent(dominatingNode,clusterID+1)
        agentList.append(agent)

def testRandomWalk():
    global nodeNumber
    numberList = [100, 500, 1000]
    p = [1, 0.5, 0.05]
    agentList = []
    agentPercentage = [0.5]
    agentNumber = 0
    
    #Import the graph
    importedGraph = read_graphml("PDMap.graphml")
    #Change the PDMAP graph from directed to undirected graph
    bioGraph = importedGraph.to_undirected().copy()
    
    #manipulate the graph
    interestedGraph = bioGraph
    nodeList = nodes(interestedGraph)
    #if the graph label is not int, change it to int for easier indexing
    newLabels = [int(nodeList[i].replace("n", "")) for i in range(len(nodeList))]
    mapping = dict(zip(nodeList, newLabels))
    interestedGraph = relabel_nodes(interestedGraph, mapping)
    nodeNumber = number_of_nodes(interestedGraph)
    dominatingSet = dominating_set(interestedGraph)
    
    #initialize the visit list from dominating set
    # iteration = 0
#     averageIteration = 0
#     generateFromDominate(agentList, dominatingSet)
#     for i in range(10):
#         iteration = 0
#         print 'Agent: ',len(agentList), ' Percentage: ', (float(len(agentList))/float(nodeNumber)) *100
#         visitList = [1 for n in range(number_of_nodes(interestedGraph))]
#         while visitList.count(0) != len(visitList):
#             for agent in agentList:
#                 if visitList.count(0) == len(visitList):
#                     break
#                 agent.neighborMove(interestedGraph, agentList, visitList)
#                 iteration += 1
#         averageIteration += iteration
#     averageIteration = averageIteration/10
#     print averageIteration
    # Test how the agent number can affect the graph coverage in PDMAP Graph
    iteration = 0
    print 'PDMAP Graph Total node: ', nodeNumber
    for percent in agentPercentage:
        agentList = []
        agentNumber = int((float(nodeNumber) * percent))
        generateAgent(nodeNumber, agentList, agentNumber)
        print 'Agent: ',len(agentList), ' Percentage: ', (float(len(agentList))/float(nodeNumber)) *100
        visitList = [1 for n in range(number_of_nodes(interestedGraph))]
        while visitList.count(0) != len(visitList):
            for agent in agentList:
                if visitList.count(0) == len(visitList):
                    break
                agent.neighborMove(interestedGraph, agentList, visitList)
                iteration += 1
        print iteration
    # Test how the agent number can affect the graph coverage in Random Graph    
    iteration = 0
    for number in numberList:
        nodeNumber = number
        print 'Random Graph Total node: ', nodeNumber
        for prob in p:
            print 'Random Graph connect probability: ', prob
            for percent in agentPercentage:
                interestedGraph = erdos_renyi_graph(number, prob)
                print average_clustering(interestedGraph)
                agentList = []
                visitList = [1 for n in range(number_of_nodes(interestedGraph))]
                agentNumber = int((float(nodeNumber) * percent))
                generateAgent(nodeNumber, agentList, agentNumber)
                print 'Agent: ',len(agentList), ' Percentage: ', (float(len(agentList))/float(nodeNumber)) *100
                while visitList.count(0) != len(visitList):
                    for agent in agentList:
                        if visitList.count(0) == len(visitList):
                            break
                        agent.neighborMove(interestedGraph, agentList, visitList)
                        iteration += 1
                print iteration

def testSmallWorld():
    global nodeNumber
    karateGraph = karate_club_graph()
    
    agentList = []
    agentPercentage = [0.1, 0.3, 0.5]
    agentNumber = 0
    iteration = 0
    interestedGraph = karateGraph
    nodeNumber = number_of_nodes(interestedGraph)
    averageDegree = (2*number_of_edges(karateGraph))/nodeNumber
    print 'Karate Graph Total node: ', nodeNumber
    for percent in agentPercentage:
        agentList = []
        agentNumber = int((float(nodeNumber) * percent))
        generateAgent(nodeNumber, agentList, agentNumber)
        print 'Agent: ',len(agentList), ' Percentage: ', (float(len(agentList))/float(nodeNumber)) *100
        visitList = [1 for n in range(number_of_nodes(interestedGraph))]
        while visitList.count(0) != len(visitList):
            for agent in agentList:
                if visitList.count(0) == len(visitList):
                    break
                agent.neighborMove(interestedGraph, agentList, visitList)
                iteration += 1
        print iteration
    randomGraph = erdos_renyi_graph(nodeNumber, averageDegree, 1)
    interestedGraph = randomGraph
    print 'Random Graph Total node: ', nodeNumber
    for percent in agentPercentage:
        agentList = []
        agentNumber = int((float(nodeNumber) * percent))
        generateAgent(nodeNumber, agentList, agentNumber)
        print 'Agent: ',len(agentList), ' Percentage: ', (float(len(agentList))/float(nodeNumber)) *100
        visitList = [1 for n in range(number_of_nodes(interestedGraph))]
        while visitList.count(0) != len(visitList):
            for agent in agentList:
                if visitList.count(0) == len(visitList):
                    break
                agent.neighborMove(interestedGraph, agentList, visitList)
                iteration += 1
        print iteration
    
    
    
if __name__ == "__main__":
    global nodeNumber
    testRandomWalk()
    testSmallWorld()


    
    
    
    