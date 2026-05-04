import streamlit as st

def render_design_rationale():
    st.header("Design Rationale")

    st.markdown("""
    This project uses EM-DAT disaster data to explore disaster frequency and human impact across time,
    geography, and disaster classification levels.

    **Multiple Views:**  
    The dashboard uses line charts, boxplots, bar charts, maps, and summary cards to provide different
    perspectives on the same dataset.

    **Filtering:**  
    Sidebar filters allow users to focus on specific regions, disaster categories, and time periods.

    **Aggregation and Derived Attributes:**  
    The project derives decade, human impact, deaths per event, affected population per event, and
    human impact per event to support higher-level analysis.

    **Hierarchical Drilldown:**  
    EM-DAT disaster categories are hierarchical, moving from Disaster Group to Subgroup, Type, and Subtype.
    The classification selector allows users to analyze the data at different levels of granularity.

    **Time-Series Visualization:**  
    Line charts are used to show whether disasters are becoming more frequent over time.

    **Distribution Visualization:**  
    Boxplots are used to compare how deaths and affected population are distributed across disaster categories.

    **Spatial Visualization:**  
    The map view shows how human impact varies geographically.

    **Log Scale:**  
    Disaster impact data is highly skewed, so log scale options help reveal patterns that may be hidden by
    extreme outliers.

    **Design Choices:**  
    The dashboard prioritizes position and length for quantitative comparisons, uses color primarily for
    category distinction, and uses filtering and top-N controls to reduce clutter.
    """)