import streamlit as st
import plotly.express as px 
import pandas as pd

def render_compare_charts(filtered_df):
    st.header("Compare Disaster Types")
    st.write(
        "Select two disaster types to compare trends and impact side-by-side."
    )

    compare_df = filtered_df.copy()

    # Make sure numeric columns are numeric
    numeric_cols = [
        "Total Deaths",
        "Total Affected",
        "No. Affected",
        "No. Injured",
        "No. Homeless"
    ]

    for col in numeric_cols:
        if col in compare_df.columns:
            compare_df[col] = pd.to_numeric(compare_df[col], errors="coerce").fillna(0)

    # Create Total Affected if it does not already exist
    if "Total Affected" not in compare_df.columns:
        affected_parts = [
            col for col in ["No. Affected", "No. Injured", "No. Homeless"]
            if col in compare_df.columns
        ]

        if affected_parts:
            compare_df["Total Affected"] = compare_df[affected_parts].sum(axis=1)
        else:
            compare_df["Total Affected"] = 0

    # Dropdown options
    disaster_types = sorted(compare_df["Disaster Type"].dropna().unique())

    col1, col2 = st.columns(2)

    with col1:
        type_1 = st.selectbox(
            "Choose first disaster type",
            disaster_types,
            index=disaster_types.index("Flood") if "Flood" in disaster_types else 0
        )

    with col2:
        default_index = disaster_types.index("Storm") if "Storm" in disaster_types else min(1, len(disaster_types) - 1)

        type_2 = st.selectbox(
            "Choose second disaster type",
            disaster_types,
            index=default_index
        )

    selected_types = [type_1, type_2]

    comparison_df = compare_df[compare_df["Disaster Type"].isin(selected_types)].copy()

    if comparison_df.empty:
        st.warning("No data available for the selected disaster types.")
    else:
        st.subheader(f"{type_1} vs. {type_2}")

        # Summary metrics
        summary = (
            comparison_df
            .groupby("Disaster Type")
            .agg(
                Events=("Disaster Type", "count"),
                Total_Deaths=("Total Deaths", "sum"),
                Total_Affected=("Total Affected", "sum")
            )
            .reset_index()
        )

        summary["Avg Deaths per Event"] = summary["Total_Deaths"] / summary["Events"]
        summary["Avg Affected per Event"] = summary["Total_Affected"] / summary["Events"]

        metric_col1, metric_col2 = st.columns(2)

        for i, row in summary.iterrows():
            with metric_col1 if i == 0 else metric_col2:
                st.markdown(f"### {row['Disaster Type']}")
                st.metric("Total Events", f"{row['Events']:,.0f}")
                st.metric("Total Deaths", f"{row['Total_Deaths']:,.0f}")
                st.metric("Total Affected", f"{row['Total_Affected']:,.0f}")
                st.metric("Avg Deaths per Event", f"{row['Avg Deaths per Event']:,.1f}")
                st.metric("Avg Affected per Event", f"{row['Avg Affected per Event']:,.1f}")

        st.divider()

        # Events over time
        events_over_time = (
            comparison_df
            .groupby(["Start Year", "Disaster Type"])
            .size()
            .reset_index(name="Number of Events")
        )

        fig_events = px.line(
            events_over_time,
            x="Start Year",
            y="Number of Events",
            color="Disaster Type",
            markers=True,
            title="Events Over Time"
        )

        fig_events.update_layout(
            xaxis_title="Year",
            yaxis_title="Number of Events",
            legend_title="Disaster Type"
        )

        st.plotly_chart(fig_events)

        # Total deaths over time
        deaths_over_time = (
            comparison_df
            .groupby(["Start Year", "Disaster Type"], as_index=False)["Total Deaths"]
            .sum()
        )

        fig_deaths = px.line(
            deaths_over_time,
            x="Start Year",
            y="Total Deaths",
            color="Disaster Type",
            markers=True,
            title="Total Deaths Over Time"
        )

        fig_deaths.update_layout(
            xaxis_title="Year",
            yaxis_title="Total Deaths",
            legend_title="Disaster Type"
        )

        st.plotly_chart(fig_deaths)

        # Total affected over time
        affected_over_time = (
            comparison_df
            .groupby(["Start Year", "Disaster Type"], as_index=False)["Total Affected"]
            .sum()
        )

        fig_affected = px.line(
            affected_over_time,
            x="Start Year",
            y="Total Affected",
            color="Disaster Type",
            markers=True,
            title="Total Affected Over Time"
        )

        fig_affected.update_layout(
            xaxis_title="Year",
            yaxis_title="Total Affected",
            legend_title="Disaster Type"
        )

        st.plotly_chart(fig_affected)

        # Average impact per event
        avg_impact = summary.melt(
            id_vars="Disaster Type",
            value_vars=["Avg Deaths per Event", "Avg Affected per Event"],
            var_name="Impact Metric",
            value_name="Average Impact"
        )

        fig_avg = px.bar(
            avg_impact,
            x="Disaster Type",
            y="Average Impact",
            color="Impact Metric",
            barmode="group",
            title="Average Impact per Event"
        )

        fig_avg.update_layout(
            xaxis_title="Disaster Type",
            yaxis_title="Average Impact",
            legend_title="Metric"
        )

        st.plotly_chart(fig_avg)

        # Optional table
        with st.expander("View comparison data"):
            st.dataframe(
                comparison_df[
                    [
                        "Start Year",
                        "Country",
                        "Disaster Type",
                        "Disaster Subtype",
                        "Total Deaths",
                        "Total Affected"
                    ]
                ],
                width="stretch"
            )