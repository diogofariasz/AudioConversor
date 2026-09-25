from gtts import gTTS
import tkinter as tk
from tkinter import messagebox, filedialog
import pygame
import speech_recognition as sr
from pydub import AudioSegment
import os
import tempfile


pygame.mixer.init()

caminho_audio = None


def gerar_audio():
    global caminho_audio

    texto = entrada_texto.get("1.0", tk.END).strip()

    if not texto:
        messagebox.showwarning("Aviso", "Digite algum texto primeiro.")
        return

    caminho = filedialog.asksaveasfilename(
        title="Salvar áudio",
        defaultextension=".mp3",
        filetypes=[("Arquivo MP3", "*.mp3")],
        initialfile="audio_gtts.mp3"
    )

    if not caminho:
        return

    try:
        pygame.mixer.music.stop()

        audio = gTTS(text=texto, lang="pt", slow=False)
        audio.save(caminho)

        caminho_audio = caminho

        botao_reproduzir.config(state=tk.NORMAL)
        botao_parar.config(state=tk.NORMAL)
        botao_audio_texto.config(state=tk.NORMAL)

        label_arquivo.config(
            text=f"Áudio selecionado:\n{caminho}"
        )

        messagebox.showinfo(
            "Sucesso",
            f"Áudio gerado com sucesso!\n\nSalvo em:\n{caminho}"
        )

    except Exception as erro:
        messagebox.showerror(
            "Erro",
            f"Não foi possível gerar o áudio.\n\n{erro}"
        )


def selecionar_audio():
    global caminho_audio

    caminho = filedialog.askopenfilename(
        title="Selecionar áudio",
        filetypes=[
            ("Arquivos de áudio", "*.mp3 *.wav *.ogg *.flac"),
            ("Arquivo MP3", "*.mp3"),
            ("Arquivo WAV", "*.wav"),
            ("Arquivo OGG", "*.ogg"),
            ("Arquivo FLAC", "*.flac"),
            ("Todos os arquivos", "*.*")
        ]
    )

    if not caminho:
        return

    caminho_audio = caminho

    botao_reproduzir.config(state=tk.NORMAL)
    botao_parar.config(state=tk.NORMAL)
    botao_audio_texto.config(state=tk.NORMAL)

    label_arquivo.config(
        text=f"Áudio selecionado:\n{caminho}"
    )


def reproduzir_audio():
    if caminho_audio is None:
        messagebox.showwarning(
            "Aviso",
            "Gere ou selecione um áudio primeiro."
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


def audio_para_texto():
    if caminho_audio is None:
        messagebox.showwarning(
            "Aviso",
            "Gere ou selecione um áudio primeiro."
        )
        return

    try:
        pygame.mixer.music.stop()

        reconhecedor = sr.Recognizer()

        extensao = os.path.splitext(caminho_audio)[1].lower()

        if extensao == ".mp3":
            audio = AudioSegment.from_mp3(caminho_audio)

        elif extensao == ".wav":
            audio = AudioSegment.from_wav(caminho_audio)

        elif extensao == ".ogg":
            audio = AudioSegment.from_ogg(caminho_audio)

        elif extensao == ".flac":
            audio = AudioSegment.from_file(
                caminho_audio,
                format="flac"
            )

        else:
            audio = AudioSegment.from_file(caminho_audio)

        caminho_wav = os.path.join(
            tempfile.gettempdir(),
            "audio_conversao_gtts.wav"
        )

        audio.export(caminho_wav, format="wav")

        with sr.AudioFile(caminho_wav) as fonte:
            dados_audio = reconhecedor.record(fonte)

        texto_reconhecido = reconhecedor.recognize_google(
            dados_audio,
            language="pt-BR"
        )

        resultado_texto.delete("1.0", tk.END)
        resultado_texto.insert(tk.END, texto_reconhecido)

    except sr.UnknownValueError:
        messagebox.showerror(
            "Erro",
            "Não foi possível entender o áudio."
        )

    except sr.RequestError as erro:
        messagebox.showerror(
            "Erro",
            f"Erro no serviço de reconhecimento:\n{erro}"
        )

    except Exception as erro:
        messagebox.showerror(
            "Erro",
            f"Não foi possível converter o áudio.\n\n{erro}"
        )


def fechar_programa():
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    janela.destroy()


janela = tk.Tk()
janela.title("Conversor de Texto para Áudio - gTTS")
janela.geometry("850x700")
janela.minsize(650, 500)


canvas = tk.Canvas(janela)

scrollbar = tk.Scrollbar(
    janela,
    orient=tk.VERTICAL,
    command=canvas.yview
)

canvas.configure(
    yscrollcommand=scrollbar.set
)

scrollbar.pack(
    side=tk.RIGHT,
    fill=tk.Y
)

canvas.pack(
    side=tk.LEFT,
    fill=tk.BOTH,
    expand=True
)


frame_principal = tk.Frame(canvas)

canvas_window = canvas.create_window(
    (0, 0),
    window=frame_principal,
    anchor="nw"
)


def atualizar_scroll(event=None):
    canvas.configure(
        scrollregion=canvas.bbox("all")
    )


def ajustar_largura(event):
    canvas.itemconfig(
        canvas_window,
        width=event.width
    )


frame_principal.bind(
    "<Configure>",
    atualizar_scroll
)

canvas.bind(
    "<Configure>",
    ajustar_largura
)


def rolar_mouse(event):
    canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )


canvas.bind_all(
    "<MouseWheel>",
    rolar_mouse
)


titulo = tk.Label(
    frame_principal,
    text="Conversor de Texto para Áudio - gTTS",
    font=("Arial", 20, "bold")
)

titulo.pack(pady=20)


instrucao = tk.Label(
    frame_principal,
    text="Digite o texto que deseja transformar em áudio:",
    font=("Arial", 12)
)

instrucao.pack(pady=5)


entrada_texto = tk.Text(
    frame_principal,
    height=12,
    width=90,
    font=("Arial", 12),
    wrap=tk.WORD
)

entrada_texto.pack(
    padx=25,
    pady=10,
    fill=tk.X
)


frame_botoes = tk.Frame(frame_principal)
frame_botoes.pack(pady=10)


botao = tk.Button(
    frame_botoes,
    text="GERAR ÁUDIO",
    font=("Arial", 12, "bold"),
    command=gerar_audio,
    padx=20,
    pady=10
)

botao.grid(
    row=0,
    column=0,
    padx=5
)


botao_selecionar = tk.Button(
    frame_botoes,
    text="SELECIONAR ÁUDIO",
    font=("Arial", 12, "bold"),
    command=selecionar_audio,
    padx=20,
    pady=10
)

botao_selecionar.grid(
    row=0,
    column=1,
    padx=5
)


botao_reproduzir = tk.Button(
    frame_botoes,
    text="▶ REPRODUZIR",
    font=("Arial", 12, "bold"),
    command=reproduzir_audio,
    padx=20,
    pady=10,
    state=tk.DISABLED
)

botao_reproduzir.grid(
    row=1,
    column=0,
    padx=5,
    pady=8
)


botao_parar = tk.Button(
    frame_botoes,
    text="⏹ PARAR",
    font=("Arial", 12, "bold"),
    command=parar_audio,
    padx=20,
    pady=10,
    state=tk.DISABLED
)

botao_parar.grid(
    row=1,
    column=1,
    padx=5,
    pady=8
)


botao_audio_texto = tk.Button(
    frame_botoes,
    text="🎤 ÁUDIO → TEXTO",
    font=("Arial", 12, "bold"),
    command=audio_para_texto,
    padx=20,
    pady=10,
    state=tk.DISABLED
)

botao_audio_texto.grid(
    row=2,
    column=0,
    columnspan=2,
    pady=8
)


label_arquivo = tk.Label(
    frame_principal,
    text="Nenhum áudio selecionado.",
    font=("Arial", 10),
    wraplength=780
)

label_arquivo.pack(pady=10)


label_resultado = tk.Label(
    frame_principal,
    text="Texto reconhecido do áudio:",
    font=("Arial", 14, "bold")
)

label_resultado.pack(pady=10)


resultado_texto = tk.Text(
    frame_principal,
    height=12,
    width=90,
    font=("Arial", 12),
    wrap=tk.WORD
)

resultado_texto.pack(
    padx=25,
    pady=10,
    fill=tk.X
)


label_final = tk.Label(
    frame_principal,
    text="Conversão concluída.",
    font=("Arial", 10)
)

label_final.pack(pady=20)


janela.protocol(
    "WM_DELETE_WINDOW",
    fechar_programa
)

janela.mainloop()