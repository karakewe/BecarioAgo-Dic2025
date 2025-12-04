import json
from docling.document_converter import DocumentConverter

# Creamos una instancia global del convertidor para reutilizarla
converter = DocumentConverter()


# ------------------------------
# 1. EXTRACCIÓN CRUDA
# ------------------------------

"""def extract_raw(pdf_path: str):
    
    Convierte un PDF usando Docling y devuelve la representación cruda
    en forma de diccionario (JSON-like).
    
    doc = converter.convert(pdf_path)

    # En versiones nuevas de Docling (Pydantic v2)
    if hasattr(doc, "model_dump"):
        return doc.model_dump()

    # En versiones más viejas (Pydantic v1)
    if hasattr(doc, "dict"):
        return doc.dict()

    # Fallback muy defensivo
    return json.loads(json.dumps(doc, default=str))"""

def make_json_serializable(obj):
    if isinstance(obj, dict):
        return {k: make_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_json_serializable(v) for v in obj]
    elif isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    else:
        # Convertimos cualquier objeto raro en string
        return str(obj)
    

def extract_raw(pdf_path: str):
    print("\n========================")
    print("extract_raw() SE EJECUTA")
    print("========================\n")

    try:
        doc = converter.convert(pdf_path)
        print("CONVERT OK")
    except Exception as e:
        print("ERROR EN convert():", e)
        raise e

    # Convertir documento a dict o fallback
    if hasattr(doc, "model_dump"):
        raw = doc.model_dump()
    elif hasattr(doc, "dict"):
        raw = doc.dict()
    else:
        raw = {"error": "no model_dump ni dict"}

    print("RAW KEYS:", list(raw.keys()) if isinstance(raw, dict) else "No dict")

    import os, json

    # Siempre crear la carpeta
    os.makedirs("raw_outputs", exist_ok=True)

    try:
        # 🔥 Serialización a prueba de fallos
        json_string = json.dumps(raw, indent=2, ensure_ascii=False, default=str)

        with open("raw_outputs/debug_raw.json", "w", encoding="utf8") as f:
            f.write(json_string)

        print("🔥 DEBUG RAW GUARDADO EXITOSAMENTE 🔥")
    except Exception as e:
        print("❌ ERROR GUARDANDO debug_raw.json:", e)

    print("\n==== FIN EXTRACT_RAW ====\n")

    # Retornar la versión serializada (ya limpia)
    return json.loads(json_string)


# ------------------------------
# 2. LIMPIEZA Y ESTANDARIZACIÓN
# ------------------------------

def clean_docling(raw: dict) -> dict:
    """
    Convierte la salida cruda de Docling en un JSON limpio:
    - title: string
    - sections: lista de {heading, content}
    """

    clean = {
        "title": None,
        "metadata": raw.get("version", {}),
        "sections": []
    }

    # Extraer página 0 (tu PDF es de 1 página)
    pages = raw.get("pages", [])
    if not pages:
        clean["sections"].append({
            "heading": "Document",
            "content": ""
        })
        clean["title"] = "Untitled Document"
        return clean

    assembled = pages[0].get("assembled", {})
    elements = assembled.get("elements", [])

    last_section = None

    for el in elements:
        label = el.get("label")
        text = el.get("text", "").strip()

        if not text:
            continue

        # Caso: encabezado
        if label == "section_header":
            clean["sections"].append({
                "heading": text,
                "content": ""
            })
            last_section = clean["sections"][-1]

            # Si no hay título, ponerlo
            if clean["title"] is None:
                clean["title"] = text

        # Caso: texto normal
        elif label == "text":
            if last_section is None:
                # Si no ha venido ningún encabezado
                clean["sections"].append({
                    "heading": "Document",
                    "content": ""
                })
                last_section = clean["sections"][-1]

            last_section["content"] += text + "\n"

    # Si nunca encontró título
    if clean["title"] is None:
        clean["title"] = "Untitled Document"

    return clean




# ------------------------------
# 3. CHUNKING
# ------------------------------

def chunk_text(text: str, max_words: int = 250):
    """
    Divide texto en chunks de ~max_words palabras.
    """
    words = text.split()
    for i in range(0, len(words), max_words):
        yield " ".join(words[i:i + max_words])


def add_chunks(clean_json: dict):
    """
    Agrega un arreglo "chunks" al JSON ya limpio.
    Cada chunk tiene:
      - chunk_id
      - source_section
      - text
      - approx_words
    """
    chunks = []
    chunk_id = 0

    for sec in clean_json.get("sections", []):
        section_heading = sec.get("heading", "")
        section_text = sec.get("content", "")

        for chunk in chunk_text(section_text):
            if not chunk.strip():
                continue

            chunks.append({
                "chunk_id": chunk_id,
                "source_section": section_heading,
                "text": chunk,
                "approx_words": len(chunk.split())
            })
            chunk_id += 1

    clean_json["chunks"] = chunks
    return clean_json

def save_clean(clean: dict, name: str):
    import os, json

    print("\n=== save_clean() SE EJECUTA ===")

    os.makedirs("cleaned", exist_ok=True)
    path = f"cleaned/{name}.json"

    try:
        with open(path, "w", encoding="utf8") as f:
            json.dump(clean, f, indent=2, ensure_ascii=False)
        print(f"🔥 Archivo guardado: {path}")
    except Exception as e:
        print(f"❌ ERROR guardando cleaned JSON: {e}")

    return path

