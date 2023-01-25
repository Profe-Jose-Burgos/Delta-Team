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
                "responses":["Para obtener información detallada acerca del pago de impuestos, por favor visita nuestra página https://www.samsung.com/latin/support/"
                             ]
                },

                {"tag": "cotizar",
                "patterns": ["cotizar",
                             "cotizaciones",
                             "costos",
                             "tarifa"
                             ],
                "responses":["Para obtener información detallada acerca de las cotizaciones, por favor visita nuestra página https://shop.samsung.com/latin//"
                             ]
                },

                {"tag": "factura",
                "patterns": ["factura",
                             "recibo",
                             "invoice"
                             ],
                "responses":["Las facturas detalladas de aranceles e impuestos se proporcionan con su (s) paquete (s) en el momento de la entrega."
                             ]
                },

                 {"tag": "airBill",
                "patterns": ["que guia aerea",
                             "air waybill",
                             ],
                "responses":["La guía aérea o airway bill, es el documento que funge como contrato de transporte aéreo ante una carga."
                             ]
                },

                {"tag": "incoterms",
                "patterns": ["que es incoterm",
                            "incoterm",
                            "incoterms"
                             ],
                "responses":["Son los Términos Internacionales de Comercio (INCOTERMS). Los emite la Cámara de Comercio Internacional que determinan el alcance comercial en el contrato de compraventa internacional."
                             ]
                },

                {"tag": "cambiarEntrega",
                "patterns": ["cambiar entrega",
                             "programar fecha",
                             ],
                "responses":["La guía aérea o airway bill, es el documento que funge como contrato de transporte aéreo ante una carga."
                             ]
                },

                {"tag": "citas",
                "patterns": ["cita",
                             "asesoria",
                             "reunion agente",
                             "atencion empleado",
                             "reunion colaborador",
                             "agendame una cita",
                             "conversar con colaborador"
                            ],
                    
                "responses":["Por favor, ingrese su nombre para agendarle una cita"]
                },
               
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
                "responses":["No soy capaz de responder al mensaje anterior, ¿podría hacerme otra pregunta más específica?"
                             ]
                }

            ]
    }

    save_json(library)




#_____________________main___________

if __name__ == "__main__":
    start_intents()
