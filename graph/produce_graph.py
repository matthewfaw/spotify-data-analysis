import networkx as nx
import operator
import matplotlib.pyplot as plt
from functools import reduce

'''
themap: map: String -> [String]
returns G=(V,E), the graph represented by a list of all vertices V and edges E
'''
def generate_graph(themap):
    G = nx.Graph()
    edges = [(key, val) for key,vallist in themap.items() for val in vallist]
    G.add_edges_from(edges)
    print("Number of nodes: ",G.number_of_nodes())
    print("Number of edges: ",G.number_of_edges())
    return G

def plot_graph(G, plot_name, pos=None):
    plt.clf()
    nx.draw(G, with_labels=True, pos=pos)
    # plt.show()
    plt.savefig('plots/'+plot_name,bbox_inches='tight')
