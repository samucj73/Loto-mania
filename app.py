import streamlit as st
from api_lotomania import obter_ultimos_resultados_lotomania
from estatisticas_lotomania import analisar_concursos
from probabilidade import calcular_probabilidades
from gerador_cartoes import gerar_cartoes
from conferidor import conferir_cartoes, calcular_retorno
import io

st.set_page_config(page_title="Lotomania Inteligente", layout="wide")
st.markdown(
    """
    <style>
    .title, .subtitle {
        text-align: center;
        width: 100%;
    }
    .footer {
        text-align: center;
        color: gray;
        font-size: 0.8em;
        margin-top: 50px;
        padding: 10px;
        border-top: 1px solid #eee;
    }
    </style>
    """, unsafe_allow_html=True
)

st.markdown('<h1 class="title">🎯 Lotomania Inteligente</h1>', unsafe_allow_html=True)

with st.spinner("🔄 Carregando concursos..."):
    concursos_completos = obter_ultimos_resultados_lotomania(25)

if not concursos_completos:
    st.error("❌ Não foi possível carregar os concursos. Verifique sua conexão ou tente novamente mais tarde.")
    st.stop()

# Extrair só as dezenas ordenadas como inteiros
concursos = [sorted([int(d) for d in c['dezenas']]) for c in concursos_completos]
data_ultimo = concursos_completos[0]['data']
num_ultimo = concursos_completos[0]['concurso']

# Estatísticas e probabilidades
estatisticas = analisar_concursos(concursos)
probabilidades = calcular_probabilidades(estatisticas)

st.markdown(f'<h3 class="subtitle">Último Concurso: {num_ultimo} - Data: {data_ultimo}</h3>', unsafe_allow_html=True)

# Abas principais
abas = st.tabs(["📊 Estatísticas", "🎲 Gerador de Cartões", "📋 Conferência", "🔢 Probabilidades"])

with abas[0]:
    st.header("📊 Estatísticas dos Últimos 25 Concursos")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de Concursos", estatisticas["total_concursos"])
    col2.metric("Média Pares", f'{estatisticas["pares_med"]:.2f}')
    col3.metric("Média Ímpares", f'{estatisticas["ímpares_med"]:.2f}')
    col4.metric("Média Soma das Dezenas", f'{estatisticas["soma_media"]:.2f}')

    st.write("### 🔝 Dezenas Mais Frequentes")
    st.write(estatisticas["mais_frequentes"])

    st.write("### 🔻 Dezenas Menos Frequentes")
    st.write(estatisticas["menos_frequentes"])

    st.write("### 📈 Porcentagem de Aparição das Dezenas")
    st.bar_chart(estatisticas["porcentagem_aparicao"])

with abas[1]:
    st.header("🎲 Gerador de Cartões Inteligentes")
    qtd_cartoes = st.slider("Quantidade de cartões a gerar", 1, 50, 10)
    if st.button("🔁 Gerar Cartões"):
        cartoes = gerar_cartoes(estatisticas, qtd_cartoes)
        st.session_state['cartoes_gerados'] = cartoes  # Salvar na sessão para conferência e download
        st.write("### Cartões Gerados")
        for i, cartao in enumerate(cartoes, 1):
            st.write(f"Cartão {i}: {cartao}")

        # Botão para download TXT
        txt_buffer = io.StringIO()
        for i, cartao in enumerate(cartoes, 1):
            txt_buffer.write(f"Cartão {i}: {', '.join(f'{d:02d}' for d in cartao)}\n")
        st.download_button("⬇️ Baixar Cartões (TXT)", data=txt_buffer.getvalue(), file_name="cartoes_lotomania.txt", mime="text/plain")

        # Botão para download PDF (opcional, se quiser depois posso ajudar a gerar)

with abas[2]:
    st.header("📋 Conferência dos Cartões")
    cartoes = st.session_state.get('cartoes_gerados', None)
    if not cartoes:
        st.info("Gere os cartões na aba 'Gerador de Cartões' para conferir aqui.")
    else:
        if st.button("📊 Conferir Desempenho nos Últimos 25 Concursos"):
            resultados = conferir_cartoes(cartoes, concursos)
            custo, retorno, saldo = calcular_retorno(cartoes, concursos)

            acertos_totais = [max(r) for r in resultados]
            st.write("### Faixas de Acerto por Cartão (Melhor Resultado entre os 25 concursos)")
            for i, acertos in enumerate(acertos_totais, 1):
                st.write(f"Cartão {i}: {acertos} acertos")

            st.success(f"💰 Custo Total: R$ {custo:.2f}")
            st.success(f"🏆 Retorno Total: R$ {retorno:.2f}")
            saldo_str = f"+R$ {saldo:.2f}" if saldo >= 0 else f"-R$ {abs(saldo):.2f}"
            st.metric("📈 Saldo Final", saldo_str)

with abas[3]:
    st.header("🔢 Probabilidades Baseadas nas Estatísticas")
    st.write("### Principais Probabilidades Calculadas")
    st.metric("Média Soma", f'{probabilidades["media_soma"]:.2f}')
    st.metric("Média Pares", f'{probabilidades["media_pares"]:.2f}')
    st.metric("Média Repetidas", f'{probabilidades["media_repetidas"]:.2f}')
    st.metric("Média Sequências", f'{probabilidades["media_sequencias"]:.2f}')

    st.write("### Dezenas Mais Frequentes")
    st.write(probabilidades["mais_frequentes"])

    st.write("### Dezenas Menos Frequentes")
    st.write(probabilidades["menos_frequentes"])

    st.write("### Percentual de Dezenas Altas")
    st.write(f'{probabilidades["alta_baixa_balanceado"]["media_altas"]*100:.2f}%')

# Rodapé personalizado
st.markdown(
    """
    <div class="footer">
        <p><strong>SAMUCJ TECHNOLOGY</strong> <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Corporate_2025_logo.svg/120px-Corporate_2025_logo.svg.png" alt="Corporate 2025" style="height:20px; vertical-align: middle;"></p>
    </div>
    """, unsafe_allow_html=True
)
