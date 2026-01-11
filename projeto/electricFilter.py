import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
from scipy.fft import fft, fftfreq, ifft
from tkinter import Tk, filedialog
import os

def selecionar_audio(nome_do_tipo):
    print(f"Selecione o arquivo de áudio para {nome_do_tipo}:")
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    caminho_arquivo = filedialog.askopenfilename(
        title=f"Selecione o arquivo de áudio para {nome_do_tipo}",
        filetypes=[("Arquivos de áudio", "*.wav *.mp3 *.flac *.ogg"), ("Todos os arquivos", "*.*")]
    )
    root.destroy()
    if caminho_arquivo:
        print(f"Carregando: {os.path.basename(caminho_arquivo)}...")
        y, sr = librosa.load(caminho_arquivo, sr=44100, mono=True)
        return y, sr, os.path.basename(caminho_arquivo)
    else:
        return None, None, None

# --- ETAPA 1: Carregamento dos Áudios ---
print("--- Seleção dos Áudios ---")
y_grave, sr_grave, nome_grave = selecionar_audio("GRAVE (Baixa Freq)")
y_medio, sr_medio, nome_medio = selecionar_audio("MÉDIO (Média Freq)")
y_agudo, sr_agudo, nome_agudo = selecionar_audio("AGUDO (Alta Freq)")

if y_grave is None or y_medio is None or y_agudo is None:
    raise Exception("Cancelado: É necessário selecionar os três arquivos.")

# Igualar tamanhos para somar
min_len = min(len(y_grave), len(y_medio), len(y_agudo))
y_grave, y_medio, y_agudo = y_grave[:min_len], y_medio[:min_len], y_agudo[:min_len]

# Criar a mistura
sinal_misturado = y_grave + y_medio + y_agudo
fs = sr_grave
N = len(sinal_misturado)

# --- ETAPA 2: Menu de Escolha do Filtro ---
print("\nQual áudio você deseja isolar/recuperar?")
print("1 - Grave (Usa Filtro Passa-Baixa)")
print("2 - Agudo (Usa Filtro Passa-Alta)")
print("3 - Médio (Usa Filtro Passa-Faixa)")
escolha = input("Digite o número da opção (1, 2 ou 3): ")

# Definição das frequências angulares
freqs = fftfreq(N, d=1/fs)
omega = 2 * np.pi * freqs

# Lógica Matemática dos Filtros 
fc_grave = 400   # Corte para o Passa-Baixa
fc_agudo = 3000  # Corte para o Passa-Alta

if escolha == '1': # ISOLAR GRAVE
    print(f"Isolando Grave com corte em {fc_grave}Hz...")
    RC = 1 / (2 * np.pi * fc_grave)
    H = 1 / (1 + 1j * omega * RC)
    alvo_original = y_grave
    nome_alvo = nome_grave
    tipo_filtro = "Passa-Baixa (Low-Pass)"

elif escolha == '2': # ISOLAR AGUDO
    print(f"Isolando Agudo com corte em {fc_agudo}Hz...")
    RC = 1 / (2 * np.pi * fc_agudo)
    H = (1j * omega * RC) / (1 + 1j * omega * RC)
    alvo_original = y_agudo
    nome_alvo = nome_agudo
    tipo_filtro = "Passa-Alta (High-Pass)"

elif escolha == '3': # ISOLAR MÉDIO
    print(f"Isolando Médio (entre {fc_grave}Hz e {fc_agudo}Hz)...")
    RC_hp = 1 / (2 * np.pi * fc_grave) 
    RC_lp = 1 / (2 * np.pi * fc_agudo) 
    H_passa_alta = (1j * omega * RC_hp) / (1 + 1j * omega * RC_hp)
    H_passa_baixa = 1 / (1 + 1j * omega * RC_lp)
    H = H_passa_alta * H_passa_baixa 
    alvo_original = y_medio
    nome_alvo = nome_medio
    tipo_filtro = "Passa-Faixa (Band-Pass)"
else:
    raise Exception("Opção inválida.")

# --- ETAPA 3: Processamento (Freq e Tempo) ---
X_mistura = fft(sinal_misturado)
Y_saida = H * X_mistura
X_alvo_original = fft(alvo_original)

# [NOVO] Obtendo a resposta de saída no tempo (IFFT)
# y(t) = Inversa de Fourier da Saída
y_recuperado = ifft(Y_saida).real 

# --- ETAPA 4: Plotagem ---
plt.figure(figsize=(12, 12))

# Plot 1: Domínio do Tempo (Entrada Misturada)
plt.subplot(3, 1, 1)
librosa.display.waveshow(sinal_misturado, sr=fs, color='gray', alpha=0.5)
plt.title('Entrada: Mistura dos 3 Áudios (Tempo)')
plt.ylabel('Amplitude')

# Configuração do eixo X para freq
limite_visualizacao = np.argmax(freqs > 8000) 

# Plot 2: Domínio da Frequência (Entrada vs Saída Filtrada)
plt.subplot(3, 1, 2)
plt.plot(freqs[:limite_visualizacao], np.abs(X_mistura[:limite_visualizacao]), color='lightgray', label='Entrada (Sujo)')
plt.plot(freqs[:limite_visualizacao], np.abs(Y_saida[:limite_visualizacao]), color='blue', linewidth=1.5, label='Saída Filtrada Y(jw)')
plt.title(f"Espectro de Frequência: {tipo_filtro}")
plt.ylabel("Magnitude")
plt.legend()
plt.grid(True, alpha=0.3)

# [ALTERADO] Plot 3: Domínio do Tempo (Saída Recuperada vs Original)
plt.subplot(3, 1, 3)

# Zoom de 50ms para ver a forma de onda
trecho = int(0.05 * fs)
tempo_eixo = np.linspace(0, 0.05, trecho)

plt.plot(tempo_eixo, y_recuperado[:trecho], color='blue', linewidth=1.5, label='Sua Resposta y(t) (IFFT)')
plt.plot(tempo_eixo, alvo_original[:trecho], color='green', linestyle='--', alpha=0.7, label=f'Original: {nome_alvo}')

plt.title("Validação Final: Comparação da Forma de Onda (Zoom 50ms)")
plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()