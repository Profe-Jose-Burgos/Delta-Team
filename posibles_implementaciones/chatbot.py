from time import sleep

import nltk, json, pickle
import numpy as np
import random
from nltk.stem import SnowballStemmer
from tensorflow.python.keras.models import load_model
import pandas as pd

stemmer = SnowballStemmer("spanish")

model = load_model("chatbot_model.h5")
intents = json.loads(open("intent.json").read())
words = pickle.load(open("words.pkl","rb"))
classes = pickle.load(open("classes.pkl","rb"))


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for i in sentence_words:
        for j, w in enumerate(words):
            if w == i:
                bag[j] = 1
                if show_details:
                    print("encontrado en la bolsa: ",w)
    return (np.array(bag))

def predict_class(sentence,model):
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    error_threshold = 0.25

    results = []
    for i,j in enumerate(res):
        if j > error_threshold:
            results.append([i,j])
    #else:
    #   return "No entendí tu pregunta o inquietud, ¿podría usted ser más específico"

    results.sort (key=lambda x:x[1], reverse = True)
    return_list = []
    for i in results:
        return_list.append({"intent": classes[i[0]], "probability": str(i[1])})
    print("return list: ", return_list)
    return return_list


#ORIGINAL
# def get_responses(ints, intents_json):
#     tag = ints[0]["intent"]
#     list_of_intents = intents_json["intents"]
#     for i in list_of_intents:
#         if (i["tag"] == tag):
#             result = random.choice(i["responses"])
#             break
#     return result


def get_responses(ints, intents_json):
    tag = ints[0]["intent"]
    list_of_intents = intents_json["intents"]
    result = random.choice([i["responses"] for i in list_of_intents if i["tag"]==tag][0])
    if (tag == 'citas'):
        info = wait_cita() #PARA JURADOS LINEA 74
        result = guardar_cita(info)
    return result

#Aqui lo que intente hacer fue que para realizar una cita poder evitar que se saliera de la conversacion, 
# para que pudiera leer el nombre y poder guardarlo en un archivo excel (la funcion que esta aqui abajo)
# Pero no me funciono, les dejo saber mi problema, gracias por su atencion, intente bastantes veces,
# pero el tiempo no me dio, si me pudieran apoyar seria magnifico, gracias

def guardar_cita(info):
    df = pd.DataFrame(columns=['Nombres'])
    hours = pd.date_range(start='8:00am', end='5:00pm', freq='H')
    df.set_index(hours, inplace=True)
    for i in df.index:
        if pd.isnull(df.at[i, 'Nombres']):
            df.at[i, 'Nombres'] = info
            break
        df.to_excel('Citas.xlsx')

    for i in reversed(df.index):
        if not pd.isnull(df.at[i, 'Nombres']):
            hora_asignada = i
            break
        
    message = 'Su cita ha sido programada, la hora que se le asigno es: ', hora_asignada
    return message



def chatbot_response(text):
    ints = predict_class(text,model)
    if type(ints) == type("string"):
        res = ints
    else :
        res = get_responses(ints,intents)
    return res

# Las siguientes funcion solamente es para probarla en consola ------------------------------
def start_bot():
    user_text = ''
    print('Prueba en consola, para salir escriba salir')
    while user_text != 'salir':
        user_text = input()
        print(chatbot_response(user_text))

def bot(user_text):
    #start_chatbot() #PRUEBA EN CONSOLA
    res = chatbot_response(user_text)
    return res

#hasta aqui ----------------------------------------------------------------------------------

from intents import start_intents
from model_builder import start_model
from MAIN import wait_cita

def start_chatbot():
    start_intents()
    start_model()
    #start_bot() #PRUEBA EN CONSOLA

# Y esto es ya para ejecutarlo en consola-----------------------
# if __name__ == '__main__':
#     start_bot()
# Hasta aqui ---------------------------------------------------






