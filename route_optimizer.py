import pandas as pd
import networkx as nx

print("Loading roads data...")
roads = pd.read_csv('roads.csv')

print("Building graph...")
G = nx.DiGraph()

# Add edges to graph
for _, row in roads.iterrows():
    G.add_edge(row['u'], row['v'], length=row['length'])

def shortest_route(source, target):
    try:
        length, path = nx.single_source_dijkstra(G, source=source, target=target, weight='length')
        return length, path
    except nx.NetworkXNoPath:
        return None, []

# Example usage (replace with actual node ids from locations.csv)
source_node = roads['u'].iloc[0]
target_node = roads['v'].iloc[-1]

length, path = shortest_route(source_node, target_node)
print(f"Shortest route length: {length}")
print(f"Route path: {path}")
