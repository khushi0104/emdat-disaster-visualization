import streamlit as st 

def render_data_explorer(filtered_df):
    st.subheader("Disaster Records")

    # Choose which columns are searchable
    searchable_columns = [
        "Disaster Type",
        "Disaster Subtype",
        "Country",
        "Region",
        "Location",
        "Start Year"
    ]

    # Only keep columns that actually exist in your dataframe
    searchable_columns = [col for col in searchable_columns if col in filtered_df.columns]

    search_column_selection = st.multiselect(
        "Filter Columns",
        options=searchable_columns,
        default=None
    )

    table_search = st.text_input(
        "",
        placeholder="Search by disaster type, country, region, location, year..."
    )

    # Start with the already sidebar-filtered dataframe
    table_df = filtered_df.copy()

    # Apply table-specific search
    if table_search and search_column_selection:
        search_mask = table_df[search_column_selection].astype(str).apply(
            lambda row: row.str.contains(table_search, case=False, na=False).any(),
            axis=1
        )
        table_df = table_df[search_mask]

    # Column selector
    display_columns = st.multiselect(
        "Choose columns to display",
        options=["All"] + list(table_df.columns),
        default=["All"]
    )

    # Display final table
    if "All" in display_columns:
        st.dataframe(
            table_df,
            width="stretch"
        )
    elif display_columns:
        st.dataframe(
            table_df[display_columns],
            width="stretch"
        )
    else:
        st.warning("Please select at least one column to display.")