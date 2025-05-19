import streamlit as st
from api_lotomania import obter_ultimos_resultados_lotomania
from estatisticas_lotomania import analisar_concursos
from probabilidade import calcular_probabilidades
from gerador_cartoes import gerar_cartoes
from conferidor import conferir_cartoes, calcular_retorno
import pandas as pd
import io

st.set_page_config(page_title="Lotomania Inteligente", layout="wide")

def centralizar_titulo(texto):
    st.markdown(f"<h1 style='text-align: center;'>{texto}</h1>", unsafe_allow_html=True)

def centralizar_subtitulo(texto):
    st.markdown(f"<h3 style='text-align: center;'>{texto}</h3>", unsafe_allow_html=True)

def rodape():
    st.markdown(
        """
        <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #f1f1f1;
            color: #555;
            text-align: center;
            padding: 10px 0;
            font-size: 14px;
            border-top: 1px solid #ddd;
        }
        </style>
        <div class="footer">
            <span>© SAMUCJ TECHNOLOGY <img src="https://cdn-icons-png.flaticon.com/512/2534/2534856.png" alt="Corporate 2025" width="20" style="vertical-align:middle; margin-left:5px;" /></span>
        </div>
        """,
        unsafe_allow_html=True,
    )

centralizar_titulo("🎯 Lotomania Inteligente")

with st.spinner("🔄 Carregando concursos..."):
    concursos_completos = obter_ultimos_resultados_lotomania(25)

# Filtra concursos válidos e extrai dezenas
concursos = []
ult_concurso_num = None
for c in concursos_completos:
    dezenas = c.get('dezenas')
    if not dezenas or not isinstance(dezenas, list):
        st.warning(f"Concurso {c.get('concurso', '?')} está com dezenas inválidas: {dezenas}")
        continue
    try:
        dezenas_int = sorted(int(d) for d in dezenas)
        concursos.append(dezenas_int)
        if ult_concurso_num is None or c.get('concurso', 0) > ult_concurso_num:
            ult_concurso_num = c.get('concurso', 0)
    except Exception as e:
        st.error(f"Erro ao processar dezenas do concurso {c.get('concurso', '?')}: {e}")

if not concursos:
    st.error("❌ Não foi possível carregar os concursos válidos. Verifique sua conexão ou tente novamente mais tarde.")
    rodape()
    st.stop()

centralizar_subtitulo(f"Último Concurso Carregado: {ult_concurso_num}")

estatisticas = analisar_concursos(concursos)
probabilidades = calcular_probabilidades(estatisticas)

tab1, tab2, tab3 = st.tabs(["📊 Estatísticas", "🎲 Gerador de Cartões", "📋 Conferência"])

with tab1:
    st.header("Estatísticas dos Últimos 25 Concursos")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de Concursos", estatisticas.get("total_concursos", "N/A"))
    col2.metric("Média Pares", f'{estatisticas.get("pares_med", 0):.2f}')
    col3.metric("Média Ímpares", f'{estatisticas.get("ímpares_med", 0):.2f}')
    col4.metric("Média Soma das Dezenas", f'{estatisticas.get("soma_media", 0):.2f}')

    st.subheader("Dezenas Mais Frequentes")
    df_mais = pd.DataFrame(estatisticas.get("mais_frequentes", []), columns=["Dezenas"])
    st.dataframe(df_mais)

    st.subheader("Dezenas Menos Frequentes")
    df_menos = pd.DataFrame(estatisticas.get("menos_frequentes", []), columns=["Dezenas"])
    st.dataframe(df_menos)

    st.subheader("Probabilidades Calculadas")
    for chave, valor in probabilidades.items():
        if isinstance(valor, dict):
            st.write(f"**{chave}:**")
            for k, v in valor.items():
                st.write(f"- {k}: {v:.2f}")
        elif isinstance(valor, list):
            st.write(f"**{chave}:** {', '.join(str(x) for x in valor)}")
        else:
            st.write(f"**{chave}:** {valor}")

with tab2:
    st.header("Gerador de Cartões Inteligentes")
    qtd_cartoes = st.slider("Quantidade de cartões a gerar", 1, 50, 10)
    if st.button("🔁 Gerar Cartões"):
        cartoes = gerar_cartoes(estatisticas, qtd_cartoes)

        # Mostrar cartões gerados
        for i, cartao in enumerate(cartoes, 1):
            st.write(f"Cartão {i}: {', '.join(f'{d:02d}' for d in cartao)}")

        # Botão para download TXT
        txt_buffer = io.StringIO()
        for i, cartao in enumerate(cartoes, 1):
            linha = f"Cartão {i}: " + ", ".join(f"{d:02d}" for d in cartao) + "\n"
            txt_buffer.write(linha)
        txt_buffer.seek(0)

        st.download_button(
            label="⬇️ Baixar Cartões (.txt)",
            data=txt_buffer,
            file_name="cartoes_lotomania.txt",
            mime="text/plain"
        )

with tab3:
    st.header("Conferência dos Cartões")
    if 'cartoes' not in locals():
        st.info("Primeiro gere os cartões na aba 'Gerador de Cartões' para poder conferir.")
    else:
        resultados = conferir_cartoes(cartoes, concursos)
        custo, retorno, saldo = calcular_retorno(cartoes, concursos)

        acertos_totais = [max(r) for r in resultados]
        st.write("Faixas de Acerto por Cartão (Melhor Resultado entre os 25 concursos):")
        for i, acertos in enumerate(acertos_totais, 1):
            st.write(f"- Cartão {i}: {acertos} acertos")

        st.success(f"Custo Total: R$ {custo:.2f}")
        st.success(f"Retorno Total: R$ {retorno:.2f}")
        saldo_str = f"+R$ {saldo:.2f}" if saldo >= 0 else f"-R$ {abs(saldo):.2f}"
        st.metric("Saldo Final", saldo_str)

rodape()
