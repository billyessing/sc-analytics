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


def app():
  # select players
  @st.cache
  def get_data():
    df = pd.read_excel('data/season_stats_cleaned_ALL.xlsx')
    df[['Jersey', 'Bye', '3Rd Avg Mins', 'BasePow PPM']] = df[['Jersey', 'Bye', '3Rd Avg Mins', 'BasePow PPM']].astype(str)
    df['HG'] = pd.to_numeric(df['HG'], errors='coerce')
    return df


  def bar_chart(col, stats):
    avgs = []
    avgs_flat = []
    for player in selected_players:  
      avgs.append(pd.DataFrame({
        'player': [player] * len(stats),
        'stat': stats,
        'scores': list(main_df[(main_df['Player name'] == player) & (main_df['Year'].isin(selected_years))][stats].mean())
      }))

      avgs_flat.append([player] + list(main_df[(main_df['Player name'] == player) & (main_df['Year'].isin(selected_years))][stats].mean()))
    
    col.dataframe(pd.DataFrame(avgs_flat, columns=['Player name'] + stats))

    if avgs:
      avgs_df = pd.concat(avgs)
      fig, ax = plt.subplots()
      sns.barplot(x='stat', hue='player', y='scores', data=avgs_df)
      col.pyplot(fig)



  # define static lists
  key_stats = [
    'Pts', 'Mins', 'Base', 'Create', 'Evade', 'Neg'
  ]

  sc_stats = [
    'TR', 'TS', 'LT', 'GO', 'MG', 'FG', 'MF', 'TA', 'MT', 
    'TB', 'FD', 'OL', 'IO', 'LB', 'LA', 'FT', 'KB', 'H8', 
    'HU', 'HG', 'IT', 'KD', 'PC', 'ER', 'SS'
  ]


  # get data
  main_df = get_data()
  years = sorted(main_df['Year'].unique(), reverse=True)
  players = sorted(main_df['Player name'].unique().astype(str))


  # variable inputs
  container = st.sidebar.container()
  all_years = st.sidebar.checkbox('Select all', key='all_years')
  selected_years = container.multiselect('Select years:', years, years) if all_years else container.multiselect('Select years:', years, [2021]) # select years

  selected_players = st.sidebar.multiselect('Select players:', players, ['Nicholas Hynes']) # select players

  container = st.sidebar.container()
  all_stats = st.sidebar.checkbox('Select all', key='all_stats')
  selected_stats = container.multiselect('Select stats:', sc_stats, sc_stats) if all_stats else container.multiselect('Select stats:', sc_stats, ['TR', 'TS', 'LT', 'TA', 'MT', 'HU', 'OL']) # select stats


  # get filtered dataset
  main_df_selection_df = main_df[(main_df['Year'].isin(selected_years)) & (main_df['Player name'].isin(selected_players))]

  # outputs

  st.header('NRL SuperCoach Stats')


  c1, c2 = st.columns((1,1))

  c1.write('### Key stats')
  bar_chart(c1, key_stats)

  if selected_stats:
    c2.write('### Selected stats')
    bar_chart(c2, selected_stats)


  st.write('')
  st.write('')

  st.markdown('### Full dataset')
  st.dataframe(main_df_selection_df)