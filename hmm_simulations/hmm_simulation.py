from matplotlib import _label_from_arg
from pandas.core.generic import RandomState
from hmmlearn import hmm
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt


# 1. obter dados históricos da Ibovespa
ibov_data = yf.download('^BVSP', start='2010-01-01', end='2025-01-01', auto_adjust=True)
ibov_returns = np.log(ibov_data['Close']/ibov_data['Close'].shift(1)).dropna()
returns_array = ibov_returns.values.reshape(-1, 1)

# 2. Ajustar um HMM gaussiano com 2 estados
model = hmm.GaussianHMM(n_components=2, covariance_type='full', n_iter = 1000, random_state=42)
model.fit(returns_array)

# 3. Prever os estados futuros
hidden_states = model.predict(returns_array)

# 4. Analisar as características dos estados
print("Matriz de transição:")
print(np.round(model.transmat_, 3)) # ainda não sei direito o que isso significa
print("\n Médias dos retornos por estado:")
print(np.round(model.means_, 3))
print("\n Volatilidade por estado:")
print(np.round(model.covars_, 3))

# 5. Identificar qual estado é de alta ou baixa volatilidade
low_volatility_state = np.argmin(np.sqrt(model.covars_)) # por que raiz quadrada
high_volatility_state = np.argmax(np.sqrt(model.covars_)) # por que raiz quadrada

print(f"Estado de baixa volatilidade: {low_volatility_state}")
print(f"Estado de alta volatilidade: {high_volatility_state}")

# 6. Visualizar os regimes ao longo do tempo
fig,ax = plt.subplots(figsize=(15, 8))
ax.plot(ibov_data.index[-len(hidden_states):], ibov_data['Close'][-len(hidden_states):], label='Ibovespa')
ax.set_title('Regimes de Volatilidade da Ibovespa')
ax.set_ylabel('Preço da Ibovespa')

# colorir o fundo do gráfico de acordo com o regime
for i, state in enumerate(hidden_states):
    if state == low_volatility_state:
        ax.axvspan(ibov_returns.index[i], ibov_returns.index[i+1] if i+1 < len(ibov_returns.index) else ibov_returns.index[i], color='green', alpha=0.3)
plt.legend()
plt.show()
