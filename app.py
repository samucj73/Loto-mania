import streamlit as st
from api_lotomania import obter_ultimos_concursos
from estatisticas_lotomania import analisar_concursos
from probabilidades_lotomania import calcular_probabilidades
from gerador_lotomania import gerar_cartoes_lotomania
from conferencia_lotomania import conferir_cartoes

concursos = obter_ultimos_concursos()
estatisticas = analisar_concursos(concursos)
probabilidades = calcular_probabilidades(estatisticas)

st.set_page_config(page_title="Lotomania Inteligente", layout="wide")
st.title("🎯 Lotomania Inteligente")

aba = st.sidebar.radio("Navegar", ["📊 Estatísticas", "🎲 Gerar Cartões", "✅ Conferência"])

if aba == "📊 Estatísticas":
    st.header("📊 Estatísticas dos últimos 25 concursos")
    st.write("Dezenas mais frequentes:", estatisticas["frequencia"].most_common(20))
    st.write("Distribuição de pares/ímpares média:", estatisticas["pares_med"])
    st.write("Média de soma:", sum(estatisticas["somas"]) / len(estatisticas["somas"]))
    st.write("Média de repetidas:", sum(estatisticas["repetidas"]) / len(estatisticas["repetidas"]))
    st.write("Média de sequências:", sum(estatisticas["sequencias"]) / len(estatisticas["sequencias"]))

elif aba == "🎲 Gerar Cartões":
    st.header("🎲 Gerador Inteligente de Cartões")
    qtd = st.slider("Quantidade de cartões a gerar", 1, 50, 10)
    fixas = st.text_input("Dezenas fixas (separadas por vírgula)", "")
    excluidas = st.text_input("Dezenas a excluir (separadas por vírgula)", "")

    fixas = [int(x.strip()) for x in fixas.split(",") if x.strip().isdigit()]
    excluidas = [int(x.strip()) for x in excluidas.split(",") if x.strip().isdigit()]

    if st.button("Gerar Cartões"):
        cartoes = gerar_cartoes_lotomania(estatisticas, probabilidades, qtd_cartoes=qtd, fixas=fixas, excluidas=excluidas)
        st.success(f"{len(cartoes)} cartões gerados!")
        for i, c in enumerate(cartoes):
            st.code(f"Cartão {i+1}: {c}")

        st.session_state["cartoes_gerados"] = cartoes

elif aba == "✅ Conferência":
    st.header("✅ Conferência dos Cartões Gerados")
    cartoes = st.session_state.get("cartoes_gerados", [])

    if not cartoes:
        st.warning("Nenhum cartão gerado ainda.")
    else:
        preco = st.number_input("Preço por jogo (R$)", value=3.00, step=0.50)
        if st.button("Conferir Cartões"):
            resultado = conferir_cartoes(cartoes, concursos, preco_por_jogo=preco)

            st.subheader("Resumo Geral")
            st.write(f"🧾 Cartões conferidos: {resultado['cartoes_conferidos']}")
            st.write(f"💰 Total gasto: R$ {resultado['total_gasto']:.2f}")
            st.write(f"🎯 Total ganho: R$ {resultado['total_premio']:.2f}")
            lucro = resultado["lucro_ou_prejuizo"]
            st.success(f"📈 Lucro: R$ {lucro:.2f}" if lucro > 0 else f"📉 Prejuízo: R$ {lucro:.2f}")

            with st.expander("🔍 Detalhamento dos cartões"):
                for i, r in enumerate(resultado["detalhado"]):
                    st.write(f"Cartão {i+1}: {r['cartao']}")
                    st.write(f"Melhor acerto: {r['melhor_acerto']} pontos")
                    st.write(f"Premiação estimada: R$ {r['premio']:.2f}")
                    st.write("Acertos:", r["resultados"])
                    st.markdown("---")
