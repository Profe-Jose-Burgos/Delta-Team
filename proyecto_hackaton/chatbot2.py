import nltk, json, pickle, numpy, random
from nltk.stem import SnowballStemmer
from tensorflow.python.keras.models import load_model

stemmer = SnowballStemmer('spanish')

# Cargamos los archivos para trabajar con el chatbot
model = load_model('chatbot_model.h5')
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('words.pkl', 'rb'))

def clean_sentence(sentence): #Primera funcion para "tokenizar" y "lematizar" las palabras que introduzca el usuario
    sentence_words = nltk.word_tokenize(sentence) #Aqui se tokeniza
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words] #Aqui se lematizan 
    return sentence_words

def bow(sentence, words, show_details=True): 
    sentence_words = clean_sentence(sentence)
    bag = [0] * len(words)
    for i in sentence_words:
        for j, w in enumerate(words):
            if w == i:
                bag[j] = 1
                # if show_details:
                #     print(w)
    return (numpy.array(bag))

def predict_class(sentence, model):
    p = bow(sentence, words, show_details=True)
    res = model.predict(numpy.array([p]))[0]
    error_threshold = 0.25
    results = [[i, r] for i, r in enumerate(res) if r>error_threshold]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'inetnt' : classes[r[0]], 'probability' : str(r[1])})
    return return_list

def get_response(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if (i['tag'] == tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(text):
    ints = predict_class(text, model)
    res = get_response(ints, intents)
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

def start_chatbot():
    start_intents()
    start_model()
    #start_bot() #PRUEBA EN CONSOLA

# Y esto es ya para ejecutarlo en consola-----------------------
# if __name__ == '__main__':
#     start_bot()
# Hasta aqui ---------------------------------------------------


