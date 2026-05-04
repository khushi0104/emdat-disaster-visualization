import streamlit as st
import warnings

from tabs.design import render_design_rationale
from tabs.dashboard import render_dashboard
from tabs.insights import render_insights
from tabs.explorer import render_data_explorer
from tabs.compare import render_compare_charts

from data import load_data
from filters import sidebar_filters
from trace_chart_error import traced_plotly_chart


warnings.filterwarnings("ignore", message=".*keyword arguments have been deprecated.*")

st.set_page_config(page_title="Disaster Exploration Tool", layout="wide")
st.title("Disaster Visualization Explorer")


df = load_data()
filtered_df, classification_level = sidebar_filters(df)
st.plotly_chart = traced_plotly_chart


dashboard_tab, explorer_tab, compare_tab, insights_tab, design_tab = st.tabs(
    ["Dashboard", 
     "Data Explorer", 
     "Compare", 
     "Key Insights", 
     "Design Rationale"])

with dashboard_tab: render_dashboard(filtered_df, classification_level)
with insights_tab: render_insights(filtered_df, classification_level)
with explorer_tab: render_data_explorer(filtered_df)
with compare_tab: render_compare_charts(filtered_df)
with design_tab: render_design_rationale()