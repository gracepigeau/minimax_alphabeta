"""
CISC 352, Assignment 2 - Alpha Beta Pruning

        SUBMITTED: March 16th, 2018
        TEAM NAME: Not Better Than NASA But We Try Really Hard
        MEMBERS: Katherine Baillie, Colton Barr, Matt Dixon, Cesur Kavaslar, Grace Pigeau, Lauren Yates

"""

#Read the input graphs into a list and return
def readInFile():
    #Go through .txt file
    with open('alphabeta.txt', 'r') as file:
        #Instantiate an empty list to hold the nodes and edges
        output = []
        #Go through each graph in the file
        for line in file:
            #boolean to keep track of whether nodes or edges are being input
            #Note: first set of {} is nodes, second set of {} is edges
            isedges = False
            #Instantiate empty list to hold the nodes
            nodes = []
            #Instantiate empty list to hole the edges
            edges = []
            #Booleans to keep track of which element in () is being recorded
            isfirst = False
            issecond = False
            #Instantiate an empty string to hold the first element in each set of ()
            first = ''
            #Instantiate an empty string to hold the second element in each set of ()
            second = ''
            
            for ch in line:
                #Once the end of a () is reached, add the first and second string to the proper list
                if ch == ')':
                    issecond = False
                    if isedges == False:
                        nodes.append((first, second))
                    else:
                        edges.append((first, second))
                    first = ''
                    second = ''
                #Once you've finished recording the first element, prepare to record the second in a ()
                if ch == ',' and isfirst == True:
                    isfirst = False
                    issecond = True
                #Record next character in the first element of a ()
                if isfirst == True:
                    first += ch
                #Record next character in the second element of a ()
                elif issecond == True and ch != ',':
                    second += ch
                #Prepare to record the first element in a set of ()
                if ch == '(':
                    isfirst = True
                #Start recording edges instead of nodes
                if ch == ' ':
                    isedges = True
            output.append((nodes,edges))

        # Prep & clear contents of output file 
        open('alphabeta_out.txt', 'w').close()
        
        return output

#Append the solution array to the output file
def writeToFile(finalStr):
        with open('alphabeta_out.txt', 'a') as file:
                file.write(finalStr + "\n\r")
        file.close()

#Create a class to define a node in a graph
class Node:

    #A node in a graph has a name, a type (MAX, MIN, or LEAF, and children nodes)
    def __init__(self, name, nodeType, children):
        self.name = name
        self.nodeType = nodeType
        self.children = children

    #Adds a child (node) to the specified node
    def addChild(self, child):
        self.children.append(child)

    #Prints out a node and it's children in an easy to read format
    def printNode(self):
        print("\nNode: " + self.name)
        print("Type: " + self.nodeType)
        if self.nodeType == 'LEAF':
            print("Children: NONE")
        else:           
            print("Children: ")
            for child in self.children:
                print(str(child.name))

#Takes in a list of nodes, and a list of edges and combines them to create a graph
def createGraph(nodes, edges):

    #Initialize an empty list which will define the graph
    graph = []

    #Go through the list of nodes and define each one using the node class
    #Append each node to the graph
    for pair in nodes:
        newnode = Node(pair[0], pair[1], [])
        graph.append(newnode)
        
    #Go through the list of edges and add the correct children to each node in the graph
    for edge in edges:
        #If the edge connects to a number, initialize a leaf node and add it to the graph
        if edge[1].isdigit():
            leafnode = Node(edge[1], 'LEAF', [])
            graph.append(leafnode)
            for node in graph:
                if node.name == edge[0]:
                    node.addChild(leafnode)
        else:
            for node in graph:
                if node.name == edge[1]:
                    child = node
            for node in graph:
                if node.name == edge[0]:
                    node.addChild(child)
    return graph

def alpha_beta(current, alpha, beta, count):

    #If current node is a leaf return its value and increment the leaf counter
    if current.nodeType == "LEAF":
        count += 1
        return int(current.name), count

    #If current node is on a MAX level
    if current.nodeType == "MAX":
        #Find the maximum value of all the nodes children and the current alpha
        for child in current.children:
            value, count = alpha_beta(child, alpha, beta, count)
            tempalpha = float('-inf')
            tempalpha = max(tempalpha, value)
            if tempalpha > alpha:
                alpha = tempalpha
            #If the alpha value is greater than beta don't check anymore leaves
            if alpha >= beta:
                break
        return alpha, count
    
    #If current node is on a MIN level
    if current.nodeType == "MIN":
        #Find the minimum value of all the nodes children and the current beta
        for child in current.children:
            value, count = alpha_beta(child, alpha, beta, count)
            tempbeta = float('inf')
            tempbeta = min(tempbeta, value)
            if tempbeta < beta:
                beta = tempbeta
            #If the beta value is less than alpha don't check anymore leaves
            if beta <= alpha:
                break
        return beta, count

def main():

    #Read in the file containing the graphs
    allTrees = readInFile()

    #Code for testing:
    #print(str(allTrees[0][0]))
    #print(str(allTrees[0][1]))

    #Cycle through all the graphs and calculate the final score and the number of leaves visited
    for i in range(0,len(allTrees)):

        #Create the graph based on the input file
        graph = createGraph(allTrees[i][0], allTrees[i][1])

        score, leafs = alpha_beta(graph[0], float('-inf'), float('inf'), 0)

        #Code for testing:
        #print("Score = " + str(score))
        #print("Leaf Nodes Examined = " + str(leafs))

        #Write the answer to the output file
        finalStr = "Graph: " + str(i+1) + ": Score: " + str(score) + "; Leaf Nodes Examined: " + str(leafs)
        writeToFile(finalStr)
        

main()
                    
