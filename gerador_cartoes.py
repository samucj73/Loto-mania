import random

def gerar_cartoes(estatisticas, quantidade=10):
    dezenas_por_freq = [dezena for dezena, _ in estatisticas["mais_frequentes"]]
    todas_dezenas = list(range(100))

    cartoes = []
    for _ in range(quantidade):
        # Seleciona até 15 dezenas mais frequentes (ou menos, se não houver tantas)
        qtd_mais_frequentes = min(15, len(dezenas_por_freq))
        dezenas_mais_freq = random.sample(dezenas_por_freq, qtd_mais_frequentes)
        
        # Completa as dezenas restantes para totalizar 50
        restantes = list(set(todas_dezenas) - set(dezenas_mais_freq))
        dezenas_restantes = random.sample(restantes, 50 - qtd_mais_frequentes)
        
        cartao = sorted(dezenas_mais_freq + dezenas_restantes)
        cartoes.append(cartao)
    return cartoes
