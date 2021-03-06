from serialize import save
from graph import produce_graph as pg
import networkx as nx
from functools import reduce

related_artists_map = save.load('related_artists_2017-09-20 00:27:32.909349')
G = pg.generate_graph(related_artists_map)

# Get the connected components
graphs = list(nx.connected_component_subgraphs(G))
print("Connected components: ",len(graphs))

# # plot one of the graphs
pg.plot_graph(graphs[1], 'a_connected_component.png')

# Eccentricity of a sample node:
print('Eccentricity of Arcade fire node:',nx.eccentricity(graphs[0],'Arcade Fire'))

# Get a node and all it's neighbors
H = nx.ego_graph(G,'Arcade Fire',radius=1)
pg.plot_graph(H, 'ego_graph.png')

# Get the shortest path between two nodes
path = nx.shortest_path(G,source='Arcade Fire',target='Kendrick Lamar')
print('Path from Arcade Fire to Kendrick Lamar:')
print(reduce((lambda u,v:u+' -> '+v),path))

# Get shortest path lengths to all other nodes
lengths = nx.single_source_shortest_path_length(G,'Arcade Fire')
print('Longest path from Arcade Fire to any other node:')
max_path_length = max(lengths.values())
print(max_path_length)
print('Dst nodes of max length from Arcade Fire:')
print([k for k,v in lengths.items() if v == max_path_length])

# Plot paths from Arcade Fire to Kendrick Lamar
GG = nx.relabel_nodes(G,{'Joey Bada$$':'Joey Badass'})
paths = list(nx.all_simple_paths(GG,source='Arcade Fire',target='Kendrick Lamar',cutoff=6))
vertices_in_path = [v for path in paths for v in path]
pg.plot_graph(GG.subgraph(vertices_in_path),'arcade_fire_to_kendrick.png')
