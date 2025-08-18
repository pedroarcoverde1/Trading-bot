import yfinance as yf

def main():
    ticker = 'PETR4.SA'
    data = yf.download(ticker, start='2020-01-01', end='2023-01-01')
    print(data.head())
    print(data.columns)

if __name__ == '__main__':
    main()
