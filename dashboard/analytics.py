import pandas as pd

class Analytics:

    def __init__(self) -> None:
        self.cdi = pd.read_csv("dashboard/CDI.csv")
        self.moedas = pd.read_csv("dashboard/moedas.csv")
        self.proventos = pd.read_csv("dashboard/proventos.csv")
        self.trades = pd.read_csv("dashboard/trades.csv")

    def provendos_ano():
        df = self.cdo.copy()
        print(df)
