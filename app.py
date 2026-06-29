import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import streamlit as st

from modules.estilo import VIXPAR_CSS
from modules import pagina_receita_financeira
from modules import pagina_em_construcao

st.set_page_config(
    page_title="Automação de Relatórios do Fechamento - PIS e COFINS",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(VIXPAR_CSS, unsafe_allow_html=True)

if "pagina" not in st.session_state:
    st.session_state.pagina = "home"

CARDS = [
    {
        "id": "receita_financeira",
        "icone": "💰",
        "titulo": "Receita Financeira",
        "descricao": "Calcula PIS e COFINS sobre o montante da Receita Financeira e gera a tabela-resumo por empresa, conta e centro de lucro.",
        "status": "ativo",
    },
    {
        "id": "outras_receitas",
        "icone": "📑",
        "titulo": "Outras Receitas",
        "descricao": "Automação do fechamento de Outras Receitas.",
        "status": "em_breve",
    },
    {
        "id": "pat_vale_transporte",
        "icone": "🚌",
        "titulo": "Pat/Vale Transporte",
        "descricao": "Automação do fechamento de PAT e Vale Transporte.",
        "status": "em_breve",
    },
    {
        "id": "retencao_clientes",
        "icone": "🔒",
        "titulo": "Retenção de Clientes",
        "descricao": "Automação do fechamento de Retenção de Clientes.",
        "status": "em_breve",
    },
]


def ir_para(pagina_id: str):
    st.session_state.pagina = pagina_id


def render_topbar():
    st.markdown(
        """
        <div class="vix-topbar">
            <p class="vix-eyebrow">VIXPAR · Fechamento Fiscal</p>
            <h1 class="vix-title">Automação de Relatórios do Fechamento — PIS e COFINS</h1>
            <p class="vix-subtitle">Selecione um card para automatizar o relatório correspondente.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_home():
    render_topbar()

    linha1 = st.columns(2, gap="medium")
    linha2 = st.columns(2, gap="medium")
    colunas = linha1 + linha2

    for col, card in zip(colunas, CARDS):
        with col:
            tag_classe = "vix-tag-ativo" if card["status"] == "ativo" else "vix-tag-em-breve"
            tag_texto = "Disponível" if card["status"] == "ativo" else "Em breve"

            st.markdown(
                f"""
                <div class="vix-card">
                    <div class="vix-card-icon">{card['icone']}</div>
                    <span class="vix-card-tag {tag_classe}">{tag_texto}</span>
                    <p class="vix-card-title">{card['titulo']}</p>
                    <p class="vix-card-desc">{card['descricao']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write("")
            disabled = card["status"] != "ativo"
            label = "Abrir" if not disabled else "Em breve"
            if st.button(label, key=f"btn_{card['id']}", disabled=disabled, use_container_width=True):
                ir_para(card["id"])
                st.rerun()

    st.markdown(
        """
        <div class="vix-footer">VIXPAR · Painel interno de automação de relatórios do fechamento</div>
        """,
        unsafe_allow_html=True,
    )


def render_botao_voltar():
    if st.button("← Voltar para os Cards", key="btn_voltar", type="secondary"):
        ir_para("home")
        st.rerun()


PAGINAS = {
    "home": render_home,
    "receita_financeira": lambda: pagina_receita_financeira.render(render_botao_voltar),
    "outras_receitas": lambda: pagina_em_construcao.render(
        "Outras Receitas", "📑", render_botao_voltar
    ),
    "pat_vale_transporte": lambda: pagina_em_construcao.render(
        "Pat/Vale Transporte", "🚌", render_botao_voltar
    ),
    "retencao_clientes": lambda: pagina_em_construcao.render(
        "Retenção de Clientes", "🔒", render_botao_voltar
    ),
}

pagina_atual = st.session_state.pagina
PAGINAS.get(pagina_atual, render_home)()
