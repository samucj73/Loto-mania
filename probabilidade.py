def calcular_probabilidades(estatisticas):
    # Calcula a média da soma das dezenas dos concursos
    soma_media = estatisticas["soma_media"]

    # Média de pares nas dezenas sorteadas
    pares_media = estatisticas["pares_med"]

    # Média da quantidade de dezenas repetidas em relação ao concurso anterior
    repetidas_media = estatisticas.get("repetidas_med", 0)

    # Média do tamanho das sequências encontradas
    sequencias_media = estatisticas.get("sequencias_med", 0)

    # Frequência de cada dezena (chave deve ser int)
    frequencia = estatisticas["frequencia"]
    todas_dezenas = list(frequencia.items())
    todas_dezenas.sort(key=lambda x: x[1], reverse=True)

    # Top 30 dezenas mais frequentes
    mais_frequentes = [d[0] for d in todas_dezenas[:30]]

    # Últimas 30 dezenas menos frequentes
    menos_frequentes = [d[0] for d in todas_dezenas[-30:]]

    # Dezenas altas são as > 50
    altas = [d for d in frequencia if d > 50]
    media_altas = len(altas) / len(frequencia) if frequencia else 0

    return {
        "media_soma": soma_media,
        "media_pares": pares_media,
        "media_repetidas": repetidas_media,
        "media_sequencias": sequencias_media,
        "mais_frequentes": mais_frequentes,
        "menos_frequentes": menos_frequentes,
        "alta_baixa_balanceado": {"media_altas": media_altas}
    }
