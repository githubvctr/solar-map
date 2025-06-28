import streamlit as st

def capacity_filter_slider(max_capacity: float, default: float = 5.0) -> float:
    return st.sidebar.slider(
        "Minimum Capacity (MW)",
        0.0,
        float(max_capacity),
        default
    )

def enable_selection_mode():
    return st.sidebar.checkbox("Enable selection mode")

def display_selection_summary(gdf):
    selected = gdf[gdf["Name"].isin(st.session_state.selected_municipalities)]
    st.sidebar.markdown("### Selected Municipalities")
    # Convert to MW for display
    selected = selected.copy()
    selected["Installaties (MW)"] = selected["Installaties (aantal)"] / 1000
    st.sidebar.write(selected[["Name", "Installaties (MW)"]])
    st.sidebar.metric("Total MW", round(selected["Installaties (MW)"].sum(), 2))
