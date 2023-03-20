import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import streamlit as st


def main():
    # load data sets
    df_edges = pd.read_csv('data/graph_edges.csv')
    df_1721 = pd.read_csv('data/voting_1721.csv')

    threshold = st.slider(label='Specify minimum similarity threshold to display in graph',
                          min_value=0.0,
                          max_value=1.0,
                          value=0.8,
                          step=0.01)

    # filter out low or negative correlations
    df_edges_filtered = df_edges.loc[(df_edges['correlation'] > threshold) & (df_edges['id1'] != df_edges['id2'])]

    def create_graph_from_df(df):

        # create list of nodes

        A = list(df["id1"].unique())
        B = list(df["id2"].unique())
        node_list = set(A + B)

        # create graph

        G = nx.Graph()

        for i in node_list:
            G.add_node(i)

        for i, j in df_edges_filtered.iterrows():
            G.add_edges_from([(j["id1"], j["id2"])])

        pos = nx.spring_layout(G, k=0.5, iterations=50)

        for n, p in pos.items():
            G.nodes[n]['pos'] = p

        # create plotly network graph

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
                color=[],
                size=10,
                line_width=2))

        # color node points
        color_mapper = {'': 'white', 'AfD': 'lightblue', 'CDU': 'black', 'CSU': 'darkblue', 'FDP': 'yellow',
                        'GRÜNE': 'green', 'Linke': 'magenta', 'SPD': 'red'}

        node_color = []
        node_text = []
        for node in node_list:
            party = df_1721.loc[df_1721['id_de_parliament'] == node, 'party_text'].values[0]
            lname = df_1721.loc[df_1721['id_de_parliament'] == node, 'lastname'].values[0]
            fname = df_1721.loc[df_1721['id_de_parliament'] == node, 'firstname'].values[0]
            node_text.append(fname + ' ' + lname)
            try:
                node_color.append(color_mapper[party])
            except:
                node_color.append('white')

        node_trace.marker.color = node_color
        node_trace.text = node_text

        # create legend

        data = [edge_trace, node_trace]

        for party, color in color_mapper.items():
            data.append(go.Scatter(x=[None],
                                   y=[None],
                                   mode="markers",
                                   name=party,
                                   marker=dict(size=7, color=color, symbol='circle')))
        return data

    def create_plot_from_graph(graph):

        # visualize graph
        fig = go.Figure(data=graph,
                        layout=go.Layout(
                            title='<br>Network graph of voting similarity among members of german parliament',
                            titlefont_size=16,
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20, l=5, r=5, t=40),
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                        )

        fig.update_layout(showlegend=True)
        return fig

    network = create_graph_from_df(df_edges_filtered)
    plot = create_plot_from_graph(network)
    st.plotly_chart(plot)


if __name__ == "__main__":
    main()
