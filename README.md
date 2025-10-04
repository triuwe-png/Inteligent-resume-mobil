# 🧠 Bot IA Resumen Móvil (FastAPI)

**Bot IA Resumen Móvil** es una pequeña aplicación FastAPI pensada para desplegar rápido en Render o ejecutar localmente.  
Genera **resúmenes por puntos clave** (y una conclusión breve) a partir de texto pegado o archivos `.txt` / `.pdf`.  
Interfaz móvil, bilingüe (español / inglés) y con una animación de ondas mientras "piensa".

---

## Contenido del paquete

```
bot-ia-resumen-movil/
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── uploads/
└── .gitignore
```

---

## Requisitos

- Python 3.10+
- Clave de OpenAI (API Key)

---

## Instalación local

1. Clonar el repo o descomprimir el ZIP:
```bash
git clone <tu-repo>
cd bot-ia-resumen-movil
```

2. Crear y activar virtualenv (recomendado):
```bash
python -m venv env
source env/bin/activate   # Linux / macOS
env\Scripts\activate    # Windows PowerShell
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Crear archivo `.env` en la raíz con:
```
OPENAI_API_KEY=tu_clave_aqui
```

5. Ejecutar localmente:
```bash
uvicorn app:app --reload
```
Abre: http://127.0.0.1:8000

---

## Despliegue en Render.com (paso a paso)

1. Crea cuenta en https://render.com y conéctala a GitHub.
2. Sube tu proyecto a un repositorio nuevo (no subas el `.env`).
3. En Render, elige **New -> Web Service** y selecciona tu repo.
4. Configura:
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app:app --host 0.0.0.0 --port 10000`
5. En **Environment** (Advanced) agrega variable:
   - `OPENAI_API_KEY` = `sk-...` (tu clave)
6. Deploy. En unos minutos tendrás la URL pública.

---

## Uso

- Pega texto o sube .txt / .pdf
- Elige nivel (Corto / Medio / Detallado)
- Haz clic en **Generar resumen**
- Descarga el resumen con el nombre que elijas

---

## Notas

- No subas tu `.env` ni tu clave a GitHub.
- Si el modelo necesita cambiar, edita la línea `model="gpt-3.5-turbo"` en `app.py`.
- Firma: *Hecho por David Castaño 💡*
