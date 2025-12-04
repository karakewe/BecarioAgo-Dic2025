## 📌 README.md
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
.
├── main.py
├── extractor.py
├── requirements.txt
├── README.md
├── TESTS.md
│
├── samples/
│   ├── sample_math.pdf
│   ├── sample_programming.pdf
│   └── sample_science.pdf
│
├── raw_outputs/
│   └── debug_raw.json
│
├── cleaned/
│   ├── sample_math.json
│   ├── sample_programming.json
│   └── sample_science.json
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
Abrir en navegador:
➡ http://127.0.0.1:8000/docs

Aquí podrás subir PDFs desde el endpoint:
```
POST /process
```

### 📄 Bloque 2 – Convertir PDFs con Docling
Archivos de ejemplo

Crear documentos dentro del cd:
```
mkdir samples
mkdir raw_outputs
mkdir cleaned
```

Colocar PDFs en:
```
samples/
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
