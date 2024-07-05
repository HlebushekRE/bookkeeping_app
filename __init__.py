from flask import Flask, request
import mysql.connector
from config import Config
from backend import DatabaseManager

app = Flask(__name__)
app.config.from_object(Config)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1qazxsw23edc'
app.config['MYSQL_DB'] = 'bookkeeping'

mysql = mysql.connector.connect(host=app.config["MYSQL_HOST"],
                               user=app.config["MYSQL_USER"],
                               password=app.config["MYSQL_PASSWORD"],
                               database=app.config["MYSQL_DB"])

'''@app._got_first_request
def connect_db():
    DatabaseManager.connect()'''

@app.route("/register", methods=["POST"])
def register():
    return DatabaseManager.register_user(request.form["name"], request.form["surname"], request.form["login"], request.form["password"])

@app.route("/login", methods=["POST"])
def login():
    return DatabaseManager.login(request.form["username"], request.form["pasw"])

@app.route("/what_parsing", methods=["POST"])
def what_parsing():
    return DatabaseManager.what_parsing(request.files["file"])

@app.route("/insert_data", methods=["POST"])
def insert_data():
    return DatabaseManager.insert_data(request.form["ids"], request.form["date"], request.form["name"], request.form["total"], request.form["type_input"])

@app.route("/fetch_data", methods=["GET"])
def fetch_data():
    return DatabaseManager.fetch_data(request.args.get("format_filter"), request.args.get("first_date"), request.args.get("second_date"))
    
@app.route("/calculations", methods=["POST"])
def calculations():
    return DatabaseManager.calculations(request.form["tax"], request.form["first_date"], request.form["second_date"])










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















if __name__ == '__main__':
    app.run()