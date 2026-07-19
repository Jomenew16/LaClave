# LaClave — Verificador personal de noticias

Documento de seguimiento del proyecto · Creado: 18-07-2026 · Repositorio público: https://github.com/Jomenew16/LaClave

## Visión

LaClave es un verificador personal de noticias, sin ánimo comercial. Cuando llega una noticia dudosa (WhatsApp, redes u otra vía), se le pasa como enlace, texto completo o resumen, y devuelve un informe con una valoración de veracidad en escala 1-10, el detalle de qué afirmaciones son ciertas, falsas o interpretables, enlaces y referencias de contraste y, cuando sea determinable con evidencia, el origen probable del bulo. La verificación combina dos vías: reutilizar el ecosistema profesional de fact-checking (Maldita, Newtral, EFE Verifica, Factcheck.bg, EUvsDisinfo, Google Fact Check Tools…) y contrastar con medios de prestigio de distintas tendencias, ponderados por un índice de credibilidad propio que se corrige con la evidencia acumulada. Cobertura por prioridad: España > Bulgaria (EN/ES) > Europa > mundo.

Extras previstos: curador de contenidos, buffer periódico de noticias de Bulgaria en español, y posibilidad de compartir la herramienta con familia y amigos. Debe funcionar en ordenador y móvil, con coste recurrente cero.

## Decisiones acordadas (18-07-2026)

- Plataforma: dentro de la app Claude (Proyecto + Skill). Posible evolución futura a bot de Telegram (v2) si la fricción o el compartir lo piden; nada de lo construido se pierde en esa migración.
- Coste: 0 € adicionales sobre la suscripción de Claude; solo servicios con nivel gratuito.
- Volumen previsto: ocasional (1-5 verificaciones/semana).
- Reparto de trabajo: Claude asume la parte técnica con guía paso a paso; Jordi decide, revisa y aprueba (metodología, ponderaciones del índice).
- Repositorio GitHub privado como fuente de verdad; copia espejo de los documentos en `C:\Users\jorme\ClaudeLaClave`.
- Integración directa con WhatsApp: descartada (la API oficial exige identidad de empresa y número dedicado; las alternativas no oficiales arriesgan el baneo del número).

## Decisiones acordadas (19-07-2026)

- El repositorio pasa a ser **público**, a iniciativa de Jordi: el proyecto es de interés general y no maneja información sensible. Salvaguardas asociadas:
  - Nunca datos personales: ni nombres, ni teléfonos, ni mensajes brutos de WhatsApp. El registro de verificaciones guardará solo la afirmación (anonimizada), el veredicto y las fuentes.
  - Nunca claves ni tokens en el repo (el `.gitignore` de Python ayuda; revisión antes de cada push).
  - Las notas de credibilidad de medios se justifican siempre con criterios explícitos y señalamientos citables de terceros; no se mantiene una "lista negra" propia.
  - La autoría de los commits usa el email «noreply» de GitHub (`20563551+Jomenew16@users.noreply.github.com`), nunca el correo personal. Recomendado además activar en GitHub: Settings → Emails → "Keep my email addresses private".
  - Pendiente: elegir licencia (propuesta: MIT para el código y CC BY 4.0 para la documentación).
- El repo se creó con `.gitignore` de Python (adecuado: los futuros scripts auxiliares serán Python) y rama por defecto `master`.
- Push mediante **token de acceso limitado** (fine-grained: solo repo LaClave, permiso de contenidos) creado por Jordi; se guarda en `.laclave_pat.txt` local, ignorado por git, revocable en cualquier momento.
- A propuesta de Jordi: el registro capturará **datos estructurados por medio** para generar analíticas — evolución de la nota de fiabilidad, recuento de noticias falsas/engañosas/sesgadas por medio y su papel (origen, amplificador, desmentidor). Se incorpora a la Fase 5 y condiciona el diseño del registro desde la Fase 2.

## Supuestos pendientes de confirmar

- Los informes se emiten siempre en español, aunque la noticia original esté en inglés o búlgaro.
- El buffer de Bulgaria será semanal (se decidirá en la Fase 6a).

## Metodología — principios

1. **Fact-check first**: comprobar primero si la noticia ya está desmentida o verificada por fact-checkers profesionales; la mayoría de bulos son recurrentes.
2. **Desglose por afirmaciones**: el veredicto combina nota 1-10 + categoría (Verdadero / Mayormente cierto / Mezcla / Engañoso / Falso / Sin evidencia / No verificable / Opinión / Sátira) + nivel de confianza + tabla afirmación por afirmación.
3. **Contraste plural**: mínimo 3 medios de alta credibilidad y al menos 1 de línea editorial distinta.
4. **Índice de credibilidad por medio** (no por categorías), sembrado con criterios explícitos (EFCSN/IFCN, confianza por marca del Digital News Report, MBFC, pluralismo); los ajustes posteriores se basan en el registro de verificaciones y requieren aprobación de Jordi.
5. **Origen del bulo solo con evidencia citable**; en su defecto, descripción del patrón marcada como hipótesis. Nunca atribuir sin fuente.
6. **Señales de alerta deterministas**: sin autor ni fecha, urgencia emocional, "reenvía esto", dominios que imitan a medios reales, capturas sin enlace.
7. **Privacidad**: se verifican textos, no personas; anonimizar remitentes de mensajes privados.

## Límites asumidos

- Noticias de menos de 24-48 h: poco contraste publicado; el informe lo indicará y rebajará la confianza.
- Contenido audiovisual: análisis de contexto, no forense; complemento manual con Google Lens y el chatbot de Maldita.
- Paywalls duros (FT, NYT): se cubren vía titulares y cobertura equivalente de agencias y medios en abierto.
- El veredicto es probabilístico: es un primer filtro sistemático, no una sentencia.

## Plan por fases

- [x] **Fase 0 — Marco del proyecto** (1-2 sesiones). LaClave.md, repositorio GitHub (público) y commit inicial. _Completada el 19-07-2026 (push operativo mediante token de acceso limitado creado por Jordi)._
- [x] **Fase 1 — Catálogo de fuentes e índice de credibilidad v1** (1-2 sesiones). `FUENTES.md` con ~50-70 medios y ~15 verificadores (ES/BG/EU/mundo): idioma, RSS, paywall, propiedad, línea editorial y credibilidad inicial 1-10 con criterios explícitos. Claude verifica técnicamente los feeds; Jordi revisa y ajusta las ponderaciones. Entregable: catálogo aprobado. _Completada el 19-07-2026: FUENTES.md v1.0 aprobado por Jordi._
- [x] **Fase 2 — Metodología y plantilla del informe** (1 sesión). Protocolo paso a paso y plantilla fija del informe; ensayo con 2-3 casos reales. Entregable: `METODOLOGIA.md`. _Completada el 19-07-2026: v1.0 aprobada por Jordi tras el ensayo con los informes #001 y #002._
- [x] **Fase 3 — Skill y Proyecto "LaClave"** (1 sesión). Empaquetar metodología + catálogo como skill, instalación guiada en la cuenta de Jordi, creación del Proyecto, pruebas del flujo completo en PC y móvil. Entregable: verificador operativo. _Completada el 19-07-2026: skill y Proyecto instalados por Jordi y probados en ordenador y móvil con funcionamiento correcto._
- [x] **Fase 4 — Calibración con banco de pruebas** (1-2 sesiones). 25-30 noticias ya dictaminadas por fact-checkers (falsas, engañosas y ciertas; ES/BG/EU). Criterio de éxito: ≥80 % de acierto direccional y ningún bulo flagrante dado por bueno. Entregable: informe de evaluación y ajustes. _Completada el 19-07-2026: 30 casos a ciegas → **96,7 % de acierto direccional, 0 bulos aprobados, 0 falsos positivos**. Ver `EVALUACION.md`. Skill ajustada a v1.1 (búsqueda en búlgaro)._
- [x] **Fase 5 — Registro, índice dinámico y analíticas por medio** (1-2 sesiones). Registro estructurado por verificación (`registro.csv` además del texto) y revisión trimestral del índice (Claude propone ajustes con el histórico; Jordi aprueba). Analíticas por medio: evolución temporal de la nota de fiabilidad, número de noticias falsas/engañosas/sesgadas en las que aparece cada medio y en qué papel (origen, amplificador o desmentidor), aciertos como fuente de contraste. Entregable: `REGISTRO.md` + `registro.csv` + informe o panel de analíticas. _Completada el 19-07-2026: REGISTRO.md (flujo de archivo + revisión trimestral), registro consolidado con 32 verificaciones, histórico sembrado con los 57 medios del catálogo, `scripts/analiticas.py` + ANALITICAS.md, y panel visual persistente ("Panel LaClave"). Primera revisión del índice: octubre de 2026._
- [x] **Fase 6a — Buffer de Bulgaria** (1 sesión). Tarea programada (semanal por defecto) que resume y evalúa en español las noticias más relevantes del país. _Completada el 19-07-2026: tarea programada "LaClave — Boletín semanal de Bulgaria" creada (lunes ~08:00 hora de Sofía, con aviso push; fuentes ponderadas + alerta de desinformación) y ejecución de prueba lanzada._
- [x] **Fase 6b — Curador de contenidos** (1 sesión). Dado un tema o una noticia, recopilar cobertura, ordenarla por credibilidad y sintetizar lo común entre fuentes fiables. _Completada el 19-07-2026: "modo curador" añadido a la skill (v1.2), a METODOLOGIA.md (§7) y a las instrucciones del Proyecto; panorama de prueba en `panoramas/2026-07-19_pde_bulgaria.md`._
- [ ] **Fase 6c — Compartir** (1 sesión). ZIP de la skill + guía de instalación publicados en el repo (ya público).

Estimación total: 6-9 sesiones. Cada fase termina con commit, push y actualización de este documento.

## Próximos pasos

1. **Jordi: resubir `laclave.zip` (ahora v1.2)** en claude.ai → Settings → Capabilities → Skills — imprescindible para usar el modo curador desde la app (incluye también la mejora búlgara de v1.1).
2. **Revisar los dos estrenos**: el boletín de prueba de Bulgaria (llega como tarea aparte con aviso) y el panorama del PDE; el primer boletín regular llega el lunes ~08:00. Ajustes del boletín: se cambian con un mensaje en cualquier sesión.
3. **Uso cotidiano**: verificar o pedir panoramas desde la app; de vez en cuando, pegar informes o líneas `📋 Registro` en Cowork con «archiva esto» (ver REGISTRO.md).
4. Queda una única fase: **6c (paquete para compartir)** + pendientes menores: licencia (propuesta MIT + CC BY 4.0), "Keep my email addresses private" en GitHub. Primera revisión del índice: octubre de 2026.

## Registro de avances

| Fecha | Hecho |
|---|---|
| 18-07-2026 | Estudio de viabilidad completo (fact-checkers ES/BG/EU, medios y RSS, ratings de credibilidad, plataformas y costes). Decisiones: app Claude, 0 € adicionales, uso ocasional. Fase 0: LaClave.md redactado, copiado a la carpeta local y con commit local; el repo de GitHub y el push quedan para la sesión 2 (el acceso por sesión no pudo ampliarse en caliente). |
| 19-07-2026 | Repo **público** creado por Jordi (descripción propia, `.gitignore` Python, rama `master`); verificado desde fuera: correcto. Decisión de visibilidad y salvaguardas de privacidad registradas. Fase 0 completada (push pendiente de autorizar la app). Fase 1 arrancada: FUENTES.md v0.1 (catálogo de ~60 fuentes e índice inicial) entregado para revisión. |
| 19-07-2026 | Token de acceso limitado creado por Jordi (guardado en local, ignorado por git). Historial reescrito para eliminar el email personal (incluido el commit inicial) y **push completo a `master`**: repo en línea al día. **FUENTES.md v1.0 aprobado → Fase 1 completada.** Decisión: analíticas por medio (→ Fase 5). Fase 2 arrancada: METODOLOGIA.md v0.1 entregado para revisión. |
| 19-07-2026 | **Ensayo del protocolo con dos casos reales**: #001 The Objective / diversidad en el cine (Engañoso, 4/10, confianza media) y #002 Vozpópuli / "432 %" de recaudación (Engañoso, 3/10, confianza alta). Estrenados `informes/` y `registro/registro.csv`. |
| 19-07-2026 | Formato de informe validado por Jordi → **METODOLOGIA v1.0, Fase 2 completada**. Aprobada la incorporación de The Objective (6) y Vozpópuli (6) → **FUENTES v1.1**. **Fase 3 en marcha**: skill `laclave` (SKILL.md + fuentes.md compacto), instrucciones del Proyecto, guía INSTALACION.md y paquete laclave.zip entregados; pendiente instalación y pruebas de Jordi en PC y móvil. |
| 19-07-2026 | Jordi instala la skill y el Proyecto y confirma funcionamiento en PC y móvil → **Fase 3 completada**. |
| 19-07-2026 | **Fase 4 completada**: banco de 30 casos dictaminados (12 ES, 8 BG/EU, 10 verdaderos de control) y evaluación a ciegas con la skill real. Resultado: **acierto direccional 96,7 % (29/30), 0 bulos aprobados, 0 falsos positivos**; único fallo en un caso búlgaro fronterizo de <1 semana (B15), corregido con la skill v1.1 (búsqueda en búlgaro). Bonus: el verificador detectó un error del propio banco (B25, 82 escaños). Ver EVALUACION.md. |
| 19-07-2026 | **Fase 5 completada**: REGISTRO.md con el flujo de archivo (app → «archiva esto» → Cowork) y la revisión trimestral con aprobación de Jordi; `registro.csv` consolidado (32 verificaciones con columna de lote); `notas_historico.csv` sembrado con los 57 medios; `scripts/analiticas.py` y primera ANALITICAS.md; **Panel LaClave** persistido como artefacto (paleta validada en claro y oscuro). |
| 19-07-2026 | **Fase 6a completada**: tarea programada "LaClave — Boletín semanal de Bulgaria" (lunes ~08:00 hora de Sofía, aviso push), con prompt autónomo: fuentes búlgaras ponderadas del catálogo, contraste, confianza por pieza y sección de alerta de desinformación. Ejecución de prueba lanzada. **Fase 6b completada**: modo curador en la skill v1.2, METODOLOGIA §7 e instrucciones del Proyecto; panorama de prueba sobre el PDE a Bulgaria generado y archivado. |

## Recursos clave

- Fact-checkers España: [Maldita.es](https://maldita.es) (chatbot WhatsApp +34 644 229 319), [Newtral](https://www.newtral.es), [EFE Verifica](https://verifica.efe.com), [Verificat](https://www.verificat.cat), [AFP Factual](https://factual.afp.com).
- Fact-checkers Bulgaria: [Factcheck.bg](https://factcheck.bg/en/), AFP Proveri, [BROD](https://brodhub.eu/en/) (hub EDMO Bulgaria-Rumanía).
- Bases europeas/globales: [EUvsDisinfo](https://euvsdisinfo.eu/disinformation-cases/), [EDMO](https://edmo.eu)/[Iberifier](https://iberifier.eu), [Google Fact Check Explorer](https://toolbox.google.com/factcheck/explorer) y su [API gratuita](https://developers.google.com/fact-check/tools/api), [miembros EFCSN](https://members.efcsn.com/signatories).
- Semillas del índice de credibilidad: [Digital News Report 2026](https://reutersinstitute.politics.ox.ac.uk/digital-news-report/2026) (confianza por marca, España y Bulgaria), [Media Bias/Fact Check](https://mediabiasfactcheck.com), [fuentes perennes de Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Reliable_sources/Perennial_sources), [dataset Lin et al.](https://github.com/hauselin/domain-quality-ratings).
- Bulgaria en español/inglés: [Radio Bulgaria en español](https://bnrnews.bg/es), [BTA en inglés](https://www.bta.bg/en), [Novinite](https://www.novinite.com), [The Sofia Globe](https://sofiaglobe.com). Contexto: [RSF Bulgaria](https://rsf.org/en/country/bulgaria) (71/180 en 2026).

## Flujo de trabajo

- Fuente de verdad: este repositorio (GitHub, privado). Copia espejo de los documentos en la carpeta local `C:\Users\jorme\ClaudeLaClave`.
- Cada sesión de trabajo termina con commit + push y actualización de LaClave.md (plan y registro de avances).
- El entorno de trabajo en la nube es efímero: al empezar una sesión nueva se clona/actualiza el repositorio antes de continuar.
