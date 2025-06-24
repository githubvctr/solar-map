import streamlit as st

def capacity_filter_slider(max_capacity: float, default: float = 5.0) -> float:
    return st.sidebar.slider(
        "Minimum Capacity (MWp)",
        0.0,
        float(max_capacity),
        default
    )
def enable_selection_mode():
    return st.sidebar.checkbox("Enable selection mode")

def display_selection_summary(gdf):
    selected = gdf[gdf["Name"].isin(st.session_state.selected_municipalities)]
    st.sidebar.markdown("### Selected Municipalities")
    st.sidebar.write(selected[["Name", "capacity_mwp"]])
    st.sidebar.metric("Total MWp", round(selected["capacity_mwp"].sum(), 2))
