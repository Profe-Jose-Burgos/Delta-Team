from model_builder import start_model
from intents import start_intents
from time import sleep
import pandas as pd
import nltk
import json
import pickle
import numpy as np
import random
from nltk.stem import SnowballStemmer
from tensorflow.python.keras.models import load_model


stemmer = SnowballStemmer("spanish")

model = load_model("chatbot_model.h5")
intents = json.loads(open("intent.json").read())
words = pickle.load(open("words.pkl", "rb"))
classes = pickle.load(open("classes.pkl", "rb"))


# Aqui se tokeniza y se lematizan las palabras
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words


# Aqui se compara lo que ingreso el usuario ya tokenizado con la referencia
def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for i in sentence_words:
        for j, w in enumerate(words):
            if w == i:
                bag[j] = 1
                if show_details:
                    print("encontrado en la bolsa: ", w)
    return (np.array(bag))


# Para predeccir el modelo
def predict_class(sentence, model):
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    error_threshold = 0.25

    results = []
    for i, j in enumerate(res):
        if j > error_threshold:
            results.append([i, j])
    # else:
    #   return "No entendí tu pregunta o inquietud, ¿podría usted ser más específico"

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for i in results:
        return_list.append({"intent": classes[i[0]], "probability": str(i[1])})
    print("return list: ", return_list)
    return return_list


# Obtenemos respuestas
def get_responses(ints, intents_json):
    tag = ints[0]["intent"]
    list_of_intents = intents_json["intents"]
    for i in list_of_intents:
        if (i["tag"] == tag):
            result = random.choice(i["responses"])
            break
    return result


def chatbot_response(text):
    ints = predict_class(text, model)
    if type(ints) == type("string"):
        res = ints
    else:
        res = get_responses(ints, intents)
    return res


# Las siguientes funcion solamente es para probarla en consola
def start_bot():
    user_text = ''
    print('Prueba en consola, para salir escriba salir')
    while user_text != 'salir':
        user_text = input()
        print(chatbot_response(user_text))


def bot(user_text):
    # start_chatbot() #PRUEBA EN CONSOLA
    res = chatbot_response(user_text)
    return res


def start_chatbot():
    start_intents()
    start_model()
    # start_bot() #PRUEBA EN CONSOLA

# Y esto es ya para ejecutarlo en consola-----------------------
# if __name__ == '__main__':
#     start_bot()
