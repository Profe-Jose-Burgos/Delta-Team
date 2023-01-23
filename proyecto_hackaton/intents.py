import json

def save_json(datos):
    data_file = open("intent.json", "w")
    json.dump(datos, data_file, indent = 4)


def start_intents():

    library = {"intents":
            [
                {"tag": "saludos",
                "patterns": ["hola",
                             "buenos dias",
                             "buenas tardes",
                             "buenas noches",
                             "como estas",
                             "hay alguien ahi?",
                             "hey",
                             "saludos",
                             "que tal"
                             ],
                "responses":["hola soy HCK-Bot , tu asistente virtual universitario, ¿en que puedo ayudarte?"
                             ]
                },

                {"tag":"despedidas",
                 "patterns":["chao",
                             "adios",
                             "hasta luego",
                             "nos vemos",
                             "bye",
                             "hasta pronto",
                             "hasta la proxima"
                             ],
                 "responses":["hasta luego, tenga un buen dia",
                 "ha sido un placer, vuelva pronto"
                             ]
                 },            
                
               {"tag": "agradecimientos",
                "patterns": ["gracias",
                             "muchas gracias",
                             "mil gracias",
                             "muy amable",
                             "se lo agradezco",
                             "fue de ayuda",
                             "gracias por la ayuda",
                             "muy agradecido",
                             "   gracias por su tiempo",
                             "ty"
                             ],
                "responses":["de nada",
                             "feliz por ayudarlo",
                             "gracias a usted",
                             "estamos para servirle",
                             "fue un placer"
                             ]
                },
               {"tag": "norespuesta",
                "patterns": [""],
                "responses":["no se detecto una respuesta"
                             ]
                }

            ]
    }

    save_json(library)




#_____________________main___________

if __name__ == "__main__":
    start_intents()
