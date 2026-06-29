"""Estilos visuais da identidade VIXPAR: azul profundo + dourado."""

VIXPAR_CSS = """
<style>
:root {
    --vix-font-display: 'Segoe UI Semibold', 'Helvetica Neue', Arial, sans-serif;
    --vix-font-body: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;

    --vix-azul-900: #061635;
    --vix-azul-800: #0A1F44;
    --vix-azul-700: #0F2C5C;
    --vix-azul-600: #16407F;
    --vix-azul-100: #E7ECF5;
    --vix-dourado-600: #B8902F;
    --vix-dourado-500: #C9A227;
    --vix-dourado-400: #D9B84C;
    --vix-dourado-100: #F8EFD7;
    --vix-cinza-50: #F7F8FA;
    --vix-cinza-100: #EEF1F5;
    --vix-cinza-300: #C9D0DC;
    --vix-cinza-600: #5B6477;
    --vix-texto: #0A1F2A;
    --vix-sucesso: #1E7A4C;
}

html, body, [class*="css"] {
    font-family: var(--vix-font-body);
}

#MainMenu, header[data-testid="stHeader"], footer { visibility: hidden; height: 0; }

.stApp {
    background: var(--vix-cinza-50);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1180px;
}

/* ---------- Topbar institucional ---------- */
.vix-topbar {
    background: linear-gradient(135deg, var(--vix-azul-900) 0%, var(--vix-azul-700) 65%, var(--vix-azul-600) 100%);
    border-radius: 18px;
    padding: 1.9rem 2.4rem;
    margin-bottom: 2.2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 30px rgba(10, 31, 68, 0.25);
}

.vix-topbar::after {
    content: "";
    position: absolute;
    top: -40%;
    right: -8%;
    width: 280px;
    height: 280px;
    background: radial-gradient(circle, rgba(201, 162, 39, 0.22) 0%, rgba(201,162,39,0) 70%);
    border-radius: 50%;
}

.vix-topbar::before {
    content: "";
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 6px;
    background: linear-gradient(180deg, var(--vix-dourado-400), var(--vix-dourado-600));
}

.vix-eyebrow {
    font-family: var(--vix-font-display);
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    font-weight: 700;
    color: var(--vix-dourado-400) !important;
    text-transform: uppercase;
    margin: 0 0 0.5rem 0;
}

.vix-title {
    font-family: var(--vix-font-display);
    font-size: 1.9rem;
    font-weight: 800;
    color: #FFFFFF !important;
    line-height: 1.25;
    margin: 0;
    letter-spacing: -0.01em;
}

.vix-subtitle {
    color: #C7D2E8 !important;
    font-size: 0.95rem;
    margin-top: 0.55rem;
    font-weight: 400;
}

/* ---------- Cards de navegação ---------- */
.vix-card {
    background: #FFFFFF;
    border: 1px solid var(--vix-cinza-100);
    border-radius: 16px;
    padding: 1.6rem 1.5rem 1.5rem 1.5rem;
    height: 100%;
    transition: all 0.18s ease;
    position: relative;
    box-shadow: 0 2px 10px rgba(10, 31, 68, 0.04);
}

.vix-card:hover {
    border-color: var(--vix-dourado-500);
    box-shadow: 0 10px 28px rgba(10, 31, 68, 0.12);
    transform: translateY(-2px);
}

.vix-card-icon {
    width: 46px;
    height: 46px;
    border-radius: 12px;
    background: var(--vix-azul-100);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.4rem;
    margin-bottom: 0.9rem;
}

.vix-card-tag {
    font-family: var(--vix-font-display);
    font-size: 0.64rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.18rem 0.55rem;
    border-radius: 100px;
    display: inline-block;
}

.vix-tag-ativo {
    background: rgba(30, 122, 76, 0.12);
    color: var(--vix-sucesso);
}

.vix-tag-em-breve {
    background: var(--vix-cinza-100);
    color: var(--vix-cinza-600);
}

.vix-card-title {
    font-family: var(--vix-font-display);
    font-size: 1.08rem;
    font-weight: 700;
    color: var(--vix-azul-800) !important;
    margin: 0.7rem 0 0.3rem 0;
}

.vix-card-desc {
    font-size: 0.84rem;
    color: var(--vix-cinza-600) !important;
    line-height: 1.45;
    margin-bottom: 0.2rem;
}

/* Botão "entrar" de cada card, renderizado pelo Streamlit */
div[data-testid="stButton"] button[kind="secondaryFormSubmit"],
div[data-testid="stButton"] button {
    background: var(--vix-azul-800) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.86rem !important;
    padding: 0.5rem 1rem !important;
    transition: all 0.15s ease !important;
}

div[data-testid="stButton"] button:hover {
    background: var(--vix-dourado-500) !important;
    color: var(--vix-azul-900) !important;
}

div[data-testid="stButton"] button:focus:not(:active) {
    box-shadow: 0 0 0 3px rgba(201, 162, 39, 0.35) !important;
}

/* Botão secundário (voltar): kind="secondary" do próprio Streamlit */
div[data-testid="stButton"] button[kind="secondary"] {
    background: transparent !important;
    color: var(--vix-azul-700) !important;
    border: 1px solid var(--vix-cinza-300) !important;
}

div[data-testid="stButton"] button[kind="secondary"]:hover {
    background: var(--vix-cinza-100) !important;
    color: var(--vix-azul-800) !important;
    border-color: var(--vix-cinza-300) !important;
}

/* ---------- Cabeçalho de página interna ---------- */
.vix-page-header {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    margin-bottom: 0.3rem;
}

.vix-page-icon {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    background: var(--vix-azul-800);
    color: var(--vix-dourado-400);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
}

.vix-page-title {
    font-family: var(--vix-font-display);
    font-weight: 800;
    font-size: 1.45rem;
    color: var(--vix-azul-800) !important;
    margin: 0;
}

.vix-page-sub {
    color: var(--vix-cinza-600) !important;
    font-size: 0.9rem;
    margin: 0.15rem 0 1.6rem 0;
}

/* ---------- Stepper ---------- */
.vix-step {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    background: #FFFFFF;
    border: 1px solid var(--vix-cinza-100);
    border-radius: 12px;
    padding: 0.85rem 1.1rem;
    margin-bottom: 0.7rem;
}

.vix-step-num {
    width: 26px;
    height: 26px;
    border-radius: 50%;
    background: var(--vix-azul-100);
    color: var(--vix-azul-800);
    font-weight: 700;
    font-size: 0.8rem;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.vix-step-done .vix-step-num {
    background: var(--vix-sucesso);
    color: white;
}

.vix-step-text {
    font-size: 0.88rem;
    color: var(--vix-texto);
    font-weight: 500;
}

/* ---------- Caixas de status ---------- */
.vix-callout {
    border-radius: 12px;
    padding: 0.95rem 1.15rem;
    font-size: 0.88rem;
    line-height: 1.5;
    margin: 0.9rem 0;
    border: 1px solid transparent;
}

.vix-callout-info {
    background: var(--vix-azul-100);
    color: var(--vix-azul-800);
    border-color: #D2DCEF;
}

.vix-callout-success {
    background: #E7F5ED;
    color: #155A37;
    border-color: #C7E8D5;
}

/* ---------- Métricas ---------- */
div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid var(--vix-cinza-100);
    border-radius: 12px;
    padding: 0.9rem 1rem 0.6rem 1rem;
}

div[data-testid="stMetricLabel"] {
    color: var(--vix-cinza-600) !important;
}

div[data-testid="stMetricValue"] {
    color: var(--vix-azul-800) !important;
    font-family: var(--vix-font-display) !important;
}

/* ---------- Uploader ---------- */
div[data-testid="stFileUploaderDropzone"] {
    background: #FFFFFF;
    border: 2px dashed var(--vix-cinza-300);
    border-radius: 14px;
}

div[data-testid="stFileUploaderDropzone"]:hover {
    border-color: var(--vix-dourado-500);
}

/* ---------- Download button destaque dourado ---------- */
div[data-testid="stDownloadButton"] button {
    background: linear-gradient(135deg, var(--vix-dourado-500), var(--vix-dourado-600)) !important;
    color: var(--vix-azul-900) !important;
    font-weight: 700 !important;
    border: none !important;
}

div[data-testid="stDownloadButton"] button:hover {
    background: var(--vix-azul-800) !important;
    color: #FFFFFF !important;
}

/* ---------- Rodapé ---------- */
.vix-footer {
    text-align: center;
    color: var(--vix-cinza-600);
    font-size: 0.78rem;
    margin-top: 2.5rem;
    padding-top: 1.2rem;
    border-top: 1px solid var(--vix-cinza-100);
}
</style>
"""
