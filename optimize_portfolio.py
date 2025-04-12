import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
from Particle import *
from StockReturns import *
from multiobjective import *
import matplotlib.pyplot as plt

def optimize_portfolio(selected_tickers, start_date, end_date, optimization_goal):
    daily_returns = getStockReturns(selected_tickers, start_date, end_date)
    n_iterations = 250
    n_particles = 30
    n_assets = len(selected_tickers)
    # T_Bill = yf.download(['^IRX'], start_date, end_date, auto_adjust=False)
    # risk_free_rate = T_Bill['Adj Close'].mean() / 100

    # PSO parameters
    w = 0.9 # inertia
    c1 = 2 # cognitive parameter
    c2 = 2  # social parameter

    if optimization_goal == '3':
        # Initialize the swarm
        swarm = [MultiObjectiveParticle(n_assets) for _ in range(n_particles)]
        # Perform iterations

        best_values_over_iterations = [] 
        for iteration in range(n_iterations):
            global_best_returns = -float('inf')
            global_best_volatility = float('inf')
            global_best_position = None

            for particle in swarm:
                ret, vol = particle.evaluate(daily_returns)
                if particle.is_better(ret, global_best_returns, vol, global_best_volatility):
                    global_best_position = particle.position
                    global_best_returns = ret
                    global_best_volatility = vol
            best_values_over_iterations.append((global_best_returns, global_best_volatility))
            for particle in swarm:
                particle.update_velocity_and_position(global_best_position, w, c1, c2, iteration, n_iterations,swarm)
            
            print(f"Iteration {iteration}: Return: {global_best_returns}, Volatility: {global_best_volatility}")


        # Determine the optimal weights from best positions
        optimal_weights = global_best_position
        associated_risk = calculate_portfolio_volatility(global_best_position, daily_returns)
        associated_return = calculate_portfolio_return(global_best_position, daily_returns)



    else:
        # Initialize the swarm
        swarm = [Particle(n_assets) for _ in range(n_particles)]
        global_best_value = float('inf')
        global_best_position = None
        best_values_over_iterations = [] 
        # Run the PSO algorithm
        for iteration in range(n_iterations):
            for particle in swarm:
                # if optimization_goal == '1':  # Sharpe Ratio
                #     value = particle.evaluate(daily_returns, risk_free_rate, optimize_for='1')
                if optimization_goal == '1':  # Volatility
                    value = particle.evaluate(daily_returns, optimize_for='1')
                elif optimization_goal == '2':  # Return (Maximizing)
                    value = particle.evaluate(daily_returns, optimize_for='2')
                # elif optimization_goal == '4':  # Sortino Ratio
                #     value = particle.evaluate(daily_returns, risk_free_rate, optimize_for='4')
                else:
                    raise ValueError("Invalid optimization goal specified.")

                # Update the global best if needed
                if value < global_best_value:
                    global_best_value = value
                    global_best_position = np.copy(particle.position)
            best_values_over_iterations.append(-global_best_value)
            for particle in swarm:
                particle.update_velocity_and_position(global_best_position, w, c1, c2,iteration, n_iterations,swarm)

            # if optimization_goal == '1':
            #     print(f"Iteration {iteration} - Best Sharpe Ratio: {-global_best_value}")
            if optimization_goal == '1':
                print(f"Iteration {iteration} - Best Volatility: {global_best_value}")
            elif optimization_goal == '2':
                print(f"Iteration {iteration} - Best Return: {-global_best_value}")
            # elif optimization_goal == '4':
            #     print(f"Iteration {iteration} - Best Sortino Ratio: {-global_best_value}")

        optimal_weights = global_best_position
        associated_risk = calculate_portfolio_volatility(global_best_position, daily_returns)
        associated_return = calculate_portfolio_return(global_best_position, daily_returns)

        # Create a list of (ticker, weight) tuples
    ticker_weights = [(selected_tickers[i], optimal_weights[i]) for i in range(len(selected_tickers)) if optimal_weights[i] > 0.01]

    # Sort the list in descending order by weight
    sorted_ticker_weights = sorted(ticker_weights, key=lambda x: x[1], reverse=True)


    results = {
        'optimization goal': optimization_goal,
        'sorted_ticker_weights': sorted_ticker_weights,
        'associated_risk': associated_risk,
        'associated_return': associated_return
    }

   
    return results, best_values_over_iterations