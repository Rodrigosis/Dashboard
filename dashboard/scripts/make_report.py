import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from typing import List, Tuple
import os

from dashboard.scripts.analytics import Analytics

calculadora =  Analytics()


class MakeReport:

    def __init__(self):
        self.calculadora =  Analytics()
        self.dolar_hoje = self.calculadora.get_price('USDBRL=X')
        self.data_acoes = []
        self.data_r_fixa = []
        self.data_patrimonio = []

    def tipo_moeda(self, moeda:str) -> str:
        if moeda == 'real':
            m = 'R$'
        elif moeda == 'dolar':
            m = '$'
        else:
            m = '?'

        return m
    
    def create_graphcs(self, dono: str, name: str, dados: List[Tuple]):
        path = os.path.dirname(os.path.abspath(__file__))

        labels = []
        sizes = []
        for i in dados:
            if i[0] == dono:
                if i[2] < 0:
                    print(f"VALOR NEGATIVO {dono} label {i[1]} - {str(i[2])}")
                elif i[2] < 100:
                    print(f"VALOR INSIGNIFICANTE {dono} label {i[1]} - {str(i[2])}")
                else:
                    labels.append(i[1])
                    sizes.append(i[2])

        fig, ax = plt.subplots()
        # fig.set_size_inches(18.5, 10.5)
        ax.pie(sizes, labels=labels, autopct='%1.1f%%')
        ax.set_facecolor(color=None)
        plt.savefig(path + f"/../img/{name}.png", dpi=100)
    
    def percentual_carteira(self, total: float, valor: float, moeda: str) -> float:
        dolar_hoje = self.dolar_hoje

        if total != 0:
            if moeda == 'real':
                result = (valor/total)*100
            elif moeda == 'dolar':
                result = ((valor*dolar_hoje)/total)*100
        else:
            return 0
        
        return result
    
    def tabela_header(self, dono: str) -> str:
        dolar_hoje = self.dolar_hoje
        patrimonio = calculadora.calcular_patrimonio(dono=dono)
        str_result = ""

        result_dict = {}
        result_dict['Real Renda Fixa'] = {
            'valor': patrimonio['real_renda_fixa'], 'moeda': 'real',
            'valor_reais': patrimonio['real_renda_fixa'],
            'percentual': self.percentual_carteira(patrimonio['patrimonio_total'], 
                                                   patrimonio['real_renda_fixa'], 'real')}
        result_dict['Real Ações'] = {
            'valor': patrimonio['real_acoes'], 'moeda': 'real',
            'valor_reais': patrimonio['real_acoes'],
            'percentual': self.percentual_carteira(patrimonio['patrimonio_total'], 
                                                   patrimonio['real_acoes'], 'real')}
        result_dict['Real Caixa'] = {
            'valor': patrimonio['real_caixa'], 'moeda': 'real',
            'valor_reais': patrimonio['real_caixa'],
            'percentual': self.percentual_carteira(patrimonio['patrimonio_total'], 
                                                   patrimonio['real_caixa'], 'real')}
        result_dict['Dolar Renda Fixa'] = {
            'valor': patrimonio['dolar_renda_fixa'], 'moeda': 'dolar',
            'valor_reais': (patrimonio['dolar_renda_fixa'] * dolar_hoje),
            'percentual': self.percentual_carteira(patrimonio['patrimonio_total'], 
                                                   patrimonio['dolar_renda_fixa'], 'dolar')}
        result_dict['Dolar Ações'] = {
            'valor': patrimonio['dolar_acoes'], 'moeda': 'dolar',
            'valor_reais': (patrimonio['dolar_acoes'] * dolar_hoje),
            'percentual': self.percentual_carteira(patrimonio['patrimonio_total'], 
                                                   patrimonio['dolar_acoes'], 'dolar')}
        result_dict['Dolar Caixa'] = {
            'valor': patrimonio['dolar_caixa'], 'moeda': 'dolar',
            'valor_reais': (patrimonio['dolar_caixa'] * dolar_hoje),
            'percentual': self.percentual_carteira(patrimonio['patrimonio_total'], 
                                                   patrimonio['dolar_caixa'], 'dolar')}
        
        for key, ativo in result_dict.items():
            tipo_m = self.tipo_moeda(ativo['moeda'])

            str_line = f"""
                <tr>
                    <td>{key}</td>
                    <td>{tipo_m} {ativo['valor']:,.2f}</td>
                    <td>R$ {ativo['valor_reais']:,.2f}</td>
                    <td>% {ativo['percentual']:,.2f}</td>
                </tr>
"""
            str_result += str_line

            self.data_patrimonio.append((dono, key, ativo['valor_reais'], ativo['valor']))

        return str_result
    
    def tabela_renda_fixa(self, dono: str) -> str:
        renda_fixa = calculadora.calcular_cdi_proventos(dono=dono)
        str_result = ""

        for key, ativo in renda_fixa.items():
            tipo_m = self.tipo_moeda(ativo['moeda'])
            if ativo["valor"] <= 0:
                continue

            valor = ativo['valor']
            valor_str = f'{tipo_m} {valor:,.2f}'
            
            variacao = (ativo["rendimento"]/ativo["valor"])*100
            variacao = f'% {variacao:,.2f}'

            rendimento = ativo['rendimento']
            rendimento = f'{tipo_m} {rendimento:,.2f}'

            str_line = f"""
                <tr>
                    <td>{key}</td>
                    <td>{valor_str}</td>
                    <td>{variacao}</td>
                    <td>{rendimento}</td>
                </tr>
"""
            str_result += str_line

            self.data_r_fixa.append((dono, key, valor))

        return str_result

    def tabela_ativos(self, dono: str) -> str:
        ativos = self.calculadora.calcular_valorizacao_ativos(dono)
        proventos = calculadora.calcular_ativos_proventos(dono=dono)
        str_result = ""

        for key, ativo in ativos.items():
            tipo_m = self.tipo_moeda(ativo['moeda'])

            quantidade = int(ativo['quantidade'])
            valor = ativo['price_today'] * ativo['quantidade']
            valor_str = f'{tipo_m} {valor:,.2f}'

            variacao = ativo['valorizacao'] * 100
            variacao = f'% {variacao:,.2f}'

            prov = 0
            if key in proventos:
                prov = proventos[key]['proventos']
            prov = f'{tipo_m} {prov:,.2f}'

            preco_medio = ativo['preco_medio']
            preco_medio = f'{tipo_m} {preco_medio:,.2f}'

            preco_hoje = ativo['price_today']
            preco_hoje = f'{tipo_m} {preco_hoje:,.2f}'

            str_line = f"""
                <tr>
                    <td>{key}</td>
                    <td>{quantidade}</td>
                    <td>{valor_str}</td>
                    <td>{variacao}</td>
                    <td>{prov}</td>
                    <td class="vazio"></td>
                    <td>{preco_medio}</td>
                    <td>{preco_hoje}</td>
                </tr>
"""
            str_result += str_line

            if key in ['MMM', 'PG', 'JNJ', 'T', 'XOM', 'CVX']:
                self.data_acoes.append((dono, key, valor*self.dolar_hoje))
            else:
                self.data_acoes.append((dono, key, valor))

        return str_result

    def create_html(self, dono: str):
        dolar_hoje = self.dolar_hoje
        patrimonio = calculadora.calcular_patrimonio(dono=dono)
        rentabilidade_ativos = calculadora.calcular_rentabilidade_ativos(dono=dono)
        proventos_renda_fixa = calculadora.calcular_proventos_renda_fixa(dono=dono)
        proventos_ativos = calculadora.calcular_proventos_ativos(dono=dono)

        proventos_totais = proventos_renda_fixa + proventos_ativos
        rendimento_total = rentabilidade_ativos + proventos_totais

        rendimento_total_porcentagem = (rendimento_total/patrimonio['patrimonio_total']) * 100

        tabela_ativo = self.tabela_ativos(dono=dono)
        tabela_renda_fixa = self.tabela_renda_fixa(dono=dono)
        tabela_header = self.tabela_header(dono=dono)

        self.create_graphcs(dono, f'{dono}_acoes', self.data_acoes)
        self.create_graphcs(dono, f'{dono}_data_r_fixa', self.data_r_fixa)
        self.create_graphcs(dono, f'{dono}_data_patrimonio', self.data_patrimonio)

        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{dono.title()}</title>
    <link rel="stylesheet" href="css/main.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Lato&display=swap" rel="stylesheet">
</head>
<body class="doc">
    <div class="header">
        <h1>Relátório patrimonial</h1>
        <h3>Patrimonio total: R$ {patrimonio['patrimonio_total']:,.2f}</h3>
        <h4>Patrimonio em reais: R$ {patrimonio['patrimonio_real']:,.2f}</h4>
        <h4>Patrimonio em dolares: $ {patrimonio['patrimonio_dolar']:,.2f} (R$ {(patrimonio['patrimonio_dolar']*dolar_hoje):,.2f})</h4>
        </br>
        <h5>Rentabilidade Ativos em reais: R$ {rentabilidade_ativos:,.2f}</h5>
        <h5>Proventos Ativos: R$ {proventos_ativos:,.2f}</h5>
        <h5>Proventos Renda Fixa em reais: R$ {proventos_renda_fixa:,.2f}</h5>
        <h5>Proventos totais em reais: R$ {proventos_totais:,.2f}</h5>
        </br>
        <h5>Rentabilidade: R$ {rendimento_total:,.2f} ({f'% {rendimento_total_porcentagem:,.2f}'})</h5>

        <div class="imagem_001"><img src="img/{dono}_data_patrimonio.png"></div>
        <table class="table_header">
            <thead>
                <tr>
                    <th class="col_ativo">Ativo</th>
                    <th class="col_valor">Valor</th>
                    <th class="col_real">(Real)</th>
                    <th class="col_percentual">Percentual</th>
                </tr>
            </thead>
            <tbody>
                {tabela_header}
            </tbody>
        </table>

    </div>
    <div class="renda_fixa">
        <div class="imagem_002"><img src="img/{dono}_data_r_fixa.png"></div>
        <table class="table_renda_fixa">
            <thead>
                <tr>
                    <th class="col_ativo">Ativo</th>
                    <th class="col_valor">Valor</th>
                    <th class="col_variacao">Variação</th>
                    <th class="col_rendimento">Rendimento</th>
                </tr>
            </thead>
            <tbody>
                {tabela_renda_fixa}
            </tbody>
        </table>
    </div>
    <div class="renda_variavel">
        <div class="imagem_003"><img src="img/{dono}_acoes.png"></div>
        <table class="table_ativos">
            <thead>
                <tr>
                    <th class="col_ativo">Ativo</th>
                    <th class="col_cotas">Cotas</th>
                    <th class="col_valor">Valor</th>
                    <th class="col_variacao">Variação</th>
                    <th class="col_proventos">Proventos</th>
                    <th class="col_vazio"></th>
                    <th class="col_preco_medio">P. Médio</th>
                    <th class="col_preco_hoje">P. Hoje</th>
                </tr>
            </thead>
            <tbody>
                {tabela_ativo}
            </tbody>
        </table>
    </div>
    <div class="fundo_imobiliario">
        
    </div>
</body>
</html>
        """
        with open(f'dashboard/{dono}_report.html', 'w', encoding='utf-8') as f:
            f.write(html)
