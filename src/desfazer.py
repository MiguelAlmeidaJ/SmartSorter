import os
import shutil
import json
from classificador import DESTINOS

def desfazer_organizacao(pasta_origem, log_text):
    historico_path = os.path.join(pasta_origem, "historico_organizacao.json")
    if not os.path.exists(historico_path):
        log_text.insert("end", "Nenhum histórico encontrado para desfazer!\n")
        return

    with open(historico_path, "r", encoding="utf-8") as f:
        historico = json.load(f)

    for arquivo, caminho_antigo in historico.items():
        encontrado = False
        for pasta in DESTINOS.keys():
            possivel_caminho = os.path.join(pasta_origem, pasta, arquivo)
            if os.path.exists(possivel_caminho):
                shutil.move(possivel_caminho, caminho_antigo)
                encontrado = True
                break
        if not encontrado and os.path.exists(caminho_antigo):
            continue
        log_text.insert("end", f"Desfeito: {arquivo} → {caminho_antigo}\n")
        log_text.update()

    os.remove(historico_path)
    log_text.insert("end", "Última organização foi desfeita!\n")
    log_text.update()
