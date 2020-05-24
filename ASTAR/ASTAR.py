
# The following code implements A* search to solve the path finding problem in a 10x10 maze.
# However, it has some BUGS leading to infinite loops and nonoptimal solutions! 
''' 
DEBUG the code to make it work with the maze map given in the exercise. 
Hint: You might want to print the current_node and the closed_list (explored set) for each loop 
      to check if the current_node is in the closed_list.
'''

import math 
import pygame,random,time,sys
pygame.init()
m =50
Imgdirt = pygame.transform.scale(pygame.image.load('dirt.jpg'),(m,m))
Imgtree = pygame.transform.scale(pygame.image.load('tree.jpg'),(m,m))
Imgwater = pygame.transform.scale(pygame.image.load('water.png'),(m,m))
Imgfire = pygame.transform.scale(pygame.image.load('Fire.png'),(m,m))
gameSurface = pygame.display.set_mode((800,600))
pygame.display.set_caption('ASTAR')

#Color
red= pygame.Color(255,0,0)
blue = pygame.Color(65,105,255)
white = pygame.Color(255,255,255)
gray = pygame.Color(128,128,128)
class Node():
    """A node class for A* search"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0 # PATH-COST to the node
        self.h = 0 # heuristic to the goal: straight-line distance hueristic
        self.f = 0 # evaluation function f(n) = g(n) + h(n)

    def __eq__(self, other):
        return self.position == other.position


''' DEBUG THE FOLLOWING FUNCTION '''
def astar(maze, start, end):
    """Returns a list of tuples as a solution from "start" to "end" state in "maze" map using A* search.
    See lecture slide for the A* algorithm."""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []    # frontier queue
    closed_list = []  # explored set
    
    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:
        pygame.time.delay(200)
        #Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        animate(current_node,goal)
        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Check if we found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current.parent is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Expansion: Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            
            
            # Child is on the closed list
            is_in_closed = False 
            for closed_child in closed_list: 
                if child == closed_child: 
                    is_in_closed = True 
                    break 
            if is_in_closed: continue 
            
           
            # Create the f, g, and h values
            child.g = current_node.g + 1
            
            child.h =((child.position[0] - end_node.position[0])**2+(child.position[1] - end_node.position[1])**2)
            child.f = child.g + child.h
            # Child is already in the open list 
            is_in_open = False 
            for open_node in open_list: 
                if child == open_node and child.g > open_node.g:
                   is_in_open = True 
                   break 
            if is_in_open: 
                continue

            # Add the child to the open list
            open_list.append(child)   
    
def animate(Find,goal):
    for i in range(0,10):
        for j in range(0,10):
            if(maze[i][j]==0):
                gameSurface.blit(Imgdirt,pygame.Rect(j*50,i*50,m,m))
            else:
                gameSurface.blit(Imgfire,pygame.Rect(j*50,i*50,m,m))
    path = []
    current = Find
    while current.parent is not None:
        path.append(current.position)
        current = current.parent
    gameSurface.blit(Imgtree,pygame.Rect(goal[1]*50,goal[0]*50,m,m))
    for x in path:
        gameSurface.blit(Imgwater,pygame.Rect(x[1]*50,x[0]*50,m,m))

    pygame.display.flip()
    

if __name__ == '__main__':

    ''' CHANGE THE BELOW VARIABLE TO REFLECT TO THE MAZE MAP IN THE EXERCISE '''
    maze =     [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # 1: obstacle position
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
                [0, 0, 0, 1, 0, 1, 1, 1, 1, 1],
                [0, 0, 0, 1, 1, 1, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 1, 0, 0, 0]]

    start = (0, 0)
    goal = (8, 9)

    path = astar(maze, start, goal)
    if(path==None):
        pygame.quit()
    print(path)          
