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

'''
genres_map: ArtistName -> [GenreName]
num_listens: ArtistName -> totalNumListens on spotify
sigma: the edge weight filtering criterion

Returns a bipartite graph where:
    - left nodes are genres
    - right nodes are artists
    - edges connect artists to the genres under which they fall
    - edge weights correspond to the total number of times I've listened 
        to a given artist
'''
def create_genre_graph(genres_map, num_listens, sigma):
    all_genres = set([genre for genres in genres_map.values() for genre in genres])
    print('Number of genres: ',len(all_genres))
    all_artists = genres_map.keys()
    print('Number of artists: ', len(all_artists))
    
    B = nx.Graph()
    B.add_nodes_from(all_genres, bipartite=0)
    B.add_nodes_from(all_artists, bipartite=1)
    for artist, genres in genres_map.items():
        for genre in genres:
            weight = num_listens[artist]
            if weight > sigma:
                B.add_edge(genre, artist, weight=weight)
    return B

'''
Get the connected component subgraphs of G
'''
def get_connected_components(G):
    return list(nx.connected_component_subgraphs(G))

def plot_graph(G, plot_name, pos=None):
    plt.clf()
    nx.draw(G, with_labels=True, pos=pos)
    # plt.show()
    plt.savefig('plots/'+plot_name,bbox_inches='tight')
