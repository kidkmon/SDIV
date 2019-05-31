import os
import cv2
import emoji
import telebot
import numpy as np
from datetime import datetime
from keras import models
from time import sleep, strftime
from PIL import Image

def send_fire_notification(image):
    bot.send_message(chat_id, emoji.emojize(':police_car_light: :police_car_light: :police_car_light: :police_car_light: ALERTA :police_car_light: :police_car_light: :police_car_light: :police_car_light: \n Possível ocorrência de incêndio! :fire:'))
    photo = open(image, 'rb')
    bot.send_photo(chat_id, photo)
    faustao_gif = open('telegram_bot/faustao_fogo.gif', 'rb')
    bot.send_document(chat_id, faustao_gif)
    bot.send_message(chat_id, emoji.emojize('CONTATOS DE EMERGÊNCIA \n\n :fire_engine: Bombeiro: 193 \n :ambulance: Ambulânci: 911 \n :shield: Defesa Civil: 199'))

def send_image(image):
        img_name = 'fire/{}/{}.jpg'.format(date_string, strftime("%H-%M-%S"))
        cv2.imwrite(img_name, image)
        send_fire_notification(img_name)


#Configuração TelegramBot
token = "838657777:AAHvnc3nRR9uNjUm0g4NcmdiNPcjYATwcw4"

bot = telebot.TeleBot(token)
chat_id = '385861650'

#Carrega o modelo salvo
model = models.load_model('models/model.h5')
print("Modelo carregado")
video = cv2.VideoCapture(0)
print("Abrindo câmera")


date_string = strftime("%Y-%m-%d")
mydir = os.path.join(os.getcwd()+'/fire', date_string)

try:
        os.makedirs(mydir)
except FileExistsError:
        pass

cont = 0

while True:
        _, frame = video.read()

        #Converter o frame capturado para RGB
        im = Image.fromarray(frame, 'RGB')

        #Redimensionar a imagem para 128x128
        im = im.resize((128, 128))
        img_array = np.array(im)

        #Our keras model used a 4D tensor, (images x height x width x channel)
        #So changing dimension 128x128x3 into 1x128x128x3
        img_array1 = np.expand_dims(img_array, axis=0)

        #Predição do modelo com a imagem capturada
        prediction = int(model.predict(img_array1)[0][0])

        #Se a predição for 0, significa que foi capturado fogo através da Webcam.
        if(prediction == 0):
                if(cont > 50):
                        video.release()
                        cv2.destroyAllWindows()
                        send_image(frame)
                        break

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                cont += 1
                

        cv2.imshow("Capturing", frame)
        key = cv2.waitKey(1)

        if(key == ord('q')):
                break

video.release()
cv2.destroyAllWindows()
