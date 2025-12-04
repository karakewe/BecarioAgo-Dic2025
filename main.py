from fastapi import FastAPI, UploadFile, File
from extractor import extract_raw, clean_docling, add_chunks, save_clean
import uuid

app = FastAPI()

@app.get("/")
def check():
    return {"status": "ok"}


@app.post("/process")
async def process_pdf(file: UploadFile = File(...)):
    # Guardamos el PDF temporalmente
    file_id = str(uuid.uuid4())
    temp_path = f"temp_{file_id}.pdf"

    with open(temp_path, "wb") as f:
        f.write(await file.read())

    # Procesamiento
    raw = extract_raw(temp_path)
    clean = clean_docling(raw)
    final = add_chunks(clean)
    clean_path = save_clean(final, file.filename.replace(".pdf", ""))

    return final
