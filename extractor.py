import json
from docling.document import Document
from docling.document_converter import DocumentConverter


# ------------------------------
# 1. EXTRACCIÓN CRUDA
# ------------------------------

def extract_raw(pdf_path: str):
    """
    Convierte un PDF usando Docling y devuelve la representación cruda.
    """
    converter = DocumentConverter()
    doc: Document = converter.convert(pdf_path)
    return doc.model_dump()



# ------------------------------
# 2. LIMPIEZA Y ESTANDARIZACIÓN
# ------------------------------

def clean_docling(raw: dict) -> dict:
    """
    Recibe el JSON crudo de Docling y lo transforma al formato estándar:
    {
        "title": "",
        "metadata": {},
        "sections": [
            {"heading": "...", "content": "..."}
        ]
    }
    """
    clean = {
        "title": raw.get("metadata", {}).get("title", "Untitled Document"),
        "metadata": raw.get("metadata", {}),
        "sections": []
    }

    last_section = None

    for block in raw.get("elements", []):
        block_type = block.get("type")

        if block_type == "heading":
            heading = block.get("text", "").strip()
            clean["sections"].append({"heading": heading, "content": ""})
            last_section = clean["sections"][-1]

        elif block_type == "paragraph":
            if last_section is None:
                clean["sections"].append({"heading": "Introduction", "content": ""})
                last_section = clean["sections"][-1]

            content = block.get("text", "").strip()
            last_section["content"] += content + "\n"

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
    """
    chunks = []
    chunk_id = 0

    for sec in clean_json["sections"]:
        section_heading = sec["heading"]
        section_text = sec["content"]

        for chunk in chunk_text(section_text):
            chunks.append({
                "chunk_id": chunk_id,
                "source_section": section_heading,
                "text": chunk,
                "approx_words": len(chunk.split())
            })
            chunk_id += 1

    clean_json["chunks"] = chunks
    return clean_json
