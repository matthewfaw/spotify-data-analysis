from serialize import save
from graph import produce_graph as pg
import networkx as nx

genres_map = save.load('genres_2017-09-11 01:33:42.733512')
genres_map['Joey Badass'] = genres_map.pop('Joey Bada$$')

all_genres = set([genre for genres in genres_map.values() for genre in genres])
print('Number of genres: ',len(all_genres))
all_artists = genres_map.keys()
print('Number of artists: ', len(all_artists))
connections = [(genre,artist) for genre,artists in genres_map.items() for artist in artists]
print('Number of connections: ', len(connections))

# Create a bipartite graph
B = nx.Graph()
B.add_nodes_from(all_genres, bipartite=0)
B.add_nodes_from(all_artists, bipartite=1)
B.add_edges_from(connections)

# Get number of connected components
graphs = list(nx.connected_component_subgraphs(B))
print('Number of connected component subgraphs: ',len(graphs))

# Get the genres in the first connected component subgraph
l,r = nx.bipartite.sets(graphs[0])
print('Number of genres in ccs1: ',len(l))
print(l)

pos = {}
pos.update((node,(1,index)) for index, node in enumerate(all_genres))
pos.update((node,(2,index)) for index, node in enumerate(all_artists))

for index, graph in enumerate(graphs):
    pg.plot_graph(graph,'genres_subgraph_%d.png'%(index), pos)