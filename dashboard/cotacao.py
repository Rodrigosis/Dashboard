import pandas as pd
from pandas_datareader import data as web
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
# !pip install yfinance --upgrade --no-cache-dir

yf.pdr_override()


class Cotacao:

    def __init__(self) -> None:
        self.memory = {}

    def get_price(self, ativo: str):
        # assert len(date) == 8
        
        if ativo in ['MMM', 'USDBRL=X']:
            pass
        else:
            ativo = f'{ativo}.SA'

        for at in self.memory.keys():
            if at == ativo:
                return self.memory[ativo]

        df = web.get_data_yahoo(ativo, actions = True)
        price = float(df.iloc[-1]['Open'])

        if price == 0:
             price = float(df.iloc[-2]['Open'])
            
        self.memory[ativo] = price

        return price
