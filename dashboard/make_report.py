from dashboard.scripts.analytics import Analytics

calculadora =  Analytics()


class MakeReport:

    def __init__(self):
        self.calculadora =  Analytics()
        dolar_hoje = self.calculadora.get_price('USDBRL=X')
    
    def tipo_moeda(self, moeda:str) -> str:
        if moeda == 'real':
            m = 'R$'
        elif moeda == 'dolar':
            m = '$'
        else:
            m = '?'

        return m
    
    def tabela_renda_fixa(self, dono: str) -> str:
        renda_fixa = calculadora.calcular_cdi_proventos(dono=dono)
        str_result = ""

        for key, ativo in renda_fixa.items():
            tipo_m = self.tipo_moeda(ativo['moeda'])
            if ativo["valor"] <= 0:
                continue

            valor = ativo['valor']
            valor = f'{tipo_m} {valor:,.2f}'
            
            variacao = (ativo["rendimento"]/ativo["valor"])*100
            variacao = f'% {variacao:,.2f}'

            rendimento = ativo['rendimento']
            rendimento = f'{tipo_m} {rendimento:,.2f}'

            str_line = f"""
                <tr>
                    <td>{key}</td>
                    <td>{valor}</td>
                    <td>{variacao}</td>
                    <td>{rendimento}</td>
                </tr>
"""
            str_result += str_line

        return str_result

    def tabela_ativos(self, dono: str) -> str:
        ativos = self.calculadora.calcular_valorizacao_ativos(dono)
        proventos = calculadora.calcular_ativos_proventos(dono=dono)
        str_result = ""

        for key, ativo in ativos.items():
            tipo_m = self.tipo_moeda(ativo['moeda'])

            quantidade = int(ativo['quantidade'])
            valor = ativo['price_today'] * ativo['quantidade']
            valor = f'{tipo_m} {valor:,.2f}'

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
                    <td>{valor}</td>
                    <td>{variacao}</td>
                    <td>{prov}</td>
                    <td class="vazio"></td>
                    <td>{preco_medio}</td>
                    <td>{preco_hoje}</td>
                </tr>
"""
            str_result += str_line

        return str_result

    def create_html(self, dono: str):
        patrimonio_total = self.calculadora.calcular_patrimonio(dono)

        tabela_ativo = self.tabela_ativos(dono=dono)
        tabela_renda_fixa = self.tabela_renda_fixa(dono=dono)
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Rodrigo</title>
    <link rel="stylesheet" href="css/main.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Lato&display=swap" rel="stylesheet">
</head>
<body class="doc">
    <div class="header">
        <h1>Relátório patrimonial</h1>
        <h3>Patrimonio total:  R$ 112,565.13 - % 6.08</h3>
        <div class="imagem_001"><img src="img/foo.png"></div>
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
                <tr>
                    <td>Real Renda Fixa</td>
                    <td>R$ 49,262.00</td>
                    <td>R$ 49,262.00</td>
                    <td>% 2.50</td>
                </tr>
                <tr>
                    <td>Real Ações</td>
                    <td>R$ 41,523.75</td>
                    <td>R$ 41,523.75</td>
                    <td>% 31.00</td>
                </tr>
                <tr>
                    <td>Real Caixa</td>
                    <td>R$ 2,481.00</td>
                    <td>R$ 2,481.00</td>
                    <td>% 0.00</td>
                </tr>
                <tr>
                    <td>Dolar Renda Fixa</td>
                    <td>$ 0.00</td>
                    <td>R$ 0.00</td>
                    <td>% 0.00</td>
                </tr>
                <tr>
                    <td>Dolar Ações</td>
                    <td>$ 2,001.00</td>
                    <td>R$ 9,751.87</td>
                    <td>% -0.50</td>
                </tr>
                <tr>
                    <td>Dolar Caixa</td>
                    <td>$ 2,467.94</td>
                    <td>R$ 12,027.51</td>
                    <td>% 0.00</td>
                </tr>
            </tbody>
        </table>

    </div>
    <div class="renda_fixa">
        <div class="imagem_002"><img src="img/foo.png"></div>
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
        <div class="imagem_003"><img src="img/foo.png"></div>
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
        with open('dashboard/test_report.html', 'w') as f:
            f.write(html)
