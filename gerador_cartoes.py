import random

def gerar_cartoes(estatisticas, quantidade=10):
    dezenas_mais_frequentes = [dezena for dezena, _ in estatisticas["mais_frequentes"]]
    todas_dezenas = list(range(100))

    # Quadrantes: definindo 4 quadrantes da cartela 0-99
    quadrantes = {
        1: list(range(0, 25)),    # Quadrante 1: 00-24
        2: list(range(25, 50)),   # Quadrante 2: 25-49
        3: list(range(50, 75)),   # Quadrante 3: 50-74
        4: list(range(75, 100))   # Quadrante 4: 75-99
    }

    # Quantidade ideal por quadrante (pode ser ajustada)
    ideal_por_quadrante = 12  # 12x4 = 48, o resto preenche aleatoriamente

    cartoes = []
    for _ in range(quantidade):
        cartao = []

        # Selecionar dezenas mais frequentes, distribuídas nos quadrantes
        for q in quadrantes:
            # Filtra as dezenas mais frequentes que pertencem a esse quadrante
            mais_freq_q = [d for d in dezenas_mais_frequentes if d in quadrantes[q]]

            # Se tiver menos dezenas que o ideal, pega todas, senão amostra
            qtd_pegada = min(ideal_por_quadrante, len(mais_freq_q))
            selecionadas_q = random.sample(mais_freq_q, qtd_pegada) if qtd_pegada > 0 else []

            cartao.extend(selecionadas_q)

        # Se ainda faltar completar para 50 dezenas, preenche com dezenas restantes aleatórias
        faltam = 50 - len(cartao)
        usadas = set(cartao)
        restantes = list(set(todas_dezenas) - usadas)
        cartao.extend(random.sample(restantes, faltam))

        # Balancear pares e ímpares aproximando da média histórica
        media_pares = estatisticas.get("pares_med", 25)  # média esperada de pares (exemplo 25)
        pares_atual = sum(1 for d in cartao if d % 2 == 0)

        # Ajustar se houver muito desbalanceamento (>2 dezenas)
        while pares_atual > media_pares + 2:
            # Trocar um par por um ímpar disponível
            pares_no_cartao = [d for d in cartao if d % 2 == 0]
            impares_disponiveis = [d for d in restantes if d % 2 != 0]
            if not pares_no_cartao or not impares_disponiveis:
                break
            para_remover = random.choice(pares_no_cartao)
            para_adicionar = random.choice(impares_disponiveis)
            cartao.remove(para_remover)
            cartao.append(para_adicionar)
            pares_atual -= 1

        while pares_atual < media_pares - 2:
            # Trocar um ímpar por um par disponível
            impares_no_cartao = [d for d in cartao if d % 2 != 0]
            pares_disponiveis = [d for d in restantes if d % 2 == 0]
            if not impares_no_cartao or not pares_disponiveis:
                break
            para_remover = random.choice(impares_no_cartao)
            para_adicionar = random.choice(pares_disponiveis)
            cartao.remove(para_remover)
            cartao.append(para_adicionar)
            pares_atual += 1

        cartoes.append(sorted(cartao))

    return cartoes
