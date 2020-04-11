import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import cufflinks as cf

csv_file = os.path.join(os.path.dirname(__file__), "../data/hotel_bookings.csv")
df = pd.read_csv(csv_file)
