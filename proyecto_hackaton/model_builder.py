import json 
import pickle
import numpy as np
import nltk
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import Conv2D, Flatten, Dense, Dropout
from tensorflow.python.keras.optimizers import gradient_descent_v2 #SGD, fue la unica forma de importarlo 
from nltk.stem import SnowballStemmer


stemmer = SnowballStemmer("spanish")

ignored_words = ["? ¿ ! ¡ , % # "]
data_file = open("intent.json").read()
intents = json.loads(data_file)

#tokenizar

def tokenizer():
    words = []
    classes = []
    documents = []

    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            w = nltk.word_tokenize(pattern)
            words.extend(w)

            documents.append((w,intent["tag"]))

            if intent["tag"] not in classes:
                classes.append(intent["tag"])
    
    return words, classes, documents

    #lematizador


def lematizer(words,classes,documents):
    words = [stemmer.stem(w.lower()) for w in words if w not in ignored_words]
    words2 = words
    print("words after lematizing: ", len(words))

    pickle.dump(words, open("words.pkl", "wb"))

    pickle.dump(words,open("words.pkl", "wb"))
    pickle.dump(classes, open("classes.pkl", "wb"))

    return words2


    ################  preprocessing###############


def training(words, classes, documents):
    training = []
    output_empty = [0]*len(classes)

    for doc in documents:
        bag = []
        pattern_words = doc[0]
        pattern_words = [stemmer.stem(word.lower()) for word in pattern_words if word not in ignored_words]

        for palabra in words:
            bag.append(1) if palabra in pattern_words else bag.append(0)

        output_row = list(output_empty)
        output_row[classes.index(doc[1])] = 1
        training.append([bag, output_row])
    
    training = np.array(training)

    x_train = list(training[:,0])
    y_train = list(training[:,1])

    return x_train, y_train



#################### creacion del modelo #####################

def model_builder(x_train, y_train):
    model = Sequential()
    model.add(Dense(600, input_shape = (len(x_train[0]),), activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(520, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(len(y_train[0]), activation = "softmax"))

    sgd = gradient_descent_v2.SGD(learning_rate=0.01, decay=1e-6, momentum =0.9, nesterov= True)

    model.compile(loss ="categorical_crossentropy", optimizer =sgd, metrics = ["accuracy"])

    hist = model.fit(np.array(x_train), np.array(y_train), epochs = 1300, batch_size=5, verbose=1)
    model.save("chatbot_model.h5", hist)
    print("done")

def start_model():
    words, classes, documents = tokenizer()
    words2 = lematizer(words, classes, documents)
    x_train, y_train = training(words2, classes, documents)
    model_builder(x_train,y_train)


##################### Main #####################

from intents import start_intents

if __name__== "__main__":
    start_intents()
    start_model()



