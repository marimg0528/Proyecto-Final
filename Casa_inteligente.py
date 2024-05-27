import paho.mqtt.client as paho
import time
import json
import streamlit as st
import cv2
import numpy as np
from PIL import Image as Image, ImageOps as ImagOps
from keras.models import load_model

def on_publish(client, userdata, result): 
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)

broker = "broker.mqttdashboard.com"
port = 1883
client1 = paho.Client("Intento1")
client1.on_message = on_message
client1.on_publish = on_publish
client1.connect(broker, port)

model = load_model('keras_model.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)


page_bg_img = '''
<style>
[data-testid="stAppViewContainer"] {
    background-color: #F6FADC;
}
[data-testid="stMarkdownContainer"] * {
    color: black;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

st.title("Cerradura Inteligente")

img_file_buffer = st.camera_input("Toma una Foto")

if img_file_buffer is not None:
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    img = Image.open(img_file_buffer)

    newsize = (224, 224)
    img = img.resize(newsize)
    img_array = np.array(img)

    normalized_image_array = (img_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array

    prediction = model.predict(data)
    print(prediction)
    if prediction[0][0] > 0.4:
        st.header('Abriendo')
        client1.publish("MAR", "{'gesto': 'Abre'}", qos=0, retain=False)
        time.sleep(0.2)
    if prediction[0][1] > 0.4:
        st.header('Cerrando')
        client1.publish("MAR", "{'gesto': 'Cierra'}", qos=0, retain=False)
        time.sleep(0.2)
