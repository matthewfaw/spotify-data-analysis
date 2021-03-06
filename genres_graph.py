from serialize import save
import networkx as nx
import operator
from graph.produce_graph import create_genre_graph, get_connected_components, plot_graph
from graph.genre_graph_utils import decompose, get_genre_clusters, get_genre_degrees
import matplotlib.pyplot as plt

# load up data
genres_map = save.load('genres_2017-09-20 00:27:32.910281')
num_listens = save.load('total_number_of_listens_2017-09-20 00:27:32.914297')
listening_history = save.load('listening_history_2017-09-20 00:27:32.910782')

# Clean up some entries that throw errors
genres_map['Joey Badass'] = genres_map.pop('Joey Bada$$')
num_listens['Joey Badass'] = num_listens.pop('Joey Bada$$')
listening_history['Joey Badass'] = listening_history.pop('Joey Bada$$')

# Create the graph
# B = create_genre_graph(genres_map, num_listens, 100)
B = create_genre_graph(genres_map, listening_history, num_listens, 100)

# Get number of connected components
# The 0-labeled nodes can be thought of as genre clusters
graphs = get_connected_components(B)
print('Number of connected component subgraphs (genre clusters): ',len(graphs))

# Get the genre clusters for each connected component subgraph
for index, cluster in enumerate(get_genre_clusters(B)):
    if len(cluster) > 0:
        print("Genre cluster %d:"%(index))
        print(cluster)

# Get degrees:
print('Degrees of all genres: ')
degrees = get_genre_degrees(B)
print(sorted(degrees.items(), key=operator.itemgetter(1)))
max_degree_val = max(degrees.values()) 
print('Max degree: ',max_degree_val)

# print all the subgraphs
counter = 0
for graph in graphs:
    if graph.number_of_edges() > 0:
        genres, artists = decompose(graph)
        pos = {}
        pos.update((node,(1,index)) for index, node in enumerate(genres))
        pos.update((node,(2,index)) for index, node in enumerate(artists))
        plot_graph(graph, 'genres_subgraph_%d.png'%(counter),pos)
        counter += 1;


# plot # genre clusters vs sigma
sigmas = range(1,100)
genre_cluster_counts = []
for sigma in sigmas:
    G = create_genre_graph(genres_map,num_listens,sigma)
    cluster_count = 0
    for graph in get_connected_components(G):
        if graph.number_of_edges() > 0:
            cluster_count += len(get_genre_clusters(graph))
    genre_cluster_counts.append(cluster_count)
plt.clf()
plt.plot(sigmas, genre_cluster_counts)
plt.xlabel('Minimum number of listens')
plt.ylabel('# Genre Clusters')
plt.savefig('plots/num_listens_vs_num_genre_clusters.png')
