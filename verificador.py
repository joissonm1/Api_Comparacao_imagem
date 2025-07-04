from PIL import Image
import google.generativeai as genai

genai.configure(api_key="AIzaSyBtLMyuQAKoVIe8ie8119KbNO4A4UgCh6E")


def comparar_com_gemini(caminho_bi, caminho_selfie):
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    with open(caminho_bi, "rb") as f1, open(caminho_selfie, "rb") as f2:
        response = model.generate_content([
            "Compare os rostos nessas duas imagens e diga se são da mesma pessoa. Dê uma porcentagem de similaridade de 0 a 100. Responda apenas com o número.",
            {"mime_type": "image/jpeg", "data": f1.read()},
            {"mime_type": "image/jpeg", "data": f2.read()}
        ])
    
    return response.text.strip()

def verificar_identidade(caminho_bi, caminho_selfie, usar_gemini=False):
    try:
        similaridade = float(comparar_com_gemini(caminho_bi, caminho_selfie))
    except Exception as e:
        return {
            "sucesso": False,
            "mensagem": f"Erro ao usar Gemini para comparação: {str(e)}"
        }

    status = "APROVADO" if similaridade >= 55 else "REPROVADO"
    return {
        "sucesso": True,
        "similaridade": similaridade,
        "status": status
    }

