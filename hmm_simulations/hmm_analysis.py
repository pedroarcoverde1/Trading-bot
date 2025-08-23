import numpy as np
import matplotlib.pyplot as plt

def main():
    # Parâmetros dos regimes obtidos do HMM treinado anteriormente
    # (Estes valores são exemplos e devem ser substituídos pelos do seu modelo treinado)
    # Regime 0: Baixa Volatilidade
    mu_0, sigma_0 = 0.001, 0.01
    # Regime 1: Alta Volatilidade
    mu_1, sigma_1 = -0.003, 0.002

    # Matriz de transição do HMM
    trans_mat = np.array([[0.995, 0.005],
                          [0.141, 0.859]])

    # Parâmetros da simulação
    T = 2.0 # 2 anos
    dt = 1/252
    n_steps = int(T / dt)
    S0 = 60000 # Preço inicial

    # Simulação
    np.random.seed(101)
    states = np.zeros(n_steps + 1, dtype=int)
    prices = np.zeros(n_steps + 1)
    prices[0] = S0

    for t in range(1, n_steps + 1):
        # Determina o estado atual com base na matriz de transição
        previous_state = states[t-1]
        current_state = np.random.choice([0, 1], p=trans_mat[previous_state, :])
        states[t] = current_state
        
        # Seleciona os parâmetros do GBM com base no estado atual
        mu = mu_0 if current_state == 0 else mu_1
        sigma = sigma_0 if current_state == 0 else sigma_1
        
        # Simula o próximo preço usando a fórmula do GBM
        Z = np.random.standard_normal()
        prices[t] = prices[t-1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)

    # Plotar os resultados
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10), sharex=True, gridspec_kw={'height_ratios': [2, 1]})

    ax1.plot(prices)
    ax1.set_title('Simulação de Preços com Mudança de Regime (HMM + GBM)')
    ax1.set_ylabel('Preço')
    ax1.grid(True)

    ax2.plot(states, drawstyle='steps-post')
    ax2.set_title('Regime de Mercado Simulado (0=Baixa Vol, 1=Alta Vol)')
    ax2.set_xlabel('Dias de Negociação')
    ax2.set_yticks([0, 1])
    ax2.set_yticklabels(['Baixa Vol.', 'Alta Vol.'])
    ax2.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()