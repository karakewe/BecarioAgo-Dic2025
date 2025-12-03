📌 README.md
PDF Processing API (FastAPI + Docling)

1. Este proyecto implementa una API capaz de:

2. Recibir archivos PDF

3. Convertirlos a JSON usando Docling

4. Limpiar y estandarizar la estructura del JSON

5. Tokenizar/dividir el contenido en chunks

Devolver un JSON final listo para usar en modelos como Gemini

## 🚀 Instalación
1. Clonar repositorio
```
git clone <URL_DEL_REPO>
cd pdf-api
```

3. Crear entorno e instalar dependencias
```
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

## 🧩 Estructura del proyecto
```
pdf-api/
│
├── main.py
├── extractor.py
├── requirements.txt
├── README.md
│
├── samples/                   # PDFs de prueba
│
├── raw_outputs/               # JSON crudos (Docling)
│
└── cleaned/                   # JSON limpios + con chunks
```
### 🧪 Bloque 1 – Servidor corriendo

Para ejecutar FastAPI:
```
uvicorn main:app --reload
```

Abrir en navegador:
➡ http://127.0.0.1:8000/

Debe mostrarse:
```
{"status": "ok"}
```
### 📄 Bloque 2 – Convertir PDFs con Docling
Archivos de ejemplo

Colocar PDFs en:
```
samples/
```
Conversión cruda

Para convertir un PDF y guardar su salida cruda:
```
import json
from extractor import extract_raw

raw = extract_raw("samples/calculo_integral.pdf")

with open("raw_outputs/calculo_integral_raw.json", "w", encoding="utf8") as f:
    json.dump(raw, f, indent=2, ensure_ascii=False)
```
### 🧼 Bloque 3 – Limpieza y estandarización

Esquema estándar del JSON final
```
{
  "title": "Título del documento",
  "metadata": {...},
  "sections": [
    {
      "heading": "Encabezado detectado",
      "content": "Contenido limpio asociado a ese encabezado"
    }
  ]
}
```

La lógica está en extractor.py → clean_docling().

### ✂️ Bloque 4 – Chunking

Se aplica una división aproximada de 250 palabras por chunk.

Cada chunk contiene:
```
{
  "chunk_id": 0,
  "source_section": "Introducción",
  "text": "texto del chunk...",
  "approx_words": 247
}
```

chunks → se agregan al JSON final bajo:
```
"chunks": []
```
### 🧰 Bloque 5 – API Final

El endpoint principal es:
```
POST /process
```

Acepta:
```
archivo PDF (multipart/form-data)
```
Devuelve:
```
JSON completo: title, sections, chunks
```
Ejemplo con curl:
```
curl -X POST -F "file=@samples/calculo_integral.pdf" http://127.0.0.1:8000/process
```
## 📌 Checklist de pruebas realizadas

 - PDF con encabezados

 - PDF con listas

 - PDF con imágenes

 - PDF con tablas simples

 - PDFs largos

 - PDFs cortos

 - Verificación de que los chunks no superen 250 palabras
