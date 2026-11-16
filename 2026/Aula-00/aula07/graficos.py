"""Graficos dos notebooks de Sistemas de Banco de Dados I.

Este arquivo e usado pelo notebook e nao precisa ser alterado.
Cada funcao recebe o resultado de uma consulta e desenha o grafico.

Regra das colunas: a PRIMEIRA coluna do SELECT da o nome de cada barra
(ou de cada ponto da linha) e a SEGUNDA coluna da o valor. As demais
colunas aparecem na tabela, mas nao entram no grafico.
"""
from decimal import Decimal

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter
from IPython.display import display

AZUL = "#2a78d6"
TEXTO = "#0b0b0b"
TEXTO_SECUNDARIO = "#52514e"
GRADE = "#e4e3df"
FUNDO = "#fcfcfb"


def _tabela(resultado):
    if hasattr(resultado, "DataFrame"):
        df = resultado.DataFrame()
    else:
        df = pd.DataFrame(resultado)
    if df.shape[1] < 2:
        raise ValueError("A consulta precisa ter pelo menos duas colunas: o nome e o valor.")
    df = df.copy()
    rotulo, valor = df.columns[0], df.columns[1]
    df[rotulo] = df[rotulo].map(lambda x: "(nulo)" if x is None or (isinstance(x, float) and pd.isna(x)) else x)
    decimal = any(isinstance(x, Decimal) and x != x.to_integral_value() for x in df[valor]) or any(
        isinstance(x, Decimal) and x.as_tuple().exponent < 0 for x in df[valor])
    df[valor] = df[valor].map(lambda x: float(x) if isinstance(x, Decimal) else x)
    df[valor] = pd.to_numeric(df[valor]).fillna(0)
    df.attrs["decimal"] = decimal
    return df, rotulo, valor


def _numero(v, casas=False):
    if not casas and float(v).is_integer():
        texto = f"{int(v):,}"
    else:
        texto = f"{v:,.2f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def _rotulo_texto(x):
    if isinstance(x, float) and x.is_integer():
        return str(int(x))
    if isinstance(x, Decimal) and x == x.to_integral_value():
        return str(int(x))
    return str(x)


def _eixos(titulo, largura, altura):
    fig, ax = plt.subplots(figsize=(largura, altura), dpi=110)
    fig.patch.set_facecolor(FUNDO)
    ax.set_facecolor(FUNDO)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color(GRADE)
    ax.tick_params(colors=TEXTO_SECUNDARIO, labelsize=9)
    ax.set_title(titulo, loc="left", color=TEXTO, fontsize=12, pad=12)
    return fig, ax


def barras(resultado, titulo="", horizontal=False):
    """Grafico de barras. Use horizontal=True quando os nomes forem longos."""
    df, rotulo, valor = _tabela(resultado)
    display(df)
    nomes = [_rotulo_texto(x) for x in df[rotulo]]
    valores = list(df[valor])
    titulo = titulo or f"{valor} por {rotulo}"
    mostrar_valores = len(valores) <= 15
    if horizontal:
        fig, ax = _eixos(titulo, 9, max(2.5, 0.42 * len(valores) + 1))
        ax.barh(nomes[::-1], valores[::-1], color=AZUL, height=0.6)
        ax.xaxis.grid(True, color=GRADE, linewidth=0.8)
        ax.set_axisbelow(True)
        ax.set_xlabel(valor, color=TEXTO_SECUNDARIO)
        if mostrar_valores:
            for i, v in enumerate(valores[::-1]):
                ax.annotate(_numero(v, df.attrs["decimal"]), (v, i), xytext=(4, 0), textcoords="offset points",
                            va="center", fontsize=8, color=TEXTO_SECUNDARIO)
    else:
        fig, ax = _eixos(titulo, 9, 4.2)
        ax.bar(nomes, valores, color=AZUL, width=0.6)
        ax.yaxis.grid(True, color=GRADE, linewidth=0.8)
        ax.set_axisbelow(True)
        ax.set_ylabel(valor, color=TEXTO_SECUNDARIO)
        if len(nomes) > 6 or max(len(n) for n in nomes) > 10:
            plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
        if mostrar_valores:
            for i, v in enumerate(valores):
                ax.annotate(_numero(v, df.attrs["decimal"]), (i, v), xytext=(0, 3), textcoords="offset points",
                            ha="center", fontsize=8, color=TEXTO_SECUNDARIO)
    (ax.xaxis if horizontal else ax.yaxis).set_major_formatter(FuncFormatter(lambda v, _: _numero(v)))
    fig.tight_layout()
    plt.show()


def linha(resultado, titulo=""):
    """Grafico de linha, para valores ao longo do tempo (meses, por exemplo)."""
    df, rotulo, valor = _tabela(resultado)
    display(df)
    nomes = [_rotulo_texto(x) for x in df[rotulo]]
    valores = list(df[valor])
    titulo = titulo or f"{valor} por {rotulo}"
    fig, ax = _eixos(titulo, 9, 4.2)
    ax.plot(nomes, valores, color=AZUL, linewidth=2, marker="o", markersize=6)
    ax.yaxis.grid(True, color=GRADE, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.set_xlabel(rotulo, color=TEXTO_SECUNDARIO)
    ax.set_ylabel(valor, color=TEXTO_SECUNDARIO)
    ax.set_ylim(bottom=0)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: _numero(v)))
    if valores:
        i_max = max(range(len(valores)), key=lambda i: valores[i])
        ax.annotate(_numero(valores[i_max], df.attrs["decimal"]), (i_max, valores[i_max]), xytext=(0, 8),
                    textcoords="offset points", ha="center", fontsize=8, color=TEXTO_SECUNDARIO)
    fig.tight_layout()
    plt.show()
