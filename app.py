import os
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import openai
import PyPDF2
import io

# Config
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def extract_text_from_pdf(file_bytes: bytes) -> str:
    texto = ""
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        for page in reader.pages:
            try:
                texto += page.extract_text() or ""
            except Exception:
                pass
    except Exception:
        texto = ""
    return texto

def format_summary_points(text: str) -> str:
    return text.strip()

@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "resumen": "", "status": ""})

@app.post("/resumir", response_class=HTMLResponse)
async def post_resumir(request: Request,
                       texto: str = Form(""),
                       nivel: str = Form("corto"),
                       filename_user: str = Form("resumen.txt"),
                       file: UploadFile = File(None)):
    contenido = texto or ""
    origen = ""
    if file is not None and file.filename != "":
        origen = file.filename
        content_bytes = await file.read()
        if file.filename.lower().endswith(".pdf"):
            contenido = extract_text_from_pdf(content_bytes)
        elif file.filename.lower().endswith(".txt"):
            try:
                contenido = content_bytes.decode("utf-8")
            except:
                contenido = content_bytes.decode("latin-1", errors="ignore")
        else:
            contenido = f"Formato no soportado: {file.filename}. Sube .pdf o .txt."

    if not contenido.strip():
        resumen = "No se ha recibido texto para resumir."
        return templates.TemplateResponse("index.html", {"request": request, "resumen": resumen, "status": "error"})

    prompt = f"Resume el siguiente texto en formato de puntos clave y una breve conclusión. Nivel: {nivel}.\n\nTexto:\n{contenido[:20000]}"

    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"system","content":"Eres un asistente que resume textos en español o inglés, y entrega puntos clave numerados y una breve conclusión."},
                      {"role":"user","content":prompt}],
            temperature=0.2,
            max_tokens=600
        )
        resumen_raw = resp.choices[0].message["content"]
        resumen = format_summary_points(resumen_raw)
        status = "ok"
    except Exception as e:
        resumen = f"Error generando resumen: {e}"
        status = "error"

    return templates.TemplateResponse("index.html", {"request": request, "resumen": resumen, "status": status, "origen": origen})

@app.post("/download")
async def download(resumen_text: str = Form(...), filename: str = Form("resumen.txt")):
    if not filename.lower().endswith(".txt"):
        filename += ".txt"
    return StreamingResponse(io.BytesIO(resumen_text.encode("utf-8")), media_type="text/plain", headers={"Content-Disposition": f"attachment; filename={filename}"})
