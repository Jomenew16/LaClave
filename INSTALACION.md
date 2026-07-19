# INSTALACION.md — Poner LaClave en tu app de Claude

Vas a instalar dos cosas complementarias: la **skill "laclave"** (el verificador completo, que puede activarse en cualquier chat) y el **Proyecto "LaClave 🔎"** (un espacio dedicado que funciona siempre, incluso si la skill no se activa).

## Paso 1 — Subir la skill (5 min, desde el ordenador)

1. Localiza `laclave.zip` en tu carpeta `ClaudeLaClave`.
2. Abre https://claude.ai en el navegador e inicia sesión.
3. Ve a **Settings (⚙️) → Capabilities** y comprueba que **Code execution / Skills** está activado.
4. En la sección **Skills**, pulsa **Upload skill** y selecciona `laclave.zip`.
5. Verás "laclave" en tu lista de skills. Déjala activada.

Los nombres de menú pueden variar ligeramente con las actualizaciones; si algo no coincide, busca "skills" dentro de Settings.

## Paso 2 — Crear el Proyecto (5 min)

1. En claude.ai, menú lateral → **Projects → New project**. Nombre: `LaClave 🔎`.
2. Dentro del proyecto, abre **Instructions** (instrucciones personalizadas) y pega todo el bloque indicado de `app/instrucciones_proyecto.md` (está en tu carpeta).
3. En el conocimiento del proyecto (**Project knowledge**), sube el archivo `skill/laclave/fuentes.md` (el catálogo).

## Paso 3 — Probar en el ordenador

Abre el proyecto y pega un titular, enlace o texto sospechoso. Debe responder con el informe LaClave (veredicto, nota, desglose por afirmaciones, fuentes). Prueba también en un chat normal (fuera del proyecto) escribiendo "verifica esta noticia: …" para comprobar que la skill se activa sola.

## Paso 4 — Probar en el móvil

- **Ruta rápida**: en WhatsApp, mantén pulsado el mensaje → Compartir → **Claude** → escribe "verifica".
- **Ruta proyecto**: abre la app de Claude → Projects → `LaClave 🔎` → pega la noticia.

Cuéntale a Claude en la sesión de Cowork qué tal ha ido cada ruta (especialmente si la skill saltó sola): con eso se cierra la Fase 3.

## Problemas típicos

- **No aparece "Skills" en Settings**: hazlo desde la web claude.ai (no desde la app móvil) y revisa que Code execution esté activado.
- **La skill no se activa en un chat**: pídelo explícitamente ("usa la skill laclave") o usa el Proyecto.
- **Se acaba el límite de uso**: cada informe consume varias búsquedas; espera al siguiente ciclo del plan.

## Compartir con familia y amigos (más adelante, Fase 6c)

Cualquier persona con cuenta de Claude (incluso gratuita) puede subir este mismo `laclave.zip` a su cuenta siguiendo el Paso 1, y crear su propio proyecto con el Paso 2.
