from chatbot import bot, model, predict_class
from keep_session import start_keep_session
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
import re
from unicodedata import normalize
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


filepath = "./whatsapp_session.txt"
#driver = webdriver.Edge()


def crear_driver_session():

    with open(filepath) as fp:
        for cnt, line in enumerate(fp):
            if cnt == 0:
                executor_url = line
            if cnt == 1:
                session_id = line

    def new_command_execute(self, command, params=None):
        if command == "newSession":
            return {"success": 0, "value": None, "sessionId": session_id}
        else:
            return org_command_execute(self, command, params)

    org_command_execute = RemoteWebDriver.execute

    RemoteWebDriver.execute = new_command_execute

    new_driver = webdriver.Remote(
        command_executor=executor_url, desired_capabilities={})
    new_driver.session_id = session_id

    RemoteWebDriver.execute = org_command_execute

    return new_driver


driver = crear_driver_session()


def checkMensajes(chat):
    try:
        numMes = chat.find_element(By.CLASS_NAME, "_1pJ9J").text

        msleer = re.findall("\d+", numMes)

        if len(msleer) != 0:
            pending = True

        else:
            pending = False

    except:
        pending = False
    return pending


def buscar_chats():
    print("BUSCANDO CHATS")

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "_1RAKT")))

        print(len(driver.find_elements(By.CLASS_NAME, "_1RAKT")))
        if len(driver.find_elements(By.CLASS_NAME, "zaKsw")) == 0:

            print("CHAT ABIERTO")
            message = identificar_mensaje()

            if message != None:
                return True
        else:

            chats = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "_1Oe6M")))
            for chat in chats:
                print("DETECTANDO CHATS")
                print("mensajes sin leer:", len(chats))

                porresponder = checkMensajes(chat)
                if porresponder:
                    chat.click()
                    sleep(2)
                    return True
                else:
                    print("CHATS ATENDIDOS")
                    continue
        return False
    except TimeoutError:
        print("Timed out waiting for element to appear")


def normalizar(message: str):
    message = re.sub(
        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1",
        normalize("NFD", message), 0, re.I
    )
    return normalize('NFC', message)


def identificar_mensaje():
    print("Entro a identificar mensaje")
    element_box_message = driver.find_elements(By.CLASS_NAME, "_27K43")
    print("mensajes:", element_box_message)
    posicion = len(element_box_message) - 1
    print("posicion", posicion)
    element_message = element_box_message[posicion].find_elements(
        By.CLASS_NAME, "_21Ahp")
    print("mensaje luego de la caja: ", element_message)
    message = element_message[0].text.lower().strip()
    print("MENSAJE RECIBIDO:", message)
    return normalizar(message)


def preparar_respuestas(message: str):
    print("PREPARANDO RESPUESTA")
    response = bot(message)
    return response


hours = pd.date_range(start='8:00am', end='5:00pm', freq='H')
citas_df = pd.DataFrame(index=hours, columns=['Nombres'])


def guardar_cita(info):
    for i in citas_df.index:
        if pd.isnull(citas_df.at[i, 'Nombres']):
            citas_df.at[i, 'Nombres'] = info
            break
    citas_df.to_excel('Citas.xlsx')
    for i in reversed(citas_df.index):
        if not pd.isnull(citas_df.at[i, 'Nombres']):
            hora_asignada = i
            break

    message = 'Su cita ha sido programada, la hora que se le asigno es: {}'.format(
        hora_asignada.strftime('%H:%M %p'))
    return message


def procesar_mensaje(message: str):
    chatbox = driver.find_element(
        By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')
    ints = predict_class(message, model)
    message = identificar_mensaje()
    if ints[0]["intent"] == "citas":
        chatbox = driver.find_element(
            By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')
        chatbox.send_keys(
            "Por favor, ingrese su nombre completo para agendarle una cita", Keys.ENTER)
        sleep(30)
        message = identificar_mensaje()
        if (message == 'por favor, ingrese su nombre completo para agendarle una cita'):
            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        else:
            response = guardar_cita(message)
            chatbox = driver.find_element(
                By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')
            chatbox.send_keys(response, Keys.ENTER)
            sleep(2)
            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    else:
        response = preparar_respuestas(message)
        chatbox = driver.find_element(
            By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')
        chatbox.send_keys(response, Keys.ENTER)
        sleep(2)
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()


def whatsapp_bot_init():
    global driver
    driver = crear_driver_session()

    esperando = 1

    while esperando == 1:
        esperando = len(driver.find_elements(By.CLASS_NAME, "_1meIt"))
        sleep(5)
        print("waiting logging:", esperando)

    while True:
        if not buscar_chats():
            sleep(5)
            continue

        message = identificar_mensaje()

        if message == None:
            continue
        else:
            procesar_mensaje(message)


# ______________________________________________MAIN_________________________________________

if __name__ == "__main__":
    start_keep_session()
    sleep(4)
    whatsapp_bot_init()
