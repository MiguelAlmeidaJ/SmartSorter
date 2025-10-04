import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import openai
from organizador import organizar_pasta
from desfazer import desfazer_organizacao
from classificador import CATEGORIAS, salvar_categorias

openai.api_key = ""  # Coloque sua chave aqui

def criar_interface():
    janela = tk.Tk()
    janela.title("SmartSorter - Controle Total do Usuário")
    janela.geometry("780x700")

    # --- Seleção de pasta ---
    tk.Label(janela, text="Selecione a pasta que deseja organizar:", font=("Arial", 12)).pack(pady=10)
    caminho_var = tk.StringVar()
    frame = tk.Frame(janela)
    frame.pack()
    tk.Entry(frame, textvariable=caminho_var, width=50).pack(side=tk.LEFT, padx=5)
    tk.Button(frame, text="Procurar", command=lambda: caminho_var.set(filedialog.askdirectory())).pack(side=tk.LEFT)

    # --- Opções ---
    var_ia = tk.BooleanVar(value=False)
    tk.Checkbutton(janela, text="Usar IA para classificação (opcional)", variable=var_ia).pack(pady=5)

    var_correcao = tk.BooleanVar(value=True)
    tk.Checkbutton(janela, text="Ativar correção manual antes de mover cada arquivo", variable=var_correcao).pack(pady=5)

    # --- Log ---
    log_text = tk.Text(janela, height=25, width=90)
    log_text.pack(pady=10)

    # --- Botões principais ---
    tk.Button(janela, text="Organizar", bg="#4CAF50", fg="white",
              font=("Arial", 11, "bold"),
              command=lambda: organizar_pasta(caminho_var.get(), log_text, var_ia.get(), openai, var_correcao.get())).pack(pady=5)

    tk.Button(janela, text="Desfazer Última Organização", bg="#f44336", fg="white",
              font=("Arial", 11, "bold"),
              command=lambda: desfazer_organizacao(caminho_var.get(), log_text)).pack(pady=5)

    # --- Categorias personalizadas ---
    tk.Label(janela, text="Categorias personalizadas:", font=("Arial", 10, "bold")).pack(pady=5)
    listbox_categorias = tk.Listbox(janela, height=7)
    listbox_categorias.pack()
    for cat in CATEGORIAS:
        listbox_categorias.insert(tk.END, cat)

    # --- Entrada e botões para adicionar/editar/remover ---
    frame_nova = tk.Frame(janela)
    frame_nova.pack(pady=5)
    entrada_categoria = tk.Entry(frame_nova, width=30)
    entrada_categoria.pack(side=tk.LEFT, padx=5)

    def adicionar_categoria():
        nova = entrada_categoria.get().strip()
        if nova and nova not in CATEGORIAS:
            CATEGORIAS.append(nova)
            salvar_categorias()
            listbox_categorias.insert(tk.END, nova)
            entrada_categoria.delete(0, tk.END)

    def editar_categoria():
        try:
            index = listbox_categorias.curselection()[0]
            antiga = CATEGORIAS[index]
            nova = simpledialog.askstring("Editar Categoria", f"Renomear '{antiga}' para:")
            if nova and nova not in CATEGORIAS:
                CATEGORIAS[index] = nova
                salvar_categorias()
                listbox_categorias.delete(index)
                listbox_categorias.insert(index, nova)
        except IndexError:
            messagebox.showwarning("Aviso", "Selecione uma categoria para editar.")

    def remover_categoria():
        try:
            index = listbox_categorias.curselection()[0]
            cat = CATEGORIAS[index]
            if messagebox.askyesno("Confirmação", f"Remover categoria '{cat}'?"):
                CATEGORIAS.pop(index)
                salvar_categorias()
                listbox_categorias.delete(index)
        except IndexError:
            messagebox.showwarning("Aviso", "Selecione uma categoria para remover.")

    tk.Button(frame_nova, text="Adicionar", command=adicionar_categoria).pack(side=tk.LEFT, padx=2)
    tk.Button(frame_nova, text="Editar", command=editar_categoria).pack(side=tk.LEFT, padx=2)
    tk.Button(frame_nova, text="Remover", command=remover_categoria).pack(side=tk.LEFT, padx=2)

    janela.mainloop()

if __name__ == "__main__":
    criar_interface()
