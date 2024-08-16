import cv2
import face_recognition as fr
import cvzone
import os
import time
from pyfirmata import Arduino, SERVO
import subprocess
import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
import numpy as np
from datetime import datetime  # Import para data e hora

# Configuração do Arduino e dos LEDs
board = Arduino('COM3')
board.digital[8].mode = SERVO

def rotateServo(angle):
    board.digital[8].write(angle)
    time.sleep(0.015)

ledVM = board.get_pin('d:7:o')  # LED Vermelho
ledVD = board.get_pin('d:5:o')  # LED Verde
ledAM = board.get_pin('d:6:o')  # LED Amarelo

# Configuração do VideoCapture e das imagens
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 640)  # Largura
cap.set(4, 480)  # Altura

imgBackgroud = cv2.imread('Resources/screem/menu.png')
imgLogin = cv2.imread('Resources/screem/6.png')
imgError = cv2.imread('Resources/screem/7.png')
imgMarked = cv2.imread('Resources/screem/4.png')
imgActive = cv2.imread('Resources/screem/1.png')
imgAnalize = cv2.imread('Resources/screem/5.png')

# Obter as dimensões das imagens
height, width, _ = imgBackgroud.shape

def carregar_base():
    global nomes, encods, funcoes
    nomes = []
    encods = []
    funcoes = []

    lista = os.listdir('pessoas')

    for arquivo in lista:
        if arquivo.endswith('.png'):
            img = cv2.imread(f'pessoas/{arquivo}')
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Verifica se há rosto na imagem antes de calcular o encoding
            face_encodings = fr.face_encodings(img)
            if face_encodings:  # Se a lista não estiver vazia
                encods.append(face_encodings[0])
                nomes.append(os.path.splitext(arquivo)[0])

                # Verifica se o arquivo da função existe e lê o conteúdo
                funcao_path = f'pessoas/{os.path.splitext(arquivo)[0]}_funcao.txt'
                if os.path.exists(funcao_path):
                    with open(funcao_path, 'r') as file:
                        funcoes.append(file.read().strip())
                else:
                    funcoes.append('Não informada')
            else:
                print(f"Nenhum rosto encontrado na imagem {arquivo}. Ignorando...")

    print('Base carregada!')

carregar_base()

def compararEnc(encImg):
    for id, enc in enumerate(encods):
        comp = fr.compare_faces([encImg], enc)
        if comp[0]:
            return True, nomes[id], funcoes[id]
    return False, None, None

def voltar():
    print("Voltando ao menu principal...")
    cap.release()
    cv2.destroyAllWindows()
    root.quit()  # Fecha a janela Tkinter
    subprocess.Popen(["python", "menu_principal.py"])  # Executa o script do menu principal

# Criar a interface gráfica do Tkinter
root = tk.Tk()
root.title("Reconhecimento Facial")

# Criar o Canvas para mostrar a imagem
canvas = Canvas(root, width=width, height=height)
canvas.pack()

# Criar o botão "Voltar"
btn_voltar = tk.Button(root, text="Voltar", command=voltar, font=('Arial', 16), width=25, bg='#6f50f8', fg='white')
canvas.create_window(1010, 550, window=btn_voltar)  # Posicionar o botão

# Função para atualizar o Canvas com a imagem da câmera
def update_canvas(img):
    # Converter a imagem OpenCV para uma imagem PIL
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(image=img_pil)

    # Atualizar o Canvas com a nova imagem
    canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
    canvas.image = img_tk

# Loop principal para reconhecimento facial
faceLoc = []
sleepRegister = False
sleepError = False

def process_frame():
    global faceLoc, sleepRegister, sleepError

    success, img = cap.read()
    if not success:
        print("Falha ao capturar imagem da câmera.")
        return

    imgP = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgActual = imgActive.copy()
    sleepRegister = False
    sleepError = False

    try:
        faceLoc.append(fr.face_locations(imgP)[0])
    except:
        faceLoc = []

    if faceLoc:
        y1, x2, y2, x1 = faceLoc[-1]
        w, h = x2 - x1, y2 - y1
        cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=2, colorR=(255, 0, 0))
        imgActual = imgAnalize.copy()
        ledAM.write(1)  # Acende o LED amarelo indicando que está analisando

    if len(faceLoc) > 20:
        encodeImg = fr.face_encodings(imgP)[0]
        comp, nome, funcao = compararEnc(encodeImg)

        if comp:
            imgActual = imgLogin.copy()
            faceLoc = []
            sleepRegister = True
            ledAM.write(0)
            ledVD.write(1)
            rotateServo(130)
            time.sleep(7)
            rotateServo(0)
            ledVD.write(0)
            cv2.putText(imgActual, f'{nome} - {funcao}', (910, 510), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Registrar data, hora, nome e função do login em um arquivo
            login_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            with open("logins.txt", "a") as file:
                file.write(f'{nome} ({funcao}) entrou em: {login_time}\n')

        else:
            imgActual = imgError.copy()
            faceLoc = []
            sleepError = True
            ledVM.write(1)
            ledAM.write(0)
            time.sleep(5)
            ledVM.write(0)

    imgBackgroud[162:162 + 480, 55:55 + 640] = img
    imgBackgroud[44:44 + 633, 808:808 + 414] = imgActual

    if sleepRegister:
        cv2.putText(imgBackgroud, f'{nome} - {funcao}', (900, 510), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    update_canvas(imgBackgroud)

    if sleepRegister or sleepError:
        cv2.waitKey(1500)

    root.after(10, process_frame)  # Agendar a próxima execução

# Iniciar o processo de captura e atualização
process_frame()

# Iniciar o loop da interface gráfica do Tkinter
root.mainloop()
