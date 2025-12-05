import streamlit as st
import pandas as pd

# ------------------------------------------
# Load all horizon results
# ------------------------------------------
results_7  = pd.read_csv('/Users/shreyasramani/Downloads/7_day_forecast - Sheet1.csv')
results_14 = pd.read_csv('/Users/shreyasramani/Downloads/14_day_forecast - Sheet1.csv')

# Keep them in a dictionary for easy access
horizon_map = {
    "7-Day Forecast": results_7,
    "14-Day Forecast": results_14,
}

# ------------------------------------------
# Streamlit UI
# ------------------------------------------
st.title("SNN Regional Disease Forecasting Dashboard")

state = st.selectbox("Select a State", results_7["state"].unique())

horizon = st.radio(
    "Select Forecast Horizon:",
    ["7-Day Forecast", "14-Day Forecast"],
    horizontal=True
)

df = horizon_map[horizon]
row = df[df["state"] == state].iloc[0]

# ------------------------------------------
# Display Forecast Accuracy Metrics
# ------------------------------------------
st.subheader(f"{horizon} — Forecasting Performance ({state})")

mae_col = [col for col in row.index if "MAE" in col][0]
rmse_col = [col for col in row.index if "RMSE" in col][0]

st.metric("MAE", f"{row[mae_col]:.3f}")
st.metric("RMSE", f"{row[rmse_col]:.3f}")

# ------------------------------------------
# Module Contributions
# ------------------------------------------
st.subheader("Module Contribution Scores")

contrib = {
    "Temporal": row["temporal"],
    "Mobility": row["mobility"],
    "Vaccination": row["vaccine"],
    "Environment": row["environment"]
}

st.bar_chart(pd.DataFrame.from_dict(contrib, orient="index", columns=["Contribution"]))

# ------------------------------------------
# Narrative Interpretation
# ------------------------------------------
st.subheader("Interpretation")

if "7-Day" in horizon:
    st.write(
        f"For short-term (7-day) forecasts, predictions for **{state}** are influenced "
        "most strongly by temporal momentum and vaccination/environment features, "
        "with moderate influence from mobility."
    )

elif "14-Day" in horizon:
    st.write(
        f"At the 14-day horizon, the SNN begins shifting away from pure temporal momentum. "
        "Vaccination and mobility signals increase in importance, indicating that "
        "medium-range forecasts rely more on behavioral trends and immunity levels."
    )

else:
    st.write(
        "Vaccination becomes the dominant driver for **{state}**, reflecting "
        "its stabilizing effect on long-term transmission dynamics."
    )
