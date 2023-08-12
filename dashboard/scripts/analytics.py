import pandas as pd
import os

from scripts.cotacao import Cotacao


class Analytics:

    def __init__(self) -> None:
        path = os.path.dirname(os.path.abspath(__file__))
        self.cdi = pd.read_csv(path + "/../csv/CDI.csv")
        self.moedas = pd.read_csv(path + "/../csv/moedas.csv")
        self.proventos = pd.read_csv(path + "/../csv/proventos.csv")
        self.trades = pd.read_csv(path + "/../csv/trades.csv")
        self.get_price = Cotacao().get_price

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
            acoes["real"][a] = {"quantidade": df_temp['quantidade'].sum(), "preco_atual": self.get_price(ativo=a)}

        for a in acoes_dolar:
            df_temp = df[df['ativo'] == a]
            acoes["dolar"][a] = {"quantidade": df_temp['quantidade'].sum(), "preco_atual": self.get_price(ativo=a)}

        return acoes


    def calcular_patrimonio(self, dono: str):
        dolar_hoje = self.get_price('USDBRL=X')
        patrimonio_moeda = self.calcular_patrimonio_moeda(dono)
        patrimonio_reserva = self.calcular_cdi_proventos(dono)
        patrimonio_acoes = self.calcular_patrimonio_acoes(dono)

        real = 0
        for key, caixa in patrimonio_reserva.items():
            real += caixa['valor']

        dolar = patrimonio_moeda['dolares']
        ativos_real = 0
        ativos_dolar = 0

        for key, value in patrimonio_acoes['real'].items():
            ativos_real = (value['quantidade'] * value['preco_atual']) + ativos_real

        for key, value in patrimonio_acoes['dolar'].items():
            ativos_dolar = (value['quantidade'] * value['preco_atual']) + ativos_dolar

        patrimonio_total = real + ativos_real + (dolar * dolar_hoje) + (ativos_dolar * dolar_hoje)

        patrimonio = {"patrimonio_total": patrimonio_total,
                      "patrimonio_moeda_real": real,
                      "patrimonio_moeda_dolar": dolar,
                      "patrimonio_ativos_real": ativos_real,
                      "patrimonio_ativos_dolar": ativos_dolar,
                      "dolar_hoje": dolar_hoje}

        return patrimonio

    def calcular_valorizacao_ativos(self, dono: str):
        df = self.trades.copy()
        df = df[df['dono'] == dono]

        lista_de_ativos = df['ativo']
        lista_de_ativos = list(set(lista_de_ativos))

        results = {}
        for ativo in lista_de_ativos:
            df_ativo = df[df['ativo'] == ativo]

            price = self.get_price(ativo)
            quantidade = df_ativo['quantidade'].sum()
            valor_hoje = price * quantidade

            valor_compra = 0
            for index, i in df_ativo.iterrows():
                if i['tipo_de_ordem'] == 'compra':
                    valor_compra += float(i['preco']) * float(i['quantidade'])

            valorizacao = (valor_hoje/valor_compra)-1
            preco_medio = valor_compra/quantidade
            results[ativo] = {'price_today': price, 'quantidade': quantidade, 'valorizacao': valorizacao, 'valor_investido': valor_compra, 'preco_medio': preco_medio}
        
        return results
    
    def calcular_ativos_proventos(self, dono: str):
        df = self.proventos.copy()
        df = df[df['dono'] == dono]

        lista_de_ativos = df['ativo']
        lista_de_ativos = list(set(lista_de_ativos))

        results = {}
        for ativo in lista_de_ativos:
            df_ativo = df[df['ativo'] == ativo]

            proventos = df_ativo['valor'].sum()
            
            results[ativo] = {'proventos': proventos}
        
        return results
    
    def calcular_cdi_proventos(self, dono: str):
        df = self.cdi.copy()
        df = df[df['dono'] == dono]

        lista_de_caixas = df['tag']
        lista_de_caixas = list(set(lista_de_caixas))

        results = {}
        for caixa in lista_de_caixas:
            df_caixa = df[df['tag'] == caixa]
            valor = df_caixa['valor'].sum()

            df_caixa_rendimento = df_caixa[df_caixa['fonte'] == 'rendimento']
            rendimento = df_caixa_rendimento['valor'].sum()

            results[caixa] = {'valor': valor, 'rendimento': rendimento}
        
        return results
