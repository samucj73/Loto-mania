import random

def gerar_cartoes_lotomania(estatisticas, probabilidades, qtd_cartoes=10, fixas=None, excluidas=None):
    fixas = set(fixas) if fixas else set()
    excluidas = set(excluidas) if excluidas else set()
    
    mais_frequentes = set(probabilidades["mais_frequentes"])
    menos_frequentes = set(probabilidades["menos_frequentes"])

    cartoes = []
    tentativas_max = qtd_cartoes * 10
    tentativas = 0

    while len(cartoes) < qtd_cartoes and tentativas < tentativas_max:
        dezenas = set(fixas)
        while len(dezenas) < 50:
            d = random.randint(1, 100)
            if d in dezenas or d in excluidas:
                continue
            dezenas.add(d)

        dezenas = list(dezenas)
        dezenas.sort()

        if len(set(dezenas) & menos_frequentes) > 5:
            tentativas += 1
            continue

        pares = len([d for d in dezenas if d % 2 == 0])
        if abs(pares - probabilidades["media_pares"]) > 3:
            tentativas += 1
            continue

        soma = sum(dezenas)
        if abs(soma - probabilidades["media_soma"]) > 150:
            tentativas += 1
            continue

        seq = 1
        max_seq = 1
        for i in range(1, len(dezenas)):
            if dezenas[i] == dezenas[i - 1] + 1:
                seq += 1
                max_seq = max(max_seq, seq)
            else:
                seq = 1
        if max_seq < int(probabilidades["media_sequencias"]):
            tentativas += 1
            continue

        altas = len([d for d in dezenas if d > 50])
        media_altas = probabilidades["alta_baixa_balanceado"]["media_altas"]
        if abs(altas - media_altas) > 5:
            tentativas += 1
            continue

        cartoes.append(dezenas)
        tentativas = 0

    return cartoes
