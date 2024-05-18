import paho.mqtt.client as paho
import time
import streamlit as st
import requests

broker = "broker.mqttdashboard.com"
port = 1883
client1 = paho.Client("Intento3")

def on_publish(client, userdata, result):
    print("El dato ha sido publicado\n")

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)

client1.on_message = on_message
client1.on_publish = on_publish

client1.connect(broker, port)

URL_BOMBILLA = "https://wokwi.com/projects/377066087789108225"

def encender_bombilla():
    try:
        response = requests.get(URL_BOMBILLA)
        if response.status_code == 200:
            st.success("¡La luz se ha encendido!")
        else:
            st.error("Hubo un problema al intentar encender la bombilla.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {e}")

st.title("Control de Bombillo")
st.write("Escribe algo en el siguiente cuadro y presiona el botón para encender la luz.")

input_texto = st.text_input("Escribe aquí:")
boton_encender = st.button("Encender Bombilla")

if (input_texto=="hola"):
    client1.publish("MAR","{'led': 'Enciende'}",qos=0, retain=False)
    st.write ("hola")
if (input_texto=="adios"):
    client1.publish("MAR","{'led': 'Apaga'}",qos=0, retain=False)
