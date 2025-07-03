# extrair.py
import google.generativeai as genai

genai.configure(api_key="AIzaSyB_CvI0fHhBSvBv_Sb3K-uYGBTRseAtYvw") 
model = genai.GenerativeModel("gemini-1.5-flash")

def extrair_nome(caminho_frente_bi):
    with open(caminho_frente_bi, "rb") as f:
        response = model.generate_content([
            "Extraia apenas o nome completo do cidadão desta imagem. Responda somente com o nome.",
            {"mime_type": "image/jpeg", "data": f.read()}
        ])
    return response.text.strip()

def extrair_bi(caminho_frente_bi):
    with open(caminho_frente_bi, "rb") as f:
        response = model.generate_content([
            "Extraia apenas o número do bilhete de identidade desta imagem. Responda somente com o número.",
            {"mime_type": "image/jpeg", "data": f.read()}
        ])
    return response.text.strip()

def extrair_data_nascimento(caminho_verso_bi):
    with open(caminho_verso_bi, "rb") as f:
        response = model.generate_content([
            "Extraia apenas a data de nascimento desta imagem. Responda somente com a data no formato dd/mm/aaaa.",
            {"mime_type": "image/jpeg", "data": f.read()}
        ])
    return response.text.strip()

def extrair_data_validade(caminho_verso_bi):
    with open(caminho_verso_bi, "rb") as f:
        response = model.generate_content([
            "Extraia apenas a data de validade do bilhete. Responda somente com a data no formato dd/mm/aaaa.(inicio) - dd/mm/aaaaa (fim), para saberes a data de validade deves ver o seguinte: Emitido em: e Valido até:, no caso o emito em será o inicio e o válido até será o fim",
            {"mime_type": "image/jpeg", "data": f.read()}
        ])
    return response.text.strip()
    
def identificar_lado_bi(imagem_bytes):
    prompt = (
        "Esta imagem é a frente ou o verso de um bilhete de identidade angolano? "
        "Considere como frente se contiver o nome completo do cidadão, nome dos pais e o número do bilhete. "
        "Considere como verso se contiver datas, impressão digital ou sexo ou morada ou até mesmo um QR code. "
        "Responda apenas com 'frente' ou 'verso'."
    )
    response = model.generate_content([
        prompt,
        {"mime_type": "image/jpeg", "data": imagem_bytes}
    ])
    return response.text.strip().lower()

