import random

def gerar_cartoes(estatisticas, quantidade=10):
    dezenas_por_freq = [dezena for dezena, _ in estatisticas["mais_frequentes"]]
    todas_dezenas = list(range(100))

    cartoes = []
    for _ in range(quantidade):
        dezenas_com_peso = sorted(
            random.sample(dezenas_por_freq, min(15, len(dezenas_por_freq)))
            + random.sample(list(set(todas_dezenas) - set(dezenas_por_freq)), 35)
        )
        cartoes.append(sorted(set(dezenas_com_peso)))
    return cartoes
