import os
import tkinter as tk
from tkinter import Canvas
from PIL import ImageTk, ImageDraw, Image
import cv2


def abrir_reconhecimento():
    root.withdraw()  # Esconde o menu principal
    os.system('python reconhecimento.py')
    root.deiconify()  # Traz o menu principal de volta após o reconhecimento


def abrir_cadastro():
    root.withdraw()  # Esconde o menu principal
    os.system('python cadastro.py')
    root.deiconify()  # Traz o menu principal de volta após o cadastro

def fechar_menu():
    root.destroy()

def criar_retangulo_arredondado(imagem, largura, altura, raio):
    """Cria uma imagem com retângulo de cantos arredondados."""
    # Criar uma máscara para o retângulo arredondado
    mask = Image.new('L', (largura, altura), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), (largura, altura)], raio, fill=255)

    # Aplicar a máscara à imagem
    imagem = imagem.convert('RGBA')
    imagem_com_mascara = Image.new('RGBA', (largura, altura))
    imagem_com_mascara.paste(imagem, (0, 0), mask)

    return imagem_com_mascara


# Interface gráfica principal
root = tk.Tk()
root.title('Sistema de Reconhecimento Facial')

# Carregar a imagem de fundo
bg_image_path = 'Resources/screem/menu.png'
bg_image = Image.open(bg_image_path)
bg_image_tk = ImageTk.PhotoImage(bg_image)

# Criar um Canvas para exibir a imagem de fundo
canvas = Canvas(root, width=bg_image_tk.width(), height=bg_image_tk.height())
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, anchor='nw', image=bg_image_tk)

# Carregar a imagem de sobreposição
overlay_image_path = 'Resources/screem/exemplo.png'
overlay_image = Image.open(overlay_image_path)

# Redimensionar a imagem (opcional)
novo_tamanho = (635, 479)  # Novo tamanho (largura, altura)
overlay_image = overlay_image.resize(novo_tamanho, Image.LANCZOS)

# Criar a imagem com cantos arredondados
overlay_image_arredondada = criar_retangulo_arredondado(overlay_image, novo_tamanho[0], novo_tamanho[1], 10)

# Converter para PhotoImage e adicionar no Canvas
overlay_image_tk = ImageTk.PhotoImage(overlay_image_arredondada)
canvas.create_image(59, 163, anchor='nw', image=overlay_image_tk)


# Adicionar título e botões no Canvas
label1 = tk.Label(root, text="Bem Vindo!", font=('Arial', 19, 'bold'), bg='white', fg='#6f50f8')
label2 = tk.Label(root, text="Escolha uma opção", font=('Arial', 19, 'bold'), bg='white', fg='#6f50f8')

# Modificar a cor de fundo dos botões
btn_reconhecimento = tk.Button(root, text="Reconhecimento", command=abrir_reconhecimento,
                               font=('Arial', 16), width=25, bg='#6f50f8', fg='white')
btn_cadastro = tk.Button(root, text="Cadastro", command=abrir_cadastro, font=('Arial', 16),
                         width=25, bg='#6f50f8', fg='white')
btn_fechar = tk.Button(root, text="Sair", command=fechar_menu, font=('Arial', 16),
                         width=25, bg='#6f50f8', fg='white')

# Posicionar os widgets no Canvas usando o método create_window()
canvas.create_window(1010, 100, window=label1)  # Posicionar o label 1
canvas.create_window(1010, 150, window=label2)  # Posicionar o label 2
canvas.create_window(1010, 350, window=btn_reconhecimento)  # Posicionar o botão de reconhecimento
canvas.create_window(1010, 450, window=btn_cadastro)  # Posicionar o botão de cadastro
canvas.create_window(1010, 550, window=btn_fechar)  # Posicionar o botão de fechar

root.mainloop()
