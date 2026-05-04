import streamlit as st
from data import get_summary_df

def render_insights(filtered_df, classification_level):
    st.subheader("Key Insights")

    summary_df = get_summary_df(filtered_df, classification_level)

    if not summary_df.empty:
        most_frequent = summary_df.sort_values("Event_Count", ascending=False).iloc[0]
        most_deadly_total = summary_df.sort_values("Total_Deaths", ascending=False).iloc[0]
        most_deadly_per_event = summary_df.sort_values("Deaths per Event", ascending=False).iloc[0]
        most_affected_total = summary_df.sort_values("Total_Affected", ascending=False).iloc[0]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.info(
                f"**Most Frequent:**\n\n"
                f"{most_frequent[classification_level]} has the highest number of recorded events "
                f"with {int(most_frequent['Event_Count']):,} events."
            )

        with col2:
            st.warning(
                f"**Highest Total Deaths:**\n\n"
                f"{most_deadly_total[classification_level]} has the highest total deaths "
                f"with {int(most_deadly_total['Total_Deaths']):,} deaths."
            )

        with col3:
            st.error(
                f"**Highest Deaths per Event:**\n\n"
                f"{most_deadly_per_event[classification_level]} has the highest deaths per event "
                f"with {most_deadly_per_event['Deaths per Event']:,.2f} deaths per event."
            )

        st.info(
            f"**Interpretation:** The most frequent disaster category is not always the most devastating. "
            f"Using normalized metrics such as deaths per event and affected population per event helps separate "
            f"frequency from severity."
        )
