def conferir_cartoes(cartoes, concursos):
    resultados = []
    for cartao in cartoes:
        acertos = []
        for resultado in concursos:
            acerto = len(set(cartao).intersection(set(resultado)))
            acertos.append(acerto)
        resultados.append(acertos)
    return resultados

def calcular_retorno(cartoes, concursos):
    premios = {
        20: 500000,
        19: 25000,
        18: 1500,
        17: 200,
        16: 50,
        15: 10,
        # Remove premiação para 0 acertos, pois não é realista na Lotomania
    }
    custo_total = len(cartoes) * 3.0
    retorno_total = 0

    resultados = conferir_cartoes(cartoes, concursos)
    for acertos_por_cartao in resultados:
        max_acertos = max(acertos_por_cartao)
        retorno_total += premios.get(max_acertos, 0)

    saldo = retorno_total - custo_total
    return custo_total, retorno_total, saldo
