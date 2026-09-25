import asyncio
import edge_tts
import tkinter as tk
from tkinter import messagebox, filedialog
import pygame

pygame.mixer.init()

caminho_audio = None


async def gerar_com_edge(texto, caminho):
    voz = "pt-BR-AntonioNeural"

    comunicacao = edge_tts.Communicate(
        texto,
        voz
    )

    await comunicacao.save(caminho)


def gerar_audio():
    global caminho_audio

    texto = entrada_texto.get("1.0", tk.END).strip()

    if not texto:
        messagebox.showwarning(
            "Aviso",
            "Digite algum texto primeiro."
        )
        return

    caminho = filedialog.asksaveasfilename(
        title="Salvar áudio",
        defaultextension=".mp3",
        filetypes=[
            ("Arquivo MP3", "*.mp3")
        ],
        initialfile="audio.mp3"
    )

    if not caminho:
        return

    try:

        pygame.mixer.music.stop()

        asyncio.run(
            gerar_com_edge(
                texto,
                caminho
            )
        )

        caminho_audio = caminho

        botao_reproduzir.config(state=tk.NORMAL)
        botao_parar.config(state=tk.NORMAL)

        messagebox.showinfo(
            "Sucesso",
            f"Áudio gerado com sucesso!\n\n"
            f"Salvo em:\n{caminho}"
        )

    except Exception as erro:
        messagebox.showerror(
            "Erro",
            f"Não foi possível gerar o áudio.\n\n{erro}"
        )


def reproduzir_audio():
    if caminho_audio is None:
        messagebox.showwarning(
            "Aviso",
            "Gere um áudio primeiro."
        )
        return

    try:
        pygame.mixer.music.load(caminho_audio)
        pygame.mixer.music.play()

    except Exception as erro:
        messagebox.showerror(
            "Erro",
            f"Não foi possível reproduzir o áudio.\n\n{erro}"
        )


def parar_audio():
    pygame.mixer.music.stop()


def fechar_programa():
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    janela.destroy()

janela = tk.Tk()
janela.title("Conversor de Texto para Áudio - edge-tts")
janela.geometry("700x550")
janela.resizable(True, True)

titulo = tk.Label(
    janela,
    text="Conversor de Texto para Áudio",
    font=("Arial", 20, "bold")
)
titulo.pack(pady=20)

instrucao = tk.Label(
    janela,
    text="Digite o texto que deseja transformar em áudio:",
    font=("Arial", 12)
)
instrucao.pack(pady=5)

entrada_texto = tk.Text(
    janela,
    height=15,
    width=75,
    font=("Arial", 12),
    wrap=tk.WORD
)
entrada_texto.pack(
    padx=20,
    pady=10,
    fill="both",
    expand=True
)

frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=15)

botao = tk.Button(
    frame_botoes,
    text="GERAR ÁUDIO",
    font=("Arial", 12, "bold"),
    command=gerar_audio,
    padx=20,
    pady=10
)
botao.grid(row=0, column=0, padx=5)

botao_reproduzir = tk.Button(
    frame_botoes,
    text="▶ REPRODUZIR",
    font=("Arial", 12, "bold"),
    command=reproduzir_audio,
    padx=20,
    pady=10,
    state=tk.DISABLED
)
botao_reproduzir.grid(row=0, column=1, padx=5)

botao_parar = tk.Button(
    frame_botoes,
    text="⏹ PARAR",
    font=("Arial", 12, "bold"),
    command=parar_audio,
    padx=20,
    pady=10,
    state=tk.DISABLED
)
botao_parar.grid(row=0, column=2, padx=5)

janela.protocol(
    "WM_DELETE_WINDOW",
    fechar_programa
)

janela.mainloop()
