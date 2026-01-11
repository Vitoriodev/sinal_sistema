import numpy as np
import librosa
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog
from scipy.signal import find_peaks

while True:
    
    # seleciona arquivo
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    arquivo_de_audio = filedialog.askopenfilename(
        title="selecione um audio",
        filetypes=[("Arquivos de Áudio", "*.mp3 *.wav *.ogg *.flac"), ("Todos os arquivos", "*.*")]
    )


    try:
        if arquivo_de_audio:
            y, sr = librosa.load(arquivo_de_audio)
            
            n = len(y)
            fourier = np.fft.fft(y)
            frequencias = np.fft.fftfreq(n, d=1/sr)

            # Pegar apenas a parte positiva
            meio = n // 2
            frequencias_reais = frequencias[:meio]
            magnitude = np.abs(fourier[:meio])

            # 3. ENCONTRAR A FREQUÊNCIA FUNDAMENTAL (Maior Amplitude)
            indice_fundamental = np.argmax(magnitude)
            freq_fundamental = frequencias_reais[indice_fundamental]
            amp_fundamental = magnitude[indice_fundamental]

            # 4. ENCONTRAR HARMÔNICAS (Outros picos significativos)
            # 'height' define uma altura mínima para não pegar ruído
            # 'distance' evita pegar vários pontos do mesmo pico
            picos, propriedades = find_peaks(magnitude, height=amp_fundamental*0.1, distance=20)
            freq_picos = frequencias_reais[picos]
            amp_picos = magnitude[picos]

            # 5. PLOTAR
            plt.figure(figsize=(12, 6))
            plt.plot(frequencias_reais, magnitude, label='Espectro', color='gray', alpha=0.5)

            # Destacar a Fundamental
            plt.scatter(freq_fundamental, amp_fundamental, color='red', label=f'Maior Frequência Na Amplitude: {freq_fundamental:.2f} Hz', zorder=5)

            # Destacar Harmônicas (remover a fundamental da lista de harmônicas para não repetir)
            plt.scatter(freq_picos, amp_picos, color='blue', marker='x', label='Harmônicas/Picos')

            plt.title("Análise de Fourier: Fundamental e Harmônicas")
            plt.xlabel("Frequência (Hz)")
            plt.ylabel("Amplitude")
            plt.xlim(0, 3000) # Foco na região de interesse
            plt.legend()
            plt.grid(True, linestyle='--')
            plt.show()

            print(f"Frequência Fundamental: {freq_fundamental:.2f} Hz")
            
            
        else:
            print("somente arquivo de audio")
        
        
    except TypeError:
        print("erro de tipo de arquivo")
