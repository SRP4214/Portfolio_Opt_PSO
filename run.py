import streamlit as st
import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Import the optimization function from your module
from optimize_portfolio import optimize_portfolio

# Initialize selected tickers 
# in session state if not already set
if "selected_tickers" not in st.session_state:
    st.session_state.selected_tickers = []

def add_ticker(ticker):
    """Add ticker to session state if not already present."""
    ticker = ticker.strip().upper()
    if not ticker:
        st.warning("Ticker cannot be empty.")
        return False
    if ticker in st.session_state.selected_tickers:
        st.warning(f"{ticker} is already in the selected tickers list.")
        return False
    st.session_state.selected_tickers.append(ticker)
    return True

def remove_ticker(ticker):
    """Remove ticker from session state."""
    if ticker in st.session_state.selected_tickers:
        st.session_state.selected_tickers.remove(ticker)
    else:
        st.error(f"{ticker} is not in the selected tickers list.")

st.title("Portfolio Optimization Using PSO")

# --- Recommended Companies Section ---
st.header("Our Recommended Companies")
recommended_tickers = ['MSFT', 'AAPL', 'NVDA', 'AMZN', 'META', 'GOOGL', 'LLY', 'AVGO', 'JPM', 'NFLX']
cols = st.columns(5)
for i, ticker in enumerate(recommended_tickers):
    col = cols[i % 5]
    # If ticker is already selected, display it as plain text; otherwise, show an "Add" button.
    if ticker in st.session_state.selected_tickers:
        col.markdown(f"**{ticker}**")
    else:
        if col.button(ticker, key=f"btn_add_{ticker}"):
            success = add_ticker(ticker)
            if success:
                st.rerun()  # Force a rerun to update the selected tickers immediately

st.markdown("---")

# --- Custom Ticker Input Using a Form ---
st.header("Add Custom Ticker")
with st.form("custom_ticker_form", clear_on_submit=True):
    custom_ticker = st.text_input("Input custom ticker (e.g., TSLA)", key="custom_ticker_input")
    submitted = st.form_submit_button("Add Custom Ticker")
    if submitted:
        if not custom_ticker:
            st.error("Please enter a valid ticker symbol.")
        else:
            success = add_ticker(custom_ticker)
            if success:
                st.success(f"Ticker {custom_ticker.strip().upper()} added successfully.")
                st.rerun()
                
st.markdown("---")

# --- Selected Tickers Section ---
st.markdown('<a id="selected_tickers"></a>', unsafe_allow_html=True)
st.header("Selected Tickers")
if st.session_state.selected_tickers:
    # Iterate over a copy to avoid issues while modifying the list.
    for ticker in st.session_state.selected_tickers.copy():
        c1, c2 = st.columns([3, 1])
        with c1:
            st.write(ticker)
        with c2:
            if st.button("X", key=f"remove_{ticker}", on_click=remove_ticker, args=(ticker,)):
                st.rerun()
else:
    st.write("No tickers selected yet.")

st.markdown("---")

# --- Additional Parameters ---
start_date = st.date_input("Start Date", datetime.date(2015, 1, 1))
end_date = st.date_input("End Date", datetime.date(2024, 1, 1))

goal_options = {
    # "Maximize Sharpe Ratio": "1",
    "Minimize Volatility": "1",
    "Maximize Returns": "2",
    # "Maximize Sortino Ratio": "4",
    "MOPSO (Max Returns - Min Risk)": "3"
}
goal_label = st.radio("Select Optimization Goal", list(goal_options.keys()))
goal = goal_options[goal_label]

st.markdown("---")

# --- Optimization Trigger ---
if st.button("Optimize Portfolio"):
    if not st.session_state.selected_tickers:
        st.error("Please select at least one ticker before optimization.")
    else:
        try:
            with st.spinner("Optimizing portfolio..."):
                result = optimize_portfolio(
                    st.session_state.selected_tickers,
                    start_date.strftime("%Y-%m-%d"),
                    end_date.strftime("%Y-%m-%d"),
                    goal
                )
            st.success("Optimization complete!")
        except Exception as e:
            st.error(f"An error occurred during optimization: {e}")
        
        # --- Display Allocation Results ---
        st.subheader("Allocations")
        allocations = result[0].get("sorted_ticker_weights", [])
        if allocations:
            try:
                df_alloc = pd.DataFrame(allocations, columns=["Ticker", "Weight"])
                df_alloc["Weight"] = df_alloc["Weight"] * 100  # Convert to percentage
                st.dataframe(df_alloc)
                fig_pie = px.pie(
                    df_alloc, names="Ticker", values="Weight",
                    title="Portfolio Allocation (%)",
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                st.plotly_chart(fig_pie)
            except Exception as e:
                st.error(f"Error displaying allocations: {e}")
        else:
            st.warning("No allocation data available.")
        
        # --- Display Statistical Summary ---
        st.subheader("Statistical Summary")
        associated_risk = result[0].get("associated_risk", None)
        associated_return = result[0].get("associated_return", None)
        if associated_risk is not None and associated_return is not None:
            st.write(f"**Associated Risk:** {associated_risk * 100:.2f}%")
            st.write(f"**Associated Return:** {associated_return * 100:.2f}%")
        else:
            st.warning("No statistical summary data available.")
        
        # --- Plot Optimization Progress ---
        best_values = result[1]
        if best_values:
            try:
                if goal == "3":
                    iterations = list(range(1, len(best_values) + 1))
                    returns = [item[0] for item in best_values]
                    volatility = [item[1] for item in best_values]
                    fig_combined = go.Figure()
                    fig_combined.add_trace(go.Scatter(
                        x=iterations, y=returns, mode='lines+markers',
                        name='Global Best Returns',
                        line=dict(color='rgb(75, 192, 192)')
                    ))
                    fig_combined.add_trace(go.Scatter(
                        x=iterations, y=volatility, mode='lines+markers',
                        name='Global Best Volatility',
                        yaxis="y2",
                        line=dict(color='rgb(255, 99, 132)')
                    ))
                    fig_combined.update_layout(
                        title="Optimization Progress",
                        xaxis_title="Iteration",
                        yaxis=dict(title="Returns"),
                        yaxis2=dict(title="Volatility", overlaying='y', side='right'),
                        legend=dict(x=0, y=1.1, orientation="h")
                    )
                    st.plotly_chart(fig_combined)
                else:
                    iterations = list(range(1, len(best_values) + 1))
                    fig_line = px.line(
                        x=iterations, y=best_values,
                        labels={"x": "Iteration", "y": goal_label},
                        title="Optimization Progress"
                    )
                    st.plotly_chart(fig_line)
            except Exception as e:
                st.error(f"Error plotting optimization progress: {e}")
        else:
            st.warning("No optimization progress data available.")
        
        # --- Scroll to Selected Tickers Section ---
        st.markdown('<script>window.location.href="#selected_tickers";</script>', unsafe_allow_html=True)
