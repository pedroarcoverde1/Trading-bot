import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

def simulate_gbm(s0, mu, sigma, T, dt, N_sim = 1):
    # simula o movimento browniano geométrico
    # Parâmetros:
        # s0: preço inicial
        # mu: taxa de retorno média
        # sigma: volatilidade
        # T: tempo total da simulação
        # dt: tamanho do passo de tempo
        # N_sim: número de simulações
    n_steps = int (T / dt)
    paths = np.zeros((n_steps + 1, N_sim))
    paths[0] = s0

    for t in range(1, n_steps + 1):
        Z = np.random.standard_normal(size=N_sim)
        paths[t] = paths[t - 1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)
        return paths


# 1.Obter dados históricos
ticker = 'PETR4.SA'
data = yf.download(ticker, start='2020-01-01', end='2023-01-01')
log_returns = np.log(data['Close'] / data['Close'].shift(1))
log_returns.dropna(inplace=True)

# 2. Calcular o dift (mu) e a volatilidade (sigma)
mu = log_returns.mean()
sigma = log_returns.std()
print(f"Drift anual: {mu:.4f}")
print(f"Volatilidade anual: {sigma:.4f}")

# 3. Definir os parâmetros da simulação
S0 = data['Close'][-1] # Preço inicial é o ultimo preço conhecido
T = 1.0
dt = 1/252 # 1 dia de retorno

np.random.seed(42)
sim = simulate_gbm(S0, mu, sigma, T, dt, N_sim=1)

# 4. Plotar os resultados
plt.figure(figsize=(10, 6))
plt.plot(sim)
plt.xlabel('Tempo')
plt.ylabel('Preço')
plt.title('Simulação de Preço do Ativo')
plt.show()
