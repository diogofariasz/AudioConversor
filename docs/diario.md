# Relatório de testes dos conversores de áudio Sprint 1 (22/09/2026 a 28/09/2026)

## 1. Acertos

Durante os testes, os três métodos de conversão de texto para áudio apresentaram funcionamento adequado:

- gTTS: conseguiu transformar o texto digitado em um arquivo de áudio `.mp3`.
- pyttsx3: conseguiu gerar o áudio localmente em formato `.wav`.
- Edge TTS: conseguiu gerar o áudio `.mp3` utilizando uma voz em português.
- Foi possível selecionar arquivos de áudio já existentes.
- Foi possível reproduzir e parar os áudios pela interface.
- A interface gráfica funcionou corretamente, incluindo a barra de rolagem da página.
- O sistema conseguiu utilizar o FFmpeg através do pydub para trabalhar com diferentes formatos de áudio.
- Os arquivos foram salvos corretamente nos locais escolhidos.
- Os três códigos foram posteriormente organizados e padronizados, deixando a estrutura mais limpa e semelhante entre os programas.

## 2. Erros e problemas encontrados

Apesar de a conversão de texto para áudio ter funcionado bem, foram identificados problemas principalmente na etapa de áudio para texto.

## 3. Problemas na sintaxe da conversão de áudio para texto

A parte de áudio para texto ficou mais complexa e menos organizada do que a conversão de texto para áudio.

Nos códigos gTTS e Edge TTS, é necessário verificar o formato do arquivo antes de realizar a conversão:

```python
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
```

Depois disso, o arquivo precisa ser convertido para WAV e somente então enviado ao `SpeechRecognition`.

Por isso, a sintaxe da conversão de áudio para texto não ficou tão boa quanto a da conversão de texto para áudio. O código funciona, mas essa parte pode ser simplificada e melhor organizada.

## 4. Conclusão

Os testes mostraram que a conversão de texto para áudio apresentou bons resultados nos três conversores. A interface, a geração, a seleção e a reprodução dos arquivos funcionaram corretamente.

O principal problema foi a etapa de áudio para texto, que apresentou erros no reconhecimento das palavras e uma estrutura de código mais complexa.

Portanto, a conversão de áudio para texto é a principal parte que precisa ser aprimorada, tanto em relação à organização da sintaxe quanto à qualidade do reconhecimento.

Resultado geral: os conversores de texto para áudio funcionaram satisfatoriamente, enquanto a conversão de áudio para texto apresentou resultados inferiores e deve ser considerada a principal parte a ser aprimorada.

///////////////////////////////////////////////////////////////////////////////