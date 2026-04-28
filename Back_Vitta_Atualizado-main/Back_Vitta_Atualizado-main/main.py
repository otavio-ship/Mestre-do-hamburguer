import os
import fdb
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True,
     origins=["http://localhost:5173/",
              "http://10.92.3.138:5000"
              "http://10.92.3.138:5173"])


app.config['SECRET_KEY'] = ''

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


try:
    con = fdb.connect(
        host='localhost',
        database=r'C:\Users\Aluno\Downloads\BANCO (1)\BANCO.FDB',
        user='SYSDBA',
        password='sysdba',
        charset='UTF8'
    )
    print("Conexão com Firebird estabelecida com sucesso!")
except Exception as e:
    print(f"Erro ao conectar no banco: {e}")
    con = None


from view import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
