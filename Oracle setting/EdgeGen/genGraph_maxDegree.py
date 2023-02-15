
"""
Generates random graph with given max degree
"""
import collections
import sys
from random import choices
import random
import numpy as np
import math
import pandas as pd 
import pdb
from itertools import combinations 

#Generate a symmetric random graph
#Below code generates the neighboor vertices for each node. 
# The density of the graph can be changed through random.randint(1, noVer/3)
#random.seed(3)
#np.random.seed(3)


""" A Python Class
A simple Python graph class, demonstrating the essential 
facts and functionalities of graphs.
"""
def cycle_exists(G):                     # - G is a directed graph
    color = { u : "white" for u in G  }  # - All nodes are initially white
    found_cycle = [False]                # - Define found_cycle as a list so we can change
                                         # its value per reference, see:
                                         # http://stackoverflow.com/questions/11222440/python-variable-reference-assignment
    for u in G:                          # - Visit all nodes.
        if color[u] == "white":
            dfs_visit(G, u, color, found_cycle)
        if found_cycle[0]:
            break
    return found_cycle[0]
 
#-------
 
def dfs_visit(G, u, color, found_cycle):
    if found_cycle[0]:                          # - Stop dfs if cycle is found.
        return
    color[u] = "gray"                           # - Gray nodes are in the current path
    for v in G[u]:                              # - Check neighbors, where G[u] is the adjacency list of u.
        if color[v] == "gray":                  # - Case where a loop in the current path is present.  
            found_cycle[0] = True       
            return
        if color[v] == "white":                 # - Call dfs_visit recursively.   
            dfs_visit(G, v, color, found_cycle)
    color[u] = "black"

class Graph(object):

    def __init__(self, graph_dict=None):
        """ initializes a graph object 
            If no dictionary or None is given, 
            an empty dictionary will be used
        """
        if graph_dict == None:
            graph_dict = {}
        self.__graph_dict = graph_dict

    def vertices(self):
        """ returns the vertices of a graph """
        return list(self.__graph_dict.keys())

    def edges(self):
        """ returns the edges of a graph """
        return self.__generate_edges()

    def add_vertex(self, vertex):
        """ If the vertex "vertex" is not in 
            self.__graph_dict, a key "vertex" with an empty
            list as a value is added to the dictionary. 
            Otherwise nothing has to be done. 
        """
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = []

    def add_edge(self, edge):
        """ assumes that edge is of type set, tuple or list; 
            between two vertices can be multiple edges! 
        """
        edge = set(edge)
        (vertex1, vertex2) = tuple(edge)
        if vertex1 in self.__graph_dict:
            self.__graph_dict[vertex1].append(vertex2)
        else:
            self.__graph_dict[vertex1] = [vertex2]

    def __generate_edges(self):
        """ A static method generating the edges of the 
            graph "graph". Edges are represented as sets 
            with one (a loop back to the vertex) or two 
            vertices 
        """
        edges = []
        for vertex in self.__graph_dict:
            for neighbour in self.__graph_dict[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges

    def __str__(self):
        res = "vertices: "
        for k in self.__graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        return res

    def isCyclicUtil(self, v, visited, recStack): 
  
        # Mark current node as visited and  
        # adds to recursion stack 
        visited[v] = True
        recStack[v] = True
  
        # Recur for all neighbours 
        # if any neighbour is visited and in  
        # recStack then graph is cyclic 
        for neighbour in self.graph[v]: 
            if visited[neighbour] == False: 
                if self.isCyclicUtil(neighbour, visited, recStack) == True: 
                    return True
            elif recStack[neighbour] == True: 
                return True
  
        # The node needs to be poped from  
        # recursion stack before function ends 
        recStack[v] = False
        return False
    
    
    def isCyclic(self): 
        visited = [False] * self.V 
        recStack = [False] * self.V 
        for node in range(self.V): 
            if visited[node] == False: 
                if self.isCyclicUtil(node, visited, recStack) == True: 
                    return True
        return False
    
    
    def is_connected(self, 
                         vertices_encountered = None, 
                         start_vertex=None):
            """ determines if the graph is connected """
            if vertices_encountered is None:
                vertices_encountered = set()
            gdict = self.__graph_dict        
            vertices = list(gdict.keys()) # "list" necessary in Python 3 
            if not start_vertex:
                # chosse a vertex from graph as a starting point
                start_vertex = vertices[0]
            vertices_encountered.add(start_vertex)
            if len(vertices_encountered) != len(vertices):
                for vertex in gdict[start_vertex]:
                    if vertex not in vertices_encountered:
                        if self.is_connected(vertices_encountered, vertex):
                            return True
            else:
                return True
            return False
        

    def find_all_paths(self, start_vertex, end_vertex, path=[]):
        """ find all paths from start_vertex to 
            end_vertex in graph """
        graph = self.__graph_dict 
        path = path + [start_vertex]
        if start_vertex == end_vertex:
            return [path]
        if start_vertex not in graph:
            return []
        paths = []
        for vertex in graph[start_vertex]:
            if vertex not in path:
                extended_paths = self.find_all_paths(vertex, 
                                                     end_vertex, 
                                                     path)
                for p in extended_paths: 
                    paths.append(p)
        return paths


def find_all_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if not start in graph:
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths


def GenRandomGraph_maxdegree(noVer,max_degree):
    enter = 0
    enter2 = 1
   # while not enter or not enter2:
    while not enter:
        vertices = list(range(noVer))
        all_edges_dic ={}
        for node1 in vertices:    
            for node2 in range(node1+1,noVer):
                all_edges_dic[(node1,node2)] = [-1,-2,-3]
        selected_edges = []
        select_nodes_1 = random.sample(vertices, int(noVer/2)-2)
        candidate_neighbor_nodes = list(range(noVer))
        current_degrees = [0 for i in range(noVer)]
        for this_node in select_nodes_1:
            if max_degree-current_degrees[this_node]==0:
              continue
            this_degree = random.randint(1,max_degree-current_degrees[this_node])
            current_degrees[this_node] = current_degrees[this_node] + this_degree
            candidate_n_freq = []
            for c_n in candidate_neighbor_nodes:
                if c_n!=this_node:
                    candidate_n_freq.extend([c_n for t_f in range(max_degree-current_degrees[c_n])])
            selected_neighbors = random.sample(candidate_n_freq,min(this_degree,len(candidate_n_freq)))
            for this_sel_n in selected_neighbors:
                edge_options = all_edges_dic[tuple(sorted(list((this_node,this_sel_n))))]
                rand_dir = random.sample(edge_options,1)[0]
                all_edges_dic[tuple(sorted(list((this_node,this_sel_n))))].remove(rand_dir)
                current_degrees[this_sel_n] = current_degrees[this_sel_n]+1
                selected_edges.append([min(this_node,this_sel_n),rand_dir,max(this_node,this_sel_n)])
                
   
       
        D_true = np.zeros((noVer,noVer),dtype=int)
        for ii in vertices:
              for ii_2 in range(ii+1,noVer):
                if [ii,-1,ii_2] in selected_edges and [ii,-2,ii_2] in selected_edges:
                    D_true[ii,ii_2] = -3
                elif [ii,-1,ii_2] in selected_edges:
                    D_true[ii,ii_2] = -1
                elif [ii,-2,ii_2] in selected_edges:
                    D_true[ii,ii_2] = -2

                    
        E_true = np.zeros((noVer,noVer),dtype=int)
        for ii in vertices:
              for ii_2 in range(ii+1,noVer):
                if [ii,-3,ii_2] in selected_edges:
                    E_true[ii,ii_2] = -1
                
        

           
           
        for ii in vertices:
             for ii_2 in vertices:
                 if D_true[ii,ii_2]==-1:
                     D_true[ii_2,ii]=-2
                 if D_true[ii,ii_2]==-2:
                     D_true[ii_2,ii]=-1
                 if D_true[ii,ii_2]==-3:
                     D_true[ii_2,ii]=-3
    
                     
        for ii in vertices:
             for ii_2 in vertices:
                 if E_true[ii,ii_2]==-1:
                     E_true[ii_2,ii]=-1  

        
        
        for i in vertices:
            degree= 0 
            degree = degree + sum(D_true[i,:]!=0)
            degree = degree + sum(E_true[i,:]!=0)
            for j in vertices:
                if D_true[i,j] == -3:
                    degree = degree+1
            if degree > max_degree:
                pdb.set_trace()
                    
        
                    
             
        dum_verts = []
        for ii in vertices:
            add_verts = []
            for jj in vertices:
                if D_true[ii,jj]!=0 or E_true[ii,jj]!=0:
                    add_verts.append(jj)
            dum_verts.append(add_verts)
        graph_init = dict(zip(vertices,dum_verts)) 
        graph = Graph(graph_init)
        enter = graph.is_connected()
        
        
        while not enter and max_degree == 2:
            
            available_nodes = [t_n for t_n in vertices if current_degrees[t_n]<max_degree]
            if len(available_nodes)<2:
                break
            n1,n2 = random.sample(available_nodes,2)
            edge_options = all_edges_dic[tuple(sorted(list((n1,n2))))]
            rand_dir = random.sample(edge_options,1)[0]
            all_edges_dic[tuple(sorted(list((n1,n2))))].remove(rand_dir)
            current_degrees[n1] = current_degrees[n1]+1
            current_degrees[n2] = current_degrees[n2]+1
            selected_edges.append([min(n1,n2),rand_dir,max(n1,n2)])
            
            
            D_true = np.zeros((noVer,noVer),dtype=int)
            for ii in vertices:
                  for ii_2 in range(ii+1,noVer):
                    if [ii,-1,ii_2] in selected_edges and [ii,-2,ii_2] in selected_edges:
                        D_true[ii,ii_2] = -3
                    elif [ii,-1,ii_2] in selected_edges:
                        D_true[ii,ii_2] = -1
                    elif [ii,-2,ii_2] in selected_edges:
                        D_true[ii,ii_2] = -2

                        
            E_true = np.zeros((noVer,noVer),dtype=int)
            for ii in vertices:
                  for ii_2 in range(ii+1,noVer):
                    if [ii,-3,ii_2] in selected_edges:
                        E_true[ii,ii_2] = -1
                    
            

               
               
            for ii in vertices:
                  for ii_2 in vertices:
                      if D_true[ii,ii_2]==-1:
                          D_true[ii_2,ii]=-2
                      if D_true[ii,ii_2]==-2:
                          D_true[ii_2,ii]=-1
                      if D_true[ii,ii_2]==-3:
                          D_true[ii_2,ii]=-3
        
                         
            for ii in vertices:
                  for ii_2 in vertices:
                      if E_true[ii,ii_2]==-1:
                          E_true[ii_2,ii]=-1  

            
            
            for i in vertices:
                degree= 0 
                degree = degree + sum(D_true[i,:]!=0)
                degree = degree + sum(E_true[i,:]!=0)
                for j in vertices:
                    if D_true[i,j] == -3:
                        degree = degree+1
                if degree > max_degree:
                    pdb.set_trace()
                        
            
                        
                 
            dum_verts = []
            for ii in vertices:
                add_verts = []
                for jj in vertices:
                    if D_true[ii,jj]!=0 or E_true[ii,jj]!=0:
                        add_verts.append(jj)
                dum_verts.append(add_verts)
            graph_init = dict(zip(vertices,dum_verts)) 
            graph = Graph(graph_init)
            enter = graph.is_connected()
            
        
            
            
    
        
    D_true_ASP = np.zeros((noVer,noVer),dtype=int)
    E_true_ASP = -E_true
    
    for ii in vertices:
        for ii_2 in vertices:
            if D_true[ii,ii_2]==-2 or D_true[ii,ii_2]==-3:
                D_true_ASP[ii,ii_2] = 1
                                    
                
    
    pd.DataFrame(D_true_ASP).to_csv("../ASP_oracle_parallel/hyttinen2014uai_ver6/pkg/R/D.csv",  index=None)  
    pd.DataFrame(E_true_ASP).to_csv("../ASP_oracle_parallel/hyttinen2014uai_ver6/pkg/R/E.csv",  index=None)  
    
    
    pd.DataFrame(D_true_ASP).to_csv("../ASP_run/hyttinen2014uai_ver6/pkg/R/D.csv",  index=None)  
    pd.DataFrame(E_true_ASP).to_csv("../ASP_run/hyttinen2014uai_ver6/pkg/R/E.csv",  index=None)  
    
    
    pd.DataFrame(D_true_ASP).to_csv("../ASP_run_newASP/hyttinen2014uai_ver6/pkg/R/D.csv",  index=None)  
    pd.DataFrame(E_true_ASP).to_csv("../ASP_run_newASP/hyttinen2014uai_ver6/pkg/R/E.csv",  index=None)  

    return(D_true, E_true, dum_verts)
    
    
    
