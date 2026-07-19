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
  - Pendiente: elegir licencia (propuesta: MIT para el código y CC BY 4.0 para la documentación).
- El repo se creó con `.gitignore` de Python (adecuado: los futuros scripts auxiliares serán Python) y rama por defecto `master`.

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

- [x] **Fase 0 — Marco del proyecto** (1-2 sesiones). LaClave.md, repositorio GitHub (público) y commit inicial. _Completada el 19-07-2026, con un fleco: el push desde Claude quedará operativo al autorizar la app de Claude en el repo (ver "Próximos pasos"); mientras tanto, los archivos pueden subirse por la web._
- [ ] **Fase 1 — Catálogo de fuentes e índice de credibilidad v1** (1-2 sesiones). `FUENTES.md` con ~50-70 medios y ~15 verificadores (ES/BG/EU/mundo): idioma, RSS, paywall, propiedad, línea editorial y credibilidad inicial 1-10 con criterios explícitos. Claude verifica técnicamente los feeds; Jordi revisa y ajusta las ponderaciones. Entregable: catálogo aprobado. _En curso (19-07-2026): FUENTES.md v0.1 redactado y entregado; pendiente de la revisión de Jordi._
- [ ] **Fase 2 — Metodología y plantilla del informe** (1 sesión). Protocolo paso a paso y plantilla fija del informe; ensayo con 2-3 casos reales. Entregable: `METODOLOGIA.md`.
- [ ] **Fase 3 — Skill y Proyecto "LaClave"** (1 sesión). Empaquetar metodología + catálogo como skill, instalación guiada en la cuenta de Jordi, creación del Proyecto, pruebas del flujo completo en PC y móvil. Entregable: verificador operativo.
- [ ] **Fase 4 — Calibración con banco de pruebas** (1-2 sesiones). 25-30 noticias ya dictaminadas por fact-checkers (falsas, engañosas y ciertas; ES/BG/EU). Criterio de éxito: ≥80 % de acierto direccional y ningún bulo flagrante dado por bueno. Entregable: informe de evaluación y ajustes.
- [ ] **Fase 5 — Registro e índice dinámico** (1 sesión). Plantilla de registro por verificación y procedimiento de revisión trimestral del índice (Claude propone ajustes con el histórico; Jordi aprueba). Entregable: `REGISTRO.md` + procedimiento.
- [ ] **Fase 6a — Buffer de Bulgaria** (1 sesión). Tarea programada (semanal por defecto) que resume y evalúa en español las noticias más relevantes del país.
- [ ] **Fase 6b — Curador de contenidos** (1 sesión). Dado un tema o una noticia, recopilar cobertura, ordenarla por credibilidad y sintetizar lo común entre fuentes fiables.
- [ ] **Fase 6c — Compartir** (1 sesión). ZIP de la skill + guía de instalación; decidir si el repositorio pasa a público.

Estimación total: 6-9 sesiones. Cada fase termina con commit, push y actualización de este documento.

## Próximos pasos (arranque de la siguiente sesión)

1. **Jordi** (1 minuto; desbloquea el push de Claude): en https://github.com/settings/installations → app **Claude** → Configure → "Repository access" → añadir `LaClave` → Save. Si al iniciar una tarea de Cowork la app ofrece añadir un repositorio de GitHub como contexto, añadir también `LaClave`.
2. **Jordi** (opcional, para ver el plan en GitHub hoy mismo): en https://github.com/Jomenew16/LaClave → "Add file" → "Upload files" → arrastrar `LaClave.md`, `README.md` y `FUENTES.md` desde `C:\Users\jorme\ClaudeLaClave` → "Commit changes".
3. **Claude** (en cuanto haya acceso): reconciliar historiales (la rama remota es `master`; la local, `main`) y hacer push; desde ahí, push directo al final de cada sesión.
4. **Fase 1 en curso**: Jordi revisa `FUENTES.md` (notas, inclusiones/exclusiones, regla de "sin lista negra propia"); con sus ajustes se cierra el catálogo v1 y pasamos a la Fase 2 (metodología y plantilla del informe).

## Registro de avances

| Fecha | Hecho |
|---|---|
| 18-07-2026 | Estudio de viabilidad completo (fact-checkers ES/BG/EU, medios y RSS, ratings de credibilidad, plataformas y costes). Decisiones: app Claude, 0 € adicionales, uso ocasional. Fase 0: LaClave.md redactado, copiado a la carpeta local y con commit local; el repo de GitHub y el push quedan para la sesión 2 (el acceso por sesión no pudo ampliarse en caliente). |
| 19-07-2026 | Repo **público** creado por Jordi (descripción propia, `.gitignore` Python, rama `master`); verificado desde fuera: correcto. Decisión de visibilidad y salvaguardas de privacidad registradas. Fase 0 completada (push pendiente de autorizar la app). Fase 1 arrancada: FUENTES.md v0.1 (catálogo de ~60 fuentes e índice inicial) entregado para revisión. |

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
