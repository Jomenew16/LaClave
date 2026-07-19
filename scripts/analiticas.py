#!/usr/bin/env python3
"""Genera ANALITICAS.md a partir de registro/registro.csv y registro/notas_historico.csv.

Uso:  python3 scripts/analiticas.py   (desde la raíz del repositorio)
"""
import csv
import io
import os
import sys
from collections import Counter, defaultdict
from datetime import date

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRO = os.path.join(RAIZ, "registro", "registro.csv")
HISTORICO = os.path.join(RAIZ, "registro", "notas_historico.csv")
SALIDA = os.path.join(RAIZ, "ANALITICAS.md")

VEREDICTOS_ORDEN = ["Verdadero", "Mayormente cierto", "Mezcla", "Engañoso", "Falso",
                    "Sin evidencia", "No verificable", "Opinión", "Sátira"]


def leer(ruta):
    with open(ruta, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=";"))


def partes(campo):
    """Divide un campo multi-valor por comas, limpiando paréntesis aclaratorios."""
    out = []
    for p in (campo or "").split(","):
        p = p.strip()
        if not p or p.lower() in {"ninguno", "sin medio"}:
            continue
        base = p.split("(")[0].strip()
        if base:
            out.append(base)
    return out


def tabla(filas, cabeceras):
    lineas = ["| " + " | ".join(cabeceras) + " |",
              "|" + "|".join(["---"] * len(cabeceras)) + "|"]
    for fila in filas:
        lineas.append("| " + " | ".join(str(c) for c in fila) + " |")
    return "\n".join(lineas)


def main():
    reg = leer(REGISTRO)
    hist = leer(HISTORICO)
    out = io.StringIO()
    w = out.write

    reales = [r for r in reg if r["lote"] == "real"]
    calib = [r for r in reg if r["lote"] == "calibracion"]

    w("# ANALITICAS.md — Analíticas del registro LaClave\n\n")
    w(f"Generado el {date.today().isoformat()} por `scripts/analiticas.py` · ")
    w(f"{len(reg)} verificaciones ({len(reales)} de uso real, {len(calib)} de calibración)\n\n")

    # --- Veredictos ---
    w("## Distribución de veredictos\n\n")
    c = Counter(r["veredicto"] for r in reg)
    filas = [(v, c[v], f"{100*c[v]/len(reg):.0f} %") for v in VEREDICTOS_ORDEN if c[v]]
    w(tabla(filas, ["Veredicto", "Casos", "%"]) + "\n\n")
    problem = sum(c[v] for v in ("Falso", "Engañoso", "Mezcla"))
    w(f"Contenido problemático (Falso/Engañoso/Mezcla): **{problem}/{len(reg)}** "
      f"({100*problem/len(reg):.0f} %).\n\n")

    # --- Ámbito y confianza ---
    w("## Por ámbito y confianza\n\n")
    ca = Counter(r["ambito"] for r in reg)
    cc = Counter(r["confianza"] for r in reg)
    w(tabla(sorted(ca.items(), key=lambda x: -x[1]), ["Ámbito", "Casos"]) + "\n\n")
    w(tabla([(k, v) for k, v in cc.items()], ["Confianza", "Casos"]) + "\n\n")

    # --- Medios: papeles ---
    w("## Medios por papel\n\n")
    origen = Counter()
    desmiente = Counter()
    confirma = Counter()
    for r in reg:
        mo = (r["medio_origen"] or "").strip()
        if mo and not mo.startswith("sin medio"):
            origen[mo.split("(")[0].strip()] += 1
        for m in partes(r["medios_desmienten"]):
            desmiente[m] += 1
        for m in partes(r["medios_confirman"]):
            confirma[m] += 1
        vp = (r["verificador_previo"] or "").strip()
        if vp and vp.lower() not in {"ninguno"} and not vp.startswith("no localizado"):
            desmiente[vp.split("(")[0].strip()] += 0  # ya contado en desmienten normalmente

    w("### Origen de contenido falso o engañoso\n\n")
    w("(cuenta solo casos con origen identificable)\n\n")
    w(tabla(origen.most_common(), ["Origen", "Casos"]) + "\n\n")

    w("### Desmentidores (fuentes que desmontaron casos)\n\n")
    w(tabla(desmiente.most_common(), ["Fuente", "Desmentidos"]) + "\n\n")

    w("### Confirmadores (fuentes que sostuvieron hechos ciertos)\n\n")
    w(tabla(confirma.most_common(12), ["Fuente", "Confirmaciones"]) + "\n\n")

    # --- Notas medias ---
    w("## Notas medias\n\n")
    notas_prob = [float(r["nota"]) for r in reg if r["veredicto"] in ("Falso", "Engañoso", "Mezcla") and r["nota"]]
    notas_ok = [float(r["nota"]) for r in reg if r["veredicto"] in ("Verdadero", "Mayormente cierto") and r["nota"]]
    filas = [("Contenido problemático", f"{sum(notas_prob)/len(notas_prob):.1f}/10" if notas_prob else "—"),
             ("Contenido verídico", f"{sum(notas_ok)/len(notas_ok):.1f}/10" if notas_ok else "—")]
    w(tabla(filas, ["Grupo", "Nota media"]) + "\n\n")

    # --- Evolución del índice ---
    w("## Índice de credibilidad: evolución\n\n")
    revs = sorted({h["fecha_revision"] for h in hist})
    w(f"Revisiones registradas: {len(revs)} ({', '.join(revs)}). ")
    cambios = [h for h in hist if h["nota_anterior"]]
    if not cambios:
        w("Por ahora solo existe la **semilla inicial** del catálogo; la serie temporal "
          "por medio empezará a dibujarse con la primera revisión (prevista: octubre de 2026).\n\n")
    else:
        w("Cambios de nota registrados:\n\n")
        w(tabla([(h["fecha_revision"], h["medio"], h["nota_anterior"], h["nota_nueva"], h["motivo"])
                 for h in cambios],
                ["Fecha", "Medio", "Antes", "Después", "Motivo"]) + "\n\n")

    grupos = defaultdict(list)
    for h in hist:
        # nota vigente = última fila por medio
        grupos[h["medio"]] = h
    por_grupo = defaultdict(list)
    for h in grupos.values():
        por_grupo[h["grupo"]].append((h["medio"], h["nota_nueva"]))
    w("Notas vigentes por grupo (nº de medios): ")
    w(" · ".join(f"{g} ({len(v)})" for g, v in por_grupo.items()) + "\n\n")

    # --- Fuera de catálogo ---
    w("## Medios fuera de catálogo detectados\n\n")
    catalogados = {h["medio"] for h in hist}
    fuera = Counter()
    for cnt in (desmiente, confirma):
        for m, n in cnt.items():
            if m not in catalogados:
                fuera[m] += n
    if fuera:
        w("Candidatos a incorporación si reaparecen (regla: ≥3 apariciones):\n\n")
        w(tabla(fuera.most_common(), ["Fuente", "Apariciones"]) + "\n\n")
    else:
        w("Ninguno.\n\n")

    with open(SALIDA, "w", encoding="utf-8") as f:
        f.write(out.getvalue())
    print(f"OK → {SALIDA}")
    print(f"  verificaciones: {len(reg)} | veredictos: {dict(c)}")
    print(f"  top desmentidores: {desmiente.most_common(6)}")
    print(f"  origenes: {origen.most_common()}")


if __name__ == "__main__":
    sys.exit(main())
