import librosa
import librosa.display
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog
import customtkinter as ctk

# selecionar o arquivo de audio
while True:
    
    try:
        root = Tk()
        root.withdraw() # a janela Tkinter não vai aparecer
        root.attributes("-topmost", True) # a janela pra poder selecionar o arquivo vai aparecer na frente de tudo

        # abrir a janela para selecionar o arquivor
        print("selecione o arquivo de audio: ")
        caminho_de_audio = filedialog.askopenfilename( # vai abrir o explorado de arquivos 
            title="selecione um audio",
            filetypes=[("Arquivos de Áudio", "*.mp3 *.wav *.ogg *.flac"), ("Todos os arquivos", "*.*")] # esse vai mostra somentes os arquivos de audios 
        )     

        # carregar os arquivos de audios
        # y = amplitude e sr = amostragem
        if caminho_de_audio:
            print(f"arquivo carregado: {caminho_de_audio}")
            y, sr = librosa.load(caminho_de_audio) 

            # criar o grafico.
            plt.figure(figsize=(10, 4)) # tamanho do grafico
            librosa.display.waveshow(y, sr=sr, color="blue")

            # organiza o grafico
            plt.title(f"Domínio do tempo: {caminho_de_audio.split("/")[-1]}") # vai mostra o nome do arquivo 
            plt.xlabel("tempo (Segundos)")
            plt.ylabel("Amplitude")
            plt.tight_layout() #vai ajusta as margens dos textos
            plt.show() # vai abrir a janela 
            
        else:
            print("Nenhum arquivo foi selecionado")
            app = ctk.CTk()
            app.geometry("300x200")
            app.title("Opção 1")

            label = ctk.CTkLabel(app, text="Arquivo não foi adicionado!", font=("Arial", 16))
            label.pack(expand=True)

            app.mainloop()
            break
        
    except:
        print("erro de tipo de arquivo")
        print("somente arquivo de audio")
        app = ctk.CTk()
        app.geometry("300x200")
        app.title("Análise Espectral")

        label = ctk.CTkLabel(app, text="Erro de arquivo incompatível!", font=("Arial", 16))
        label.pack(expand=True)

        app.mainloop()