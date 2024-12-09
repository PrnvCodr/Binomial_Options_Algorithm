import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns


# Page configuration
st.set_page_config(
    page_title="Binomial Option Pricing Model",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded")


# Custom CSS to inject into Streamlit
st.markdown("""
<style>
/* Adjust the size and alignment of the CALL and PUT value containers */
.metric-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 8px; /* Adjust the padding to control height */
    width: auto; /* Auto width for responsiveness, or set a fixed width if necessary */
    margin: 0 auto; /* Center the container */
}

/* Custom classes for CALL and PUT values */
.metric-call {
    background-color: #90ee90; /* Light green background */
    color: black; /* Black font color */
    margin-right: 10px; /* Spacing between CALL and PUT */
    border-radius: 10px; /* Rounded corners */
}

.metric-put {
    background-color: #ffcccb; /* Light red background */
    color: black; /* Black font color */
    border-radius: 10px; /* Rounded corners */
}

/* Style for the value text */
.metric-value {
    font-size: 1.5rem; /* Adjust font size */
    font-weight: bold;
    margin: 0; /* Remove default margins */
}

/* Style for the label text */
.metric-label {
    font-size: 1rem; /* Adjust font size */
    margin-bottom: 4px; /* Spacing between label and value */
}

</style>
""", unsafe_allow_html=True)


class BinomialOptionPricing:
    def __init__(
        self,
        time_to_maturity: float,
        strike: float,
        current_price: float,
        volatility: float,
        interest_rate: float,
        steps: int
    ):
        self.time_to_maturity = time_to_maturity
        self.strike = strike
        self.current_price = current_price
        self.volatility = volatility
        self.interest_rate = interest_rate
        self.steps = steps

    def calculate_prices(self):
        time_to_maturity = self.time_to_maturity
        strike = self.strike
        current_price = self.current_price
        volatility = self.volatility
        interest_rate = self.interest_rate
        steps = self.steps

        # Time step and the up/down factor (u/d)
        dt = time_to_maturity / steps
        u = np.exp(volatility * np.sqrt(dt))  # Up factor
        d = 1 / u  # Down factor
        q = (np.exp(interest_rate * dt) - d) / (u - d)  # Risk-neutral probability

        # Initialize the option prices at the final step (maturity)
        option_prices = np.zeros(steps + 1)
        for i in range(steps + 1):
            option_prices[i] = max(0, current_price * (u ** i) * (d ** (steps - i)) - strike)

        # Backward induction to calculate option price at the initial step
        for j in range(steps - 1, -1, -1):
            for i in range(j + 1):
                option_prices[i] = np.exp(-interest_rate * dt) * (q * option_prices[i + 1] + (1 - q) * option_prices[i])

        call_price = option_prices[0]

        # For put option
        option_prices = np.zeros(steps + 1)
        for i in range(steps + 1):
            option_prices[i] = max(0, strike - current_price * (u ** i) * (d ** (steps - i)))

        # Backward induction for put option
        for j in range(steps - 1, -1, -1):
            for i in range(j + 1):
                option_prices[i] = np.exp(-interest_rate * dt) * (q * option_prices[i + 1] + (1 - q) * option_prices[i])

        put_price = option_prices[0]

        # Greeks calculation (Delta and Gamma)
        # For simplicity, we calculate the Delta and Gamma based on the binomial model
        delta = (option_prices[1] - option_prices[0]) / (current_price * u - current_price * d)
        gamma = (option_prices[2] - 2 * option_prices[1] + option_prices[0]) / (0.5 * (current_price * u - current_price * d) ** 2)

        self.call_price = call_price
        self.put_price = put_price
        self.call_delta = delta
        self.put_delta = 1 - delta
        self.call_gamma = gamma
        self.put_gamma = gamma

        return call_price, put_price


# Sidebar for User Inputs
with st.sidebar:
    st.title("📊 Binomial Option Pricing Model")
    st.write("`Created by:`")
    linkedin_url = "https://www.linkedin.com/in/pranav-kashyap122/"
    st.markdown(f'<a href="{linkedin_url}" target="_blank" style="text-decoration: none; color: inherit;"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="25" height="25" style="vertical-align: middle; margin-right: 10px;">`Pranav Kashyap`</a>', unsafe_allow_html=True)

    current_price = st.number_input("Current Asset Price", value=100.0)
    strike = st.number_input("Strike Price", value=100.0)
    time_to_maturity = st.number_input("Time to Maturity (Years)", value=1.0)
    volatility = st.number_input("Volatility (σ)", value=0.2)
    interest_rate = st.number_input("Risk-Free Interest Rate", value=0.05)
    steps = st.number_input("Number of Steps in Binomial Model", value=100)

    st.markdown("---")
    calculate_btn = st.button('Heatmap Parameters')
    spot_min = st.number_input('Min Spot Price', min_value=0.01, value=current_price*0.8, step=0.01)
    spot_max = st.number_input('Max Spot Price', min_value=0.01, value=current_price*1.2, step=0.01)
    vol_min = st.slider('Min Volatility for Heatmap', min_value=0.01, max_value=1.0, value=volatility*0.5, step=0.01)
    vol_max = st.slider('Max Volatility for Heatmap', min_value=0.01, max_value=1.0, value=volatility*1.5, step=0.01)

    spot_range = np.linspace(spot_min, spot_max, 10)
    vol_range = np.linspace(vol_min, vol_max, 10)


def plot_heatmap(binomial_model, spot_range, vol_range, strike):
    call_prices = np.zeros((len(vol_range), len(spot_range)))
    put_prices = np.zeros((len(vol_range), len(spot_range)))

    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            binomial_temp = BinomialOptionPricing(
                time_to_maturity=binomial_model.time_to_maturity,
                strike=strike,
                current_price=spot,
                volatility=vol,
                interest_rate=binomial_model.interest_rate,
                steps=binomial_model.steps
            )
            binomial_temp.calculate_prices()
            call_prices[i, j] = binomial_temp.call_price
            put_prices[i, j] = binomial_temp.put_price

    # Plotting Call Price Heatmap
    fig_call, ax_call = plt.subplots(figsize=(10, 8))
    sns.heatmap(call_prices, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), annot=True, fmt=".2f", cmap="viridis", ax=ax_call)
    ax_call.set_title('CALL')
    ax_call.set_xlabel('Spot Price')
    ax_call.set_ylabel('Volatility')

    # Plotting Put Price Heatmap
    fig_put, ax_put = plt.subplots(figsize=(10, 8))
    sns.heatmap(put_prices, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), annot=True, fmt=".2f", cmap="viridis", ax=ax_put)
    ax_put.set_title('PUT')
    ax_put.set_xlabel('Spot Price')
    ax_put.set_ylabel('Volatility')

    return fig_call, fig_put


# Main Page for Output Display
st.title("Binomial Option Pricing Model")

# Table of Inputs
input_data = {
    "Current Asset Price": [current_price],
    "Strike Price": [strike],
    "Time to Maturity (Years)": [time_to_maturity],
    "Volatility (σ)": [volatility],
    "Risk-Free Interest Rate": [interest_rate],
}
input_df = pd.DataFrame(input_data)
st.table(input_df)

# Calculate Call and Put values
binomial_model = BinomialOptionPricing(time_to_maturity, strike, current_price, volatility, interest_rate, steps)
call_price, put_price = binomial_model.calculate_prices()

# Display Call and Put Values in colored tables
col1, col2 = st.columns([1, 1], gap="small")

with col1:
    # Using the custom class for CALL value
    st.markdown(f"""
        <div class="metric-container metric-call">
            <div>
                <div class="metric-label">CALL Value</div>
                <div class="metric-value">${call_price:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    # Using the custom class for PUT value
    st.markdown(f"""
        <div class="metric-container metric-put">
            <div>
                <div class="metric-label">PUT Value</div>
                <div class="metric-value">${put_price:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("")
st.title("Options Price - Interactive Heatmap")
st.info("Explore how option prices fluctuate with varying 'Spot Prices and Volatility' levels using interactive heatmap parameters, all while maintaining a constant 'Strike Price'.")

# Interactive Sliders and Heatmaps for Call and Put Options
col1, col2 = st.columns([1, 1], gap="small")

with col1:
    st.subheader("Call Price Heatmap")
    heatmap_fig_call, _ = plot_heatmap(binomial_model, spot_range, vol_range, strike)
    st.pyplot(heatmap_fig_call)

with col2:
    st.subheader("Put Price Heatmap")
    _, heatmap_fig_put = plot_heatmap(binomial_model, spot_range, vol_range, strike)
    st.pyplot(heatmap_fig_put)
