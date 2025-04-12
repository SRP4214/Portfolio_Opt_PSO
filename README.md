# 📈 Multi-Objective Portfolio Optimization using PSO

This project implements a multi-objective optimization strategy for financial portfolio construction using Particle Swarm Optimization (PSO). The application retrieves live financial data, applies optimization logic to maximize returns and minimize risk, and provides an interactive visualization interface using Streamlit.

## 🚀 Features

- Multi-objective optimization of stock portfolios
- Real-time stock data fetching via yfinance
- Interactive UI for selecting stocks, tuning PSO parameters
- Visual analytics: Efficient frontier, return vs. risk, and more
- Built-in support for constraints like number of assets, risk level, etc.

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/portfolio-optimizer-pso.git
cd portfolio-optimizer-pso
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the app**
```bash
streamlit run run.py
```

## 📊 How it Works

1. Users select stocks and PSO parameters in the Streamlit UI.
2. Stock data is fetched using yfinance.
3. The optimizer uses PSO to find a set of portfolios optimizing return and minimizing variance.
4. Results are visualized using Plotly and Matplotlib.

## ⚙️ Key Modules

- **multiobjective.py**: Defines objective functions such as portfolio return and variance.
- **Particle.py**: Implements the particle class for PSO.
- **optimize_portfolio.py**: Runs PSO algorithm over the financial dataset.
- **run.py**: Streamlit app to integrate UI and backend optimization logic.

## 📦 Requirements

See requirements.txt for all required libraries:
- yfinance
- streamlit
- pandas
- plotly
- matplotlib
- numpy



## 📊 Example Visualizations

The app generates several visualizations to help understand optimization results:

- Efficient Frontier
- Portfolio weights distribution
- Risk vs Return tradeoff
- Asset correlation matrix
- Historical performance simulation

## Screenshots:
<img width="1417" alt="Screenshot 2025-04-12 at 5 07 58 PM" src="https://github.com/user-attachments/assets/e718d566-fb7b-43b1-9680-85626bfaabb2" />

<img width="1433" alt="Screenshot 2025-04-12 at 5 08 49 PM" src="https://github.com/user-attachments/assets/e1c72848-e54d-4602-8645-10b147551812" />

<img width="678" alt="Screenshot 2025-04-12 at 5 09 30 PM" src="https://github.com/user-attachments/assets/b0d4b088-f1f0-4931-8167-5e3e9418ebf8" />

<img width="775" alt="Screenshot 2025-04-12 at 5 09 35 PM" src="https://github.com/user-attachments/assets/0ffb34d9-e642-4b42-979f-ef30e431498c" />
