import pandas as pd

class Analytics:

    def __init__(self) -> None:
        self.cdi = pd.read_csv("CDI.csv")
        self.moedas = pd.read_csv("moedas.csv")
        self.proventos = pd.read_csv("proventos.csv")
        self.trades = pd.read_csv("trades.csv")
        self.dolar = 5.10

    def get_preco_acao_b3(self, ativo: str):
        data = {
            "ITSA4": 9.74,
            "ITUB4": 28.64,
            "IRBR3": 38.88,
            "MGLU3": 3.70,
            "BBAS3": 50.08,
            "CMIG4": 12.67,
            "TAEE3": 12.58,
            "MMM": 104.54,        
        }

        return data[ativo]

    def calcular_patrimonio_moeda(self, dono: str):
        df = self.moedas.copy()
        df = df[df['dono'] == dono]
        df = df[df['ativo'] == 'dolar']
        df = df.sort_values(['data'])
        dolares = df['valor'].sum()

        df_p = self.proventos.copy()
        df_p = df_p[df_p['dono'] == dono]
        proventos_dolar = df_p[df_p['moeda'] == 'dolar'].sum()['valor']
        proventos_real = df_p[df_p['moeda'] == 'real'].sum()['valor']

        return {"dolares": dolares, "proventos_dolar": proventos_dolar, "proventos_real": proventos_real}


    def calcular_patrimonio_reservas(self, dono: str):
        df = self.cdi.copy()
        df = df[df['dono'] == dono]
        df_reservas = df[df['tag'] == 'reservas']
        df_caixa_investimentos = df[df['tag'] == 'caixa_investimentos']
        df_robank_dayane = df[df['tag'] == 'robank_dayane']
        reservas = df_reservas['valor'].sum()
        caixa_investimentos = df_caixa_investimentos['valor'].sum()
        robank_dayane = df_robank_dayane['valor'].sum()

        return {"reservas": reservas, "caixa_investimentos": caixa_investimentos, "robank_dayane": robank_dayane}


    def calcular_patrimonio_acoes(self, dono: str):
        df = self.trades.copy()

        df = df[df['dono'] == dono]

        acoes_real = df[df['moeda'] == 'real']
        acoes_real = list(acoes_real['ativo'])
        acoes_real = sorted(set(acoes_real))

        acoes_dolar = df[df['moeda'] == 'dolar']
        acoes_dolar = list(acoes_dolar['ativo'])
        acoes_dolar = sorted(set(acoes_dolar))

        acoes = {"real": {}, "dolar": {}}

        for a in acoes_real:
            df_temp = df[df['ativo'] == a]
            acoes["real"][a] = {"quantidade": df_temp['quantidade'].sum(), "preco_atual": self.get_preco_acao_b3(ativo=a)}

        for a in acoes_dolar:
            df_temp = df[df['ativo'] == a]
            acoes["dolar"][a] = {"quantidade": df_temp['quantidade'].sum(), "preco_atual": self.get_preco_acao_b3(ativo=a)}

        return acoes


    def calcular_patrimonio(self, dono: str):
        dolar_hoje = 5.30
        patrimonio_moeda = self.calcular_patrimonio_moeda(dono)
        patrimonio_reserva = self.calcular_patrimonio_reservas(dono)
        patrimonio_acoes = self.calcular_patrimonio_acoes(dono)

        # print(patrimonio_moeda)
        # print(patrimonio_reserva)
        # print(patrimonio_acoes)

        real = patrimonio_moeda['proventos_real'] + patrimonio_reserva['reservas'] + patrimonio_reserva['caixa_investimentos'] + patrimonio_reserva['robank_dayane']
        dolar = patrimonio_moeda['proventos_dolar'] + patrimonio_moeda['dolares']
        ativos_real = 0
        ativos_dolar = 0

        for key, value in patrimonio_acoes['real'].items():
            ativos_real = (value['quantidade'] * value['preco_atual']) + ativos_real

        for key, value in patrimonio_acoes['dolar'].items():
            ativos_dolar = (value['quantidade'] * value['preco_atual']) + ativos_dolar

        print(f"Real: {real:,.2f}")
        print(f"Dolar: {dolar:,.2f} ({dolar*dolar_hoje:,.2f})")
        print(f"Ativos Real: {ativos_real:,.2f}")
        print(f"Ativos Dolar: {ativos_dolar:,.2f} ({ativos_dolar*dolar_hoje:,.2f})")

        return real + ativos_real + (dolar * dolar_hoje) + (ativos_dolar * dolar_hoje)
