import streamlit as st
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
def load_data_yearly():
    penguin_file = st.file_uploader("Select Your Local CSV file")
    if penguin_file is None:
        st.stop()
    year_data = pd.read_csv(penguin_file)
    return year_data

raw_data = load_data_yearly()

raw_data["ChargerID"] = raw_data["ChargerID"].map(lambda x: f"ST{x}")
raw_data["UserID"] = raw_data["UserID"].map(lambda x: f"EV{x}")

G = nx.from_pandas_edgelist(raw_data, "UserID", 'ChargerID', ['Demand', 'Duration'])
loc_dict = {}
for charger_id,loc in zip(raw_data["ChargerID"],raw_data["Location"]):
    loc_dict[charger_id] = loc
# Set the locations as node attributes
nx.set_node_attributes(G, loc_dict, 'location')

charg_company_dict = {}
for charger_id,chc in zip(raw_data["ChargerID"],raw_data["ChargerCompany"]):
    charg_company_dict[charger_id] = chc
# Set the charging company as node attributes
nx.set_node_attributes(G, charg_company_dict, 'charging_company')

ChargerType_dict = {}
for charger_id,ct in zip(raw_data["ChargerID"],raw_data["ChargerType"]):
    ChargerType_dict[charger_id] = ct
# Set the charging type as node attributes
nx.set_node_attributes(G, ChargerType_dict, 'charger_type')

number_of_conections = {}
for adjacencies,node in zip(G.adjacency(),G.nodes()):
    number_of_conections[node] = len(adjacencies[1])
# Set the number of connections as node attributes
nx.set_node_attributes(G, number_of_conections, 'number_of_connections')

node_attributes = list(G.nodes(data=True))
pos = nx.spring_layout(G)

# Set the positions as node attributes
nx.set_node_attributes(G, pos, 'pos')
# drawing part
edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = G.nodes[edge[0]]['pos']
    x1, y1 = G.nodes[edge[1]]['pos']
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

node_x = []
node_y = []
for node in G.nodes():
    x, y = G.nodes[node]['pos']
    node_x.append(x)
    node_y.append(y)

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        # colorscale options
        #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
        #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
        #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
        colorscale='YlGnBu',
        reversescale=True,
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line_width=2))
# defining shape of nodes
shape_nodes = []
for node in list(G.nodes):
    if node.startswith("ST"):
        shape_nodes.append("diamond")
    if node.startswith("EV"):
        shape_nodes.append("circle")

node_adjacencies = []
node_text = []
for adjacencies,node in zip(G.adjacency(),G.nodes()):
    node_adjacencies.append(len(adjacencies[1]))
    node_text.append(f'{node}: '+str(len(adjacencies[1])))

node_trace.marker.color = node_adjacencies
node_trace.marker.symbol = shape_nodes
node_trace.text = node_attributes

fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='<br>Network graph made with Python',
                titlefont_size=16,
                showlegend=False,
                hovermode='x',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="Python code: <a href='https://plotly.com/python/network-graphs/'> https://plotly.com/python/network-graphs/</a>",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )

st.plotly_chart(fig)