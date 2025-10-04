import os
import shutil
import json
from datetime import datetime
from tkinter import simpledialog, Tk
from classificador import classificar_arquivo, MEMORIA, salvar_memoria, atualizar_prioridade, CATEGORIAS, salvar_categorias

def organizar_pasta(pasta_origem, log_text, usar_ia=False, openai=None, permitir_correcao_usuario=True):
    if not pasta_origem:
        log_text.insert("end", "Nenhuma pasta selecionada!\n")
        return

    log_text.insert("end", f"\nIniciando organização em: {pasta_origem}\n")
    log_text.update()

    historico_path = os.path.join(pasta_origem, "historico_organizacao.json")
    historico = {}

    # Cria pastas
    for pasta in CATEGORIAS:
        os.makedirs(os.path.join(pasta_origem, pasta), exist_ok=True)

    for arquivo in os.listdir(pasta_origem):
        caminho_arquivo = os.path.join(pasta_origem, arquivo)
        if os.path.isdir(caminho_arquivo):
            continue

        _, extensao = os.path.splitext(arquivo)
        categoria_sugerida = classificar_arquivo(caminho_arquivo, extensao, usar_ia, openai)

        # --- Correção manual pelo usuário ---
        if permitir_correcao_usuario:
            root = Tk()
            root.withdraw()  # esconde janela principal
            prompt = f"Arquivo: {arquivo}\nCategoria sugerida: {categoria_sugerida}\nEscolha a categoria correta ou crie nova:"
            opcoes = CATEGORIAS + ["Nova categoria..."]
            escolha = simpledialog.askstring("Confirmar Categoria", prompt)
            if escolha:
                if escolha.lower() == "nova categoria..." or escolha not in CATEGORIAS:
                    nova = simpledialog.askstring("Nova Categoria", "Digite o nome da nova categoria:")
                    if nova and nova not in CATEGORIAS:
                        CATEGORIAS.append(nova)
                        salvar_categorias()
                        categoria = nova
                    else:
                        categoria = categoria_sugerida
                else:
                    categoria = escolha
            else:
                categoria = categoria_sugerida
            root.destroy()
        else:
            categoria = categoria_sugerida

        atualizar_prioridade(caminho_arquivo, categoria)

        historico[arquivo] = caminho_arquivo
        destino = os.path.join(pasta_origem, categoria, arquivo)
        shutil.move(caminho_arquivo, destino)

        log_text.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] {arquivo} → {categoria}\n")
        log_text.update()

    # Salva histórico para desfazer
    with open(historico_path, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=4)

    log_text.insert("end", "Organização concluída com sucesso!\n")
    log_text.update()
