import os
import sys
import json
from utils import ler_pdf, ler_docx, ler_imagem

# --- Função para obter caminho base (PyInstaller) ---
def base_path(path=""):
    if getattr(sys, "frozen", False):
        # Caminho dentro do executável
        return os.path.join(sys._MEIPASS, path)
    else:
        # Caminho normal
        return os.path.join(os.path.dirname(__file__), path)

# --- Categorias personalizadas ---
CATEGORIAS_PATH = base_path("../data/categorias.json")

def carregar_json(path, default):
    """Carrega JSON seguro, cria se não existir ou estiver vazio/corrompido"""
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default, f, ensure_ascii=False, indent=4)
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                return default
            return data
    except json.JSONDecodeError:
        return default

CATEGORIAS_DATA = carregar_json(CATEGORIAS_PATH, {"categorias": ["Documentos", "Imagens", "Planilhas", "Outros"]})
CATEGORIAS = CATEGORIAS_DATA.get("categorias", ["Documentos", "Imagens", "Planilhas", "Outros"])
DESTINOS = {cat: cat for cat in CATEGORIAS}

# --- Memória incremental ---
MEMORIA_PATH = base_path("../data/memoria.json")
MEMORIA = carregar_json(MEMORIA_PATH, {})

def salvar_memoria():
    with open(MEMORIA_PATH, "w", encoding="utf-8") as f:
        json.dump(MEMORIA, f, ensure_ascii=False, indent=4)

def salvar_categorias():
    with open(CATEGORIAS_PATH, "w", encoding="utf-8") as f:
        json.dump({"categorias": CATEGORIAS}, f, ensure_ascii=False, indent=4)

# --- Classificação por IA ---
def classificar_por_ia(texto, openai):
    try:
        prompt = f"Classifique o conteúdo a seguir em: {', '.join(CATEGORIAS)}.\n\nConteúdo:\n{texto}"
        resposta = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=10
        )
        categoria = resposta.choices[0].text.strip()
        return categoria if categoria in CATEGORIAS else "Outros"
    except:
        return "Outros"

# --- Classificação principal ---
def classificar_arquivo(caminho, extensao, usar_ia=False, openai=None, prioridade_usuario=True):
    # Primeiro verifica memória
    if caminho in MEMORIA and prioridade_usuario:
        return MEMORIA[caminho]["categoria"]

    texto = ""
    if usar_ia and openai:
        if extensao.lower() == ".pdf":
            texto = ler_pdf(caminho)
        elif extensao.lower() == ".docx":
            texto = ler_docx(caminho)
        elif extensao.lower() in [".jpg", ".jpeg", ".png"]:
            texto = ler_imagem(caminho)
        if texto:
            categoria = classificar_por_ia(texto, openai)
            MEMORIA[caminho] = {"categoria": categoria, "peso": 1}
            salvar_memoria()
            return categoria

    # Classificação por extensão
    for cat in CATEGORIAS:
        if cat.lower() in extensao.lower():
            MEMORIA[caminho] = {"categoria": cat, "peso": 1}
            salvar_memoria()
            return cat

    MEMORIA[caminho] = {"categoria": "Outros", "peso": 1}
    salvar_memoria()
    return "Outros"

# --- Atualizar prioridade manual ---
def atualizar_prioridade(caminho, categoria_corrigida):
    if caminho in MEMORIA:
        MEMORIA[caminho]["categoria"] = categoria_corrigida
        MEMORIA[caminho]["peso"] += 1
    else:
        MEMORIA[caminho] = {"categoria": categoria_corrigida, "peso": 2}
    salvar_memoria()
