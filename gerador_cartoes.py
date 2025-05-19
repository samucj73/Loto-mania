import random

def gerar_cartoes(estatisticas, quantidade=10):
    todas_dezenas = list(range(100))
    mais_freq = [dezena for dezena, _ in estatisticas["mais_frequentes"]]
    menos_freq = [dezena for dezena, _ in estatisticas["menos_frequentes"]]
    
    def gerar_classico():
        qtd_mais_frequentes = min(15, len(mais_freq))
        dezenas_mais_freq = random.sample(mais_freq, qtd_mais_frequentes)
        restantes = list(set(todas_dezenas) - set(dezenas_mais_freq))
        dezenas_restantes = random.sample(restantes, 50 - qtd_mais_frequentes)
        return sorted(dezenas_mais_freq + dezenas_restantes)

    def gerar_balanceado():
        pares = [d for d in todas_dezenas if d % 2 == 0]
        impares = [d for d in todas_dezenas if d % 2 != 0]
        altas = [d for d in todas_dezenas if d >= 50]
        baixas = [d for d in todas_dezenas if d < 50]

        qtd_pares = round(estatisticas['pares_med'])
        qtd_impares = 50 - qtd_pares

        dezenas = set(random.sample(pares, qtd_pares) + random.sample(impares, qtd_impares))
        # Ajuste para soma aproximada
        while True:
            soma = sum(dezenas)
            if abs(soma - estatisticas['soma_media']) <= 100:
                break
            dezenas = set(random.sample(todas_dezenas, 50))
        return sorted(dezenas)

    def gerar_por_quadrantes():
        quadrantes = {
            1: [i for i in range(0, 25)],
            2: [i for i in range(25, 50)],
            3: [i for i in range(50, 75)],
            4: [i for i in range(75, 100)],
        }
        dezenas = []
        for q in quadrantes.values():
            dezenas += random.sample(q, 12)  # 4 quadrantes x 12 = 48
        dezenas += random.sample(list(set(todas_dezenas) - set(dezenas)), 2)
        return sorted(dezenas)

    def gerar_aleatorio_filtrado():
        while True:
            dezenas = sorted(random.sample(todas_dezenas, 50))
            soma = sum(dezenas)
            pares = len([d for d in dezenas if d % 2 == 0])
            repetidas = random.randint(10, 30)  # estimativa

            if (
                abs(soma - estatisticas['soma_media']) < 100 and
                abs(pares - estatisticas['pares_med']) <= 5 and
                abs(repetidas - estatisticas['media_repetidas']) <= 5
            ):
                return dezenas

    # Estratégias disponíveis
    estrategias = [
        gerar_classico,
        gerar_balanceado,
        gerar_por_quadrantes,
        gerar_aleatorio_filtrado,
    ]

    cartoes = []
    for i in range(quantidade):
        estrategia = estrategias[i % len(estrategias)]
        cartao = estrategia()
        cartoes.append(cartao)

    return cartoes
