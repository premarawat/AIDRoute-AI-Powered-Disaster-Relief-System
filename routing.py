import networkx as nx

def add_combined_cost(G, alpha=0.7, beta=0.3):
    for u, v, data in G.edges(data=True):
        data['combined_cost'] = alpha * data.get('length', 1.0) + beta * data.get('risk_score', 0.0)
    return G

def district_to_node(district_name, node_to_district, G):
    # Pick the first node in the district for routing simplicity
    for node, district in node_to_district.items():
        if district == district_name:
            return node
    return None

def shortest_safest_route(G, source_node, target_node):
    try:
        length, path = nx.single_source_dijkstra(G, source=source_node, target=target_node, weight='combined_cost')
        return length, path
    except Exception as e:
        return None, []
