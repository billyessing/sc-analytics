from select import select
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import random
import altair as alt
import plotly.express as px


# select players
@st.cache
def get_data():
  return pd.read_excel('data/test.xlsx')


def bar_chart(stats):
  avgs = []
  avgs_flat = []
  for player in selected_players:  
    avgs.append(pd.DataFrame({
      'player': [player] * len(stats),
      'stat': stats,
      'scores': list(main_df[main_df['Player name'] == player][stats].mean())
    }))

    avgs_flat.append([player] + list(main_df[main_df['Player name'] == player][stats].mean()))
  
  st.dataframe(pd.DataFrame(avgs_flat, columns=['Player name'] + stats))

  if avgs:
    avgs_df = pd.concat(avgs)
    fig, ax = plt.subplots()
    sns.barplot(x='stat', hue='player', y='scores', data=avgs_df)
    st.pyplot(fig)



# define static lists
key_stats = [
  'Pts', 'Mins', 'Base', 'Create', 'Evade'
]

sc_stats = [
  'TR', 'TS', 'LT', 'GO', 'MG', 'FG', 'MF', 'TA', 
  'MT', 'TB', 'FD', 'OL', 'IO', 'LB', 'LA', 'FT', 'KB', 
  'H8', 'HU', 'HG', 'IT', 'KD', 'PC', 'ER', 'SS'
]


# get data
main_df = get_data()
players = sorted(main_df['Player name'].unique())


# variable inputs
selected_players = st.sidebar.multiselect('Select players:', players, ['Nicholas Hynes']) # select players

container = st.sidebar.container()
all = st.sidebar.checkbox('Select all')
selected_stats = container.multiselect('Select stats:', sc_stats, sc_stats) if all else container.multiselect('Select stats:', sc_stats, ['TR', 'TS', 'LT', 'TA', 'MT']) # select stats


# get filtered dataset
main_df_selection_df = main_df[main_df['Player name'].isin(selected_players)]

# outputs
st.header('NRL SuperCoach Stats')

st.markdown('### Full dataset')
st.dataframe(main_df_selection_df)

st.write('### Key stats')
bar_chart(key_stats)

st.write('### Selected stats')
bar_chart(selected_stats)
