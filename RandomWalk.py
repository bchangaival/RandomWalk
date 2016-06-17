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
    def neighborMove(self, graph, visitList):
        overlap = True
        occupiedNeighbors = 0
        neighborList = graph.neighbors(self.position)
        #check if the neighbors are all occupied
        for neighbor in neighborList:
            for agent in agentList:
                if neighbor == agent.getPosition():
                    occupiedNeighbors += 1
        if occupiedNeighbors == len(neighborList):
            self.randomMove(visitList)
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
    def randomMove(self, visitList):
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
        
if __name__ == "__main__":
    agentList = []
    agentPercentage = 0.2
    global nodeNumber
    
    #Import the graph
    importedGraph = read_graphml("PrunedPDMAp.graphml")
    bioGraph = importedGraph.to_undirected().copy()
    karateGraph = karate_club_graph()
    #manipulate the graph
    interestedGraph = bioGraph
    nodeList = nodes(interestedGraph)
    #if the graph label is not int, change it to int for easier indexing
    newLabels = [int(nodeList[i].replace("n", "")) for i in range(len(nodeList))]
    mapping = dict(zip(nodeList, newLabels))
    interestedGraph = relabel_nodes(interestedGraph, mapping)
    nodeNumber = number_of_nodes(interestedGraph)
    dominatingSet = dominating_set(interestedGraph)
    agentNumber = int((float(nodeNumber) * agentPercentage))
    print "Number of agent: ", agentNumber
    #initialize the visit list
    visitList = [1 for n in range(number_of_nodes(interestedGraph))]
    
    # generateFromDominate(agentList, dominatingSet)
    generateAgent(nodeNumber, agentList, agentNumber)
    iteration = 0
    print 'Total node: ', nodeNumber
    print 'Agent: ',len(agentList), ' Percentage: ', (float(len(agentList))/float(nodeNumber)) *100
    while visitList.count(0) != len(visitList):
        for agent in agentList:
            agent.neighborMove(interestedGraph, visitList)
        iteration += 1
    print iteration*len(agentList)
    
    #test if the graph has small world property
    # totalLength = 0.0;
#     iteration = 0;
#     for g in connected_component_subgraphs(interestedGraph):
#         if len(g) >1:
#             totalLength += average_shortest_path_length(g)
#         iteration +=1
#     averagePathLength = totalLength/float(iteration)
#     print "APL: ", averagePathLength
#     edgeList = interestedGraph.edges()
#     essentialEdges = set(interestedGraph.edges())
#     essentialEdges = list(essentialEdges)
#     strippedGraph = Graph()
#     strippedGraph.add_nodes_from(nodes(interestedGraph))
#     strippedGraph.add_edges_from(essentialEdges)
#     print len(nodes(strippedGraph)), " and ", len(nodes(interestedGraph))
#     print len(edges(strippedGraph)), " and ", len(edges(interestedGraph))
#     print "K-Degree: ", average_degree_connectivity(strippedGraph)
#     # print essentialEdges
#     print "CC: ",average_clustering(strippedGraph)
    
    
    