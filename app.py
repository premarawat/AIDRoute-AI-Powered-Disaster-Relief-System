import streamlit as st
import osmnx as ox
import networkx as nx
from geopy.distance import geodesic
import folium
from streamlit_folium import st_folium
import pandas as pd
import numpy as np

st.set_page_config(layout="wide", page_title="AIDRoute Uttarakhand Dashboard")

st.title("AIDRoute - AI & Statistics based Disaster Relief Routing (Uttarakhand)")

# ----- Load Graph and Data -----

@st.cache_data(show_spinner=True)
def load_road_network():
    place = "Uttarakhand, India"
    G = ox.graph_from_place(place, network_type='drive')

    for u, v, k, data in G.edges(keys=True, data=True):
        if 'length' not in data:
            if 'geometry' in data:
                data['length'] = data['geometry'].length
            else:
                point_u = (G.nodes[u]['y'], G.nodes[u]['x'])
                point_v = (G.nodes[v]['y'], G.nodes[v]['x'])
                data['length'] = geodesic(point_u, point_v).meters
    return G

@st.cache_data(show_spinner=False)
def get_district_centroids():
    # Centroids for Uttarakhand districts (lat, lon)
    return {
        "Dehradun": (30.3165, 78.0322),
        "Haridwar": (29.9457, 78.1642),
        "Nainital": (29.3919, 79.4542),
        "Udham Singh Nagar": (28.9754, 79.3957),
        "Almora": (29.5987, 79.6581),
        "Pithoragarh": (29.5588, 80.2200),
        "Rudraprayag": (30.2833, 79.0167),
        "Tehri Garhwal": (30.3343, 78.4577),
        "Champawat": (29.3099, 80.1351),
        "Chamoli": (30.5079, 79.4083),
        "Bageshwar": (29.8591, 79.8862),
    }

# Dummy demand data per district
def get_demand_data():
    districts = list(get_district_centroids().keys())
    np.random.seed(42)
    demand = np.random.randint(50, 300, len(districts))
    df = pd.DataFrame({"District": districts, "Demand": demand})
    return df.sort_values(by="Demand", ascending=False)

# Dummy hazard data per district (hazard and severity)
def get_hazard_data():
    districts = list(get_district_centroids().keys())
    hazards = [
        "Flood Risk", "Landslide Risk", "Forest Fire", "Earthquake", "Cold Wave", "Heavy Rainfall"
    ]
    np.random.seed(101)
    data = []
    for d in districts:
        hazard = np.random.choice(hazards)
        severity = np.random.choice(["Low", "Medium", "High", "Very High"], p=[0.3, 0.4, 0.2, 0.1])
        data.append({"District": d, "Hazard": hazard, "Severity": severity})
    df = pd.DataFrame(data)
    return df

# Priority zones by combined score (demand x hazard severity factor)
def get_priority_zones(demand_df, hazard_df):
    severity_map = {"Low": 1, "Medium": 2, "High": 3, "Very High": 4}
    merged = demand_df.merge(hazard_df, on="District")
    merged["Severity_Score"] = merged["Severity"].map(severity_map)
    merged["Priority_Score"] = merged["Demand"] * merged["Severity_Score"]
    merged_sorted = merged.sort_values(by="Priority_Score", ascending=False)
    return merged_sorted

# --- Helper for Risk (same as before)
def compute_risk_score(u, v):
    length = G.edges[u, v, 0]['length']
    max_length = 10000
    risk = min(length / max_length, 1.0)
    return risk

# ----- Main app -----

G = load_road_network()
district_centroids = get_district_centroids()

# Sidebar menu for views
view = st.sidebar.selectbox("Select Dashboard View", [
    "Route Planner",
    "Demand Chart",
    "Hazards Summary",
    "Priority Zones",
    "Core Logic"
])

# Show relevant content by selected view
if view == "Route Planner":
    st.header("Route Planner")
    districts = list(district_centroids.keys())
    source_district = st.selectbox("Select Source District", districts)
    dest_district = st.selectbox("Select Destination District", districts, index=1)

    source_node = ox.nearest_nodes(G, district_centroids[source_district][1], district_centroids[source_district][0])
    dest_node = ox.nearest_nodes(G, district_centroids[dest_district][1], district_centroids[dest_district][0])

    alpha = st.slider("Alpha (Distance weight)", 0.0, 1.0, 0.7, 0.05)
    beta = st.slider("Beta (Risk weight)", 0.0, 1.0, 0.3, 0.05)

    st.markdown("""
    **Cost formula:**

    $$Cost = \\alpha \\times Distance + \\beta \\times Risk$$
    """)

    for u, v, k, data in G.edges(keys=True, data=True):
        length = data['length']
        risk = compute_risk_score(u, v)
        data['cost'] = alpha * length + beta * (risk * 10000)

    try:
        path = nx.shortest_path(G, source=source_node, target=dest_node, weight='cost')
        path_length = sum(G.edges[u, v, 0]['length'] for u, v in zip(path[:-1], path[1:]))
        path_cost = sum(G.edges[u, v, 0]['cost'] for u, v in zip(path[:-1], path[1:]))
    except Exception as e:
        st.error(f"Routing failed: {e}")
        path = []
        path_length = None
        path_cost = None

    if path_length is not None:
        st.markdown(f"### Route from **{source_district}** to **{dest_district}**")
        st.markdown(f"- Distance (meters): {path_length:.2f}")
        st.markdown(f"- Combined Cost: {path_cost:.2f} (weighted sum)")
    else:
        st.info("No route found for selected districts.")

    if path:
        latlons = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in path]
        avg_lat = sum(lat for lat, lon in latlons) / len(latlons)
        avg_lon = sum(lon for lat, lon in latlons) / len(latlons)

        m = folium.Map(location=[avg_lat, avg_lon], zoom_start=8)
        folium.PolyLine(latlons, color='blue', weight=5, opacity=0.8).add_to(m)
        folium.Marker(latlons[0], popup=f"Source: {source_district}", icon=folium.Icon(color='green')).add_to(m)
        folium.Marker(latlons[-1], popup=f"Destination: {dest_district}", icon=folium.Icon(color='red')).add_to(m)
        st_folium(m, width=900, height=600)

elif view == "Demand Chart":
    st.header("Demand by District")
    demand_df = get_demand_data()
    st.bar_chart(data=demand_df.set_index("District")["Demand"])

elif view == "Hazards Summary":
    st.header("Hazards by District")
    hazard_df = get_hazard_data()
    st.dataframe(hazard_df)

elif view == "Priority Zones":
    st.header("Top Priority Zones")
    demand_df = get_demand_data()
    hazard_df = get_hazard_data()
    priority_df = get_priority_zones(demand_df, hazard_df)
    st.dataframe(priority_df[["District", "Demand", "Hazard", "Severity", "Priority_Score"]])

elif view == "Core Logic":
    st.header("Core Logic (Cost Formula)")
    st.markdown(f"""
    $$\\text{{Cost}} = \\alpha \\times \\text{{Distance}} + \\beta \\times \\text{{Risk}}$$

    - \\( \\alpha \\) = weight for shortest distance (slider in route planner)
    - \\( \\beta \\) = weight for safest route (risk avoidance)

    **Why?**

    - To balance fastest route and safest route based on hazard risk.
    - Risk is a dummy score proportional to road segment length here (for demo).
    - Tunable sliders help NGO adjust based on priorities (speed vs safety).
    """)

