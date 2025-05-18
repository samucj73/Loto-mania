def conferir_cartoes(cartoes, concursos, preco_por_jogo=3.00):
    premios_estimados = {
        20: 3000000,
        19: 50000,
        18: 3000,
        17: 300,
        16: 50,
        15: 20
    }

    resultados = []
    total_premio = 0
    total_gasto = len(cartoes) * preco_por_jogo

    for cartao in cartoes:
        resultado = {
            "cartao": cartao,
            "resultados": [],
            "melhor_acerto": 0,
            "premio": 0
        }

        for concurso in concursos:
            acertos = len(set(cartao) & set(concurso))
            if acertos >= 15:
                resultado["resultados"].append(acertos)
                resultado["melhor_acerto"] = max(resultado["melhor_acerto"], acertos)
                resultado["premio"] += premios_estimados.get(acertos, 0)

        total_premio += resultado["premio"]
        resultados.append(resultado)

    return {
        "cartoes_conferidos": len(cartoes),
        "total_gasto": total_gasto,
        "total_premio": total_premio,
        "lucro_ou_prejuizo": total_premio - total_gasto,
        "detalhado": resultados
    }
