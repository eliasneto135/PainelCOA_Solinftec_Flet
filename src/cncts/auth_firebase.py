import os

import firebase_admin
from firebase_admin import credentials, firestore
import bcrypt
from src.cncts.getenv import URL_PROJECT_FIREBASE, AUTH_FIREBASE

print(os.path.abspath(f'{AUTH_FIREBASE}'))

# cred = credentials.Certificate(os.path.abspath(f'{AUTH_FIREBASE}'))
cred = credentials.Certificate(f'{AUTH_FIREBASE}')
firebase_admin.initialize_app(cred)
db = firestore.client()

def hash_senha(senha):
    salt = bcrypt.gensalt()
    senha_criptografada = bcrypt.hashpw(senha.encode('utf-8'), salt)
    print(senha_criptografada)
    return senha_criptografada.decode('utf-8')

def verificar_senha(senha, senha_criptografada):
    return bcrypt.checkpw(senha.encode('utf-8'), senha_criptografada.encode('utf-8'))

def registrar_usuario(nome_usuario, senha):
    senha_hash = hash_senha(senha)
    usuario_ref = db.collection("usuarios").document(nome_usuario)
    usuario_ref.set({"senha": senha_hash})

def alterar_senha(nome_usuario, senha):
    senha_hash = hash_senha(senha)
    usuario_ref = db.collection("usuarios").document(nome_usuario)
    usuario_ref.set({"senha": senha_hash})

def autenticar_usuario(nome_usuario, senha):
    usuario_ref = db.collection("usuarios").document(nome_usuario)
    usuario = usuario_ref.get()

    if usuario.exists:
        senha_hash = usuario.to_dict().get("senha")
        return verificar_senha(senha, senha_hash)
    else:
        return False

def registrar_log(nome_usuario, datahora):
    try:
        doc_ref = db.collection("log").document()  # para gerar um id automatico.
        doc_ref.set({"usuario": nome_usuario, "datahora": f"{datahora}"})
        print(f"Document added with ID: {doc_ref.id}")
    except Exception as e:
        print(f"Error adding document: {e}")

def post_param(frota):
    doc_ref = db.collection("parametros").document(frota)
    frota_param = doc_ref.get()

    if frota_param.exists:
        json_param_frota = {
            "frota": frota_param.to_dict().get("frota"),
            "id_firebase": frota_param.to_dict().get("frota"),
            "alertas": {
                'alrt_frota': frota_param.to_dict().get("alrt_frota"),
                'alrt_talhao':  frota_param.to_dict().get('alrt_talhao'),
                'alrt_veloc':  frota_param.to_dict().get('alrt_veloc'),
                'alrt_rpm':  frota_param.to_dict().get('alrt_rpm'),
                'alrt_temp':  frota_param.to_dict().get('alrt_temp'),
                'alrt_rt':  frota_param.to_dict().get('alrt_rt'),
                'alrt_oper':  frota_param.to_dict().get('alrt_oper'),
                'alrt_implem':  frota_param.to_dict().get('alrt_implem'),
                'alrt_op':  frota_param.to_dict().get('alrt_op')
            },
            "parametros": {
                'param_veloc':  frota_param.to_dict().get('param_veloc'),
                'param_rpm':  frota_param.to_dict().get('param_rpm'),
                'param_temp':  frota_param.to_dict().get('param_temp')
            }
        }
    else:
        try:
            doc_ref = db.collection("parametros").document(f"{frota}")  # para gerar um id automatico.
            doc_ref.set({'frota': frota,
                 'alrt_frota': True,
                 'alrt_talhao': True,
                 'alrt_veloc': True,
                 'alrt_rpm': True,
                 'alrt_temp': True,
                 'alrt_rt': True,
                 'alrt_oper': True,
                 'alrt_implem': True,
                 'alrt_op': True,
                 'param_veloc': 3,
                 'param_rpm': 2100,
                 'param_temp': 103
            })
            print(f"Document added with ID: {doc_ref.id}")
            doc_ref = db.collection("parametros").document(frota)
            frota_param = doc_ref.get()
            json_param_frota = {
                "frota": frota_param.to_dict().get("frota"),
                "id_firebase": frota_param.to_dict().get("frota"),
                "alertas": {
                    'alrt_frota': frota_param.to_dict().get("alrt_frota"),
                    'alrt_talhao': frota_param.to_dict().get('alrt_talhao'),
                    'alrt_veloc': frota_param.to_dict().get('alrt_veloc'),
                    'alrt_rpm': frota_param.to_dict().get('alrt_rpm'),
                    'alrt_temp': frota_param.to_dict().get('alrt_temp'),
                    'alrt_rt': frota_param.to_dict().get('alrt_rt'),
                    'alrt_oper': frota_param.to_dict().get('alrt_oper'),
                    'alrt_implem': frota_param.to_dict().get('alrt_implem'),
                    'alrt_op': frota_param.to_dict().get('alrt_op')
                },
                "parametros": {
                    'param_veloc': frota_param.to_dict().get('param_veloc'),
                    'param_rpm': frota_param.to_dict().get('param_rpm'),
                    'param_temp': frota_param.to_dict().get('param_temp')
                }
            }
        except Exception as e:
            print(f"Error adding document: {e}")
    return json_param_frota


def edit_param(frota, dados):
    print(frota, dados)
    doc_ref = db.collection("parametros").document(frota)
    frota_param = doc_ref.get()
    if frota_param.exists:
        try:
            doc_ref = db.collection("parametros").document(f"{frota}")  # para gerar um id automatico.
            doc_ref.set(dados)
        except Exception as e:
            print(f"Error adding document: {e}")