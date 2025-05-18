def calcular_probabilidades(estatisticas):
    soma_media = sum(estatisticas["somas"]) / len(estatisticas["somas"])
    pares_media = estatisticas["pares_med"]
    repetidas_media = sum(estatisticas["repetidas"]) / len(estatisticas["repetidas"])
    sequencias_media = sum(estatisticas["sequencias"]) / len(estatisticas["sequencias"])

    todas_dezenas = list(estatisticas["frequencia"].items())
    todas_dezenas.sort(key=lambda x: x[1], reverse=True)

    mais_frequentes = [d[0] for d in todas_dezenas[:30]]
    menos_frequentes = [d[0] for d in todas_dezenas[-30:]]

    altas = [d for d in estatisticas["frequencia"] if d > 50]
    media_altas = len(altas) / len(estatisticas["frequencia"])

    return {
        "media_soma": soma_media,
        "media_pares": pares_media,
        "media_repetidas": repetidas_media,
        "media_sequencias": sequencias_media,
        "mais_frequentes": mais_frequentes,
        "menos_frequentes": menos_frequentes,
        "alta_baixa_balanceado": {"media_altas": media_altas}
    }
