import numpy as np
import yfinance as yf
from StockReturns import * 
from Particle import *

class MultiObjectiveParticle:
    def __init__(self, n_assets):
        self.position = np.random.dirichlet(np.ones(n_assets), size=1)[0]
        self.velocity = np.zeros(n_assets)
        self.best_position = np.copy(self.position)
        self.best_returns = -float('inf')
        self.best_volatility = float('inf')

    def evaluate(self, returns):
        current_return = calculate_portfolio_return(self.position, returns)
        current_volatility = calculate_portfolio_volatility(self.position, returns)
        if (self.is_better(current_return, self.best_returns, current_volatility, self.best_volatility)):
            self.best_position = np.copy(self.position)
            self.best_returns = current_return
            self.best_volatility = current_volatility
        return current_return, current_volatility

    def is_better(self, ret1, ret2, vol1, vol2):
        better_return = ret1 > ret2
        better_volatility = vol1 < vol2
        return better_return and better_volatility

    def update_velocity_and_position(self, global_best_position, w, c1, c2, iteration, n_iterations, particles):
        w = 0.9 - (0.5) * (1 - (iteration / n_iterations) ** 2) # Non-linear decay of inertia weight
        # random coefficients
        r1 = np.random.rand(self.best_position.shape[0])
        r2 = np.random.rand(self.best_position.shape[0])
        
        individual_distance = np.mean([np.linalg.norm(p.position - p.best_position) for p in particles])
        global_distance = np.mean([np.linalg.norm(p.position - global_best_position) for p in particles])

        # Adjust c1 and c2 based on distances
        c1 = min(2.5, c1 + 0.05 * (individual_distance - 0.1))  # Encourage more exploration if far from personal best
        c2 = min(2.5, c2 + 0.05 * (global_distance - 0.1))  # Encourage more exploitation if far from global best

        inertia = w * self.velocity
        cognitive = c1 * r1 * (self.best_position - self.position)
        social = c2 * r2 * (global_best_position - self.position)
        self.velocity = inertia + cognitive + social
        self.position += self.velocity
        self.position = np.clip(self.position, 1e-3, None)  # Prevent 0 weights that can lead to division by zero
        self.position /= np.sum(self.position)  # Normalize to ensure the sum of weights is 1