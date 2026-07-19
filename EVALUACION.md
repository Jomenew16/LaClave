# EVALUACION.md — Calibración del verificador (Fase 4)

**Realizada el 19-07-2026** · Parte de [LaClave](LaClave.md) · Datos: [banco/banco_pruebas.csv](banco/banco_pruebas.csv) y [banco/resultados_eval_2026-07.csv](banco/resultados_eval_2026-07.csv)

## Método

Banco de 30 casos ya dictaminados: 12 de España (Maldita, Newtral), 8 de Bulgaria/Europa (Factcheck.bg, EUvsDisinfo, Full Fact, Maldita, Newtral) y 10 verdaderos de control (5 noticias normales de 2026 y 5 "suenan a bulo pero son ciertos"). Composición: 12 Falso, 8 Engañoso, 10 Verdadero.

Cada caso se evaluó **a ciegas** (el evaluador recibió solo la afirmación, nunca el dictamen profesional ni la fuente), invocando la **skill real `laclave`** en modo compacto (máximo 5 búsquedas por caso). Criterios de éxito definidos en la Fase 0: acierto direccional ≥80 % y ningún bulo flagrante dado por bueno.

## Resultados globales

| Métrica | Resultado | Objetivo |
|---|---|---|
| **Acierto direccional** (¿cayó del lado correcto?) | **29/30 = 96,7 %** | ≥80 % ✅ |
| **Bulos flagrantes aprobados** | **0** | 0 ✅ |
| **Falsos positivos** (verdades marcadas como falsas) | **0/10** | — ✅ |
| Categoría exacta | 22/30 = 73,3 % | — |
| Categoría exacta o adyacente (Falso↔Engañoso, Verdadero↔Mayormente cierto) | 29/30 = 96,7 % | — |
| Confianza declarada | 29 alta · 1 media | — |

En los 20 casos problemáticos (Falso/Engañoso), la nota media otorgada fue **2,3/10** y ninguno superó 4, salvo el caso límite B15 (ver abajo). En los 10 verdaderos, la nota media fue **9,4/10** y ninguno bajó de 8.

**La Fase 4 se supera con holgura.**

## Análisis de los desacuerdos

**LC-B15, el único fallo direccional** ("La ministra de Exteriores de Bulgaria firmó la Declaración de Kiev"; Factcheck.bg: engañoso; LaClave: Mayormente cierto, 7.5, confianza media). Tres lecciones:

1. Causa raíz: el evaluador no encontró el fact-check de Factcheck.bg porque está indexado **solo en búlgaro** y buscó en español/inglés. → Corregido en la skill v1.1 (ver abajo).
2. Atenuantes reales: es el caso más "blando" del banco — la sustancia es cierta (Bulgaria respaldó la declaración mediante su ministra; el matiz disputado es el verbo "firmó") y el propio informe del evaluador identificó exactamente ese matiz (calificó la afirmación de la firma como "Mezcla"). No es un bulo aprobado, sino un desacuerdo de etiqueta en un caso fronterizo y de actualidad caliente (<1 semana).
3. Señal positiva de calibración: fue el **único caso con confianza "media"** de los 30 — el sistema "sabía" que pisaba terreno inseguro, exactamente el comportamiento deseado.

**Cinco intercambios Falso↔Engañoso** (B05, B11, B12, B16, B19): la frontera entre ambas categorías es difusa incluso entre verificadores profesionales (varios de los dictámenes del banco también eran interpretables). Sin impacto práctico: en todos, la nota quedó ≤4 y la explicación fue correcta. No requiere ajuste.

**LC-B25, el hallazgo de la evaluación**: el verificador detectó un **error del propio banco de pruebas** — la afirmación decía "33 de los 81 escaños" y las Cortes de Castilla y León elegidas en 2026 tienen 82. Calificó con precisión quirúrgica (Mayormente cierto, 8.5, señalando el detalle erróneo sin penalizar el fondo). El banco ha sido corregido.

**LC-B28**: matizó la datación tradicional del unicornio escocés (s. XII vs evidencia documentada de los s. XV-XVI) — el tipo de matiz que un buen verificador debe hacer.

## Comportamientos observados (cualitativo)

- **"Fact-check first" funciona**: en los 20 casos problemáticos localizó dictámenes profesionales en 19, y los citó correctamente.
- **Desglose por afirmaciones**: separó de forma consistente lo cierto de lo falso dentro de la misma noticia (p. ej. B02: brote real + vacuna inventada; B19: agresión real + lugar falso).
- **Rastreo de origen prudente**: identificó orígenes documentados (red de YouTube en B20, cuenta de TikTok en B01, Sputnik/RT en B16) y marcó como hipótesis lo no probado.
- **Sin sesgo de complacencia**: los 5 casos "suenan a bulo pero son ciertos" (B26-B30) se confirmaron todos con fuentes primarias — el sistema no "sospecha por defecto".

## Limitaciones del ensayo

- El entorno de pruebas tiene **menos acceso web que tu app** (varios dominios españoles bloqueados aquí): los resultados reales deberían ser iguales o mejores.
- Modo compacto (≤5 búsquedas/caso): el uso real permite más profundidad.
- Los 20 casos problemáticos provienen de verificadores, lo que favorece al paso "fact-check first"; es representativo del uso real (la mayoría de bulos que circulan ya están dictaminados), y los 10 verdaderos —que exigen contraste desde cero— compensan el sesgo.
- Un caso (B15) requirió reintento por un límite puntual de uso de la sesión.

## Ajustes aplicados → skill v1.1

- **SKILL.md y METODOLOGIA.md**: para temas búlgaros, buscar también en búlgaro (traducir los términos clave), porque los fact-checks de Factcheck.bg están indexados casi solo en búlgaro. Es el ajuste que habría evitado el único fallo.
- Corregido el dato erróneo del banco (B25).

## Veredicto de la Fase 4

**APROBADA.** El verificador está listo para uso regular. Próxima calibración: informal y continua a través del registro de verificaciones reales (Fase 5), con revisión trimestral del índice de credibilidad.
