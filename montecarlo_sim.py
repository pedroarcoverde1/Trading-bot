from simulation import simulate_gbm
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf

def main():
    # fazer 10.000 simulações
    num_simulations = 10000

    # 1.Obter dados históricos
    ticker = 'PETR4.SA'
    data = yf.download(ticker, start='2020-01-01', end='2023-01-01')
    log_returns = np.log(data['Close'] / data['Close'].shift(1))
    log_returns.dropna(inplace=True)

    # 2. Calcular o dift (mu) e a volatilidade (sigma)
    mu = log_returns.mean()
    mu = mu.item()
    sigma = log_returns.std()
    sigma = sigma.item()
    print(f"Drift anual: {mu:.5f}")
    print(f"Volatilidade anual: {sigma:.5f}")

    # 3. Definir os parâmetros da simulação
    S0 = data['Close'].iloc[-1] # Preço inicial é o ultimo preço conhecido
    T = 1.0
    dt = 1/252 # 1 dia de retorno
    np.random.seed(42)

    sim = simulate_gbm(S0, mu, sigma, T, dt, N_sim=num_simulations)
    plt.figure(figsize=(10, 6))
    plt.plot(sim[ : , : 100], linewidth=0.5, alpha=0.7)
    plt.title(f'Simulação de Monte Carlo (GBM) para {ticker} (num_simulations={num_simulations})')
    plt.xlabel('Dias de Negociação')
    plt.ylabel('Preço')
    plt.grid(True)

    # calcular e plotar o preço final médio e intervalos de confiança
    final_prices = sim[-1:]
    mean_price = np.mean(final_prices)
    ci_95_upper = np.percentile(final_prices, 97.5)
    ci_95_lower = np.percentile(final_prices, 2.5)
    print(f"Preço final médio: {mean_price:.2f}")
    print(f"Intervalo de confiança 95%: ({mean_price - ci_95_lower:.2f}, {mean_price + ci_95_upper:.2f})")

    # adicionar linhsa de estatísticas ao gráfico
    plt.axhline(y = int(mean_price), color='red', linestyle='--', label='Preço final médio')
    plt.axhline(y = int(ci_95_upper), color='green', linestyle=':', label='Intervalo de confiança 95%')
    plt.axhline(y = int(ci_95_lower), color='green', linestyle=':', label='Intervalo de confiança 95%')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
