from scripts.analytics import Analytics

calculadora =  Analytics()


class MakeReport:

    def __init__(self):
        self.calculadora =  Analytics()

    def create_html(self, dono: str):
        patrimonio_total = self.calculadora.calcular_patrimonio(dono)

        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Games</title>
    <link rel="stylesheet" href="css/main.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Lato&display=swap" rel="stylesheet">
</head>
<body class="containers">
    {divs}
</body>
</html>
        """
