import pandas as pd
import streamlit as st

# --------------------------------
# Load Data
# --------------------------------
FILE_PATH = "data/public_emdat.csv"

def make_unique_columns(columns):
    seen = {}
    new_cols = []

    for col in columns:
        if col not in seen:
            seen[col] = 0
            new_cols.append(col)
        else:
            seen[col] += 1
            new_cols.append(f"{col}_{seen[col]}")

    return new_cols

@st.cache_data
def load_data():
    raw_df = pd.read_csv(FILE_PATH)

    cols_to_keep = [
        "DisNo.", 
        "Disaster Group",
        "Disaster Subgroup",
        "Disaster Type",
        "Disaster Subtype",
        "Event Name", 
        "Country",
        "Subregion",
        "Region",
        "Disaster Subtype",
        "Origin",
        "Appeal",
        "Magnitude",
        "Magnitude Scale",
        "Start Year",
        "Start Month",
        "End Year",
        "End Month",
        "Total Deaths",
        "Total Affected",
        "Reconstruction Costs, Adjusted ('000 US$)",
        "Insured Damage, Adjusted ('000 US$)", 
        "Total Damage, Adjusted ('000 US$)"
    ]

    existing_cols = [col for col in cols_to_keep if col in raw_df.columns]
    df = raw_df[existing_cols]

    # Numeric Cleanup
    for col in ["Start Year",
                "Start Month",
                "End Year",
                "End Month",
                "Total Deaths",
                "Total Affected",
                "Reconstruction Costs, Adjusted ('000 US$)",
                "Insured Damage, Adjusted ('000 US$)", 
                "Total Damage, Adjusted ('000 US$)"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in ["Total Deaths",
                "Total Affected",
                "Reconstruction Costs, Adjusted ('000 US$)",
                "Insured Damage, Adjusted ('000 US$)", 
                "Total Damage, Adjusted ('000 US$)"]:
        df[col] = df[col].fillna(-1)

    for col in ["Start Month", "End Month"]:
        df[col] = df[col].fillna(1)

    # Derived fields
    df["Decade"] = (df["Start Year"] // 10) * 10

    if "Total Deaths" in df.columns and "Total Affected" in df.columns:
        df["Human Impact"] = df["Total Deaths"] + df["Total Affected"]

    df.columns = make_unique_columns(df.columns)

    # Cleanup
    return df

def get_summary_df(filtered_df, classification_level):
    summary_df = (
        filtered_df.groupby(classification_level, as_index=False)
        .agg(
            Event_Count=("DisNo.", "count"),
            Total_Deaths=("Total Deaths", "sum"),
            Total_Affected=("Total Affected", "sum"),
            Human_Impact=("Human Impact", "sum")
        )
    )

    summary_df["Deaths per Event"] = summary_df["Total_Deaths"] / summary_df["Event_Count"]
    summary_df["Affected per Event"] = summary_df["Total_Affected"] / summary_df["Event_Count"]
    summary_df["Human Impact per Event"] = summary_df["Human_Impact"] / summary_df["Event_Count"]

    return summary_df
