#CW1

#In this project, I decide to make a maze game using the definition of A* path planning method inside our powerpoint.
#The users will have an interactive communication with our system and need to input their designed maze to solve.
#After they input their maze, the game system will first decide if the maze input by the users is valid or not.
#For the valid maze design, the system will apply the A* path planing to find the best route.
#For the invalid maze, the system will ask if users want to modify their maze. If not, the game will be automatically closed.

#We import the necessary package to use in our project.
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

#Firstly, we build a Node class for our A* path planning.
class Node:
#Here, the parent and position means the parent and position of the node.
#g is the cost from the start point to the location of our current node.
#h is the calcualted cost from our current node towards the end point.
#f is the total cost of current node based on the definition of A*, it equals: f = g + h.
#At beginning we innitialize all the g, h, f value to be 0.
    def __init__ (self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0
#We also define a method to check the equality of the node with other nodes.
    def __eq__ (self, other):
        return self.position == other.position

# Second, we define a function for returning the complete route we find from the route planning function afterwards.
def return_path(current_node,maze):
    # Here, we innitialize the path to be an empty list
    path = []
    # Find the number of rows and columns based on the shape of our maze. And create a numpy array with size equals to the maze.
    # All entries of result is innitialized to be 0.
    num_rows = np.shape(maze)[0]
    num_columns = np.shape(maze)[1]
    result = np.zeros((np.shape(maze)))
    #Then we make our result matrix based on the designed mazes by users, where we set the block into 1 and clear route to be -1.
    for i in range (num_columns):
        for j in range (num_rows):
            if maze[j][i] == 1:
                result[j][i] == 1
            else:
                result[j][i] = -1
    current = current_node
    # We find the path from the start point to end point by adding the position of whole route and then reverse the collect positions.
    while current is not None:
        path.append (current.position)
        current = current.parent
    path = path[::-1]
    # Here we innitialize the start node position to be 1.
    start_value = 1
    for i in range(len(path)):
        # We then mark the position of the found route with each step plus 1 inside the result matrix and return our result matrix.
        result[path[i][0]][path[i][1]] = start_value
        start_value = start_value + 1
    return result

# Here, we then define a function search which take in the value of maze, start, end in list form and cost in integer to return
# the path as a tuple.
def search(maze, cost, start, end):
    # Initializing and create the start point and end point as well as the value of g, h and f.
    start_node = Node(None, tuple(start))
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, tuple(end))
    end_node.g = end_node.h = end_node.f = 0
    
    # Create two lists to store the position of Nodes already visited and the Node to be visited.
    yet_to_visit_list = []
    visited_list = []
    yet_to_visit_list.append(start_node)

    # innitializing a counter for counting the times of iterations during the path planning to check if the while loop is infinite.
    # We set the maximum possible iterations to be max_iterations
    outer_iterations = 0
    max_iterations = (len(maze) // 2) ** 10
    
    # Define the up, down, right, left, movement of the path.
    move = [[-1,0],[0,-1],[1,0],[0,1]]

    no_rows, no_columns = np.shape(maze)
    
    # Making a while loop to find the path until the end point is archieved.
    while len(yet_to_visit_list) > 0:
        # Each time when the while loop runs, the iteration counter will plus 1.
        outer_iterations = outer_iterations + 1
        # Obtain the current node to go.
        current_node = yet_to_visit_list[0]
        current_index = 0
        for index, item in enumerate(yet_to_visit_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        # To check if our while loop has too many iterations to go which is abnormal in our case.
        if outer_iterations > max_iterations:
            print("The pathfinding has too many iterations which is abnormal.")
            return return_path(current_node, maze)
        
        # We delete the current node visited and add it to the list of nodes already visited.
        yet_to_visit_list.pop(current_index)
        visited_list.append(current_node)
        
        # When the end point is reached, we will stop the while loop and return the path we obtained.
        if current_node == end_node:
            return return_path(current_node,maze)
        
        # We create a list of children nodes of the current nodes, ie. the adjacent nodes of current nodes
        children = []
        for new_position in move:
            
            # Obtaining the node position.
            node_position = (current_node.position[0] + new_position[0],current_node.position[1] + new_position[1])
            
            # To check if our movement is inside the boundary of the designed maze.
            if(node_position[0] > (no_rows - 1) or node_position[0] < 0 or node_position[1] > (no_columns - 1) or node_position[1] < 0):
                continue
            
            # To check if our movement hit the blocks set by the users.
            if maze[node_position[0]][node_position[1]] != 0:
                continue
            
            # Create a new Node with its position.
            new_node = Node(current_node, node_position)
            
            # Add the new node created into the list of valid adjacent nodes to go.
            children.append(new_node)
        
        # Loop inside the valid adjacent nodes to go to find the best movement using the definition of A* path planning method.
        for child in children:
            
            # To check if our child node is already inside the list of visited node, if yes, the loop will stop, else it will continue.
            if len([visited_child for visited_child in visited_list if visited_child == child]) > 0:
                continue
            
            # Calculating the g value for the current node.
            child.g = current_node.g + cost
            
            # Calculating the square of Euclidean distance from current node to the end point, ie. the h value by definition.
            child.h = (((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2))
            
            # Calculating the f value by simply adding up the values of g and h.
            child.f = child.g + child.h
            
            # To check if the child node is already inside the yet_to_visit list and if the value of g is already lower, if yes the loop
            # will continue, else it will stop.
            if len([i for i in yet_to_visit_list if child == i and child.g > i.g]) > 0:
                continue
            
            # We add the child node found into the yet_to_visit list to go.
            yet_to_visit_list.append(child)


# maze = np.array(0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1,0,0,1,0,0,0,0,0,1,0)
# 0,1,0,0,0,0,1,1,1,1,1,1,0,1,0,1,0,0,0,1,0,0,1,0,0,0,0,0,1,0

# We will then create a Class of Maze to achieve the iteractive functions with users to find the path of maze based on their design.

class Maze:
    
    # Initializing the beginning value of list of maze to be empty list.
    def __init__(self):
        self.maze = []
    
    # Define a function of mazePath to communicate with users to obtain their designed maze.
    def mazePath (self):
        print("Welcome to the A* path planning game!")
        print("To solve the maze you want, you need to input your designed maze into matrix, the default start point")
        print("is located at the up left corner of your maze and the default end point is at the lower right corner.")
        
        # Ask if the users want to solve a maze, if the answer is yes, the while loop will start, if not the game will be closed.
        A = input("Hello! Do you want to solve a maze?")
        while A == 'Yes' or A == 'yes' or A == 'Y' or A == 'y':
            
            # obtaining the maze designed by user in 0,1 form as well as the number of rows and columns for the system to transfer the
            # designed maze into a gird style to see.
            B = input("Enter the entries rowwise separated by commas (maze must be in form of M*N numpy array where 0 represents unblocked route, and 1 represents the blocks):")
            User_Row = int(input("Enter the number of rows:"))
            User_Col = int(input("Enter the number of columns:"))
            Entries_S = B.split(",")
            Entries_I = []
            
            # Create a list Entries_I to contain all entries of maze in integers.
            for p in range(len(Entries_S)):
                Entries_I.append(int(Entries_S[p]))
                
            # Use a try function to check if the maze entered by the users is in the M*N form or not. And the system will ask the
            # users to enter the maze again if it is not in the valid shape.
            try:
                Maze = np.reshape(Entries_I,(User_Row,User_Col))
                num_rows = np.shape(Maze)[0]
                num_columns = np.shape(Maze)[1]
                num_grid = num_rows * num_columns
                
                # Check if the user block the whole maze which makes the system impossible to find a path.
                if np.max(np.sum(Maze, axis = 1)) == num_columns:
                    E = input("You blocked the maze into two sides which made the system impossible to find a route, do you want to enter your maze again?")
                    A = E

                elif np.max(np.sum(Maze, axis = 0)) == num_rows:
                    F = input("You blocked the maze into two sides which made the system impossible to find a route, do you want to enter your maze again?")
                    A = F
                
                # Check if the user has blocked the default start point and end point of the maze which also make the system impossible 
                # to find the path.
                elif Maze[0][0] == 1 or Maze[num_rows-1][num_columns-1] == 1:
                    I = input("You should not block the start / end point, do you want to enter your maze again?")
                    A = I
                        
                # After making sure the validity of maze, we display the maze designed by users in grid to let them ensure if this is
                # the maze they really want to solve.
                else:
                    print("The maze you have entered is:")
                    print(Maze)
                    
                    # Display the maze using the matplotlib package.
                    # where white grids represent the clear route and blue grids represent the blocks.
                    cmap = colors.ListedColormap(['white', 'blue'])
                    bounds = [0,0.5,1]
                    norm = colors.BoundaryNorm(bounds, cmap.N)

                    fig, ax = plt.subplots()
                    ax.imshow(Maze, cmap=cmap, norm=norm)

                    # Draw gridlines
                    ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
                    ax.set_xticks(np.arange(-.5,num_columns, 1));
                    ax.set_yticks(np.arange(-.5,num_rows , 1));

                    plt.show()
                    
                    # To obtain the confirmation from user to see if they get the maze they want to design, if yes, the system will then
                    # find the path for their maze using the A* methods we defined before.
                    User_Confirmation = input("Is the maze shown correct?(Answer [Correct/correct/C/c] or [Incorrect/incorrect/I/i] to avoid errors):")
                    if User_Confirmation == 'Correct' or User_Confirmation == 'correct' or User_Confirmation == 'C' or User_Confirmation == 'c':
                        
                        # Set the default start point as upper left corner and the end point to be the lower right corner.
                        start = [0,0]
                        end = [num_rows-1, num_columns-1]
                        cost = 1
                        print("Congradulations, the maze is correct, and here comes the route result:")
                        # Apply the path planning method we defined to find the optimized route towards the end point.
                        path = search(Maze, cost, start, end)
                        print(path)
                        
                        # Display the path planning we find inside the maze designed by the users using the matplotlib package again.
                        # where white grids represent the clear route, blue grids represent the blocks and red grids represent the path
                        # found by the system.
                        cmap = colors.ListedColormap(['white', 'blue', 'red'])
                        bounds = [-2,-0.5,0.5,num_grid]
                        norm = colors.BoundaryNorm(bounds, cmap.N)

                        fig, ax = plt.subplots()
                        ax.imshow(path, cmap=cmap, norm=norm)

                        # Draw gridlines
                        ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
                        ax.set_xticks(np.arange(-.5,num_columns, 1));
                        ax.set_yticks(np.arange(-.5,num_rows , 1));

                        plt.show()
                        
                        # At last, to check if the users want to design a maze again. If not, the game will be closed. 
                        # If yes, we will restart the while loop again to find the path for the new maze.
                        H = input("Do you want to enter your maze again?")
                        A = H
                        
                    # If the user realize that the maze shown is not what they want, the system will allow them to input the maze again.
                    elif User_Confirmation == 'Incorrect' or User_Confirmation == 'incorrect' or User_Confirmation == 'I' or User_Confirmation == 'i':
                        G = input("Do you want to enter your maze again?")
                        A = G
                        
                    # If the user input something irrelavant, the game will be closed.
                    else:
                        break
                        
            # If the maze entered by user is not in M*N form, a ValueError will occur and the system will ask for a correction of maze.
            except ValueError:
                C = input("The maze is not in an M*N form, do you want to enter your maze again?")
                A = C
                
        # Close the game.
        print("The game is closed. Goodbye!")

# To evoke the path planning game when running the code.
l = Maze()
l.mazePath()

# The project for CW1 is finished. Thank you!
