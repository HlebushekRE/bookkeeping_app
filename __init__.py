from flask import Flask, request, jsonify, send_file
import mysql.connector
from config import Config
from backend import DatabaseManager
import threading


app = Flask(__name__)
app.config.from_object(Config)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1qazxsw23edcG308:'
app.config['MYSQL_DB'] = 'bookkeeping'

mysql = mysql.connector.connect(host=app.config["MYSQL_HOST"],
                               user=app.config["MYSQL_USER"],
                               password=app.config["MYSQL_PASSWORD"],
                               database=app.config["MYSQL_DB"])



@app.route("/")
def  index ():
    return 'Веб-приложение с Python Flask!'

@app.route("/register", methods=["POST"])
def register():
    db = DatabaseManager()
    db.connect()
    return db.register_user(request.form["name"], request.form["surname"], request.form["login"], request.form["password"])

@app.route("/login", methods=["POST"])
def login():
    db = DatabaseManager()
    db.connect()
    return db.login(request.form["username"], request.form["pasw"])

@app.route("/what_parsing", methods=["POST"])
def what_parsing():
    db = DatabaseManager()
    db.connect()

    print('\n')
    print(request.files["file"], type(request.files["file"]))
    print('\n')
    return db.what_parsing(request.files["file"])

@app.route("/insert_data", methods=["POST"])
def insert_data():
    db = DatabaseManager()
    db.connect()
    return db.insert_data(request.form["ids"], request.form["date"], request.form["name"], request.form["total"], request.form["type_input"])

@app.route("/fetch_data", methods=["POST"])
def fetch_data():
    db = DatabaseManager()
    db.connect()
    print('\n')
    print(request.form["format_filter"])
    print(request.form["first_date"])
    print(request.form["second_date"])
    print('\n')
    return db.fetch_data(request.form["format_filter"], request.form["first_date"], request.form["second_date"])
    
@app.route("/calculations", methods=["POST"])
def calculations():
    db = DatabaseManager()
    db.connect()
    result = db.calculations(request.form["tax"], request.form["first_date"], request.form["second_date"])
    return result









# файл backend.py, соединение с бд
#def connect():

# файл backend.py, отключение соединения с бд
#def close():

# файл main.py, регистрация
#def reg_user(self, *args):
    # вызывает connect(), register_user(), close()

# файл backend.py, Отправка данных на сервер для сохранения
#def register_user(self, name, surname, login, password):
    # использует execute()

# файл main.py, вход в аккаунт
#def login_usr(self, *args):
    # вызывает connect(), login(), close()

# файл backend.py, Отправка данных на сервер для сохранения
#def login(self, username, pasw):
    # использует execute(), возвращает True, если аккаунт существует

# файл main.py, Отправка файла PDF на сервер
#def send_file(self):
    # вызывает connect(), what_parsing(), close(), передаёт файл PDF

# файл backend.py, получает PDF файл, работает с ним
#def what_parsing(self, link):
    # в зависимости от встроенных условий, либо вызывает parsing_primorye(), либо parsing_sber(), передаёт PDF файл туда

# файл backend.py, получает PDF файл для парсинга
#def parsing_primorye(self, link):
    # Большой алгоритм, использует различные функции, в том числе execute для записи в бд

# файл backend.py, получает PDF файл для парсинга
#def parsing_sber(self, link):
    # Большой алгоритм, использует различные функции, в том числе execute для записи в бд

# файл main.py, Отправка запроса в файл backend.py для получения данных из бд
#def print_results(self):
    # вызывает connect(), calculations(), close(), передаёт данные для запроса и принимает обратно для вывода

# файл backend.py, Принимает данные и возвращает данные 
#def calculations(self, tax, first_date, second_date):
    # Принимает данные для запроса, проводит запрос к бд для получения данных, проводит расчёты, возвращает данные

# файл main.py, Отправка запроса в файл backend.py для получения данных(другие) из бд
#def print_table(self):
    # Отправляет данные для запроса, вызывает connect(), fetch_data(), close()

# файл backend.py, отправка select запроса к бд, возврат данных
#def fetch_data(self, format_filter, first_date, second_date):
    # Принимает данные, работает с ними используя функции из класса, отправляет новые данные назад

# файл main.py, Отправка данных на сервер для сохранения
#def manual_input(self):
    # вызывает connect(), insert_data(), close(), для записи в бд

# файл backend.py, Отправка данных на сервер для сохранения
#def insert_data(self, ids, date, name, total, type_input):
    # Принимает данные, вызывает функции из своего класса на сервере, записывает полученные данные в бд








def run_app():
    app.run()

threading.Thread(target=run_app).start()






'''if __name__ == '__main__':
    app.run()'''