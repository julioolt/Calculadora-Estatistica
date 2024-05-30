import matplotlib.pyplot as plt
import pandas as pd  # Parte Funcional: Importação da biblioteca pandas para manipulação de dados
from collections import Counter
import PySimpleGUI as sg  # Parte Visual: Importação da biblioteca PySimpleGUI para construir a interface gráfica

# Funções de cálculo estatístico

def calcular_media(valores):
    return valores.mean()  # Parte Funcional: Uso do método mean() do pandas para calcular a média

def calcular_mediana(valores):
    return valores.median()  # Parte Funcional: Uso do método median() do pandas para calcular a mediana

def calcular_moda(valores):
    contador = Counter(valores)
    max_frequencia = max(contador.values())
    moda = [k for k, v in contador.items() if v == max_frequencia]
    return moda

def desenhar_grafico(valores, operacao, resultado):
    plt.figure()
    if operacao == 'media':
        plt.bar(range(len(valores)), valores)
        plt.axhline(y=resultado, color='r', linestyle='--', label=f'Média: {resultado:.2f}')
        plt.legend()
    elif operacao == 'mediana':
        valores_ordenados = sorted(valores)
        cores = ['red' if v == resultado else 'blue' for v in valores_ordenados]
        plt.bar(range(len(valores_ordenados)), valores_ordenados, color=cores)
    elif operacao == 'moda':
        contador = Counter(valores)
        plt.bar(contador.keys(), contador.values())
    
    plt.title(f'Gráfico de {operacao.capitalize()}')  # Parte Visual: Definição do título do gráfico
    plt.ylabel('Frequência')  # Parte Visual: Definição do rótulo do eixo y
    plt.xlabel('Valores')  # Parte Visual: Definição do rótulo do eixo x
    plt.savefig('grafico.png')  # Parte Funcional: Salvando o gráfico como imagem
    plt.close()

# Layout da interface gráfica

sg.theme('Reddit')  # Parte Visual: Definição do tema da interface gráfica

layout = [
    [sg.Text('Tipo de Operação (Media, Moda, Mediana)'), sg.Input(key='operacao')],  # Parte Visual: Entrada para selecionar a operação
    [sg.Text('Digite os Valores separando por vírgula'), sg.Input(key='valor')],  # Parte Visual: Entrada para os valores
    [sg.Button('Calcular')],  # Parte Visual: Botão para iniciar o cálculo
    [sg.Text('', key='resultado', size=(40, 1))],  # Parte Visual: Espaço para mostrar o resultado
    [sg.Image(key='grafico')]  # Parte Visual: Espaço para exibir o gráfico
]

# Criação da janela

janela = sg.Window('Calculadora Estatística', layout)  # Parte Visual: Criação da janela com o título "Calculadora Estatística"

# Loop principal da interface gráfica

while True:
    eventos, valores = janela.read()
    if eventos == sg.WIN_CLOSED:
        break
    if eventos == 'Calcular':
        operacao = valores['operacao'].lower()
        try:
            valor = pd.Series(list(map(float, valores['valor'].split(','))))  # Parte Funcional: Conversão dos valores para um objeto do tipo pd.Series
        except ValueError:
            janela['resultado'].update('Por favor, insira números válidos separados por vírgula.')
            continue

        if operacao == 'media':
            resultado = calcular_media(valor)
        elif operacao == 'mediana':
            resultado = calcular_mediana(valor)
        elif operacao == 'moda':
            resultado = calcular_moda(valor)
        else:
            resultado = 'Operação inválida. Por favor, insira Media, Moda ou Mediana.'
            janela['resultado'].update(resultado)
            continue

        janela['resultado'].update(f'Resultado: {resultado}')  # Parte Visual: Atualização do espaço de resultado com o valor calculado
        desenhar_grafico(valor, operacao, resultado)  # Parte Funcional: Chamada da função para desenhar o gráfico
        janela['grafico'].update('grafico.png')  # Parte Visual: Atualização do espaço de gráfico com a imagem gerada

janela.close()
