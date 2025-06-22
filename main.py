from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from verificador import verificar_identidade

app = FastAPI()

# Liberar o frontend (React) para consumir essa API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, troque por ["https://seudominio.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Criar pasta temporária para uploads
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/verificar")
async def verificar(bi: UploadFile = File(...), selfie: UploadFile = File(...)):
    caminho_bi = os.path.join(UPLOAD_DIR, bi.filename)
    caminho_selfie = os.path.join(UPLOAD_DIR, selfie.filename)

    # Salvar os arquivos localmente
    with open(caminho_bi, "wb") as buffer:
        shutil.copyfileobj(bi.file, buffer)
    with open(caminho_selfie, "wb") as buffer:
        shutil.copyfileobj(selfie.file, buffer)

    # Comparar usando apenas Gemini (a versão simplificada)
    resultado = verificar_identidade(caminho_bi, caminho_selfie)

    # Limpar arquivos após uso
    os.remove(caminho_bi)
    os.remove(caminho_selfie)

    return resultado

