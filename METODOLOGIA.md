# METODOLOGIA.md — Protocolo de verificación y plantilla del informe

**v0.1 (borrador, pendiente de revisión por Jordi)** · 19-07-2026 · Parte de [LaClave](LaClave.md) · Catálogo de fuentes: [FUENTES.md](FUENTES.md)

## 0. Entrada

El verificador acepta: **enlace**, **texto completo**, **resumen** o **captura de pantalla** de una noticia. Al recibirla, se normaliza: titular, afirmaciones que contiene, fecha, autor y medio de origen (si constan). La ausencia de fecha, autor o fuente no impide verificar, pero se anota como señal de alerta.

## 1. Protocolo paso a paso

**Paso 1 — Triaje y desglose.** Identificar las afirmaciones verificables (hechos comprobables) y separarlas de opinión, predicción o sátira. Si no hay nada verificable, el informe lo dice con claridad (categoría "Opinión" o "No verificable") y termina ahí.

**Paso 2 — Fact-check first.** Buscar cada afirmación en los verificadores profesionales antes de investigar desde cero: Google Fact Check Explorer como buscador general; Maldita, Newtral, EFE Verifica y AFP Factual para España; Factcheck.bg y AFP Proveri para Bulgaria; EUvsDisinfo si suena a narrativa geopolítica. La mayoría de bulos son recurrentes: si ya está dictaminado, se adopta el veredicto profesional, citándolo, y se pasa al informe.

**Paso 3 — Contraste plural** (solo si no está ya dictaminada). Buscar cobertura en agencias y en al menos **3 medios con nota ≥7.5**, de los cuales al menos **1 de línea editorial distinta** al resto (FUENTES.md). Reglas: primar fuentes primarias (boletines oficiales, datos, documentos, declaraciones íntegras) cuando existan; comprobar fechas (¿es una noticia vieja recirculada como nueva?); comprobar que el titular refleja lo que dice el cuerpo.

**Paso 4 — Señales de alerta** (checklist determinista; cada una se anota):

- Sin autor, sin fecha o sin medio identificable
- Lenguaje de urgencia emocional o petición de reenvío ("¡comparte antes de que lo borren!")
- Dominio que imita a un medio real, o web recién creada
- Captura de pantalla sin enlace a la fuente
- Cifras o citas sin fuente localizable
- Petición de dinero, datos personales o descargas

**Paso 5 — Veredicto.** Por afirmación y global, con la escala de la sección 2. Nivel de confianza: **alta / media / baja**, según cobertura disponible y frescura del asunto (noticias de <24-48 h: confianza baja por defecto, con recomendación de re-verificar pasado ese plazo).

**Paso 6 — Origen.** Solo con evidencia citable (un verificador o EUvsDisinfo lo documenta). Sin evidencia: descripción del patrón marcada explícitamente como hipótesis. Nunca atribuir sin fuente.

**Paso 7 — Registro.** Volcar la fila estructurada del caso (sección 4).

## 2. Escala y categorías

Categorías de veredicto: **Verdadero · Mayormente cierto · Mezcla · Engañoso** (hechos ciertos, marco que induce a error) **· Falso · Sin evidencia · No verificable · Opinión · Sátira**.

Correspondencia orientativa con la nota 1-10 (solo categorías factuales):

| Nota | Categoría global |
|---|---|
| 9-10 | Verdadero |
| 7-8.9 | Mayormente cierto |
| 5-6.9 | Mezcla |
| 3-4.9 | Engañoso |
| 1-2.9 | Falso |

Reglas duras:

- **Anti-media-verdad**: si una afirmación central es falsa, la nota global no supera 4 aunque el resto sea cierto (el conjunto engaña).
- "Sin evidencia", "No verificable", "Opinión" y "Sátira" no llevan nota numérica: se explica por qué.
- Toda nota va acompañada de su nivel de confianza; una nota con confianza baja se presenta como provisional.

## 3. Plantilla del informe (salida fija)

```
🔎 LaClave — Informe de verificación

📰 Noticia: [titular o resumen] ([enlace] · [fecha] · [medio de origen, si consta])
⚖️ Veredicto: [categoría] · Nota: X/10 · Confianza: [alta/media/baja]
📌 En una frase: [síntesis de una línea]

Afirmaciones analizadas:
1. "[afirmación]" → [categoría] — [explicación en 1-2 frases, con fuentes]
2. ...

🚩 Señales de alerta: [lista, o "ninguna"]
🧭 Origen: [documentado, con cita | hipótesis marcada | no determinable]
📚 Fuentes consultadas: [enlaces, cada uno con su nota de credibilidad del catálogo]
📝 Notas: [matices, contexto, qué falta por saber, cuándo conviene re-verificar]
```

## 4. Registro estructurado (diseñado para las analíticas por medio)

Cada verificación añade una fila a `registro/registro.csv`:

| Campo | Contenido |
|---|---|
| id, fecha | Identificador y fecha de la verificación |
| tipo_entrada | enlace / texto / resumen / captura |
| ambito, tema | ES, BG, EU o mundo; tema breve |
| afirmacion | Afirmación principal, **anonimizada** (nunca texto bruto de mensajes ni datos de remitentes) |
| veredicto, nota, confianza | Categoría global, nota 1-10 (o —), alta/media/baja |
| medio_origen | Medio o canal donde se originó/detectó (si consta) |
| medios_confirman | Medios que sostienen los hechos (separados por `;`) |
| medios_desmienten | Medios que los desmienten |
| verificador_previo | Verificador profesional que ya lo había dictaminado, si aplica |
| senales | Número de señales de alerta |
| notas | Observaciones libres |

Analíticas derivables por medio (Fase 5): número de veces como **origen** de contenido falso/engañoso; número de veces que **confirma** o **desmiente** correctamente; **evolución de su nota** de fiabilidad. Los cambios de nota se guardan en `registro/notas_historico.csv` (fecha_revision, medio, nota_anterior, nota_nueva, motivo), de modo que cada medio tenga su serie temporal.

## 5. Casos especiales

- **Imágenes y vídeos**: análisis de contexto y coherencia (qué muestra, cuándo, si circuló antes), no análisis forense; se recomienda complementar con Google Lens y el chatbot de Maldita (acepta imágenes/vídeo). El límite se declara en el informe.
- **Última hora (<24-48 h)**: confianza baja por defecto; el informe sugiere re-verificar pasado el plazo.
- **Noticias en búlgaro** (u otros idiomas): se traducen y se aplica el mismo protocolo, citando la fuente original.
- **Cadenas sin fuente**: se verifican las afirmaciones igualmente; las señales de alerta pesan más en la confianza.
- **Privacidad**: si la entrada es un mensaje privado, se eliminan nombres, teléfonos y cualquier dato personal antes de procesar y de registrar.

## 6. Ensayo (pendiente, cierra la Fase 2)

Antes de aprobar la v1.0, ensayaremos el protocolo con 2-3 casos reales (idealmente: un bulo ya desmentido, una noticia verdadera y una media verdad). Jordi puede enviar el primer caso cuando quiera.

## 7. Para revisar por Jordi

- ¿Te encaja la plantilla del informe (formato, emojis, longitud)?
- ¿De acuerdo con la regla anti-media-verdad (afirmación central falsa → nota ≤4)?
- ¿Los campos del registro cubren las analíticas que imaginas (evolución de nota, recuentos por medio y papel)?
- ¿Algún caso especial que eche en falta?
