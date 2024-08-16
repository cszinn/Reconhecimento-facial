import cv2
import os
import tkinter as tk
from tkinter import Label, Entry, Button, StringVar, Canvas
from PIL import Image, ImageTk


def voltar_menu():
    root.destroy()
    os.system('python menu_principal.py')  # Executa o menu principal


def cadastrar():
    nome = nome_var.get()
    funcao = funcao_var.get()

    # Verificar se o nome já existe
    if os.path.exists(f'pessoas/{nome}.png'):
        # Carregar a imagem de conflito e exibir no Canvas
        img_conflict = Image.open('Resources/screem/4.png')
        img_conflict_tk = ImageTk.PhotoImage(img_conflict)
        img_conflict_id = canvas.create_image(808, 44, anchor='nw', image=img_conflict_tk)
        canvas.image = img_conflict_tk  # Manter referência da imagem para evitar garbage collection
        label_status.config(text=f'O nome "{nome}" já existe. Escolha outro nome.')

        # Esconder os campos de entrada e o botão
        canvas.itemconfigure(entry_nome_window, state='hidden')
        canvas.itemconfigure(entry_funcao_window, state='hidden')
        canvas.itemconfigure(button_capturar_window, state='hidden')

        # Esperar 3 segundos e restaurar os elementos
        root.after(3000, lambda: restaurar_campos(img_conflict_id))
        return

    if nome and funcao:
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        success, img = cap.read()
        cap.release()

        if success:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_path = f'pessoas/{nome}.png'
            cv2.imwrite(img_path, img_rgb)

            # Salvar a função da pessoa em um arquivo de texto
            with open(f'pessoas/{nome}_funcao.txt', 'w') as f:
                f.write(funcao)

            label_status.config(text=f'{nome} cadastrado com sucesso!')
        else:
            label_status.config(text='Falha ao capturar a imagem.')
    else:
        label_status.config(text='Por favor, insira um nome e uma função.')


def restaurar_campos(img_conflict_id):
    # Remover a imagem de conflito
    canvas.delete(img_conflict_id)

    # Restaurar os campos de entrada e o botão
    canvas.itemconfigure(entry_nome_window, state='normal')
    canvas.itemconfigure(entry_funcao_window, state='normal')
    canvas.itemconfigure(button_capturar_window, state='normal')

    # Limpar a mensagem de status
    label_status.config(text='')


def capturar_foto():
    cadastrar()


# Interface gráfica para cadastro
root = tk.Tk()
root.title('Cadastro de Usuário')

# Carregar a imagem de fundo
bg_image_path = 'Resources/screem/menu.png'
bg_image = Image.open(bg_image_path)
bg_image_tk = ImageTk.PhotoImage(bg_image)

# Criar um Canvas para exibir a imagem de fundo
canvas = Canvas(root, width=bg_image_tk.width(), height=bg_image_tk.height())
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, anchor='nw', image=bg_image_tk)

# Coordenadas e configurações de cores
label_nome_x, label_nome_y = 1010, 100
entry_nome_x, entry_nome_y = 1010, 150
button_capturar_x, button_capturar_y = 1010, 450
button_voltar_y = 550  # Posicionamento ajustado
label_status_x, label_status_y = 1010, 500

# Definir as variáveis de entrada
nome_var = StringVar()
funcao_var = StringVar()

# Adicionar os elementos da interface gráfica no Canvas
canvas.create_text(label_nome_x, label_nome_y,
                   text='Nome do colaborador',
                   font=('Arial', 18, 'bold'),
                   fill='#6f50f8',
                  )

entry_nome = Entry(root, textvariable=nome_var)
entry_nome_window = canvas.create_window(entry_nome_x, entry_nome_y, window=entry_nome)


button_capturar = Button(root, text='Capturar Foto', command=capturar_foto, bg='#6f50f8', fg='white',
                         font=('Arial', 16), width=25)
button_capturar_window = canvas.create_window(button_capturar_x, button_capturar_y, window=button_capturar)

label_status = Label(root, text='', font=('Arial', 14))
canvas.create_window(label_status_x, label_status_y, window=label_status)

# Adicionar descrições adicionais
desc_x, desc_y = 1010, 250
canvas.create_text(desc_x, desc_y,
                   text='Função na empresa',
                   font=('Arial', 18, 'bold'),
                   fill='#6f50f8',
                  )

entry_funcao = Entry(root, textvariable=funcao_var)
entry_funcao_window = canvas.create_window(1010, 300, window=entry_funcao)

# Botão "Voltar" ajustado para ficar logo abaixo do botão "Capturar Foto"
button_voltar = Button(root, text="Voltar", command=voltar_menu, font=('Arial', 16),
                       width=25, bg='#6f50f8', fg='white')
canvas.create_window(button_capturar_x, button_voltar_y, window=button_voltar)

root.mainloop()
