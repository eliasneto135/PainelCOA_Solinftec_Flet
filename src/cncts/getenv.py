import os
import sys
from os import getenv
from dotenv import load_dotenv

if getattr(sys, 'frozen', False):  # Se estiver rodando como executável
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(__file__)

dotenv_path = os.path.join(base_dir, ".env")
load_dotenv(dotenv_path)

IP_API_LIBERALI = getenv("IP_API_LIBERALI")
URL_FIREBASE = getenv("URL_FIREBASE")
AUTH_API_LIBERALI = getenv("AUTH_API_LIBERALI")
URL_DB_SQLITE = getenv("URL_DB_SQLITE")
URL_AUTH_SOLINFTEC = getenv('URL_AUTH_SOLINFTEC')
PW_API_SOLINFTEC = getenv('PW_API_SOLINFTEC')
USER_API_SOLINFTEC = getenv('USER_API_SOLINFTEC')
URL_LIST_EQPM = getenv('URL_LIST_EQPM')
ORIN_REF1 = getenv('ORIN_REF1')
URL_INFO_EQPM = getenv('URL_INFO_EQPM')
ORIN_REF_2 = getenv('ORIN_REF_2')
URL_COMANDO_ONLINE_SOLINFTEC = getenv('URL_COMANDO_ONLINE_SOLINFTEC')
URL_AUTHORITY_SOLINFTEC = getenv('URL_AUTHORITY_SOLINFTEC')
URL_PROJECT_FIREBASE = getenv('URL_PROJECT_FIREBASE')
URL_INT_SOLINFTEC = getenv('URL_INT_SOLINFTEC')
URL_LOGIN_API_ZEUS = getenv('URL_LOGIN_API_ZEUS')
EMAIL_LOGIN_API_ZEUS = getenv('EMAIL_LOGIN_API_ZEUS')
PW_LOGIN_API_ZEUS = getenv('PW_LOGIN_API_ZEUS')

NEW_URL_AUTH_SOLINFTEC = getenv('NEW_URL_AUTH_SOLINFTEC')
NEW_URL_INT_SOLINFTEC = getenv('NEW_URL_INT_SOLINFTEC')

AUTH_FIREBASE = getenv('AUTH_FIREBASE')
