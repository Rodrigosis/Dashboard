import pandas as pd
import os

from dashboard.scripts.cotacao import Cotacao


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

        dolares = df[df['ativo'] == 'dolar']
        dolares = dolares['valor'].sum()

        reais = df[df['ativo'] == 'real']
        reais = reais['valor'].sum()

        return {"dolares": dolares, "reais": reais}

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

        moeda = self.calcular_patrimonio_moeda(dono)
        renda_fixa = self.calcular_cdi_proventos(dono)
        acoes = self.calcular_patrimonio_acoes(dono)

        reais = moeda['reais']
        dolares = moeda['dolares']

        renda_fixa_dolar = 0
        renda_fixa_real = 0
        for key, ativo in renda_fixa.items():
            if ativo['moeda'] == 'real':
                renda_fixa_real += ativo['valor']
            elif ativo['moeda'] == 'dolar':
                renda_fixa_dolar += ativo['valor']

        acoes_real = 0
        acoes_dolar = 0
        for key, value in acoes['real'].items():
            acoes_real = (value['quantidade'] * value['preco_atual']) + acoes_real

        for key, value in acoes['dolar'].items():
            acoes_dolar = (value['quantidade'] * value['preco_atual']) + acoes_dolar

        patrimonio = {"real_caixa": reais,
                      "real_acoes": acoes_real,
                      "real_renda_fixa": renda_fixa_real,
                      "dolar_caixa": dolares,
                      "dolar_acoes": acoes_dolar,
                      "dolar_renda_fixa": renda_fixa_dolar}
        
        patrimonio_real = patrimonio['real_caixa'] + patrimonio['real_acoes'] + patrimonio['real_renda_fixa']
        patrimonio_dolar =  patrimonio['dolar_caixa'] + patrimonio['dolar_acoes'] + patrimonio['dolar_renda_fixa']

        patrimonio_total = patrimonio_real + (patrimonio_dolar*dolar_hoje)
        patrimonio['patrimonio_real'] = patrimonio_real
        patrimonio['patrimonio_dolar'] = patrimonio_dolar
        patrimonio['patrimonio_total'] = patrimonio_total

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
            
            moeda = df_ativo['moeda'].to_list()[0]
            valorizacao = (valor_hoje/valor_compra)-1
            preco_medio = valor_compra/quantidade
            results[ativo] = {'price_today': price, 'quantidade': quantidade, 'valorizacao': valorizacao, 'valor_investido': valor_compra, 'preco_medio': preco_medio, 'moeda': moeda}
        
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

            moeda = df_caixa['moeda'].to_list()[0]

            results[caixa] = {'valor': valor, 'rendimento': rendimento, 'moeda': moeda}
        
        return results
