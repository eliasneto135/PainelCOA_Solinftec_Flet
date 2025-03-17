import os

import firebase_admin
from firebase_admin import credentials, firestore
import bcrypt
from src.cncts.getenv import URL_PROJECT_FIREBASE, AUTH_FIREBASE

print(os.path.abspath(f'{AUTH_FIREBASE}'))

cred = credentials.Certificate(os.path.abspath(f'{AUTH_FIREBASE}'))
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
