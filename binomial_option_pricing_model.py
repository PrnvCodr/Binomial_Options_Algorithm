import numpy as np

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

    def run(self):
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

        self.call_price = call_price
        self.put_price = put_price

        # Greeks calculation (Delta and Gamma)
        # For simplicity, we calculate the Delta and Gamma based on the binomial model
        delta = (option_prices[1] - option_prices[0]) / (current_price * u - current_price * d)
        gamma = (option_prices[2] - 2 * option_prices[1] + option_prices[0]) / (0.5 * (current_price * u - current_price * d) ** 2)

        self.call_delta = delta
        self.put_delta = 1 - delta
        self.call_gamma = gamma
        self.put_gamma = gamma


if __name__ == "__main__":
    time_to_maturity = 2
    strike = 90
    current_price = 100
    volatility = 0.2
    interest_rate = 0.05
    steps = 100  # Number of steps in the binomial tree

    # Binomial Option Pricing
    binomial_model = BinomialOptionPricing(
        time_to_maturity=time_to_maturity,
        strike=strike,
        current_price=current_price,
        volatility=volatility,
        interest_rate=interest_rate,
        steps=steps
    )
    binomial_model.run()

    # Printing the results
    print(f"Call Option Price: {binomial_model.call_price}")
    print(f"Put Option Price: {binomial_model.put_price}")
    print(f"Call Delta: {binomial_model.call_delta}")
    print(f"Put Delta: {binomial_model.put_delta}")
    print(f"Call Gamma: {binomial_model.call_gamma}")
    print(f"Put Gamma: {binomial_model.put_gamma}")
