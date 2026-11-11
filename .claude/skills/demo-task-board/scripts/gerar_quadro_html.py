#!/usr/bin/env python3
"""Gera o quadro de tarefas (HTML, 3 colunas) a partir de talk/demos/tarefas/tarefas.md.

Uso (na raiz do projeto): python3 .claude/skills/demo-task-board/scripts/gerar_quadro_html.py [--hoje AAAA-MM-DD]
"""
import argparse, html, re, sys
from datetime import date, timedelta
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
FONTE = RAIZ / "talk/demos/tarefas/tarefas.md"
SAIDA = RAIZ / "talk/demos/tarefas/tarefas.html"
FONTES = "../../../fontes"
SECOES = {"backlog": "Backlog", "para amanhã": "Para amanhã", "in progress": "In progress", "done": "Done"}
CLASSE = {"backlog": "backlog", "para amanhã": "amanha", "in progress": "inprogress", "done": "done"}
DIAS_SEM = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]
LIMITE_AMANHA = 3
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
LIMITE_WIP = 3


def ler():
    dados, sec = {k: [] for k in SECOES}, None
    for linha in FONTE.read_text(encoding="utf-8").splitlines():
        if linha.startswith("## "):
            sec = linha[3:].strip().lower()
            continue
        if not linha.startswith("- ") or sec not in SECOES:
            continue
        partes = [p.strip() for p in linha[2:].split("|")]
        t = {"titulo": partes[0], "prazo": None, "deleg": None, "feito": None, "adiada": 0, "bloq": None}
        for p in partes[1:]:
            m = re.fullmatch(r"(?:prazo\s*)?(\d{4}-\d{2}-\d{2})", p)
            f = re.fullmatch(r"feito\s+(\d{4}-\d{2}-\d{2})", p)
            if f:
                t["feito"] = date.fromisoformat(f.group(1))
            elif m:
                t["prazo"] = date.fromisoformat(m.group(1))
            elif re.fullmatch(r"(?i)adiada\s+(\d+)\s*x", p):
                t["adiada"] = int(re.search(r"\d+", p).group())
            elif re.match(r"(?i)bloqueada:", p):
                t["bloq"] = p.split(":", 1)[1].strip()
            elif re.match(r"(?i)(delegar|n[ãa]o delegar)", p):
                t["deleg"] = p
            elif p:
                sys.exit(f"Campo não reconhecido '{p}' na linha: {linha}")
        dados[sec].append(t)
    return dados


def proximo_dia_util(d):
    x = d + timedelta(days=1)
    while x.weekday() >= 5:
        x += timedelta(days=1)
    return x


def fmt(d):
    return f"{d.day} {MESES[d.month-1]}"


def cartao(t, sec, hoje):
    chips = []
    if t["prazo"] and sec != "done":
        dias = (t["prazo"] - hoje).days
        cls = "atrasada" if dias < 0 else ("hoje" if dias == 0 else "")
        txt = f"Atrasada · {fmt(t['prazo'])}" if dias < 0 else (f"Hoje · {fmt(t['prazo'])}" if dias == 0 else f"Até {fmt(t['prazo'])}")
        chips.append(f'<span class="chip prazo {cls}">{txt}</span>')
    if t["feito"] and sec == "done":
        chips.append(f'<span class="chip feito">Feito {fmt(t["feito"])}</span>')
    if t["adiada"] and sec != "done":
        chips.append(f'<span class="chip adiada {"forte" if t["adiada"] >= 2 else ""}">Adiada {t["adiada"]}×</span>')
    if t["bloq"] and sec != "done":
        chips.append(f'<span class="chip bloq">Bloqueada: {html.escape(t["bloq"])}</span>')
    if t["deleg"]:
        nao = t["deleg"].lower().startswith("n")
        chips.append(f'<span class="chip {"naodeleg" if nao else "deleg"}">{html.escape(t["deleg"])}</span>')
    return f'<div class="card"><div class="t">{html.escape(t["titulo"])}</div>{"<div class=chips>" + "".join(chips) + "</div>" if chips else ""}</div>'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hoje")
    a = ap.parse_args()
    hoje = date.fromisoformat(a.hoje) if a.hoje else date.today()
    dados = ler()
    atrasadas = sum(1 for k in ("backlog", "para amanhã", "in progress") for t in dados[k] if t["prazo"] and t["prazo"] < hoje)
    wip = len(dados["in progress"])

    colunas = []
    for k, nome in SECOES.items():
        cartoes = "".join(cartao(t, k, hoje) for t in dados[k]) or '<div class="vazio">Sem tarefas</div>'
        amanha = proximo_dia_util(hoje)
        sub = f'<div class="subcol">{DIAS_SEM[amanha.weekday()]} {fmt(amanha)}</div>' if k == "para amanhã" else ""
        colunas.append(f'<section class="col {CLASSE[k]}"><h2>{nome} <b>{len(dados[k])}</b></h2>{sub}{cartoes}</section>')

    avisos = []
    if atrasadas:
        avisos.append(f'<li class="forte"><b>{atrasadas} {"tarefa atrasada" if atrasadas == 1 else "tarefas atrasadas"}</b></li>')
    if wip > LIMITE_WIP:
        avisos.append(f'<li class="forte"><b>In progress com {wip} tarefas:</b> muitas em simultâneo. Vale a pena fechar algumas antes de abrir novas.</li>')
    presas = [t for k in ("para amanhã", "in progress") for t in dados[k] if t["adiada"] >= 2]
    if presas:
        avisos.append(f'<li class="forte"><b>{len(presas)} {"tarefa adiada" if len(presas) == 1 else "tarefas adiadas"} 2 vezes ou mais:</b> vale a pena perceber o que as prende.</li>')
    if len(dados["para amanhã"]) > LIMITE_AMANHA:
        avisos.append(f'<li class="forte"><b>Para amanhã com {len(dados["para amanhã"])} tarefas:</b> um plano com mais de {LIMITE_AMANHA} prioridades dificilmente se cumpre.</li>')
    aviso_html = f'<ul class="avisos">{"".join(avisos)}</ul>' if avisos else ""

    css = f"""
@font-face{{font-family:'Poppins';font-weight:400;src:url('{FONTES}/Poppins-Regular.ttf')}}
@font-face{{font-family:'Poppins';font-weight:600;src:url('{FONTES}/Poppins-SemiBold.ttf')}}
@font-face{{font-family:'Poppins';font-weight:700;src:url('{FONTES}/Poppins-Bold.ttf')}}
@font-face{{font-family:'Titulo';font-weight:400 900;src:url('{FONTES}/PlayfairDisplay-Variable.ttf')}}
:root{{--azul:#1f3e6f;--rosa:#d6b7b6;--bege:#d8c5ae}}
*{{box-sizing:border-box}}
body{{margin:0;padding:22px 28px;background:#faf8f5;color:var(--azul);font-family:'Poppins',sans-serif}}
h1{{font-family:'Titulo',serif;font-size:30px;margin:0 0 2px}}
.sub{{font-size:14px;font-weight:600;margin-bottom:14px}}
.quadro{{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;align-items:start}}
.col{{background:#fff;border:2px solid var(--azul);border-radius:16px;padding:14px;min-height:300px}}
.col h2{{margin:0 0 12px;padding:8px 14px;border-radius:10px;font-size:19px;font-weight:700;display:flex;justify-content:space-between}}
.col h2 b{{font-weight:700}}
.backlog h2{{background:var(--bege)}}.amanha h2{{background:#f1ede7;border:2px solid var(--azul)}}.subcol{{font-size:14px;font-weight:600;margin:-6px 0 10px 4px}}.inprogress h2{{background:var(--azul);color:#fff}}.done h2{{background:var(--rosa)}}
.card{{border:1.5px solid var(--azul);border-radius:12px;padding:12px 14px;margin-bottom:10px;background:#fff}}
.t{{font-size:17px;font-weight:600;line-height:1.3}}
.chips{{display:flex;gap:8px;flex-wrap:wrap;margin-top:9px}}
.chip{{font-size:14px;font-weight:600;padding:3px 11px;border-radius:999px;border:1.5px solid var(--azul)}}
.chip.atrasada{{background:var(--rosa)}}.chip.hoje{{background:var(--bege)}}
.chip.deleg{{background:var(--azul);color:#fff}}.chip.naodeleg{{background:#f1ede7}}
.chip.feito{{background:#f1ede7}}.chip.adiada{{background:var(--bege)}}.chip.adiada.forte{{background:var(--rosa)}}.chip.bloq{{border-style:dashed}}
.vazio{{font-size:16px;font-weight:600;padding:18px 6px;text-align:center;opacity:.7}}
.avisos{{list-style:none;padding:0;margin:0 0 14px}}
.avisos li{{font-size:17px;padding:8px 14px;margin-bottom:6px;background:#f3eae9;border-left:6px solid var(--azul);border-radius:6px}}
"""
    doc = f"""<!DOCTYPE html><html lang="pt-PT"><head><meta charset="utf-8"><meta http-equiv="refresh" content="3"><title>Tarefas</title><style>{css}</style></head><body>
<h1>AS MINHAS TAREFAS</h1><div class="sub">gerado a {hoje.day} {MESES[hoje.month-1]} {hoje.year}</div>
{aviso_html}<div class="quadro">{"".join(colunas)}</div></body></html>"""
    SAIDA.write_text(doc, encoding="utf-8")
    print(SAIDA)
    print(f"Backlog {len(dados['backlog'])} · Para amanhã {len(dados['para amanhã'])} · In progress {wip} · Done {len(dados['done'])} · atrasadas {atrasadas}")


main()
