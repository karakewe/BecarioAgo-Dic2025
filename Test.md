🧪 TESTS.md — Validación del Sistema de Extracción de PDFs
# 🧪 TESTS – Checklist de Pruebas del Pipeline PDF

Este documento valida el funcionamiento completo del proyecto en los **5 bloques entregables**, asegurando que el sistema PDF → JSON → Chunks funciona de principio a fin de forma consistente.

---

# ✅ 1. PDFs probados

Se realizaron pruebas con los siguientes archivos de ejemplo ubicados en `/samples`:

| Archivo | Resultado |
|---------|-----------|
| `sample_math.pdf` | ✔ OK |
| `sample_programming.pdf` | ✔ OK |
| `sample_science.pdf` | ✔ OK |

Cada PDF generó:

- Archivos RAW en `/raw_outputs/debug_raw.json`
- JSON limpio en `/cleaned/<archivo>.json`
- Chunks válidos dentro del JSON final

---

# 📄 2. Validación del RAW (Docling)

**Ubicación del archivo generado:**  


raw_outputs/debug_raw.json


### Criterios validados:

- ✔ El archivo se genera en cada carga  
- ✔ Contiene claves:
  - `version`
  - `pages`
  - `assembled`
  - `elements`
  - `document`
- ✔ Incluye metadatos del PDF  
- ✔ Contiene todos los textos detectados  
- ✔ No existen errores de parseo  
- ✔ Bounding boxes presentes  
- ✔ Estructura compatible con Docling v2.64.0

---

# 🧹 3. Validación del JSON limpio

**Ubicación:**  


cleaned/<nombre>.json


### Estructura validada:

```json
{
  "title": "...",
  "metadata": {...},
  "sections": [
    {
      "heading": "...",
      "content": "..."
    }
  ]
}
```
Reglas verificadas:

✔ Un heading por sección (si el PDF tiene encabezado)

✔ Si no hay encabezado → heading = "Document"

✔ El contenido se concatena correctamente

✔ No quedan saltos de línea vacíos innecesarios

✔ El título del PDF se detecta correctamente

# ✂ 4. Validación del chunking
Reglas verificadas:

✔ Chunking basado en cantidad de palabras

✔ Cada chunk contiene:

chunk_id

source_section

text

approx_words

✔ No hay chunks vacíos

✔ Ningún chunk supera el límite definido (~80–120 palabras)

✔ Los chunks son compatibles con LLMs para RAG y embeddings

✔ Se mantiene la coherencia del texto dentro de cada chunk

Ejemplo validado:
{
  "chunk_id": 0,
  "source_section": "Introduction to Python Programming",
  "text": "Python is a high-level programming language widely used in data science...",
  "approx_words": 54
}

# 🌐 5. Validación del servidor FastAPI
Endpoint probado:
POST /process

Criterios validados:

✔ Upload del PDF funcionando

✔ Archivo temporal creado correctamente

✔ Integración con Docling sin fallos

✔ Respuesta JSON inmediata

✔ JSON final incluye:

título

secciones

chunks

metadatos

✔ Tiempo de respuesta adecuado

✔ Swagger UI funcional

✔ Manejo correcto de tipos MIME

# 🔁 6. Pruebas repetitivas

Cada PDF se procesó tres veces.

Resultados:

✔ No se duplican archivos en /cleaned

✔ Cada ejecución sobrescribe correctamente el RAW

✔ No se producen errores de permisos

✔ No aparecen valores None inesperados

✔ No aparecen errores de serialización JSON

✔ Se maneja correctamente PureWindowsPath → JSON

# 🧩 7. Pruebas de casos límite
PDF sin encabezados

✔ Se genera automáticamente una sección llamada "Document"

✔ Functiona el chunking

✔ No se rompe la estructura del JSON

PDF con solo texto

✔ El texto se concatena correctamente en una sola sección

PDF con múltiples bloques de texto

✔ Se mantienen los bloques en el orden correcto

PDFs muy pequeños

✔ Chunk único generado correctamente

# 🎯 8. Resultado final

El sistema completo está probado, validado y estable.
Cumple con los requerimientos funcionales de:

Extracción

Limpieza

Normalización

Chunking

Persistencia

API funcional

Listo para integrarse en pipelines de:

Recuperación aumentada (RAG)

Generación de embeddings (OpenAI / Gemini)

Sistemas de búsqueda semántica

Resumen automático de PDFs

Chatbots con conocimiento basado en documentos

# 📌 Conclusión

Todas las pruebas han sido superadas con éxito.
El sistema cumple completamente con los 5 bloques del proyecto.
