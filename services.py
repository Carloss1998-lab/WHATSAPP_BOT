import requests
import sett
import json
import time
import base64
import io
import os
from datetime import datetime 
from PIL import Image
from flask import  url_for


def decode_and_show(image,path):
    image_data = base64.b64decode(image.encode())
    image = Image.open(io.BytesIO(image_data))
    filename = f"generated_image_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    image_path = os.path.join(path, filename)
    image.save(image_path)
    image_url = f'/generated_files/{filename}'
    print("image_url")
    print(image_url)
    return image_url

    
def obtener_Mensaje_whatsapp(message):
    if 'type' not in message :
        text = 'mensaje no reconocido'
        return text

    typeMessage = message['type']
    if typeMessage == 'text':
        text = message['text']['body']
    elif typeMessage == 'button':
        text = message['button']['text']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply':
        text = message['interactive']['list_reply']['title']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text = message['interactive']['button_reply']['title']
    else:
        text = 'mensaje no procesado'
    
    
    return text

def enviar_Mensaje_whatsapp(data):
    print("Envoie du message")
    try:
        whatsapp_token = sett.whatsapp_token
        whatsapp_url = sett.whatsapp_url
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer ' + whatsapp_token}
        print("se envia ", data)
        response = requests.post(whatsapp_url, 
                                 headers=headers, 
                                 data=data)
        
        print("response.status_coderesponse.status_coderesponse.status_coderesponse.status_code")
        print(response.status_code)
        if response.status_code == 200:
            return 'mensaje enviado', 200
        else:
            return 'error al enviar mensaje', response.status_code
    except Exception as e:
        print("errrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
        return e,403
    
def text_Message(number,text):
    data = json.dumps(
            {
                "messaging_product": "whatsapp",    
                "recipient_type": "individual",
                "to": number,
                "type": "text",
                "text": {
                    "body": text
                }
            }
    )
    return data

def text_Message(number,text):
    data = json.dumps(
            {
                "messaging_product": "whatsapp",    
                "recipient_type": "individual",
                "to": number,
                "type": "text",
                "text": {
                    "body": text
                }
            }
    )
    return data

def buttonReply_Message(number, options, body, footer, sedd,messageId):
    buttons = []
    for i, option in enumerate(options):
        buttons.append(
            {
                "type": "reply",
                "reply": {
                    "id": sedd + "_btn_" + str(i+1),
                    "title": option
                }
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "buttons": buttons
                }
            }
        }
    )
    return data

def listReply_Message(number, options, body, footer, sedd,messageId):
    rows = []
    for i, option in enumerate(options):
        print("i")
        print(i)
        print(option)
        
        rows.append(
            {
                "id": sedd + "_row_" + str(i+1),
                "title": option,
                "description": ""
            }
        )
    print("rows")
    print(rows)
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "button": "Voir les options",
                    "sections": [
                        {
                            "title": "section",
                            "rows": rows
                        }
                    ]
                }
            }
        }
    )
    return data

def document_Message(number, url, caption, filename):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "document",
            "document": {
                "link": url,
                "caption": caption,
                "filename": filename
            }
        }
    )
    return data

def sticker_Message(number, sticker_id):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "sticker",
            "sticker": {
                "id": sticker_id
            }
        }
    )
    return data

def image_Message(number,image_uri):
    
    link = url_for('serve_generated_image', filename=image_uri, _external=True)
    print("linklinklinklinklink")
    print(link)
    # data = json.dumps(
    #     {
    #         "messaging_product": "whatsapp",
    #         "recipient_type": "individual",
    #         "to": number,
    #         "type": "image",
    #         "image": {
    #               "link": link
    #         }
    #     }
    # )
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "context": { "message_id": messageId },
            "type": "text",
            "text": {
                "body": link
            }
        }
    )
    # https://botsimple.vercel.app/static/Image/image.jpg
    return data



def get_media_id(media_name , media_type):
    media_id = ""
    if media_type == "sticker":
        media_id = sett.stickers.get(media_name, None)
    #elif media_type == "image":
    #    media_id = sett.images.get(media_name, None)
    #elif media_type == "video":
    #    media_id = sett.videos.get(media_name, None)
    #elif media_type == "audio":
    #    media_id = sett.audio.get(media_name, None)
    return media_id

def replyReaction_Message(number, messageId, emoji):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "reaction",
            "reaction": {
                "message_id": messageId,
                "emoji": emoji
            }
        }
    )
    return data

def replyText_Message(number, messageId, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "context": { "message_id": messageId },
            "type": "text",
            "text": {
                "body": text
            }
        }
    )
    return data

def markRead_Message(messageId):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id":  messageId
        }
    )
    return data

def administrar_chatbot(text,number, messageId, name, path, domain):
    print("administrar_chatbot pathhhhhhhhhhhhhhhh")
    print(path)
    text = text.lower() #mensaje que envio el usuario
    list = []
    markRead = markRead_Message(messageId)
    list.append(markRead)
    if "hola" in text or "model" in text or "hello" in text or "bonjour" in text or "bonsoir" in text:
        body = "Bonjour! 👋 Veuillez choisi une option?"
        footer = "Reply Bot"
        options = ["✅ Nos services", "📅 Contact"]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed1",messageId)
        replyReaction = replyReaction_Message(number, messageId, "🫡")
        list.append(replyReaction)
        list.append(replyButtonData)
    elif "servicios" in text:
        body = "Tenemos varias áreas de consulta para elegir. ¿Cuál de estos servicios te gustaría explorar?"
        footer = "Equipo Bigdateros"
        options = ["Analítica Avanzada", "Migración Cloud", "Inteligencia de Negocio"]

        listReplyData = listReply_Message(number, options, body, footer, "sed2",messageId)
        sticker = sticker_Message(number, get_media_id("perro_traje", "sticker"))

        list.append(listReplyData)
        list.append(sticker)    
    elif "service" in text:
        body = "Voici nos services?"
        footer = "Reply Bot"
        options = ["Generation de texte", "Generation d'image", "Bedrock, pas disponible"]
        
        listReplyData = listReply_Message(number, options, body, footer, "sed9",messageId)
        sticker = sticker_Message(number, get_media_id("perro_traje", "sticker"))

        list.append(listReplyData)
        list.append(sticker) 
    elif "generation de texte" in text:
        print("allllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll")
        body = "Bonjour. Je suis le bot Tom, que puis-je pour vous?"
        footer = "Reply Bot"
        options = ["Tom, what's a green card","Tom, capital France","Tom, What is AI"]

        listReplyData = listReply_Message(number, options, body, footer, "sed10",messageId)
        sticker = sticker_Message(number, get_media_id("perro_traje", "sticker"))

        list.append(listReplyData)
        list.append(sticker)  
    elif "generation d'image" in text:
        body = "Bonjour. Je suis le bot Jerry, que puis-je pour vous?"
        footer = "Reply Bot"
        options = ["Jerry, Draw a boys","Jerry, a computer","Jerry, panda eating"]

        listReplyData = listReply_Message(number, options, body, footer, "sed14",messageId)
        sticker = sticker_Message(number, get_media_id("perro_traje", "sticker"))

        list.append(listReplyData)
        list.append(sticker) 
           
    elif "tom" in text:
        api_url = sett.model_api_url
        data = {
            "system": "you're a conversational agent, give quick and clear answers to any questions you may have. Answer in the same language as the question.",
            "user": text.replace("tom", "").replace(':',"")
        }
        json_data = json.dumps(data)
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(api_url, data=json_data, headers=headers)
        if response.status_code == 200:
            print(response.json())
            data = text_Message(number,response.json())
            list.append(data)
        else:
            data = text_Message(number,response.status_code)
            list.append(data)
    elif "jerry" in text:
        # L'URL de l'API Gateway
        api_url =  sett.stable_api_url
        data = {
            "prompt": text.replace("jerry", "").replace(':',"")
        }
        json_data = json.dumps(data)
        headers = {
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(api_url, data=json_data, headers=headers)
            data = text_Message(number,"Veuillez commencer votre message par Tom : ou Jerry : pour designer le bot")
            image_uri = decode_and_show(response.text, path)
            image = image_Message(number,image_uri)
            list.append(image)

        except requests.exceptions.RequestException as e:
            # Gérer les erreurs de requête
            print(f"Une erreur de requête s'est produite : {str(e)}")
    else :
        data = text_Message(number,"Veuillez commencer votre message par Tom : ou Jerry : pour designer le bot")
        list.append(data)

    for item in list:
        print(item)
        enviar_Mensaje_whatsapp(item)

#al parecer para mexico, whatsapp agrega 521 como prefijo en lugar de 52,
# este codigo soluciona ese inconveniente.
def replace_start(s):
    if s.startswith("521"):
        return "52" + s[3:]
    else:
        return s

# para argentina
def replace_start(s):
    if s.startswith("549"):
        return "54" + s[3:]
    else:
        return s
