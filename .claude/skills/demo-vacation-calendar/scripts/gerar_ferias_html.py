#!/usr/bin/env python3
"""Gera o calendário de férias da equipa (HTML) a partir de talk/demos/ferias/ferias.md.

Uso (na raiz do projeto):
  python3 .claude/skills/demo-vacation-calendar/scripts/gerar_ferias_html.py [--de AAAA-MM-DD] [--ate AAAA-MM-DD] [--hoje AAAA-MM-DD]
"""
import argparse, html, re, sys
from datetime import date, timedelta
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
FONTE = RAIZ / "talk/demos/ferias/ferias.md"
SAIDA = RAIZ / "talk/demos/ferias/ferias.html"
FONTES = "../../../fontes"
BANDEIRA = {"Portugal": "🇵🇹", "Polónia": "🇵🇱", "Roménia": "🇷🇴", "Espanha": "🇪🇸", "Brasil": "🇧🇷"}
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
DIAS = "SDTQQSS"  # segunda=0 ... usado com (weekday()+1)%7 para D S T Q Q S S
LETRA = ["S", "T", "Q", "Q", "S", "S", "D"]  # weekday(): seg=0


def d(s):
    return date.fromisoformat(s.strip())


def ler():
    sec, pessoas, ferias, feriados, marcos = None, [], [], [], []
    for linha in FONTE.read_text(encoding="utf-8").splitlines():
        if linha.startswith("## "):
            sec = linha[3:].strip().lower()
            continue
        if not linha.startswith("- ") or sec is None:
            continue
        p = [x.strip() for x in linha[2:].split("|")]
        try:
            if sec == "pessoas":
                pessoas.append({"nome": p[0], "pais": p[1], "fonte": p[2] if len(p) > 2 else ""})
            elif sec == "férias":
                a, b = re.split(r"\s+a\s+", p[1])
                ferias.append({"nome": p[0], "ini": d(a), "fim": d(b), "estado": p[2].lower(), "fonte": p[3] if len(p) > 3 else ""})
            elif sec == "feriados":
                feriados.append({"pais": p[0], "dia": d(p[1]), "nome": p[2]})
            elif sec == "marcos":
                marcos.append({"dia": d(p[0]), "nome": p[1]})
        except Exception as e:
            sys.exit(f"Erro na linha: {linha}\n{e}")
    nomes = {x["nome"] for x in pessoas}
    for f in ferias:
        if f["nome"] not in nomes:
            sys.exit(f"Férias de pessoa desconhecida: {f['nome']} (acrescentar a ## Pessoas)")
    return pessoas, ferias, feriados, marcos


def intervalos(dias):
    """Agrupa uma lista ordenada de datas em intervalos consecutivos."""
    out = []
    for x in dias:
        if out and (x - out[-1][1]).days == 1:
            out[-1][1] = x
        else:
            out.append([x, x])
    return out


def fmt(x):
    return f"{x.day} {MESES[x.month-1][:3]}"


def per(a, b):
    return fmt(a) if a == b else f"{fmt(a)} a {fmt(b)}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--de"); ap.add_argument("--ate"); ap.add_argument("--hoje")
    a = ap.parse_args()
    hoje = d(a.hoje) if a.hoje else date.today()
    pessoas, ferias, feriados, marcos = ler()

    ini = d(a.de) if a.de else hoje.replace(day=1)
    if a.ate:
        fim = d(a.ate)
    else:
        m2 = ini.month % 12 + 1
        a2 = ini.year + (1 if ini.month == 12 else 0)
        fim = date(a2 + (1 if m2 == 12 else 0), m2 % 12 + 1, 1) - timedelta(days=1)
    dias = [ini + timedelta(days=i) for i in range((fim - ini).days + 1)]

    fer_pais = {(f["pais"], f["dia"]): f["nome"] for f in feriados}
    pais = {p["nome"]: p["pais"] for p in pessoas}
    fora = {}  # dia -> lista de nomes
    estado = {}  # (nome, dia) -> (estado, fonte)
    for f in ferias:
        x = f["ini"]
        while x <= f["fim"]:
            if x.weekday() < 5 and (pais[f["nome"]], x) not in fer_pais:  # fins de semana e feriados do país nunca contam nem se mostram como férias
                estado[(f["nome"], x)] = (f["estado"], f["fonte"])
            if x.weekday() < 5 and (pais[f["nome"]], x) not in fer_pais:
                fora.setdefault(x, []).append(f["nome"])
            x += timedelta(days=1)

    def uteis(nome):
        return sum(1 for (n, x), _ in estado.items() if n == nome and x.weekday() < 5 and (pais[n], x) not in fer_pais)

    # cabeçalho
    meses_html, dia_html = [], []
    i = 0
    while i < len(dias):
        j = i
        while j < len(dias) and dias[j].month == dias[i].month:
            j += 1
        nome_mes = MESES[dias[i].month-1].capitalize() + f" {dias[i].year}" if j - i >= 8 else MESES[dias[i].month-1][:3].capitalize()
        meses_html.append(f'<th colspan="{j-i}" class="mes">{nome_mes}</th>')
        i = j
    for x in dias:
        c = "fds" if x.weekday() >= 5 else ""
        c += " hoje" if x == hoje else ""
        c += " ini-sem" if x.weekday() == 0 else ""
        dia_html.append(f'<th class="dia {c}"><b>{x.day}</b><span>{LETRA[x.weekday()]}</span></th>')

    marco_dias = {m["dia"]: m["nome"] for m in marcos}

    def celula(nome, x):
        cls, tip = [], []
        if x.weekday() >= 5:
            cls.append("fds")
        if x.weekday() == 0:
            cls.append("ini-sem")
        if x == hoje:
            cls.append("hoje")
        fer = fer_pais.get((pais[nome], x))
        if fer:
            cls.append("feriado"); tip.append(f"Feriado: {fer}")
        if x in marco_dias:
            cls.append("marco"); tip.append(f"Marco: {marco_dias[x]}")
        e = estado.get((nome, x))
        txt = ""
        if e:
            cls.append("f-" + e[0]); tip.append(f"Férias ({e[0]}) · {e[1]}")
        elif fer:
            txt = "·"
        return f'<td class="{" ".join(cls)}" title="{html.escape(" · ".join(tip))}">{txt}</td>'

    linhas = []
    for p in pessoas:
        n = uteis(p["nome"])
        linhas.append(
            f'<tr><th class="nome"><div class="n">{html.escape(p["nome"])}</div>'
            f'<div class="s">{BANDEIRA.get(p["pais"], "")} {html.escape(p["pais"])} · {n} dias úteis</div></th>'
            + "".join(celula(p["nome"], x) for x in dias) + "</tr>")
    # linha marcos
    linhas.append('<tr class="r-marcos"><th class="nome"><div class="n">Marco</div><div class="s">data importante</div></th>' + "".join(
        f'<td class="mk {"fds" if x.weekday()>=5 else ""} {"ini-sem" if x.weekday()==0 else ""}">' + (f'<span class="mlbl">◆ {html.escape(marco_dias[x])}</span>' if x in marco_dias else "") + '</td>' for x in dias) + "</tr>")
    # linha de quem está fora
    total = len(pessoas)
    celulas = []
    for x in dias:
        n = len(fora.get(x, []))
        cls = "fds" if x.weekday() >= 5 else ""
        cls += " ini-sem" if x.weekday() == 0 else ""
        if n:
            cls += " cont c%d" % min(n, total)
        celulas.append(f'<td class="{cls}" title="{html.escape(", ".join(fora.get(x, [])))}">{n or ""}</td>')
    linhas.append('<tr class="r-fora"><th class="nome"><div class="n" style="font-size:17px">Pessoas ausentes</div><div class="s">nº de pessoas de férias</div></th>' + "".join(celulas) + "</tr>")

    # alertas
    alertas = []
    pend = [f for f in ferias if f["estado"] == "pendente"]
    for f in pend:
        alertas.append(f'<li><b>À espera da tua decisão:</b> {html.escape(f["nome"])}, {fmt(f["ini"])} a {fmt(f["fim"])} ({html.escape(f["fonte"])})</li>')
    sobrep = lambda k: [x for x in sorted(fora) if len(fora[x]) >= k and ini <= x <= fim]
    for k in range(total, 1, -1):
        for r in intervalos(sobrep(k)):
            alertas.append(f'<li class="{"forte" if k == total else ""}"><b>{k} de {total} fora ao mesmo tempo:</b> {per(r[0], r[1])} ({html.escape(", ".join(sorted(set(fora[r[0]]))))})</li>')
        # só mostrar o nível mais alto de cada dia
        break
    if total > 2:
        ja = {x for r in intervalos(sobrep(total)) for x in (r[0] + timedelta(days=i) for i in range((r[1]-r[0]).days+1))}
        resto = [x for x in sobrep(2) if x not in ja]
        for r in intervalos(resto):
            alertas.append(f'<li><b>2 fora ao mesmo tempo:</b> {per(r[0], r[1])}</li>')
    for f in ferias:
        for m in marcos:
            if f["ini"] <= m["dia"] <= f["fim"]:
                alertas.append(f'<li class="forte"><b>Coincide com um marco:</b> {html.escape(f["nome"])} está fora em "{html.escape(m["nome"])}" ({fmt(m["dia"])})</li>')
            elif 0 < (f["ini"] - m["dia"]).days <= 7:
                alertas.append(f'<li><b>Logo a seguir a um marco:</b> as férias de {html.escape(f["nome"])} começam {(f["ini"]-m["dia"]).days} {"dia" if (f["ini"]-m["dia"]).days == 1 else "dias"} depois de "{html.escape(m["nome"])}" ({fmt(m["dia"])})</li>')

    css = f"""
@font-face{{font-family:'Poppins';font-weight:400;src:url('{FONTES}/Poppins-Regular.ttf')}}
@font-face{{font-family:'Poppins';font-weight:600;src:url('{FONTES}/Poppins-SemiBold.ttf')}}
@font-face{{font-family:'Poppins';font-weight:700;src:url('{FONTES}/Poppins-Bold.ttf')}}
@font-face{{font-family:'Titulo';font-weight:400 900;src:url('{FONTES}/PlayfairDisplay-Variable.ttf')}}
:root{{--azul:#1f3e6f;--rosa:#d6b7b6;--bege:#d8c5ae}}
*{{box-sizing:border-box}}
body{{margin:0;padding:22px 28px;background:#faf8f5;color:var(--azul);font-family:'Poppins',sans-serif}}
h1{{font-family:'Titulo',serif;font-size:30px;margin:0 0 2px;letter-spacing:.5px}}
.sub{{font-size:14px;font-weight:600;margin-bottom:12px}}
.wrap{{overflow-x:auto;background:#fff;border:2px solid var(--azul);border-radius:16px}}
table{{border-collapse:collapse;table-layout:fixed;width:100%;min-width:calc(190px + var(--nd)*18px)}}
th.nome{{position:sticky;left:0;z-index:2;background:#fff;text-align:left;width:190px;min-width:190px;padding:5px 12px;border-right:2px solid var(--azul);border-bottom:1px solid #e6e0d8}}
.n{{font-size:19px;font-weight:700}}.s{{font-size:13px;font-weight:600;margin-top:2px}}
th.mes{{text-align:left;padding:6px 10px;font-size:17px;position:sticky;left:190px;font-weight:700;border-bottom:1px solid var(--azul);border-left:1px solid var(--azul)}}
th.dia{{font-weight:600;padding:4px 0;border-bottom:2px solid var(--azul);text-align:center}}
th.dia b{{display:block;font-size:12px;letter-spacing:-.3px}}th.dia span{{display:block;font-size:10px}}
td{{height:48px;border-bottom:1px solid #e6e0d8;text-align:center;font-size:14px;font-weight:700;padding:0}}
td,th.dia{{border-left:1px dashed #e6e6e6}}
.ini-sem{{border-left:1px dashed #cfcfcf!important}}
.fds{{background:#f1ede7}}
th.dia.hoje{{background:var(--azul);color:#fff}}td.hoje{{box-shadow:inset 2px 0 0 var(--azul),inset -2px 0 0 var(--azul)}}
.feriado{{background:repeating-linear-gradient(45deg,#fff,#fff 4px,#efe9e1 4px,#efe9e1 8px);color:var(--azul)}}
.f-aprovado{{background:var(--azul)!important;border-left-color:transparent!important}}
.f-pendente{{background:var(--bege)!important;box-shadow:inset 0 0 0 2px var(--azul)}}
.marco{{box-shadow:inset 0 0 0 2px var(--rosa)}}
.r-marcos td{{height:44px;position:relative;overflow:visible}}.mlbl{{position:absolute;left:2px;top:7px;z-index:1;white-space:nowrap;background:#fff;border:2px solid var(--azul);border-radius:8px;padding:3px 10px;font-size:14px;font-weight:700}}
.r-fora td{{height:38px;color:var(--azul);font-size:16px}}
.r-fora td.cont{{background:var(--rosa)}}.r-fora td.c3{{background:var(--azul);color:#fff}}
.leg{{display:flex;gap:28px;flex-wrap:wrap;margin:14px 0 4px;font-size:15px;font-weight:600}}
.leg i{{display:inline-block;width:16px;height:16px;border-radius:5px;vertical-align:-5px;margin-right:8px;border:1px solid var(--azul)}}
h2{{font-family:'Titulo',serif;font-size:22px;margin:18px 0 6px}}
ul{{list-style:none;padding:0;margin:0}}
li{{font-size:16px;padding:6px 12px;margin-bottom:6px;background:#fff;border-left:6px solid var(--bege);border-radius:6px}}
li.forte{{border-left-color:var(--azul);background:#f3eae9}}
"""
    leg = ('<div class="leg"><span><i style="background:var(--azul)"></i>Aprovadas</span>'
           '<span><i style="background:var(--bege);box-shadow:inset 0 0 0 2px var(--azul)"></i>À espera de aprovação</span>'
           '<span><i style="background:repeating-linear-gradient(45deg,#fff,#fff 3px,#e3dccf 3px,#e3dccf 6px)"></i>Feriado do país da pessoa</span>'
           '<span><i style="background:#f1ede7"></i>Fim de semana</span><span>◆ Marco = data importante do projeto</span></div>')
    doc = f"""<!DOCTYPE html><html lang="pt-PT"><head><meta charset="utf-8"><title>Férias da equipa</title><style>{css}</style></head><body>
<h1>FÉRIAS DA EQUIPA</h1><div class="sub">{fmt(dias[0])} a {fmt(dias[-1])} {dias[-1].year} · gerado a {hoje.day} {MESES[hoje.month-1]} {hoje.year}</div>
<div class="wrap"><table style="--nd:{len(dias)}"><thead><tr><th class="nome"></th>{"".join(meses_html)}</tr><tr><th class="nome"></th>{"".join(dia_html)}</tr></thead><tbody>{"".join(linhas)}</tbody></table></div>
{leg}
<h2>O que merece a tua atenção</h2><ul>{"".join(alertas) or "<li>Sem sobreposições nem conflitos.</li>"}</ul>
</body></html>"""
    SAIDA.write_text(doc, encoding="utf-8")
    print(SAIDA)
    for t in alertas:
        print("-", re.sub(r"<[^>]+>", "", t))


main()
