# Automação de Relatórios do Fechamento — PIS e COFINS (VIXPAR)

Site em Streamlit para automatizar os relatórios do fechamento fiscal da VIXPAR.

## Como rodar

1. Instale o Python 3.10+ (caso ainda não tenha).
2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Rode o site:

   ```bash
   streamlit run app.py
   ```

4. O navegador abrirá automaticamente em `http://localhost:8501`.

## Estrutura do projeto

```
vixpar_app/
├── app.py                              # página inicial (cards) e roteamento
├── requirements.txt
└── modules/
    ├── estilo.py                       # CSS com a identidade visual VIXPAR
    ├── receita_financeira.py           # regras de negócio (BD / Análise / Dinâmica)
    ├── pagina_receita_financeira.py    # tela de upload e download do card Receita Financeira
    └── pagina_em_construcao.py         # placeholder dos demais cards
```

## O que o card "Receita Financeira" faz

Ao enviar o Excel do relatório de Receita Financeira, o site gera automaticamente
uma nova planilha para download com 3 abas:

1. **BD** — cópia exata da aba original enviada, sem nenhuma alteração (fonte segura).
2. **Análise** — cópia de BD com duas colunas novas ao lado de
   *Montante em moeda interna*:
   - **PIS** = Montante × 0,65% (fórmula do Excel)
   - **COFINS** = Montante × 4% (fórmula do Excel)
3. **Dinâmica** — tabela dinâmica **nativa do Excel** (mesmo objeto PivotTable
   que se cria manualmente em Dados → Tabela Dinâmica), agrupada por
   *Empresa, Loc.negócios, Conta, Centro de lucro, Segmento* e *Texto*, somando
   *Montante em moeda interna*, *PIS* e *COFINS*. Por ser uma tabela dinâmica
   real, o Excel exibe o painel "Campos da Tabela Dinâmica" ao clicar nela,
   permitindo reorganizar, filtrar ou adicionar campos livremente.

> O Excel recalcula a tabela dinâmica automaticamente na primeira abertura do
> arquivo (a planilha é salva com `refreshOnLoad` ativado).

> O arquivo enviado deve conter, na primeira linha da primeira aba, uma coluna
> chamada exatamente **"Montante em moeda interna"**. Os demais campos usados
> na tabela-resumo (Empresa, Loc.negócios, Conta, Centro de lucro, Segmento,
> Texto) são opcionais — se algum não existir no arquivo, ele é simplesmente
> ignorado na tabela-resumo.

## Próximos passos (cards ainda não automatizados)

Os cards **Outras Receitas**, **Pat/Vale Transporte** e **Retenção de Clientes**
já estão no site, mas exibem "Em breve" — para automatizá-los, basta seguir o
mesmo padrão usado em `receita_financeira.py` e `pagina_receita_financeira.py`,
descrevendo as regras de cálculo de cada um.

## Identidade visual

Paleta baseada na marca VIXPAR: azul profundo (`#0A1F44`) e dourado (`#C9A227`),
sem dependência de fontes externas (usa as fontes do sistema), para funcionar
também em redes corporativas restritas.
