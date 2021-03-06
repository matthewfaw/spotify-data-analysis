# Spotify Data Analysis

I've started logging all my Spotify listening history in mongo.  This is the repo I use
to analyze my listening patterns so that I can have a more diverse music listening 
experience :)

## Installation

Install python requirements by running `pip3 install -r <Project Root>/requirements.txt`

## The analysis I've set up so far:

- Get the genres of all artists I listen to on Spotify
- Get the related artists for the artists I listen to
- Generate a related artists graph, and use NetworkX/Matplotlib to visualize and understand this graph

### I can view different connected components in my graph.  Here's one of them:
![One of the connected components in the graph](https://github.com/matthewfaw/spotify-data-analysis/blob/master/plots/a_connected_component.png)

### I can view Ego Graphs for the Artists I listen to.  Here's Arcade Fire's radius=1 ego graph:
![Arcade Fire's Ego Graph](https://github.com/matthewfaw/spotify-data-analysis/blob/master/plots/ego_graph.png)

### Here are all paths of length at most 6 between Arcade Fire and Kendrick Lamar:
This plot is particularly cool because it shows two tightly-connected clusters -- Indie music and Rap music.  These clusters are being connected by artists that fall somewhat between the two: Gorillaz and James Blake, for example.
![All paths of length at most 6 between Arcade Fire and Kendrick Lamar](https://github.com/matthewfaw/spotify-data-analysis/blob/master/plots/arcade_fire_to_kendrick.png)

### I can also look at the connected component (bipartite) subgraphs of Genre graphs
Spotify typically says an artist falls under a handfull of genres.  By filtering the Genre graph by threshold
totalNumberOfListens for artists, we can start to view somewhat meaningful genre groupings:
![Indie rock subgraph](https://github.com/matthewfaw/spotify-data-analysis/blob/master/plots/genres_subgraph_0.png)
![Rap subgraph](https://github.com/matthewfaw/spotify-data-analysis/blob/master/plots/genres_subgraph_1.png)

### Minimum total number of listens vs number of genre clusters
![listens_vs_clusters](https://github.com/matthewfaw/spotify-data-analysis/blob/master/plots/num_listens_vs_num_genre_clusters.png)
