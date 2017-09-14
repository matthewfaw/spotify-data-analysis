import networkx as nx
from .produce_graph import get_connected_components

'''
Returns genres, artists
'''
def decompose(G):
    return nx.bipartite.sets(G)

'''
Returns a list of genre clusters, where
each cluster is a list of genrenames
'''
def get_genre_clusters(G):
    clusters = []
    for SG in get_connected_components(G):
        genres, _ = decompose(SG)
        clusters.append(genres)
    return clusters

'''
Returns a map: GenreName -> degree of genre node
'''
def get_genre_degrees(G):
    genres, _ = decompose(G)
    degrees = G.degree(genres)
    return degrees
    
