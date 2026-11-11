
import csv
import os
import re
import statistics
from collections import defaultdict
from jiwer import wer, cer

def normalizar(texto):
    if not texto:
        return ""
    texto = texto.lower()
    texto = re.sub(r"[^\w\s]", " ", texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()

resultados = defaultdict(lambda: {"wer": [], "cer": []})

# Garante o caminho correto do arquivo mesmo executando da raiz ou de outra pasta
caminho_csv = os.path.join(os.path.dirname(__file__), "resultados_transcricoes.csv")

with open(caminho_csv, encoding="utf-8-sig", newline="") as arquivo:
    leitor = csv.DictReader(arquivo, delimiter=";")

    for linha in leitor:
        original = normalizar(linha.get("original"))
        transcricao = normalizar(linha.get("transcricao"))
        ferramenta = (linha.get("ferramenta") or "").strip()
        narrativa = (linha.get("narrativa") or "").strip()

        if not original or not transcricao:
            continue

        valor_wer = wer(original, transcricao) * 100
        valor_cer = cer(original, transcricao) * 100

        resultados[ferramenta]["wer"].append(valor_wer)
        resultados[ferramenta]["cer"].append(valor_cer)

        print(f"\nNarrativa: {narrativa}")
        print(f"Ferramenta: {ferramenta}")
        print(f"WER: {valor_wer:.2f}%")
        print(f"CER: {valor_cer:.2f}%")

print("\n===== RESULTADOS MÉDIOS =====")

for ferramenta, valores in resultados.items():
    media_wer = statistics.mean(valores["wer"])
    media_cer = statistics.mean(valores["cer"])

    desvio_wer = statistics.stdev(valores["wer"]) if len(valores["wer"]) > 1 else 0
    desvio_cer = statistics.stdev(valores["cer"]) if len(valores["cer"]) > 1 else 0

    print(f"\n{ferramenta}")
    print(f"WER médio: {media_wer:.2f}%")
    print(f"Desvio padrão WER: {desvio_wer:.2f}")
    print(f"CER médio: {media_cer:.2f}%")
    print(f"Desvio padrão CER: {desvio_cer:.2f}")
