#!/usr/bin/env python3
"""Genera app/panel_laclave.html a partir de registro/registro.csv y
registro/notas_historico.csv.

Uso:  python3 scripts/panel.py   (desde la raíz del repositorio)

El panel incluye estadísticas generales y, desde v2, el índice de
credibilidad completo por medio: rangos de veracidad desplegables,
buscador, papel de cada medio (origen / desmiente / confirma) y
evolución de su nota a lo largo de las revisiones.
"""
import csv
import html
import os
from collections import Counter, defaultdict
from datetime import date

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRO = os.path.join(RAIZ, "registro", "registro.csv")
HISTORICO = os.path.join(RAIZ, "registro", "notas_historico.csv")
SALIDA = os.path.join(RAIZ, "app", "panel_laclave.html")

# Alias que aparecen en el registro → nombre canónico del catálogo
ALIAS = {
    "Maldita": "Maldita.es", "Maldita Ciencia": "Maldita.es",
    "BNR": "BNR / Radio Bulgaria", "Radio Bulgaria": "BNR / Radio Bulgaria",
    "BBC": "BBC News / BBC Mundo", "BBC Mundo": "BBC News / BBC Mundo", "BBC News": "BBC News / BBC Mundo",
    "Der Spiegel": "Der Spiegel Int.", "Spiegel": "Der Spiegel Int.",
    "France24": "France 24", "NYT": "New York Times", "FT": "Financial Times",
    "El Pais": "El País", "eldiario.es": "elDiario.es",
    "Sofia Globe": "The Sofia Globe",
}

BANDAS = [
    (9.0, 10.01, "9 – 10 · Máxima exigencia verificadora"),
    (8.0, 9.0, "8 – 8.9 · Referencia sólida"),
    (7.0, 8.0, "7 – 7.9 · Fiable con sesgo o limitaciones"),
    (5.5, 7.0, "5.5 – 6.9 · Usable con cautela"),
    (4.0, 5.5, "4 – 5.4 · Baja fiabilidad"),
    (0.0, 4.0, "< 4 · Sin uso como fuente de contraste"),
]

VERDICT_META = [  # (nombre, var CSS, descripción tooltip)
    ("Verdadero", "--v-verdadero", "Confirmado por fuentes fiables."),
    ("Mayormente cierto", "--v-mcierto", "Cierto con algún matiz o detalle erróneo."),
    ("Mezcla", "--v-mcierto", "Partes ciertas y partes falsas."),
    ("Engañoso", "--v-enganoso", "Hechos reales con marco que induce a error."),
    ("Falso", "--v-falso", "Fabricaciones: contenido inventado o manipulado."),
]

ORIGEN_GRUPOS = [
    ("Cadenas y cuentas anónimas en redes", ["cadena", "redes", "viral", "tiktok", "cuenta de x", "facebook", "imagen"]),
    ("Declaraciones políticas y oficiales", ["declaración", "portavoces"]),
    ("Redes de desinformación organizadas", ["youtube", "sputnik", "acodap", "red de"]),
]


def leer(ruta):
    with open(ruta, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=";"))


def canon(nombre):
    n = nombre.split("(")[0].strip()
    return ALIAS.get(n, n)


def partes(campo):
    out = []
    for p in (campo or "").split(","):
        p = p.strip()
        if p and p.lower() not in {"ninguno", "sin medio"}:
            out.append(canon(p))
    return out


def e(s):
    return html.escape(str(s), quote=True)


def fnum(x):
    return f"{x:g}".replace(".", ",")


def sparkline(serie, ancho=72, alto=20):
    """Polilínea SVG para una serie de notas (mín. 2 puntos)."""
    xs = [i * (ancho - 8) / (len(serie) - 1) + 4 for i in range(len(serie))]
    lo, hi = min(serie), max(serie)
    if hi - lo < 0.5:
        lo, hi = lo - 0.5, hi + 0.5
    ys = [alto - 4 - (v - lo) * (alto - 8) / (hi - lo) for v in serie]
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    ult = f'<circle cx="{xs[-1]:.1f}" cy="{ys[-1]:.1f}" r="2.6" fill="var(--serie-1)"/>'
    return (f'<svg width="{ancho}" height="{alto}" aria-hidden="true">'
            f'<polyline points="{pts}" fill="none" stroke="var(--serie-1)" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round"/>{ult}</svg>')


def main():
    reg = leer(REGISTRO)
    hist = leer(HISTORICO)
    hoy = date.today().strftime("%d-%m-%Y")

    reales = [r for r in reg if r["lote"] == "real"]
    calib = [r for r in reg if r["lote"] == "calibracion"]

    # ---- agregados generales ----
    cv = Counter(r["veredicto"] for r in reg)
    problem = sum(cv[v] for v in ("Falso", "Engañoso", "Mezcla"))
    notas_prob = [float(r["nota"]) for r in reg if r["veredicto"] in ("Falso", "Engañoso", "Mezcla") and r["nota"]]
    notas_ok = [float(r["nota"]) for r in reg if r["veredicto"] in ("Verdadero", "Mayormente cierto") and r["nota"]]
    media_prob = sum(notas_prob) / len(notas_prob) if notas_prob else 0
    media_ok = sum(notas_ok) / len(notas_ok) if notas_ok else 0

    desmiente, confirma, origen_medio = Counter(), Counter(), Counter()
    origen_texto = []
    for r in reg:
        for m in partes(r["medios_desmienten"]):
            desmiente[m] += 1
        for m in partes(r["medios_confirman"]):
            confirma[m] += 1
        mo = (r["medio_origen"] or "").strip()
        if mo and not mo.lower().startswith("sin medio") and mo.lower() != "desconocido":
            origen_texto.append(mo)

    # ---- catálogo: nota vigente y serie por medio ----
    series = defaultdict(list)   # medio -> [(fecha, nota)]
    grupo_de = {}
    for h in hist:
        series[h["medio"]].append((h["fecha_revision"], float(h["nota_nueva"])))
        grupo_de[h["medio"]] = h["grupo"]
    for m in series:
        series[m].sort()
    catalogo = {m: s[-1][1] for m, s in series.items()}

    for mo in origen_texto:
        cm = canon(mo)
        if cm in catalogo:
            origen_medio[cm] += 1

    # agrupar orígenes para la tabla general
    grupos_origen = Counter()
    for mo in origen_texto:
        base = mo.lower()
        if canon(mo) in catalogo:
            grupos_origen["Medios de comunicación"] += 1
            continue
        for etiqueta, claves in ORIGEN_GRUPOS:
            if any(k in base for k in claves):
                grupos_origen[etiqueta] += 1
                break
        else:
            grupos_origen["Otros orígenes"] += 1

    # ---- HTML: secciones ----
    def barras(datos, var_o_color, tips):
        mx = max(v for _, v in datos) or 1
        filas = []
        for (nombre, valor), tip in zip(datos, tips):
            w = max(4, 100 * valor / mx)
            filas.append(
                f'<div class="row"><div class="name">{e(nombre)}</div>'
                f'<div class="track"><div class="bar" style="width:{w:.1f}%;background:var({var_o_color})" '
                f'data-tip="{e(tip)}"></div></div><div class="val">{e(valor)}</div></div>')
        return "\n".join(filas)

    # veredictos
    vrows = []
    mxv = max(cv.values())
    for nombre, var, desc in VERDICT_META:
        n = cv.get(nombre, 0)
        if not n:
            continue
        w = max(4, 100 * n / mxv)
        pct = round(100 * n / len(reg))
        vrows.append(
            f'<div class="row"><div class="name"><span class="chip" style="background:var({var})"></span>{e(nombre)}</div>'
            f'<div class="track"><div class="bar" style="width:{w:.1f}%;background:var({var})" '
            f'data-tip="<b>{e(nombre)} — {n} casos ({pct} %)</b><br>{e(desc)}"></div></div>'
            f'<div class="val">{n} · {pct} %</div></div>')
    veredictos_html = "\n".join(vrows)

    top_desm = desmiente.most_common(6)
    desm_html = barras(
        top_desm, "--serie-1",
        [f"<b>{e(m)} — {n} desmentidos</b><br>Nota en el catálogo: {fnum(catalogo.get(m, 0)) if m in catalogo else 'fuera de catálogo'}."
         for m, n in top_desm])
    resto_desm = [f"{e(m)} ({n})" for m, n in desmiente.most_common()[6:]]

    origen_rows = "\n".join(
        f'<tr><td>{e(k)}</td><td class="n">{v}</td></tr>'
        for k, v in grupos_origen.most_common())

    # ---- sección por medio ----
    bandas_html = []
    for lo, hi, titulo in BANDAS:
        medios = sorted(((m, n) for m, n in catalogo.items() if lo <= n < hi),
                        key=lambda x: (-x[1], x[0]))
        if not medios:
            continue
        filas = []
        for m, nota in medios:
            s = series[m]
            o, d, c = origen_medio.get(m, 0), desmiente.get(m, 0), confirma.get(m, 0)
            stats = []
            if o: stats.append(f'<span class="st sto" data-tip="<b>{e(m)}</b><br>Origen o publicador de contenido falso/engañoso en {o} caso(s) del registro.">origen {o}</span>')
            if d: stats.append(f'<span class="st std" data-tip="<b>{e(m)}</b><br>Desmintió {d} caso(s) del registro.">desmiente {d}</span>')
            if c: stats.append(f'<span class="st stc" data-tip="<b>{e(m)}</b><br>Sostuvo hechos ciertos en {c} caso(s).">confirma {c}</span>')
            stats_html = " ".join(stats) or '<span class="st st0">sin apariciones aún</span>'
            if len(s) > 1:
                delta = s[-1][1] - s[0][1]
                signo = "▲" if delta > 0 else ("▼" if delta < 0 else "•")
                cls = "up" if delta > 0 else ("down" if delta < 0 else "")
                evo = (f'{sparkline([v for _, v in s])}'
                       f'<span class="delta {cls}" data-tip="<b>{e(m)}</b><br>Nota inicial {fnum(s[0][1])} ({e(s[0][0])}) → actual {fnum(s[-1][1])} ({e(s[-1][0])}), en {len(s)} revisiones.">'
                       f'{signo} {fnum(abs(delta))}</span>')
            else:
                evo = f'<span class="delta" data-tip="Semilla del {e(s[0][0])}; la serie se dibujará con las revisiones del índice (1.ª: octubre de 2026).">— semilla</span>'
            filas.append(
                f'<div class="mrow" data-nombre="{e(m.lower())}">'
                f'<div class="mname">{e(m)}<span class="mgrupo">{e(grupo_de.get(m, ""))}</span></div>'
                f'<div class="meter" data-tip="<b>{e(m)}</b><br>Nota de credibilidad: {fnum(nota)}/10."><i style="width:{nota * 10:.0f}%"></i></div>'
                f'<div class="mnota">{fnum(nota)}</div>'
                f'<div class="mstats">{stats_html}</div>'
                f'<div class="mevo">{evo}</div></div>')
        bandas_html.append(
            f'<details class="banda"><summary><span>{e(titulo)}</span>'
            f'<span class="bcount">{len(medios)} medios</span></summary>\n' + "\n".join(filas) + "\n</details>")
    bandas_html = "\n".join(bandas_html)

    resto_nota = f' También con 1: {", ".join(resto_desm)}.' if resto_desm else ""

    tpl = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Panel LaClave — Verificador personal de noticias</title>
<style>
  .viz-root {{
    color-scheme: light;
    --surface-1: #fcfcfb; --page: #f9f9f7;
    --ink-1: #0b0b0b; --ink-2: #52514e; --ink-3: #898781;
    --grid: #e1e0d9; --baseline: #c3c2b7; --ring: rgba(11,11,11,0.10);
    --v-verdadero: #2a78d6; --v-mcierto: #1baf7a; --v-enganoso: #4a3aa7; --v-falso: #e34948;
    --serie-1: #2a78d6; --delta-good: #006300; --delta-bad: #d03b3b; --wash: rgba(42,120,214,0.08);
  }}
  @media (prefers-color-scheme: dark) {{
    :root:where(:not([data-theme="light"])) .viz-root {{
      color-scheme: dark;
      --surface-1: #1a1a19; --page: #0d0d0d;
      --ink-1: #ffffff; --ink-2: #c3c2b7; --ink-3: #898781;
      --grid: #2c2c2a; --baseline: #383835; --ring: rgba(255,255,255,0.10);
      --v-verdadero: #3987e5; --v-mcierto: #199e70; --v-enganoso: #9085e9; --v-falso: #e66767;
      --serie-1: #3987e5; --delta-good: #0ca30c; --delta-bad: #e66767; --wash: rgba(57,135,229,0.14);
    }}
  }}
  :root[data-theme="dark"] .viz-root {{
    color-scheme: dark;
    --surface-1: #1a1a19; --page: #0d0d0d;
    --ink-1: #ffffff; --ink-2: #c3c2b7; --ink-3: #898781;
    --grid: #2c2c2a; --baseline: #383835; --ring: rgba(255,255,255,0.10);
    --v-verdadero: #3987e5; --v-mcierto: #199e70; --v-enganoso: #9085e9; --v-falso: #e66767;
    --serie-1: #3987e5; --delta-good: #0ca30c; --delta-bad: #e66767; --wash: rgba(57,135,229,0.14);
  }}
  * {{ box-sizing: border-box; margin: 0; }}
  body.viz-root {{ font-family: system-ui, -apple-system, "Segoe UI", sans-serif; background: var(--page); color: var(--ink-1); padding: 20px 16px 32px; }}
  .wrap {{ max-width: 880px; margin: 0 auto; }}
  header h1 {{ font-size: 19px; font-weight: 650; letter-spacing: -0.01em; }}
  header p {{ font-size: 12.5px; color: var(--ink-2); margin-top: 3px; }}
  .card {{ background: var(--surface-1); border: 1px solid var(--ring); border-radius: 10px; padding: 16px 18px; margin-top: 14px; }}
  h2 {{ font-size: 13px; font-weight: 650; }}
  .sub {{ font-size: 11.5px; color: var(--ink-3); margin-bottom: 12px; }}
  .kpis {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 14px; margin-top: 14px; }}
  .kpi {{ background: var(--surface-1); border: 1px solid var(--ring); border-radius: 10px; padding: 13px 15px; }}
  .kpi .v {{ font-size: 26px; font-weight: 650; letter-spacing: -0.02em; }}
  .kpi .l {{ font-size: 11.5px; color: var(--ink-2); margin-top: 2px; line-height: 1.35; }}
  .kpi .d {{ font-size: 11px; color: var(--ink-3); margin-top: 4px; }}
  .good {{ color: var(--delta-good); font-weight: 600; }}
  .row {{ display: grid; grid-template-columns: 150px 1fr 58px; align-items: center; gap: 10px; padding: 4px 0; }}
  .row .name {{ font-size: 12.5px; text-align: right; }}
  .row .val {{ font-size: 12px; color: var(--ink-2); font-variant-numeric: tabular-nums; }}
  .track {{ position: relative; height: 20px; }}
  .track::before {{ content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 2px; background: var(--baseline); }}
  .bar {{ position: absolute; left: 2px; top: 1px; bottom: 1px; border-radius: 0 4px 4px 0; min-width: 4px; transition: filter .12s; }}
  .bar:hover {{ filter: brightness(1.12); }}
  .chip {{ display: inline-block; width: 9px; height: 9px; border-radius: 2px; margin-right: 6px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 12.5px; }}
  th {{ text-align: left; color: var(--ink-3); font-weight: 550; font-size: 11px; padding: 4px 8px 6px 0; border-bottom: 1px solid var(--grid); }}
  td {{ padding: 6px 8px 6px 0; border-bottom: 1px solid var(--grid); }}
  td.n {{ text-align: right; font-variant-numeric: tabular-nums; color: var(--ink-2); }}
  tr:last-child td {{ border-bottom: none; }}
  .note {{ font-size: 11.5px; color: var(--ink-3); margin-top: 10px; line-height: 1.5; }}
  footer {{ font-size: 11px; color: var(--ink-3); margin-top: 18px; line-height: 1.6; }}
  a {{ color: var(--serie-1); text-decoration: none; }}
  #tip {{ position: fixed; pointer-events: none; z-index: 10; display: none; background: var(--surface-1); border: 1px solid var(--ring); border-radius: 7px; padding: 7px 10px; font-size: 12px; box-shadow: 0 4px 14px rgba(0,0,0,.18); max-width: 250px; line-height: 1.45; }}
  .grid2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }}
  /* Índice por medio */
  #buscador {{ width: 100%; padding: 8px 12px; font-size: 13px; color: var(--ink-1); background: var(--page); border: 1px solid var(--ring); border-radius: 8px; margin-bottom: 10px; }}
  #buscador:focus {{ outline: 2px solid var(--serie-1); outline-offset: 1px; }}
  details.banda {{ border-top: 1px solid var(--grid); }}
  details.banda:last-of-type {{ border-bottom: 1px solid var(--grid); }}
  details.banda summary {{ display: flex; align-items: baseline; cursor: pointer; padding: 9px 2px; font-size: 12.5px; font-weight: 600; list-style: none; }}
  details.banda summary::before {{ content: "▸"; color: var(--ink-3); margin-right: 8px; font-size: 11px; }}
  details.banda[open] summary::before {{ content: "▾"; }}
  details.banda summary:hover {{ background: var(--wash); border-radius: 6px; }}
  .bcount {{ font-size: 11px; color: var(--ink-3); font-weight: 500; margin-left: auto; }}
  .mrow {{ display: grid; grid-template-columns: minmax(150px, 1.3fr) 90px 34px 1.2fr 110px; gap: 10px; align-items: center; padding: 5px 2px 5px 20px; font-size: 12.5px; border-top: 1px dashed var(--grid); }}
  .mname {{ line-height: 1.25; }}
  .mgrupo {{ display: block; font-size: 10.5px; color: var(--ink-3); }}
  .meter {{ height: 8px; background: var(--grid); border-radius: 4px; overflow: hidden; }}
  .meter i {{ display: block; height: 100%; background: var(--serie-1); border-radius: 4px 0 0 4px; }}
  .mnota {{ font-variant-numeric: tabular-nums; font-weight: 600; font-size: 12px; }}
  .mstats {{ display: flex; flex-wrap: wrap; gap: 4px; }}
  .st {{ font-size: 10.5px; padding: 2px 7px; border-radius: 999px; border: 1px solid var(--grid); color: var(--ink-2); white-space: nowrap; }}
  .st.sto {{ border-color: var(--v-falso); }}
  .st.std {{ border-color: var(--serie-1); }}
  .st.stc {{ border-color: var(--v-mcierto); }}
  .st.st0 {{ color: var(--ink-3); border-style: dashed; }}
  .mevo {{ display: flex; align-items: center; gap: 6px; justify-content: flex-end; }}
  .delta {{ font-size: 11px; color: var(--ink-3); white-space: nowrap; }}
  .delta.up {{ color: var(--delta-good); font-weight: 600; }}
  .delta.down {{ color: var(--delta-bad); font-weight: 600; }}
  @media (max-width: 680px) {{
    .grid2 {{ grid-template-columns: 1fr; }}
    .row {{ grid-template-columns: 118px 1fr 52px; }}
    .mrow {{ grid-template-columns: minmax(120px, 1.4fr) 60px 30px 1fr; }}
    .mevo {{ display: none; }}
  }}
</style>
</head>
<body class="viz-root">
<div class="wrap">
  <header>
    <h1>🔎 Panel LaClave</h1>
    <p>Verificador personal de noticias · actualizado el {hoy} · {len(reg)} verificaciones registradas ({len(reales)} de uso real + {len(calib)} de calibración)</p>
  </header>

  <div class="kpis">
    <div class="kpi"><div class="v">{len(reg)}</div><div class="l">verificaciones registradas</div><div class="d">{len(reales)} reales · {len(calib)} de calibración</div></div>
    <div class="kpi"><div class="v">{problem}</div><div class="l">bulos o engaños detectados</div><div class="d">{round(100 * problem / len(reg))} % de lo verificado · nota media {fnum(round(media_prob, 1))}/10</div></div>
    <div class="kpi"><div class="v good">96,7 %</div><div class="l">acierto direccional en la calibración</div><div class="d">29/30 · 0 bulos aprobados · 0 falsos positivos</div></div>
    <div class="kpi"><div class="v">{len(catalogo)}</div><div class="l">medios en el índice de credibilidad</div><div class="d">próxima revisión: octubre de 2026</div></div>
  </div>

  <div class="card">
    <h2>Veredictos emitidos</h2>
    <div class="sub">{len(reg)} verificaciones · la escala va de Verdadero a Falso</div>
    {veredictos_html}
    <div class="note">El color acompaña a la etiqueta, nunca la sustituye. Contenido problemático (Falso + Engañoso + Mezcla): {problem} casos, nota media {fnum(round(media_prob, 1))}/10 · contenido verídico: {len(notas_ok)} casos, nota media {fnum(round(media_ok, 1))}/10.</div>
  </div>

  <div class="card">
    <h2>Quién desmintió los casos problemáticos</h2>
    <div class="sub">Fuentes que desmontaron los {problem} casos falsos o engañosos (un caso puede tener varias)</div>
    {desm_html}
    <div class="note">{resto_nota} La regla «fact-check first» encontró dictamen profesional en 19 de los 20 casos problemáticos de la calibración.</div>
  </div>

  <div class="card">
    <h2>Índice de credibilidad, medio a medio</h2>
    <div class="sub">{len(catalogo)} medios agrupados por rango de veracidad · con su papel en el registro y la evolución de su nota · toca cada rango para desplegarlo</div>
    <input id="buscador" type="search" placeholder="Buscar un medio… (p. ej. RTVE, Dnevnik, Vozpópuli)" aria-label="Buscar un medio">
    {bandas_html}
    <div class="note">Las notas son hipótesis de trabajo sembradas con criterios citables (EFCSN/IFCN, confianza DNR 2026, MBFC, propiedad); las revisiones trimestrales —con evidencia del registro y aprobación de Jordi— las irán confirmando o corrigiendo, y aquí se dibujará la serie de cada medio (▲ sube, ▼ baja). Etiquetas por medio: <b>origen</b> = publicó u originó contenido falso/engañoso · <b>desmiente</b> = lo desmontó · <b>confirma</b> = sostuvo hechos ciertos.</div>
  </div>

  <div class="card">
    <h2>De dónde salió lo falso o engañoso</h2>
    <div class="sub">Origen de los {problem} casos problemáticos</div>
    <table>
      <tr><th>Origen</th><th style="text-align:right">Casos</th></tr>
      {origen_rows}
    </table>
    <div class="note">Los casos con medio identificado se reflejan también en la etiqueta «origen» de la sección por medio.</div>
  </div>

  <footer>
    Datos: <code>registro/registro.csv</code> y <code>registro/notas_historico.csv</code> · generado con <code>scripts/panel.py</code> · detalle en <code>ANALITICAS.md</code> ·
    repositorio: <a href="https://github.com/Jomenew16/LaClave">github.com/Jomenew16/LaClave</a>. Este panel se actualiza cada vez que se archivan verificaciones o se revisa el índice.
  </footer>
</div>
<div id="tip"></div>
<script>
  (function () {{
    var tip = document.getElementById("tip");
    document.querySelectorAll("[data-tip]").forEach(function (b) {{
      b.addEventListener("mousemove", function (ev) {{
        tip.innerHTML = b.getAttribute("data-tip");
        tip.style.display = "block";
        var x = Math.min(ev.clientX + 14, window.innerWidth - tip.offsetWidth - 10);
        var y = Math.min(ev.clientY + 14, window.innerHeight - tip.offsetHeight - 10);
        tip.style.left = x + "px"; tip.style.top = y + "px";
      }});
      b.addEventListener("mouseleave", function () {{ tip.style.display = "none"; }});
    }});
    var q = document.getElementById("buscador");
    q.addEventListener("input", function () {{
      var t = q.value.trim().toLowerCase();
      document.querySelectorAll("details.banda").forEach(function (d) {{
        var visibles = 0;
        d.querySelectorAll(".mrow").forEach(function (r) {{
          var ok = !t || r.getAttribute("data-nombre").indexOf(t) !== -1;
          r.style.display = ok ? "" : "none";
          if (ok) visibles++;
        }});
        if (t) {{ d.open = visibles > 0; d.style.display = visibles ? "" : "none"; }}
        else {{ d.style.display = ""; d.open = false; }}
      }});
    }});
  }})();
</script>
</body>
</html>
"""
    with open(SALIDA, "w", encoding="utf-8") as f:
        f.write(tpl)
    print(f"OK → {SALIDA}")
    print(f"  medios en catálogo: {len(catalogo)} | con actividad: "
          f"{len([m for m in catalogo if origen_medio.get(m) or desmiente.get(m) or confirma.get(m)])}")


if __name__ == "__main__":
    main()
