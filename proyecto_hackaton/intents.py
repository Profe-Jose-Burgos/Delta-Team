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
                "responses":["¡Hola!, soy SAM-BOT, tu asistente virtual de SIC-Panamá . ¿En que podemos ayudarte?"
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

                 {"tag":"agenteDcarga",
                 "patterns":["que es agente carga",
                             "courier",
                             "PO BOX",
                             "casillero"
                             ],
                 "responses":["un agente de carga es el prestador de servicios especializados que, actuando como principal o tercero entre el usuario y el transportista, desarrolla actividades para solucionar, por cuenta de su cliente o en forma directa, todos los problemas implícitos en el flujo físico de la mercancía.."
                             ]
                 },

                 {"tag": "impuestos",
                "patterns": ["impuestos",
                             "iva",
                             "tax",
                             "taxes"
                             ],
                "responses":["Para obtener información detallada acerca del pago de impuestos, por favor visita nuestra página https://delivery.dhl.com/pa"
                             ]
                },
               {"tag": "norespuesta",
                "patterns": [""],
                "responses":["no se detecto una respuesta"
                             ]
                }

                
               {"tag": "agradecimientos",
                "patterns": ["gracias",
                             "muchas gracias",
                             "mil gracias",
                             "muy amable",
                             "agradezco",
                             "gracias ayuda",
                             "agradecido",
                             "gracias su tiempo",
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
