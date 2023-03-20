import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import streamlit as st
from sklearn.decomposition import PCA

def main():
    df_features = pd.read_csv('data/cleaned_features.csv')

    df = pd.read_csv('data/voting_1721.csv')

    names = []
    parties = []
    for index in df_features['id_de_parliament']:
        party = df.loc[df['id_de_parliament'] == index, 'party_text'].values[0]
        lname = df.loc[df['id_de_parliament'] == index, 'lastname'].values[0]
        fname = df.loc[df['id_de_parliament'] == index, 'firstname'].values[0]
        names.append(fname + ' ' + lname)
        parties.append(party)


    pca3d = PCA(n_components=3)
    comps3d = pca3d.fit_transform(df_features.iloc[:, 1:])

    df_3dpca = pd.DataFrame()
    df_3dpca['id_de_parliament'] = df_features['id_de_parliament']
    df_3dpca['pc1'] = comps3d[:, 0]
    df_3dpca['pc2'] = comps3d[:, 1]
    df_3dpca['pc3'] = comps3d[:, 2]
    df_3dpca['name'] = names
    df_3dpca['party'] = parties

    color_mapper = {'': 'white', 'AfD': 'lightblue', 'CDU': 'black', 'CSU': 'darkblue', 'FDP': 'yellow',
                    'GRÜNE': 'green', 'Linke': 'magenta', 'SPD': 'red'}

    fig = px.scatter_3d(df_3dpca, x='pc1', y='pc2', z='pc3',
                        color='party', color_discrete_map=color_mapper, hover_data=['name'],)

    st.title('Similary of German Members of Parliament by Voting Behavior')
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()