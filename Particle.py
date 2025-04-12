import numpy as np

def calculate_portfolio_return(weights, returns):
    # Calculate the expected portfolio return
    portfolio_return = np.dot(weights, returns.mean()) * 252  # Assuming 252 trading days in a year
    return portfolio_return

def calculate_portfolio_volatility(weights, returns):
    # # Calculate the expected portfolio volatility
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))
    return portfolio_volatility

# Implement the PSO algorithm
class Particle:
    def __init__(self, n_assets):
        self.position = np.random.rand(n_assets)
        self.position /= self.position.sum()  # Normalize to ensure the sum of weights is 1
        self.velocity = np.zeros(n_assets)
        self.best_position = np.copy(self.position)
        self.best_value = float('inf')

    def evaluate(self, returns, optimize_for='1'):
        if optimize_for == '1':  # Volatility
            value = calculate_portfolio_volatility(self.position, returns)
        elif optimize_for == '2':  # Return (Maximizing)
            value = calculate_portfolio_return(self.position, returns)
            value = -value  # Maximizing, minimize negative
        else:
            raise ValueError("Invalid optimization goal specified.")

        if value < self.best_value:
            self.best_value = value
            self.best_position = np.copy(self.position)

        return value


    def update_velocity_and_position(self, global_best_position, w, c1, c2, iteration, max_iterations, particles):
        w = 0.9 - (0.5) * (1 - (iteration / max_iterations) ** 2) # Non-linear decay of inertia weight
        individual_distance = np.mean([np.linalg.norm(p.position - p.best_position) for p in particles])
        global_distance = np.mean([np.linalg.norm(p.position - global_best_position) for p in particles])

        # Adjust c1 and c2 based on distances
        c1 = min(2.5, c1 + 0.05 * (individual_distance - 0.1))  # Encourage more exploration if far from personal best
        c2 = min(2.5, c2 + 0.05 * (global_distance - 0.1))  # Encourage more exploitation if far from global best

        # random coefficients
        r1 = np.random.rand(self.best_position.shape[0])
        r2 = np.random.rand(self.best_position.shape[0])
        # r1, r2 = np.random.rand(2)
        inertia = w * self.velocity
        cognitive = c1 * r1 * (self.best_position - self.position)
        social = c2 * r2 * (global_best_position - self.position)
        self.velocity = inertia + cognitive + social
        self.position += self.velocity
        self.position = np.clip(self.position, 1e-3, None)  # Prevent 0 weights that can lead to division by zero
        self.position /= np.sum(self.position)  # Normalize to ensure the sum of weights is 1

