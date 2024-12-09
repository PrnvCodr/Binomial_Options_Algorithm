# Binomial Option Pricing Model

This repository implements the **Binomial Option Pricing Model** to compute the theoretical prices of European call and put options. The binomial model uses a discrete-time framework for valuing options by building a price tree to evaluate possible future asset prices.

## 🚀 Features
- https://binomialoptionsalgorithm.streamlit.app/
- **Option Pricing**: Computes prices for European call and put options using the binomial tree approach.
- **Greeks Calculation**: Calculates option sensitivities, including Delta and Gamma.
- **Customizable Parameters**: Easily modify key inputs like strike price, volatility, interest rate, and number of steps.
- **Python-Based Implementation**: A clear, extensible Python implementation suitable for both academic and professional purposes.

---

## 📋 Parameters
| Parameter               | Description                                       |
|-------------------------|---------------------------------------------------|
| `current_price`         | Price of the underlying asset.                    |
| `strike`                | Strike price of the option.                       |
| `time_to_maturity`      | Time to maturity (in years).                      |
| `volatility`            | Annualized volatility of the underlying asset.    |
| `interest_rate`         | Risk-free interest rate (annualized).             |
| `steps`                 | Number of time steps in the binomial tree.        |

---

## 🛠 Installation
1. Clone this repository:
    ```bash
    git clone https://github.com/your-username/binomial-option-pricing.git
    ```
2. Navigate to the project directory:
    ```bash
    cd binomial-option-pricing
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

---

## 📝 Usage
### Basic Example
```python
from binomial_option_pricing import BinomialOptionPricing

# Initialize parameters
time_to_maturity = 2  # in years
strike = 90           # strike price
current_price = 100   # current asset price
volatility = 0.2      # annualized volatility
interest_rate = 0.05  # annualized risk-free interest rate
steps = 100           # number of steps in the binomial tree

# Instantiate the model
model = BinomialOptionPricing(
    time_to_maturity=time_to_maturity,
    strike=strike,
    current_price=current_price,
    volatility=volatility,
    interest_rate=interest_rate,
    steps=steps
)

# Run the model
model.run()

# Print results
print(f"Call Option Price: {model.call_price}")
print(f"Put Option Price: {model.put_price}")
print(f"Call Delta: {model.call_delta}")
print(f"Put Delta: {model.put_delta}")
print(f"Call Gamma: {model.call_gamma}")
print(f"Put Gamma: {model.put_gamma}")
