# AIDRoute – AI-Powered Disaster Relief Routing & Priority Zones

AIDRoute is a data-driven disaster relief planning system designed to help NGOs
and authorities generate **risk-aware relief routes** and **priority zones**
using geospatial data, Bayesian statistics, and interactive visualizations.

The project combines **OpenStreetMap road networks**, **Points of Interest (POIs)**,
and **Bayesian inference** to support informed, transparent, and data-backed
decision-making during disaster response.

---

## 🚀 Key Features

- Download and process road networks using **OSMnx**
- Extract nodes, edges, and distances from OpenStreetMap data
- Integrate **Points of Interest (POIs)** relevant to disaster relief
- Apply **Bayesian inference** to estimate disaster risk probabilities
- Generate **risk-aware optimal routes** for relief operations
- Identify and prioritize **high-risk zones** with statistical confidence
- Interactive **Streamlit dashboard** with Folium maps
- Modular and extensible Python architecture

---

## 🧠 System Architecture

The system follows a modular pipeline:

1. **Data Extraction**
   - Road networks from OpenStreetMap (OSMnx)
   - POIs filtered and stored as structured datasets

2. **Risk & Statistical Modeling**
   - Bayesian models estimate disaster impact probabilities
   - Risk scores generated per zone using posterior distributions

3. **Routing & Optimization**
   - Routes computed using weighted graphs
   - Risk scores incorporated into routing decisions

4. **Visualization & Dashboard**
   - Interactive maps using Folium
   - Streamlit UI for user inputs and outputs

---
```
AIDRoute/
│
├── app.py # Streamlit application entry point
├── add_pois.py # POI extraction and integration
├── data_processing.py # Road network & dataset processing
├── generate_datasets.py # CSV generation from OSM data
├── routing.py # Core routing logic
├── route_optimizer.py # Risk-aware route optimization
├── risk_model.py # Risk score computation
├── bayesian_model.py # Bayesian inference model (PyMC)
├── bayesian_risk.py # Bayesian risk estimation logic
├── visualize_map.py # Folium map generation
├── utils.py # Helper utilities
│
├── locations.csv # Location data
├── pois.csv # Points of Interest
├── bayesian_risk_summary.csv # Bayesian inference outputs
│
├── requirements.txt # Python dependencies
└── README.md
```

---

## 🛠️ Technologies Used

- **Python**
- **OpenStreetMap**
- **GeoPandas**
- **Bayesian Inference**
- **NetworkX**
- **Folium & Streamlit-Folium**
- **Streamlit**
- **Pandas / NumPy**
---

👤 Author
Prema Rawat

