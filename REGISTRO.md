# REGISTRO.md — Registro de verificaciones, índice dinámico y analíticas

**v1.0 · 19-07-2026** · Parte de [LaClave](LaClave.md) · Datos: [`registro/registro.csv`](registro/registro.csv) · Histórico de notas: [`registro/notas_historico.csv`](registro/notas_historico.csv) · Salida: [`ANALITICAS.md`](ANALITICAS.md) y panel visual

## Qué se registra (y qué no)

Cada verificación deja una fila estructurada. **Nunca se registran** mensajes brutos, nombres, teléfonos ni ningún dato personal de remitentes: solo la afirmación (anonimizada), el veredicto y los metadatos. El repositorio es público; esta regla es innegociable.

## Columnas de `registro/registro.csv` (separador `;`)

| Columna | Contenido |
|---|---|
| id | `LC-AAAA-NNN` (uso real) o `LC-BNN` (calibración) |
| fecha | Fecha de la verificación |
| tipo_entrada | enlace / texto / resumen / captura |
| ambito | ES / BG / EU / mundo |
| tema | Etiqueta corta |
| afirmacion | Afirmación principal, breve y anonimizada |
| veredicto · nota · confianza | Según la escala de METODOLOGIA.md |
| medio_origen | Dónde se originó o publicó (o "sin medio") |
| medios_confirman | Fuentes que sostienen los hechos (`;` interno → separadas por `,`) |
| medios_desmienten | Fuentes que los desmienten |
| verificador_previo | Verificador profesional que ya lo había dictaminado |
| senales | Nº de señales de alerta |
| lote | `real` (uso de Jordi) / `calibracion` (Fase 4) |
| notas | Observaciones |

## Cómo se archiva una verificación

**Hecha en la app de Claude (skill o Proyecto):** cada informe termina con la línea `📋 Registro: …`. Copia esa línea — o el informe entero, que es aún mejor — y, cuando quieras (no hace falta que sea al momento), pégala en una sesión de Cowork con un simple «archiva esto». Claude añadirá la fila, regenerará las analíticas y el panel, hará commit + push y sincronizará tu carpeta. Se pueden archivar varias de golpe.

**Hecha en una sesión de Cowork:** se archiva automáticamente en la misma sesión.

## Revisión del índice de credibilidad (trimestral)

1. Claude ejecuta `scripts/analiticas.py` y presenta las analíticas del periodo.
2. Con esa evidencia, Claude **propone** ajustes de nota razonados (p. ej. «medio X: 3 casos como origen de contenido engañoso este trimestre → propuesta 6 → 5.5»), siempre con los casos citables.
3. **Jordi aprueba, modifica o rechaza** cada propuesta. Nada cambia sin su visto bueno (evita que el sistema se retroalimente en sus propios sesgos).
4. Los cambios aprobados se aplican a `FUENTES.md` (nueva versión) y se anotan en `registro/notas_historico.csv` (fecha, medio, nota anterior, nota nueva, motivo) — esa serie temporal alimenta la analítica de **evolución por medio**.

Reglas prudenciales: un solo caso nunca mueve una nota; los movimientos son graduales (±0.5 por revisión, salvo evidencia extraordinaria); subir es tan posible como bajar; los medios "fuera de catálogo" que aparezcan ≥3 veces se proponen para incorporación.

**Primera revisión programada: octubre de 2026.** El histórico arranca hoy con la semilla completa del catálogo v1.1 (57 medios), de modo que cada medio tiene su punto de partida trazado.

## Analíticas disponibles

`scripts/analiticas.py` genera `ANALITICAS.md` con: distribución de veredictos, notas medias, desglose por ámbito y confianza, y **por medio**: veces como origen de contenido falso/engañoso, veces como desmentidor acertado, veces como confirmador, y evolución de nota (a partir de la segunda revisión). El panel visual (artefacto "Panel LaClave") muestra lo esencial de un vistazo y se actualiza en cada archivo de verificaciones.
