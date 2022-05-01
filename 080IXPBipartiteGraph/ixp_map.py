#!/usr/bin/env python3

import argparse, ujson
import networkx as nx
from networkx.algorithms import bipartite

class Graph():

    def __init__(self):
        self.graph  = nx.Graph()
        self.ixps   = set()
        self.ases   = set()
    
    def import_ixp_members(self):
        try:
            with open('./ixp_membership.txt', 'r') as file:
                membership = file.read().splitlines()
                for line in membership:
                    tokens = line.split(', ')
                    if(tokens[1]=='!'):
                        token = tokens[4]
                        if(token == ''):
                            token = tokens[5]
                        self.bipartite_graph(token,tokens[3])                            
                        
            print("Data have been imported successfully...")
            
        except IOError as e:
            print("Importing data failed with error: %s" % str(e))
            exit()
    
    # Prints useful information related to the produced bipartite graph.
    def graph_info(self,graph):
        print('Graph info:')
        print('Number of nodes:',nx.number_of_nodes(graph))
        print('Number of edges:',nx.number_of_edges(graph))
        print('Graph is connected?',nx.is_connected(graph))
    
    # Creates the bipartite graph
    def bipartite_graph(self,ixp,asn):
    
        self.graph.add_node(ixp, bipartite=0)
        self.ixps.add(ixp)
        
        self.graph.add_node(asn, bipartite=1)
        self.ases.add(asn)
        
        self.graph.add_edge(ixp,asn)
                        
    # Creates the multigraphs (projections) based on the bipartite graph.
    def multigraph(self):
        
        G_1 = bipartite.weighted_projected_graph(self.graph, self.ixps)
        self.export_graph([e for e in G_1.edges(data=True)],'ixp_mg.json')
        
        print("The IXP multi-graph (IXP-MG) has been created. Check \"ixp_mg.json\" file.")
        self.graph_info(G_1)
        
        G_2 = bipartite.weighted_projected_graph(self.graph, self.ases)
        self.export_graph([e for e in G_2.edges(data=True)],'as_mg.json')

        print("The AS multi-graph (AS-MG) has been created. Check \"as_mg.json\" file.")
        self.graph_info(G_2)

    # Exports the graph to json file.
    def export_graph(self,data,filename):
        with open(filename, 'w') as file:
            ujson.dump(data, file, ensure_ascii=True)


def main():
    
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-bg','--bipartite', action='store_true', help='Produces the bipartite graph.')
    group.add_argument('-mg','--multigraph', action='store_true', help='Produces the two multigraphs based on the bipartite graph.')
    options=parser.parse_args()
    
    graph = Graph()
    
    if options.bipartite:
        graph.import_ixp_members()
        graph.export_graph([e for e in graph.graph.edges()],'bipartite.json')
        print("The bipartite graph has been created. Check \"bipartite.json\" file.")
        graph.graph_info(graph.graph)
    elif options.multigraph:
        graph.import_ixp_members()
        graph.multigraph()


if __name__ == "__main__":
    main()
