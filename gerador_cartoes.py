import random

def gerar_cartoes(estatisticas, quantidade=10):
    dezenas_por_freq = [dezena for dezena, _ in estatisticas["mais_frequentes"]]
    todas_dezenas = list(range(100))

    cartoes = []
    for _ in range(quantidade):
        qtd_mais_frequentes = min(15, len(dezenas_por_freq))
        dezenas_mais_freq = random.sample(dezenas_por_freq, qtd_mais_frequentes)
        restantes = list(set(todas_dezenas) - set(dezenas_mais_freq))
        dezenas_restantes = random.sample(restantes, 50 - qtd_mais_frequentes)
        cartao = sorted(dezenas_mais_freq + dezenas_restantes)
        cartoes.append(cartao)
    return cartoes

def gerar_cartoes_equilibrados(quantidade=10):
    todas_dezenas = list(range(100))
    cartoes = []
    for _ in range(quantidade):
        pares = [d for d in todas_dezenas if d % 2 == 0]
        impares = [d for d in todas_dezenas if d % 2 != 0]
        altas = [d for d in todas_dezenas if d > 49]
        baixas = [d for d in todas_dezenas if d <= 49]

        num_pares = random.randint(24, 26)
        num_impares = 50 - num_pares
        num_altas = random.randint(24, 26)
        num_baixas = 50 - num_altas

        selecionados = set(random.sample(pares, num_pares) + random.sample(impares, num_impares))
        selecionados = list(selecionados & set(altas))[:num_altas] + list(selecionados & set(baixas))[:num_baixas]

        while len(selecionados) < 50:
            n = random.choice(todas_dezenas)
            if n not in selecionados:
                selecionados.append(n)

        cartoes.append(sorted(selecionados))
    return cartoes

def gerar_cartoes_frio_quente(estatisticas, quantidade=10):
    mais_frequentes = [dezena for dezena, _ in estatisticas["mais_frequentes"]]
    menos_frequentes = [dezena for dezena, _ in estatisticas["menos_frequentes"]]
    todas_dezenas = list(range(100))

    cartoes = []
    for _ in range(quantidade):
        qtd_quentes = random.randint(20, 30)
        qtd_frias = 50 - qtd_quentes
        dezenas_quentes = random.sample(mais_frequentes, min(qtd_quentes, len(mais_frequentes)))
        dezenas_frias = random.sample(menos_frequentes, min(qtd_frias, len(menos_frequentes)))
        restantes = list(set(todas_dezenas) - set(dezenas_quentes) - set(dezenas_frias))
        while len(dezenas_quentes + dezenas_frias) < 50:
            r = random.choice(restantes)
            if r not in dezenas_quentes + dezenas_frias:
                if len(dezenas_quentes) < qtd_quentes:
                    dezenas_quentes.append(r)
                else:
                    dezenas_frias.append(r)
        cartoes.append(sorted(dezenas_quentes + dezenas_frias))
    return cartoes

def gerar_cartoes_por_quadrantes(estatisticas, quantidade=10):
    todas_dezenas = list(range(100))
    quadrantes = {
        "Q1": [d for d in todas_dezenas if d <= 49 and d % 10 <= 4],
        "Q2": [d for d in todas_dezenas if d <= 49 and d % 10 > 4],
        "Q3": [d for d in todas_dezenas if d > 49 and d % 10 <= 4],
        "Q4": [d for d in todas_dezenas if d > 49 and d % 10 > 4],
    }

    cartoes = []
    for _ in range(quantidade):
        cartao = []
        for q in quadrantes.values():
            qtd = 12 if len(cartao) < 48 else 50 - len(cartao)
            cartao.extend(random.sample(q, qtd))
        cartoes.append(sorted(cartao))
    return cartoes
