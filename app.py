import os
import streamlit as st
import numpy as np

# Custom imports 
from multipage import MultiPage
from pages import player_stats, new_page


# Create an instance of the app 
app = MultiPage()


# Add all your application here
app.add_page("Player stats", player_stats.app)
app.add_page("New page", new_page.app)


# The main app
app.run()