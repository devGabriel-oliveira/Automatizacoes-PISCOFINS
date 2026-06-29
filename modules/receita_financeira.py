"""
Processamento do relatório de Receita Financeira (PIS/COFINS).

Regras de negócio (definidas em Automatizar.md):
  1. Aba 1 do arquivo original -> renomeada/copiada para "BD" (intocada, fonte segura).
  2. Cópia de BD -> aba "Análise", com duas novas colunas inseridas imediatamente
     à direita de "Montante em moeda interna":
        - PIS    = Montante * 0,65%
        - COFINS = Montante * 4%
  3. Nova aba "Dinâmica" contendo uma tabela dinâmica nativa do Excel com:
        Linhas:  Empresa, Loc.negócios, Conta, Centro de lucro, Segmento, Texto
        Valores: Soma de Montante em moeda interna, Soma de PIS, Soma de COFINS
"""

from __future__ import annotations

import io
from copy import copy

import openpyxl
from openpyxl.utils import get_column_letter

COLUNA_MONTANTE = "Montante em moeda interna"
ALIQUOTA_PIS = 0.0065
ALIQUOTA_COFINS = 0.04

CAMPOS_LINHA_DINAMICA = [
    "Empresa",
    "Loc.negócios",
    "Conta",
    "Centro de lucro",
    "Segmento",
    "Texto",
]
CAMPOS_VALOR_DINAMICA = [COLUNA_MONTANTE, "PIS", "COFINS"]


class ColunaNaoEncontradaError(Exception):
    pass


def _encontrar_coluna(ws, nome_coluna: str) -> int:
    """Retorna o índice (1-based) da coluna cujo cabeçalho (linha 1) bate com nome_coluna."""
    for col in range(1, ws.max_column + 1):
        valor = ws.cell(row=1, column=col).value
        if valor is not None and str(valor).strip() == nome_coluna:
            return col
    raise ColunaNaoEncontradaError(
        f"Coluna '{nome_coluna}' não encontrada na primeira linha da planilha."
    )


def _copiar_estilo(origem_cell, destino_cell):
    if origem_cell.has_style:
        destino_cell.font = copy(origem_cell.font)
        destino_cell.border = copy(origem_cell.border)
        destino_cell.fill = copy(origem_cell.fill)
        destino_cell.number_format = copy(origem_cell.number_format)
        destino_cell.protection = copy(origem_cell.protection)
        destino_cell.alignment = copy(origem_cell.alignment)


def _duplicar_aba(wb, ws_origem, novo_nome: str):
    """Duplica completamente uma aba (valores, estilos, larguras de coluna) com novo nome."""
    ws_nova = wb.copy_worksheet(ws_origem)
    ws_nova.title = novo_nome
    return ws_nova


def _construir_aba_analise(wb, ws_bd):
    """Cria a aba 'Análise' a partir de 'BD', inserindo as colunas PIS e COFINS
    imediatamente à direita de 'Montante em moeda interna'."""
    ws_analise = _duplicar_aba(wb, ws_bd, "Análise")

    col_montante = _encontrar_coluna(ws_analise, COLUNA_MONTANTE)
    col_pis = col_montante + 1
    col_cofins = col_montante + 2

    ws_analise.insert_cols(col_pis, amount=2)

    letra_montante = get_column_letter(col_montante)

    ws_analise.cell(row=1, column=col_pis, value="PIS")
    ws_analise.cell(row=1, column=col_cofins, value="COFINS")

    header_ref_col = col_montante if col_montante != col_pis else col_pis
    cabecalho_modelo = ws_analise.cell(row=1, column=header_ref_col)
    for c in (col_pis, col_cofins):
        _copiar_estilo(cabecalho_modelo, ws_analise.cell(row=1, column=c))

    ultima_linha = ws_analise.max_row
    for row in range(2, ultima_linha + 1):
        cel_montante = ws_analise.cell(row=row, column=col_montante)
        if cel_montante.value is None:
            continue
        ref = f"{letra_montante}{row}"
        cel_pis = ws_analise.cell(row=row, column=col_pis, value=f"={ref}*0.65%")
        cel_cofins = ws_analise.cell(row=row, column=col_cofins, value=f"={ref}*4%")
        cel_pis.number_format = "#,##0.00"
        cel_cofins.number_format = "#,##0.00"

    largura_origem = ws_bd.column_dimensions[letra_montante].width
    for c in (col_pis, col_cofins):
        letra = get_column_letter(c)
        ws_analise.column_dimensions[letra].width = largura_origem or 14

    return ws_analise, col_montante, col_pis, col_cofins


def _construir_dinamica_estatica(wb, ws_analise, col_montante, col_pis, col_cofins):
    """Cria a aba 'Dinâmica': uma tabela-resumo (Empresa, Loc.negócios, Conta,
    Centro de lucro, Segmento, Texto x Soma de Montante/PIS/COFINS) construída
    com fórmulas SUMIFS, equivalente em resultado a uma tabela dinâmica do
    Excel agrupada por esses campos, mas gravada de forma 100% compatível
    (evita o XML de PivotTable nativo, que costuma ficar incompleto quando
    escrito por bibliotecas que não são o próprio Excel)."""
    ultima_linha = ws_analise.max_row
    ultima_coluna = ws_analise.max_column

    idx_por_nome = {}
    for col in range(1, ultima_coluna + 1):
        nome = ws_analise.cell(row=1, column=col).value
        if nome:
            idx_por_nome[str(nome).strip()] = col

    colunas_linha = [c for c in CAMPOS_LINHA_DINAMICA if c in idx_por_nome]
    colunas_valor = [
        (c, idx_por_nome[c]) for c in CAMPOS_VALOR_DINAMICA if c in idx_por_nome
    ]

    chaves = {}
    ordem_chaves = []
    for r in range(2, ultima_linha + 1):
        chave = tuple(
            ws_analise.cell(row=r, column=idx_por_nome[c]).value
            for c in colunas_linha
        )
        if all(v is None for v in chave):
            continue
        if chave not in chaves:
            chaves[chave] = True
            ordem_chaves.append(chave)

    ws_dinamica = wb.create_sheet("Dinâmica")

    header_font = copy(ws_analise.cell(row=1, column=1).font)
    header_fill = copy(ws_analise.cell(row=1, column=1).fill)

    headers = list(colunas_linha) + [f"Soma de {c}" for c, _ in colunas_valor]
    for j, h in enumerate(headers, start=1):
        cel = ws_dinamica.cell(row=1, column=j, value=h)
        cel.font = header_font
        cel.fill = header_fill

    letra_analise = {
        c: get_column_letter(idx_por_nome[c]) for c in colunas_linha
    }
    letras_valor = {c: get_column_letter(idx) for c, idx in colunas_valor}
    nome_aba_analise = ws_analise.title

    for i, chave in enumerate(ordem_chaves, start=2):
        for j, campo in enumerate(colunas_linha, start=1):
            ws_dinamica.cell(row=i, column=j, value=chave[j - 1])

        criterios = []
        for campo in colunas_linha:
            col_letra = letra_analise[campo]
            cel_ref = f"${get_column_letter(colunas_linha.index(campo) + 1)}{i}"
            criterios.append(
                f"'{nome_aba_analise}'!${col_letra}$2:${col_letra}${ultima_linha},"
                f"\"=\"&{cel_ref}"
            )
        criterios_str = ",".join(criterios)

        for k, (campo_valor, _idx) in enumerate(colunas_valor):
            col_destino = len(colunas_linha) + k + 1
            col_letra_valor = letras_valor[campo_valor]
            formula = (
                f"=SUMIFS('{nome_aba_analise}'!${col_letra_valor}$2:"
                f"${col_letra_valor}${ultima_linha},{criterios_str})"
            )
            cel = ws_dinamica.cell(row=i, column=col_destino, value=formula)
            cel.number_format = "#,##0.00"

    for j in range(1, len(headers) + 1):
        letra = get_column_letter(j)
        max_len = len(str(headers[j - 1]))
        ws_dinamica.column_dimensions[letra].width = max(14, max_len + 2)

    ws_dinamica.freeze_panes = "A2"
    return ws_dinamica


def processar_receita_financeira(arquivo_excel) -> bytes:
    """
    Recebe um arquivo Excel (caminho, bytes ou file-like) com o relatório de
    Receita Financeira e devolve, em memória, os bytes do arquivo já processado:
      - BD: cópia intocada da primeira aba do arquivo de origem
      - Análise: cópia de BD + colunas PIS e COFINS
      - Dinâmica: tabela dinâmica (Empresa, Loc.negócios, Conta, Centro de lucro,
        Segmento, Texto) somando Montante, PIS e COFINS

    Caso o arquivo enviado já possua abas chamadas "BD", "Análise" ou "Dinâmica"
    (por exemplo, um arquivo já processado anteriormente), elas são removidas
    antes do reprocessamento para evitar duplicidade (Análise1, Dinâmica1, etc.).
    """
    wb = openpyxl.load_workbook(arquivo_excel, data_only=False)

    ws_original = wb.worksheets[0]

    for nome_reservado in ("BD", "Análise", "Dinâmica"):
        if nome_reservado in wb.sheetnames and wb[nome_reservado] is not ws_original:
            del wb[nome_reservado]

    ws_original.title = "BD"
    ws_bd = wb["BD"]

    ws_analise, col_montante, col_pis, col_cofins = _construir_aba_analise(wb, ws_bd)

    _construir_dinamica_estatica(wb, ws_analise, col_montante, col_pis, col_cofins)

    ordem_desejada = ["BD", "Análise", "Dinâmica"]
    outras_abas = [n for n in wb.sheetnames if n not in ordem_desejada]
    wb._sheets = [wb[n] for n in ordem_desejada] + [wb[n] for n in outras_abas]

    wb.active = 0

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()
