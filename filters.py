import streamlit as st

def sidebar_filters(df):
    filtered_df = df.copy()

    # -------------------------
    # Filter Regions
    # -------------------------
    region_options = ["All"] + sorted(filtered_df["Region"].dropna().unique().tolist()) if "Region" in filtered_df.columns else ["All"]
    selected_regions = st.sidebar.multiselect("Region", region_options)

    if selected_regions:
        filtered_df = filtered_df[filtered_df["Region"].isin(selected_regions)]

    # -------------------------
    # Filter Diasaster Group
    # -------------------------
    disaster_group_options = ["All"] + sorted(filtered_df["Disaster Group"].dropna().unique().tolist()) if "Disaster Group" in filtered_df.columns else ["All"]
    selected_disaster_groups = st.sidebar.multiselect("Disaster Group", disaster_group_options)

    if selected_disaster_groups:
        filtered_df = filtered_df[filtered_df["Disaster Group"].isin(selected_disaster_groups)]

    # -------------------------
    # Filter Diasaster Subgroup
    # -------------------------
    subgroup_options = ["All"] + sorted(filtered_df["Disaster Subgroup"].dropna().unique().tolist()) if "Disaster Subgroup" in filtered_df.columns else ["All"]
    selected_subgroups = st.sidebar.multiselect("Disaster Subgroup", subgroup_options)

    if selected_subgroups:
        filtered_df = filtered_df[filtered_df["Disaster Subgroup"].isin(selected_subgroups)]

    # -------------------------
    # Filter Diasaster Type
    # -------------------------
    type_options = ["All"] + sorted(filtered_df["Disaster Type"].dropna().unique().tolist()) if "Disaster Type" in filtered_df.columns else ["All"]
    selected_types = st.sidebar.multiselect("Disaster Type", type_options)

    if selected_types:
        filtered_df = filtered_df[filtered_df["Disaster Type"].isin(selected_types)]

    # -------------------------
    # Filter Diasaster Subtype
    # -------------------------
    subtype_options = ["All"] + sorted(filtered_df["Disaster Subtype"].dropna().unique().tolist()) if "Disaster Subtype" in filtered_df.columns else ["All"]
    selected_subtypes = st.sidebar.multiselect("Disaster Subype", subtype_options)

    if selected_subtypes:
        filtered_df = filtered_df[filtered_df["Disaster Subtype"].isin(selected_subtypes)]

    # -------------------------
    # Filter Year
    # -------------------------
    if "Start Year" in df.columns:
        min_year = int(df["Start Year"].min())
        max_year = int(df["Start Year"].max())
        year_range = st.sidebar.slider("Year Range", min_year, max_year, (min_year, max_year))
    else:
        year_range = None

    if year_range is not None:
        filtered_df = filtered_df[
            (filtered_df["Start Year"] >= year_range[0]) &
            (filtered_df["Start Year"] <= year_range[1])
        ]

    # -----------------------------
    # Classification Level Selector
    # -----------------------------
    classification_level = st.sidebar.selectbox(
        "Classification Level",
        ["Disaster Group", "Disaster Subgroup", "Disaster Type", "Disaster Subtype"],
        index=2
    )

    return filtered_df, classification_level