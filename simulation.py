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
