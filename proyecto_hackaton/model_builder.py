import nltk, json, pickle
import numpy as np
import random 
from nltk.stem import SnowballStemmer
from tensorflow.python.keras.models import load_model


stemmer = SnowballStemmer("Spanish")

model = load_model("chatbot_model.h.5")
intents = json.loads(open("intent.json").read())
words = pickle.load(open("words:pkl","rb"))
classes = pickle.load(open("classes.pkl","rb"))


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [stemmer.stem(word.lowe() for word in sentence_words)]
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
        if j > error_threshold>
        results.append([i,j])
    #else:
    #   return "No entendí tu pregunta o inquietud, ¿podría usted ser más específico"

    results.sort (key=lambda x:x[1], reverse = True)
    return_list = []
    for i in results:
        return_list.append({"intent": classes[i[0]], "probability": str(i[1])})
    print("return list: ", return_list)
    return return_list

def get_responses(ints, intents_json):
    tag = ints[0]["intent"]
    list_of_intents = intents_json["intents"]
    for i in list_of_intents:
        if (i["tag"]==tag):
            result = random.choice(i["responses"])
            break
    return result

def chatbot_response(text):
    ints = predict_class(text,model)
    if type(ints) == type("string"):
        res = ints
    else :
        res = get_responses(ints,intents)
    return res

######### probar en consola ########
def start_bot():
    texto_us=""
    print('Bienvenido, para dejar el chat, escriba "salir"')
    while texto_us != "salir":
        texto_us = input()
        res = chatbot_response(texto_us)
        print(res)

def start_chatbot():
    start_intents()
    start_model()
    start_bot()  #consola


from intents import start_intents
from model_builder import start_model

if __name__ == "__main__":


    #start_chatbot()
    start_bot()


    # para ingresas con whatsapp
    #answer = bot(texto_us)





