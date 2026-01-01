import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import json
import os

imagens_lista = []

ARQUIVO_DADOS = "jogos.json"

# ===============================
# Salvamento
# ===============================
def salvar_jogos():
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(jogos, f, ensure_ascii=False, indent=4)

def carregar_jogos():
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# ===============================
# Janela Principal
# ===============================
root = tk.Tk()
root.title("Jogos Zerados")
root.geometry("900x600")

jogos = carregar_jogos()

# ===============================
# Lista com Scroll
# ===============================
lista_frame = tk.Frame(root)
lista_frame.pack(fill="both", expand=True, padx=10, pady=10)

canvas = tk.Canvas(lista_frame)
scrollbar = tk.Scrollbar(lista_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

def ajustar_largura(event):
    canvas.itemconfig(canvas_window, width=event.width)

canvas.bind("<Configure>", ajustar_largura)

canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# ===============================
# Janela Adicionar / Editar
# ===============================
def excluir_jogo(jogo):
    if jogo in jogos:
        jogos.remove(jogo)
        salvar_jogos()
        atualizar_lista()

# ===============================
# Janela Adicionar / Editar
# ===============================
def abrir_janela_jogo(jogo=None):
    janela = tk.Toplevel(root)
    janela.title("Adicionar Jogo" if jogo is None else "Editar Jogo")
    janela.geometry("500x700")
    janela.resizable(False, True)

    container = tk.Frame(janela)
    container.pack(fill="both", expand=True)

    dados = {
        "numero": tk.StringVar(value=jogo["numero"] if jogo else ""),
        "imagem": jogo["imagem"] if jogo else "",
        "nome": tk.StringVar(value=jogo["nome"] if jogo else ""),
        "categoria": tk.StringVar(value=jogo["categoria"] if jogo else ""),
        "plataforma": tk.StringVar(value=jogo["plataforma"] if jogo else ""),
        "ano": tk.StringVar(),
        "mes": tk.StringVar(),
        "dia": tk.StringVar(),
        "genero": tk.StringVar(value=jogo["genero"] if jogo else ""),
        "dificuldade": tk.StringVar(value=jogo["dificuldade"] if jogo else ""),
        "nota": tk.StringVar(value=jogo["nota"] if jogo else ""),
        "tempo": tk.StringVar(value=jogo["tempo"] if jogo else "")
    }

    def campo(label, var):
        tk.Label(container, text=label).pack(anchor="w", padx=10)
        tk.Entry(container, textvariable=var).pack(fill="x", padx=10, pady=5)

    campo("Número do jogo", dados["numero"])

    # ---------- Imagem ----------
    img_label = tk.Label(container, relief="solid")
    img_label.pack(pady=10)

    def atualizar_preview(path):
        img = Image.open(path).resize((80, 120))
        img_tk = ImageTk.PhotoImage(img)
        img_label.config(image=img_tk)
        img_label.image = img_tk

    if jogo and jogo["imagem"] and os.path.exists(jogo["imagem"]):
        atualizar_preview(jogo["imagem"])

    def escolher_imagem():
        path = filedialog.askopenfilename(
            filetypes=[("Imagens", "*.png *.jpg *.jpeg")]
        )
        if path:
            dados["imagem"] = path
            atualizar_preview(path)

    tk.Button(container, text="Escolher imagem", command=escolher_imagem).pack()

    campo("Nome do jogo", dados["nome"])

    tk.Label(container, text="Categoria").pack(anchor="w", padx=10)
    ttk.Combobox(
        container,
        textvariable=dados["categoria"],
        values=["Jogo Base", "Remake", "Remaster", "DLC/Expansão", "Mod", "Hack"]
    ).pack(fill="x", padx=10, pady=5)

    campo("Plataforma", dados["plataforma"])

    tk.Label(container, text="Data de conclusão").pack(anchor="w", padx=10)
    frame_data = tk.Frame(container)
    frame_data.pack(padx=10, pady=5)

    ttk.Combobox(frame_data, textvariable=dados["ano"],
                 values=[str(a) for a in range(1980, 2031)], width=7).pack(side="left")
    ttk.Combobox(frame_data, textvariable=dados["mes"],
                 values=["Janeiro","Fevereiro","Março","Abril","Maio","Junho",
                         "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"],
                 width=12).pack(side="left", padx=5)
    ttk.Combobox(frame_data, textvariable=dados["dia"],
                 values=[str(d) for d in range(1, 32)], width=5).pack(side="left")

    campo("Gênero", dados["genero"])
    campo("Dificuldade", dados["dificuldade"])

    tk.Label(container, text="Nota").pack(anchor="w", padx=10)
    ttk.Combobox(container, textvariable=dados["nota"],
                 values=[str(i) for i in range(1, 11)]
                 ).pack(fill="x", padx=10)

    campo("Tempo de jogo", dados["tempo"])

    def salvar():
        novo_jogo = {
            "numero": dados["numero"].get(),
            "imagem": dados["imagem"],
            "nome": dados["nome"].get(),
            "categoria": dados["categoria"].get(),
            "plataforma": dados["plataforma"].get(),
            "data": f'{dados["dia"].get()}/{dados["mes"].get()}/{dados["ano"].get()}',
            "genero": dados["genero"].get(),
            "dificuldade": dados["dificuldade"].get(),
            "nota": dados["nota"].get(),
            "tempo": dados["tempo"].get()
        }

        if jogo:
            jogos.remove(jogo)

        jogos.insert(0, novo_jogo)
        salvar_jogos()
        atualizar_lista()
        janela.destroy()

    tk.Button(container, text="Salvar", command=salvar).pack(pady=20)

# ===============================
# Atualizar Lista
# ===============================
def atualizar_lista():
    for w in scrollable_frame.winfo_children():
        w.destroy()

    imagens_lista.clear()

    for jogo in jogos:
        item = tk.Frame(scrollable_frame, bd=1, relief="solid", height=140)
        item.pack(fill="x", padx=5, pady=5)
        item.pack_propagate(False)

        # ======================
        # Número do jogo
        # ======================
        lbl_numero = tk.Label(
            item,
            text=jogo["numero"],
            width=6,
            font=("Arial", 12, "bold"),
            anchor="center"
        )
        lbl_numero.pack(side="left", padx=5)

        # ======================
        # Capa do jogo
        # ======================
        if jogo["imagem"] and os.path.exists(jogo["imagem"]):
            img = Image.open(jogo["imagem"]).resize((80, 120))
            img_tk = ImageTk.PhotoImage(img)
            imagens_lista.append(img_tk)

            lbl_img = tk.Label(item, image=img_tk)
            lbl_img.pack(side="left", padx=10)

        # ======================
        # Nome do jogo
        # ======================
        lbl_nome = tk.Label(
            item,
            text=jogo["nome"],
            font=("Arial", 12),
            anchor="w"
        )
        lbl_nome.pack(side="left", fill="x", expand=True)

        # ======================
        # Área direita (plataforma + botões)
        # ======================
        direita = tk.Frame(item)
        direita.pack(side="right", padx=10, pady=5)

        lbl_plataforma = tk.Label(
            direita,
            text=jogo["plataforma"],
            font=("Arial", 9),
            fg="gray"
        )
        lbl_plataforma.pack(anchor="e")

        btn_editar = tk.Button(
            direita,
            text="Editar",
            width=8,
            command=lambda j=jogo: abrir_janela_jogo(j)
        )
        btn_editar.pack(anchor="e", pady=2)

        btn_excluir = tk.Button(
            direita,
            text="Excluir",
            width=8,
            fg="red",
            command=lambda j=jogo: excluir_jogo(j)
        )
        btn_excluir.pack(anchor="e", pady=2)

    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))




# ===============================
# Botão Principal
# ===============================
tk.Button(root, text="Adicionar jogo",
          command=lambda: abrir_janela_jogo()).pack(pady=10)

atualizar_lista()
root.mainloop()
