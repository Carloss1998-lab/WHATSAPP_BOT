from flask import Flask, request, url_for,send_from_directory
import sett 
import services
app = Flask(__name__)

GENERATED_FILES_FOLDER = 'generated_files'
app.config['GENERATED_FILES_FOLDER'] = GENERATED_FILES_FOLDER
# app.config['SERVER_NAME'] = 'botsimple-carloss1998-lab.vercel.app'
# app.config['SERVER_NAME'] = '127.0.0.1:5000'
app.config['FORCE_HTTPS'] = True
@app.route('/')
def  home():
    return 'Hello everyone'


@app.route('/bienvenido', methods=['GET'])
def  bienvenido():
    return 'bonjour ici'

@app.route('/webhook', methods=['GET'])
def verificar_token():
    try:
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if token == sett.token and challenge != None:
            return challenge
        else:
            return 'token incorrecto', 403
    except Exception as e:
        return e,403

@app.route('/webhook', methods=['POST'])
def recibir_mensajes():
    try:
        body = request.get_json()
        print(body)
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        number = services.replace_start(message['from'])
        messageId = message['id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        text = services.obtener_Mensaje_whatsapp(message)
        services.administrar_chatbot(text, number,messageId,name,app.config['GENERATED_FILES_FOLDER'])
        return 'enviado'

    except Exception as e:
        return 'no enviado ' + str(e)


@app.route('/<filename>')
def serve_generated_image(filename):
    return send_from_directory(app.config['GENERATED_FILES_FOLDER'], filename)

if __name__ == '__main__':
    app.run()
