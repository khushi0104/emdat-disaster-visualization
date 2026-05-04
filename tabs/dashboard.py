import streamlit as st
import plotly.express as px 
from data import get_summary_df


def render_dashboard(filtered_df, classification_level):
    if "excluded_map_countries" not in st.session_state:
        st.session_state.excluded_map_countries = []
# ------------------------------------------------------ KPI SUMMARY -----------------------------------------------------------------------
    st.subheader("Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Records", f"{len(filtered_df):,}")

    if "Total Deaths" in filtered_df.columns:
        col2.metric("Total Deaths", f"{int(filtered_df['Total Deaths'].sum()):,}")

    if "Total Affected" in filtered_df.columns:
        col3.metric("Total Affected", f"{int(filtered_df['Total Affected'].sum()):,}")

    if "Human Impact" in filtered_df.columns:
        col4.metric("Combined Human Impact", f"{int(filtered_df['Human Impact'].sum()):,}")

# -----------------------------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------- GEOGRAPHIC VIEW OF DISASTER IMPACT ------------------------------------------------------
    st.subheader("Geographic View of Disaster Impact")

    map_metric = st.selectbox(
        "Map metric:",
        ["Total Deaths", "Total Affected", "Human Impact"],
        key="map_metric"
    )

    map_df = (
        filtered_df.groupby("Country", as_index=False)[map_metric]
        .sum()
    )

    # Remove countries with missing/zero values for cleaner scaling
    map_df = map_df[map_df[map_metric] > 0].copy()

    # Apply excluded countries
    if st.session_state.excluded_map_countries:
        map_df = map_df[
            ~map_df["Country"].isin(st.session_state.excluded_map_countries)
        ]

    if not map_df.empty:
        min_value = float(map_df[map_metric].min())
        max_value = float(map_df[map_metric].max())

        lower_default = float(map_df[map_metric].quantile(0.01))
        upper_default = float(map_df[map_metric].quantile(0.95))

        scale_range = st.slider(
            "Adjust map color scale",
            min_value=min_value,
            max_value=max_value,
            value=(lower_default, upper_default),
            key="map_scale_slider"
        )

        fig_map = px.choropleth(
            map_df,
            locations="Country",
            locationmode="country names",
            color=map_metric,
            hover_name="Country",
            custom_data=["Country"],
            range_color=scale_range,
            color_continuous_scale="Reds",
            title=f"{map_metric} by Country"
        )

        fig_map.update_layout(
            margin=dict(l=0, r=0, t=40, b=0)
        )

        map_event = st.plotly_chart(
            fig_map,
            key="impact_map",
            on_select="rerun",
            selection_mode="points"
        )

        selected_points = (
            map_event["selection"]["points"]
            if map_event and "selection" in map_event
            else []
        )

        if selected_points:
            clicked_country = selected_points[0]["customdata"][0]

            if clicked_country not in st.session_state.excluded_map_countries:
                st.session_state.excluded_map_countries.append(clicked_country)
                st.rerun()

        if st.session_state.excluded_map_countries:
            st.write(
                "Excluded countries:",
                ", ".join(st.session_state.excluded_map_countries)
            )

            if st.button("Reset excluded countries"):
                st.session_state.excluded_map_countries = []
                st.rerun()
 
    else:
        st.info("No map data available after excluding countries.")

# ----------------------------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------- DISASTER FREQUENCY OVER TIME -------------------------------------------------------------
    st.subheader("Disaster Frequency Over Time")


    freq_mode = st.radio(
        "Choose time aggregation:",
        ["Yearly", "By Decade"],
        horizontal=True
    )

    if freq_mode == "Yearly":
        x_col = "Start Year"
        trend_df = (
            filtered_df.groupby([x_col, classification_level])
            .size()
            .reset_index(name="Count")
        )
    else:
        x_col = "Decade"
        trend_df = (
            filtered_df.groupby([x_col, classification_level])
            .size()
            .reset_index(name="Count")
        )

    fig = px.line(
        trend_df,
        x=x_col,
        y="Count",
        color=classification_level,
        markers=True,
        custom_data=[classification_level],  
        title=f"Frequency by {classification_level}"
    )

    event = st.plotly_chart(
        fig,
        key="drill_chart",
        on_select="rerun",
        selection_mode="points"
    )

# ----------------------------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------- DISTRIBUTION OF DISASTER IMPACTS --------------------------------------------------------
    st.subheader("Distribution of Disaster Impacts")

    impact_measure = st.selectbox(
        "Choose impact variable:",
        ["Total Deaths", "Total Affected"]
    )

    log_scale = st.checkbox("Use log scale for impact distribution")

    dist_df = filtered_df[filtered_df[impact_measure] > 0].copy()

    if not dist_df.empty:
        fig2 = px.box(
            dist_df,
            y=impact_measure,
            x=classification_level,
            color=classification_level,
            title=f"Distribution of {impact_measure} by Disaster Type"
        )

        if log_scale:
            fig2.update_yaxes(type="log")

        fig2.update_layout(
            xaxis_title=classification_level,
            yaxis_title=impact_measure
        )

        st.plotly_chart(fig2)
    else:
        st.info("No nonzero values available for the selected impact variable and filters.")

# ----------------------------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------- MOST DEVASTATING DISASTER TYPES ---------------------------------------------------------
    st.subheader("Most Devastating Disaster Types")

    summary_df = get_summary_df(filtered_df, classification_level)

    impact_metric = st.selectbox(
        "Ranking metric:",
        [
            "Total_Deaths",
            "Total_Affected",
            "Human_Impact",
            "Deaths per Event",
            "Affected per Event",
            "Human Impact per Event"
        ]
    )

    rank_df = summary_df.sort_values(by=impact_metric, ascending=False)

    log_scale_rank = st.checkbox("Use log scale for ranking chart")

    top_n = st.slider("Show Top N Categories", 3, 20, 10)
    rank_df = rank_df.head(top_n)

    fig3 = px.bar(
        rank_df,
        y=impact_metric,
        x=classification_level,
        color=classification_level,
        title=f"Top {top_n} {classification_level}s by {impact_metric}"
    )

    if log_scale_rank:
        fig3.update_yaxes(type="log")

    st.plotly_chart(fig3)

# ----------------------------------------------------------------------------------------------------------------------------------------


