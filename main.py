from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import uuid
import json

from verificador import verificar_identidade
from extrair import (
    extrair_nome,
    extrair_bi,
    extrair_data_nascimento,
    identificar_lado_bi,
    extrair_data_validade
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def salvar_dados_localmente(nome_arquivo, dados):
    caminho = os.path.join("dados", f"{nome_arquivo}.json")
    os.makedirs("dados", exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

@app.post("/verificar")
async def verificar(
    frente_bi: UploadFile = File(...),
    verso_bi: UploadFile = File(...),
    selfie: UploadFile = File(...)
):
    nome_frente = f"frente_{uuid.uuid4().hex}.jpg"
    nome_verso = f"verso_{uuid.uuid4().hex}.jpg"
    nome_selfie = f"selfie_{uuid.uuid4().hex}.jpg"

    caminho_frente = os.path.join(UPLOAD_DIR, nome_frente)
    caminho_verso = os.path.join(UPLOAD_DIR, nome_verso)
    caminho_selfie = os.path.join(UPLOAD_DIR, nome_selfie)

    # Salvar os arquivos temporariamente
    with open(caminho_frente, "wb") as f:
        shutil.copyfileobj(frente_bi.file, f)
    with open(caminho_verso, "wb") as f:
        shutil.copyfileobj(verso_bi.file, f)
    with open(caminho_selfie, "wb") as f:
        shutil.copyfileobj(selfie.file, f)

    # Verificação do lado das imagens com IA
    with open(caminho_frente, "rb") as f:
        lado_frente = identificar_lado_bi(f.read())
    with open(caminho_verso, "rb") as f:
        lado_verso = identificar_lado_bi(f.read())

    if lado_frente != "frente" or lado_verso != "verso":
        # Limpa os arquivos temporários
        for caminho in [caminho_frente, caminho_verso, caminho_selfie]:
            if os.path.exists(caminho):
                os.remove(caminho)
        return {
            "erro": "As imagens parecem estar invertidas ou incorretas. "
                    "Certifique-se de enviar a frente do BI onde aparece o nome, número e nomes dos pais, "
                    "e o verso onde aparecem as datas e impressão digital."
        }

    # Extração de dados
    nome = extrair_nome(caminho_frente)
    bi = extrair_bi(caminho_frente)
    data_nascimento = extrair_data_nascimento(caminho_verso)
    data_validade = extrair_data_validade(caminho_verso)
    resultado_verificacao = verificar_identidade(caminho_frente, caminho_selfie)

    dados_extraidos = {
        "nome": nome,
        "numero_bi": bi,
        "data_nascimento": data_nascimento,
        "data_validade": data_validade,
        "verificacao": resultado_verificacao
    }

    salvar_dados_localmente("dados_extrato", dados_extraidos)

    # Limpar arquivos temporários
    for caminho in [caminho_frente, caminho_verso, caminho_selfie]:
        if os.path.exists(caminho):
            os.remove(caminho)

    return dados_extraidos

