# 🎧 Processamento de Sinais de Áudio - Sinais e Sistemas

<p align="justify">
Este repositório contém um projeto desenvolvido para a disciplina de Sinais e Sistemas do curso de Engenharia de Computação da Universidade Federal do Pará (UFPA - Campus Castanhal). O objetivo é aplicar conceitos teóricos de Transformada de Fourier, análise espectral e filtragem digital em sinais de áudio reais.
</p>
    
## 🚀 Sobre o Projeto

<p align="justify">
O sistema é uma ferramenta interativa desenvolvida em Python que permite visualizar e manipular áudios em diferentes domínios. Através de uma interface moderna construída com CustomTkinter, o usuário pode realizar análises de frequência e testar o comportamento de filtros elétricos simulados.
</p>

### Principais Funcionalidades

- **Gráfico no Domínio do Tempo:** Visualização da forma de onda (amplitude vs. tempo) para análise de dinâmica e transientes.

- **Gráficos de Fourier:** Decomposição do sinal para identificação da frequência fundamental e harmônicas principais.

- **Análise Espectral Conjunta:** Comparação simultânea de quatro fontes distintas (Agudo, Grave, Médio e Misto) para estudo de perfis de frequência.

- **Simulação de Filtros Elétricos:** Implementação de filtros Passa-Baixa, Passa-Alta e Passa-Faixa, simulando o comportamento de circuitos RC para isolar componentes específicos de uma mistura de áudio.

## 🛠️ Tecnologias Utilizadas

O projeto utiliza o ecossistema científico do Python:

- **Librosa:** Para carregamento e processamento de áudio profissional.

- **SciPy (FFT):** Para cálculos matemáticos da Transformada Rápida de Fourier e filtros.

- **Matplotlib:** Para geração de gráficos de alta qualidade.

- **NumPy:** Manipulação eficiente de vetores de dados.

- **CustomTkinter:** Interface de usuário (GUI) moderna e responsiva.

## 📂 Estrutura de Arquivos

- **main.py:** Ponto de entrada da aplicação e menu principal.

- **Grafico_Dominio.py:** Script para plotagem da onda no tempo.

- **Grafico_Fourier.py:** Análise de picos e frequências dominantes.

- **Analise_Espectral.py:** Comparação de espectros de diferentes fontes.

- **Filtro_Eletrico.py:** Processamento e filtragem de sinais misturados.

## 🏁 Como Executar

    
### Certifique-se de ter o Python 3 instalado.

Instale as dependências necessárias:
 ```
 Bash
 pip install numpy matplotlib librosa scipy customtkinter
```

Execute o script principal:
 ```  
 Bash
 python main.py
```

## 🎓 Contexto Acadêmico

<p align="justify">
Este software foi desenvolvido como parte prática da disciplina de Sinais e Sistemas. O foco principal foi a aplicação da Transformada de Fourier para entender como o som se distribui no espectro de frequências e como a matemática pode ser usada para "limpar" ou isolar sons através de filtros eletrônicos digitais.
</p>    

**Autores:** Vitorio Augusto, João Manoel e Éfran Santos
**Instituição:** UFPA - Castanhal
**Curso:** Engenharia de Computação (4º Semestre)
