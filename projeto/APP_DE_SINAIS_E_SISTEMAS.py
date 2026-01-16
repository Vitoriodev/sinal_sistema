import customtkinter as ctk
import subprocess
import sys
import os

# Configuração do tema
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Menu Principal")
        self.geometry("400x400")
        
        # Titulo
        self.label = ctk.CTkLabel(self, text="Selecione uma opção", font=("Arial", 20, "bold"))
        self.label.pack(pady=20)
        
        # botões
        self.btn1 = ctk.CTkButton(self, text="Gráfico no Domínio ", command=self.sinal_sistema)
        self.btn1.pack(pady=10)

        self.btn2 = ctk.CTkButton(self, text="Gráficos de Fourier", command=self.fourier)
        self.btn2.pack(pady=10)

        self.btn3 = ctk.CTkButton(self, text="Análise Espectral", command=self.Fourier)
        self.btn3.pack(pady=10)

        self.btn4 = ctk.CTkButton(self, text="Filtro Elétrico", command=self.electriFilter)
        self.btn4.pack(pady=10)
        
        self.btn_sair = ctk.CTkButton(self, text="Sair", fg_color="red", hover_color="darkred", command=self.destroy)
        self.btn_sair.pack(pady=10)
        
        # Função genérica para abrir scripts
    def rodar_script(self, nome_arquivo):
        #  Pega o caminho da pasta onde este script que está salvo
        pasta_do_projeto = os.path.dirname(os.path.abspath(__file__))

        #  Junta a pasta com o nome do arquivo para criar o caminho completo
        caminho_completo = os.path.join(pasta_do_projeto, nome_arquivo)

        # Verifica e executa
        if os.path.exists(caminho_completo):
            # No Linux/Mac o python3 é chamado explicitamente, mas sys.executable resolve isso
            subprocess.Popen([sys.executable, caminho_completo])
        else:
            print(f"ERRO CRÍTICO: Não achei o arquivo em: {caminho_completo}")
            # Mostra o que tem na pasta para ajudar a debugar
            print(f"Arquivos na pasta: {os.listdir(pasta_do_projeto)}")

    # Funções específicas para cada botão
    def sinal_sistema(self):
        self.rodar_script("sinal_sistema.py")

    def fourier(self):
        self.rodar_script("fourier.py")

    def Fourier(self):
        self.rodar_script("Fourier.py")
        
    def electriFilter(self):
        self.rodar_script("electriFilter.py")

if __name__ == "__main__":
    app = App()
    app.mainloop()