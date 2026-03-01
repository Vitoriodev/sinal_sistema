import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
from scipy.fft import fft, ifft, fftfreq

try: 

    # Configuração do CustomTkinter
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    class App(ctk.CTk):
        def __init__(self):
            super().__init__()
            
            self.title("Sistema de Filtragem de Áudio")
            self.geometry("400x450")

            # --- CONFIGURAÇÃO DA UI ---
            self.label = ctk.CTkLabel(self, text="Processamento de Sinais", font=("Arial", 20, "bold"))
            self.label.pack(pady=20)

            self.btn1 = ctk.CTkButton(self, text="Isolar Grave (Passa-Baixa)", command=self.acao_opcao_1)
            self.btn1.pack(pady=10)

            self.btn2 = ctk.CTkButton(self, text="Isolar Agudo (Passa-Alta)", command=self.acao_opcao_2)
            self.btn2.pack(pady=10)

            self.btn3 = ctk.CTkButton(self, text="Isolar Médio (Passa-Faixa)", command=self.acao_opcao_3)
            self.btn3.pack(pady=10)

            self.status_label = ctk.CTkLabel(self, text="Status: Aguardando seleção...", text_color="gray")
            self.status_label.pack(pady=20)

            self.btn_sair = ctk.CTkButton(self, text="Sair", fg_color="red", hover_color="darkred", command=self.destroy)
            self.btn_sair.pack(pady=10)

            # --- CARREGAMENTO INICIAL DOS DADOS ---
            # Vamos carregar os áudios assim que a classe iniciar
            self.carregar_e_processar_inicial()

        def selecionar_audio(self, nome_do_tipo):
            print(f"Selecione o arquivo de áudio para {nome_do_tipo}...")
            caminho_arquivo = filedialog.askopenfilename(
                title=f"Selecione o áudio para {nome_do_tipo}",
                filetypes=[("Áudios", "*.wav *.mp3 *.flac *.ogg"), ("Todos", "*.*")]
            )
            if caminho_arquivo:
                # Carrega o áudio com librosa
                y, sr = librosa.load(caminho_arquivo, sr=44100, mono=True)
                return y, sr, os.path.basename(caminho_arquivo)
            return None, None, None

        def carregar_e_processar_inicial(self):
            # Esconde a janela principal momentaneamente enquanto carrega
            self.withdraw()
            
            try:
                print("--- Seleção dos Áudios ---")
                # Carrega os 3 arquivos
                self.y_grave, self.sr, self.nome_grave = self.selecionar_audio("GRAVE (Baixa Freq)")
                self.y_medio, _, self.nome_medio = self.selecionar_audio("MÉDIO (Média Freq)")
                self.y_agudo, _, self.nome_agudo = self.selecionar_audio("AGUDO (Alta Freq)")

                if self.y_grave is None or self.y_medio is None or self.y_agudo is None:
                    print("Seleção cancelada. Fechando.")
                    self.destroy()
                    sys.exit()

                # Igualar tamanhos
                min_len = min(len(self.y_grave), len(self.y_medio), len(self.y_agudo))
                self.y_grave = self.y_grave[:min_len]
                self.y_medio = self.y_medio[:min_len]
                self.y_agudo = self.y_agudo[:min_len]

                # Criar Mistura
                self.sinal_misturado = self.y_grave + self.y_medio + self.y_agudo
                self.N = len(self.sinal_misturado)
                
                # Pré-calcular FFT da mistura e frequências
                self.freqs = fftfreq(self.N, d=1/self.sr)
                self.omega = 2 * np.pi * self.freqs
                self.X_mistura = fft(self.sinal_misturado)

                print("Áudios carregados e misturados com sucesso!")
                self.deiconify() # Mostra a janela novamente
                self.status_label.configure(text="Status: Áudios carregados. Escolha um filtro.")

            except Exception as e:
                print(f"Erro no carregamento: {e}")
                self.destroy()

        # --- FUNÇÃO DE PROCESSAMENTO E PLOTAGEM ---
        def gerar_graficos(self, H, alvo_original, nome_alvo, tipo_filtro):
            # Calcular a saída no domínio da frequência
            Y_saida = H * self.X_mistura
            
            # Voltar para o domínio do tempo (IFFT)
            y_recuperado = ifft(Y_saida).real 

            # --- PLOTAGEM ---
            plt.figure(figsize=(10, 10))

            # 1. Domínio do Tempo (Mistura)
            plt.subplot(3, 1, 1)
            librosa.display.waveshow(self.sinal_misturado, sr=self.sr, color='gray', alpha=0.5)
            plt.title('Entrada: Mistura dos 3 Áudios')
            plt.ylabel('Amplitude')

            # 2. Domínio da Frequência
            limite_vis = np.argmax(self.freqs > 8000) 
            plt.subplot(3, 1, 2)
            plt.plot(self.freqs[:limite_vis], np.abs(self.X_mistura[:limite_vis]), color='lightgray', label='Entrada (Mistura)')
            plt.plot(self.freqs[:limite_vis], np.abs(Y_saida[:limite_vis]), color='blue', linewidth=1.5, label='Saída Filtrada')
            plt.title(f"Espectro de Frequência: {tipo_filtro}")
            plt.legend()
            plt.grid(True, alpha=0.3)

            # 3. Comparação Final (Tempo)
            plt.subplot(3, 1, 3)
            trecho = int(0.05 * self.sr) # Zoom de 50ms
            tempo_eixo = np.linspace(0, 0.05, trecho)
            
            plt.plot(tempo_eixo, y_recuperado[:trecho], color='blue', linewidth=1.5, label='Recuperado (IFFT)')
            plt.plot(tempo_eixo, alvo_original[:trecho], color='green', linestyle='--', alpha=0.7, label=f'Original ({nome_alvo})')
            plt.title("Validação: Comparação da Forma de Onda (Zoom 50ms)")
            plt.xlabel("Tempo (s)")
            plt.legend()
            plt.grid(True, alpha=0.3)

            plt.tight_layout()
            plt.show()

        # --- AÇÕES DOS BOTÕES ---
        
        def acao_opcao_1(self):
            # Filtro Passa-Baixa (Isolar Grave)
            fc = 400
            RC = 1 / (2 * np.pi * fc)
            H = 1 / (1 + 1j * self.omega * RC)
            
            print(f"Aplicando Passa-Baixa ({fc}Hz)...")
            self.gerar_graficos(H, self.y_grave, self.nome_grave, "Passa-Baixa (Low-Pass)")

        def acao_opcao_2(self):
            # Filtro Passa-Alta (Isolar Agudo)
            fc = 3000
            RC = 1 / (2 * np.pi * fc)
            H = (1j * self.omega * RC) / (1 + 1j * self.omega * RC)
            
            print(f"Aplicando Passa-Alta ({fc}Hz)...")
            self.gerar_graficos(H, self.y_agudo, self.nome_agudo, "Passa-Alta (High-Pass)")

        def acao_opcao_3(self):
            # Filtro Passa-Faixa (Isolar Médio)
            fc_grave = 400
            fc_agudo = 3000
            RC_hp = 1 / (2 * np.pi * fc_grave)
            RC_lp = 1 / (2 * np.pi * fc_agudo)
            
            # Cascata: Passa-Alta * Passa-Baixa
            H_passa_alta = (1j * self.omega * RC_hp) / (1 + 1j * self.omega * RC_hp)
            H_passa_baixa = 1 / (1 + 1j * self.omega * RC_lp)
            H = H_passa_alta * H_passa_baixa
            
            print(f"Aplicando Passa-Faixa ({fc_grave}-{fc_agudo}Hz)...")
            self.gerar_graficos(H, self.y_medio, self.nome_medio, "Passa-Faixa (Band-Pass)")

    if __name__ == "__main__":
        app = App()
        app.mainloop()
    
except:
    print("erro de tipo de arquivo")
    print("somente arquivo de audio")
    app = ctk.CTk()
    app.geometry("300x200")
    app.title("Análise Espectral")

    label = ctk.CTkLabel(app, text="Erro de arquivo incompatível!", font=("Arial", 16))
    label.pack(expand=True)

    app.mainloop()