import numpy as np
import matplotlib.pyplot as plt
import librosa
from scipy.fft import rfft, rfftfreq
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk

try:
        
    # --- FUNÇÃO DE INTERFACE GRÁFICA ---
    def selecionar_arquivo(titulo):
        """Abre uma janela para selecionar os arquivos de áudio gravados."""
        root = tk.Tk()
        root.withdraw() # Oculta a janela principal do Tkinter
        root.attributes("-topmost", True)
        # Filtro para aceitar apenas os formatos que convertemos e testamos
        caminho = filedialog.askopenfilename(
            title=titulo, 
            filetypes=[("Arquivos de Áudio", "*.mp3 *.wav *.ogg *.flac"), ("Todos os arquivos", "*.*")]
            )
        
        root.destroy()
        return caminho

    # --- CONFIGURAÇÕES INICIAIS ---
    # Definimos as 4 fontes exigidas pelo roteiro do trabalho [cite: 8, 10, 12, 14]
    fontes = ['Agudo', 'Grave', 'Medio', 'Misto']
    dados_audio = {}
    SR_PADRAO = 22050 # Taxa de amostragem padrão para garantir consistência na FFT

    print("Selecione os arquivos de 10 a 15 segundos para análise...")

    # --- CARREGAMENTO DOS DADOS ---
    for f in fontes:
        caminho = selecionar_arquivo(f"Selecione o áudio: {f}")
        if caminho:
            # librosa.load: Lê o arquivo e normaliza a amplitude automaticamente
            # mono=True: Garante que o sinal tenha apenas um canal para análise simples
            data, _ = librosa.load(caminho, sr=SR_PADRAO, mono=True)
            dados_audio[f] = data

    # --- PROCESSAMENTO E CÁLCULO DA FFT (PONTO 7) ---
    if len(dados_audio) == 4:
        plt.figure(figsize=(12, 7))

        for rotulo, sinal in dados_audio.items():
            N = len(sinal) # Número total de amostras do sinal
            
            # rfft: Calcula a Transformada Rápida de Fourier para sinais reais (mais eficiente)
            yf = rfft(sinal)
            # rfftfreq: Gera o eixo das frequências correspondente em Hertz (Hz)
            xf = rfftfreq(N, 1 / SR_PADRAO)
            
            # Magnitude: Calculamos o valor absoluto do sinal complexo e normalizamos pelo tamanho N
            magnitude = np.abs(yf) / N
            
            # --- IDENTIFICAÇÃO DA FREQUÊNCIA FUNDAMENTAL [cite: 20, 23] ---
            # argmax: Encontra o índice onde a amplitude é maior no espectro
            idx_max = np.argmax(magnitude)
            f_fundamental = xf[idx_max]
            print(f"Sinal {rotulo}: Frequência Fundamental = {f_fundamental:.2f} Hz")

            # Plotagem individual de cada espectro no mesmo gráfico (Conjunta) [cite: 22]
            plt.plot(xf, magnitude, label=f'{rotulo} (Fund: {f_fundamental:.0f}Hz)', alpha=0.7)

        # --- FORMATAÇÃO DO GRÁFICO ---
        plt.title("Análise Conjunta da Transformada de Fourier - UFPA/Castanhal")
        plt.xlabel("Frequência (Hz)")
        plt.ylabel("Magnitude (Amplitude)")
        plt.xlim(0, 8000) # Foco na faixa audível principal para facilitar a visualização
        plt.legend() # Exibe a legenda identificando cada sinal e sua fundamental
        plt.grid(True, linestyle=':', alpha=0.6)
        plt.show()
    else:
        print("Erro: Todos os 4 arquivos devem ser selecionados para a análise conjunta.")
        
except:
    print("erro de tipo de arquivo")
    print("somente arquivo de audio")
    app = ctk.CTk()
    app.geometry("300x200")
    app.title("Análise Espectral")

    label = ctk.CTkLabel(app, text="Erro de arquivo incompatível!", font=("Arial", 16))
    label.pack(expand=True)

    app.mainloop()