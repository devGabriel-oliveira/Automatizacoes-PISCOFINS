import streamlit as st


def render(titulo: str, icone: str, render_botao_voltar):
    render_botao_voltar()

    st.markdown(
        f"""
        <div class="vix-page-header">
            <div class="vix-page-icon">{icone}</div>
            <h2 class="vix-page-title">{titulo}</h2>
        </div>
        <p class="vix-page-sub">Automação ainda não disponível</p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="vix-callout vix-callout-info">
            A automação do card <strong>{titulo}</strong> ainda está em desenvolvimento.
            Por enquanto, apenas o card <strong>Receita Financeira</strong> está disponível.
            Volte aos Cards para utilizá-lo.
        </div>
        """,
        unsafe_allow_html=True,
    )
