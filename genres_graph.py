from serialize import save
from graph import produce_graph as pg
import networkx as nx
import operator

genres_map = save.load('genres_2017-09-11 01:33:42.733512')
num_listens = save.load('total_number_of_listens_2017-09-13 00:33:36.633054')
listening_history = save.load('listening_history_2017-09-13 00:33:36.631360')

genres_map['Joey Badass'] = genres_map.pop('Joey Bada$$')
num_listens['Joey Badass'] = num_listens.pop('Joey Bada$$')
listening_history['Joey Badass'] = listening_history.pop('Joey Bada$$')

all_genres = set([genre for genres in genres_map.values() for genre in genres])
print('Number of genres: ',len(all_genres))
all_artists = genres_map.keys()
print('Number of artists: ', len(all_artists))
connections = [(genre,artist) for genre,artists in genres_map.items() for artist in artists]
print('Number of connections: ', len(connections))

# Create the bipartite graph
B = nx.Graph()
B.add_nodes_from(all_genres, bipartite=0)
B.add_nodes_from(all_artists, bipartite=1)
for artist, genres in genres_map.items():
    for genre in genres:
        B.add_edge(genre, artist, weight=num_listens[artist])

# Filter the graph by edge weights
# The idea behind this is to get a nicer understanding of the connected component subgraphs
# Perhaps these subgraphs could act as a sort of equivalence relation on the genres...
sigma = 100
filtered_edges = [(u,v,d) for u,v,d in B.edges(data=True) if d['weight'] > sigma]
B = nx.Graph()
B.add_weighted_edges_from(filtered_edges)

# Get number of connected components
# The 0-labeled nodes can be thought of as genre clusters
graphs = list(nx.connected_component_subgraphs(B))
print('Number of connected component subgraphs (genre clusters): ',len(graphs))

# Get the genre clusters for each connected component subgraph
for index, graph in enumerate(graphs):
    genres, _ = nx.bipartite.sets(graph)
    print("Genre cluster %d:"%(index))
    print(list(genres))

# Get degrees:
print('Degrees of all genres: ')
degrees = B.degree(all_genres)
print(sorted(degrees.items(), key=operator.itemgetter(1)))
max_degree_val = max(degrees.values()) 

# Get the genres in the first connected component subgraph
l,r = nx.bipartite.sets(graphs[0])
print('Number of genres in ccs1: ',len(l))
print(l)


# print all the subgraphs
pos = {}
pos.update((node,(1,index)) for index, node in enumerate(all_genres))
pos.update((node,(2,index)) for index, node in enumerate(all_artists))

for index, graph in enumerate(graphs):
    pg.plot_graph(graph,'genres_subgraph_%d.png'%(index), pos)
