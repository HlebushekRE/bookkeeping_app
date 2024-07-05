import mysql.connector
import PyPDF2
import pandas as pd
import tabula
import datetime
import re





class DatabaseManager:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost', 
                user='root', 
                passwd='1qazxsw23edc', 
                database='bookkeeping')
        
        except mysql.connector.Error as e:
            print(e)

    def close(self):
        if self.connection is not None:
            self.connection.close()

    # Так-то я её ни разу не использовал, хм
    '''def execute_query(self, query, values):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, values)
            self.connection.commit()
            return True
        
        except mysql.connector.Error as e:
            return False'''

    def calculations(self, tax, first_date, second_date):
        
        first_date = self.format_date(first_date)
        second_date = self.format_date(second_date)

        self.connect()
        cursor = self.connection.cursor()
        query = "SELECT summ, is_costs FROM register WHERE date BETWEEN %s AND %s"
        values = (first_date, second_date)
        cursor.execute(query, values)
        rows = cursor.fetchall()
        self.close()

        sum_replenishment = 0
        sum_costs = 0
        sum_tax = 0

        for row in rows:
            if row[1] == 0:
                sum_replenishment += float(row[0])
                sum_tax += float(row[0]) / 100 * tax
            else:
                sum_costs += float(row[0])

        balance = sum_replenishment - sum_costs - sum_tax

        return sum_replenishment, sum_costs, sum_tax, round(balance, 2)
        
        

    # Функция форматирования даты  
    def format_date(self, date_string):
        format = '%d.%m.%Y'
        date = datetime.datetime.strptime(date_string, format).date()
        return(date)    
    
    # Функция ручного ввода данных
    def insert_data(self, ids, date, name, total, type_input):
        self.connect()
        query = "INSERT INTO register (id_user, date, сounterparty, summ, is_costs) VALUES (%s, %s, %s, %s, %s)"
        date = self.format_date(date)
        values = (int(ids), date, name, float(total), int(type_input))
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
            print("Данные успешно добавлены")
        
        except mysql.connector.Error as e:
            print(e)

    # Функция регистрации
    def register_user(self, name, surname, login, password):
        self.connect()
        query = "INSERT INTO user (name, surname, login, password) VALUES (%s, %s, %s, %s)"
        values = (name, surname, login, password)
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
            print("Данные успешно добавлены")
        except mysql.connector.Error as e:
            print(e)

    # Функция входа
    def login(self, username, pasw):
        self.connect()
        query = "SELECT * FROM user WHERE login = %s AND password = %s"
        values = (username, pasw)

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            result = cursor.fetchall()  # Получить все строки результата запроса
            if result:  # Если есть данные
                print("Пользователь существует\n")
                return True
            else:
                print("ошибка\n")
                self.connection.commit()
        except mysql.connector.Error as e:
            print(e)

    # Функция парсинга из банка приморья
    def parsing_primorye(self, link):
        df = tabula.read_pdf(link, pages="all")
        df.pop()

        for page in df:

            page.drop('Номер', axis=1, inplace=True, errors='warn')
            page.drop('Unnamed: 3', axis=1, inplace=True, errors='warn')
            page.drop('Unnamed: 4', axis=1, inplace=True, errors='warn')
            page.drop('Unnamed: 0', axis=1, inplace=True, errors='warn')
            page.drop(0, axis=0, inplace=True, errors='warn')
            page.drop(1, axis=0, inplace=True, errors='warn')
            page = page.dropna(subset=['Реквизиты контрагента'])
            page = page.reset_index(drop=True)

            count = 0

            for i in range(len(page) - 1):
                if pd.isna(page.loc[i+1, 'Дата']):
                    count += 1
                    
                else:
                    for j in range(count):
                        page.loc[i-count, 'Реквизиты контрагента'] += ' ' + page.loc[i-count+1+j, 'Реквизиты контрагента']
                        page.drop(i-count+1+j, axis=0, inplace=True, errors='warn')
                        
                    count = 0
            else:
                for j in range(count):
                    page.loc[i+1-count, 'Реквизиты контрагента'] += ' ' + page.loc[i-count+2+j, 'Реквизиты контрагента']
                    page.drop(i-count+2+j, axis=0, inplace=True, errors='warn')
            

            page.insert(3, 'Формат', 0)

            for index, row in page.iterrows():
                if pd.isna(row['Unnamed: 1']):
                    page.loc[index, 'Формат'] = 1
                    page.loc[index, 'Unnamed: 1'] = page.loc[index, 'Unnamed: 2']
                    page.loc[index, 'Unnamed: 1'] = page.loc[index, 'Unnamed: 1'].replace(' ', '')

                else:
                    page.loc[index, 'Unnamed: 1'] = page.loc[index, 'Unnamed: 1'].replace(' ', '')
                    


            page.drop('Unnamed: 2', axis=1, inplace=True, errors='warn')

            for index, row in page.iterrows():
                page.loc[index, 'Дата'] = self.format_date(page.loc[index, 'Дата'])

            for index, row in page.iterrows():
                page.loc[index, 'Реквизиты контрагента'] = re.sub(r'ИНН \d+ Счет N \d+ ', '', page.loc[index, 'Реквизиты контрагента'])
                page.loc[index, 'Реквизиты контрагента'] = re.sub(r'ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ ', '', page.loc[index, 'Реквизиты контрагента'])
                page.loc[index, 'Реквизиты контрагента'] = re.sub(r'Требования банка по прочим операциям/', '', page.loc[index, 'Реквизиты контрагента'])

            page_list = page.to_records(index=False)
            self.connect()

            query = "INSERT INTO register (id_user, date, summ, is_costs, сounterparty) VALUES (1, %s, %s, %s, %s)"
            try:
                cursor = self.connection.cursor()
                for pages in page_list:
                    values = pages.tolist()
                    cursor.execute(query, values)
                self.connection.commit()
                print("Данные успешно добавлены")
            
            except mysql.connector.Error as e:
                print(e)

    # Функция парсинга из сбер банка
    def parsing_sber(self, link):
        df = tabula.read_pdf(link, pages="all")

        for page in df:

            if 'No документа' in page.columns:
                page.drop('Сумма по дебету', axis=1, inplace=True, errors='warn')
                page.rename(columns={'Сумма по кредиту': 'Сумма по дебету'}, inplace=True)
                page.rename(columns={'No документа': 'Сумма по кредиту'}, inplace=True)
            else:
                page.drop('Счет', axis=1, inplace=True, errors='warn')
                page.rename(columns={'Unnamed: 0': 'Счет'}, inplace=True)

            if 'Unnamed: 1' in page.columns:
                page.drop('Unnamed: 1', axis=1, inplace=True, errors='warn')
            if 'No документа ВО' in page.columns:
                page.drop('No документа ВО', axis=1, inplace=True, errors='warn')
            if 'ВО' in page.columns:
                page.drop('ВО', axis=1, inplace=True, errors='warn')
            if 'Банк (БИК и наименование)' in page.columns:
                page.drop('Банк (БИК и наименование)', axis=1, inplace=True, errors='warn')
            if 'Банк (БИК и наименование) Назначение платежа' in page.columns:
                page.drop('Банк (БИК и наименование) Назначение платежа', axis=1, inplace=True, errors='warn')
            if 'Назначение платежа' in page.columns:
                page.drop('Назначение платежа', axis=1, inplace=True, errors='warn')
            if page.columns[-1] == 'Unnamed: 0':
                page.drop('Unnamed: 0', axis=1, inplace=True, errors='warn')

            if 'Дата\rпроводки' in page.columns:
                page.rename(columns={'Дата\rпроводки': 'Дата'}, inplace=True)
            if 'Сумма по кредиту No документа' in page.columns:
                page.rename(columns={'Сумма по кредиту No документа': 'Сумма по кредиту'}, inplace=True)

            
            
            
            page.dropna(how='all', inplace=True)

            if page['Дата'][0] == 'проводки':
                page.drop(index=0, inplace=True)
            
            for index, row in page.iterrows():
                if index <= 4:
                    if pd.isna(row['Дата']):
                        page.drop(index, inplace=True)
                else:
                    break

            page = page.reset_index(drop=True)
            del_typle = ()
            
            for i in range(len(page) - 1):
                if not pd.isna(page.loc[i, 'Дата']) and pd.isna(page.loc[i, 'Счет']):
                    del_typle += (i+1, )
                    page.loc[i, 'Счет'] = page.loc[i+1, 'Счет']

            for i in del_typle:
                page.drop(index=i, axis=0, inplace=True, errors='warn')

            page = page.reset_index(drop=True)
            page['Счет'] = page['Счет'].astype(str)
            count = 0
            
            for i in range(len(page) - 1):
                if pd.isna(page.loc[i+1, 'Дата']):
                    count += 1
                    
                else:
                    for j in range(count):
                        page.loc[i-count, 'Счет'] += ' ' + page.loc[i-count+1+j, 'Счет']
                        page.drop(i-count+1+j, axis=0, inplace=True, errors='warn')
                        
                    count = 0
            else:
                for j in range(count):
                    page.loc[i+1-count, 'Счет'] += ' ' + page.loc[i-count+2+j, 'Счет']
                    page.drop(i-count+2+j, axis=0, inplace=True, errors='warn')           

            
            page.insert(3, 'Формат', 0)
            page['Сумма по кредиту'] = page['Сумма по кредиту'].astype(str)

            for index, row in page.iterrows():
                if pd.isna(row['Сумма по дебету']):
                    page.loc[index, 'Формат'] = 1
                    if len(row['Сумма по кредиту']) > 15:
                        page.loc[index, 'Сумма по кредиту'] = re.sub(r'[а-яА-Я]', '', page.loc[index, 'Сумма по кредиту'])
                        key = 0
                        temp = '1234567890 ,'
                        for i, char in enumerate(iter(row['Сумма по кредиту'])):
                            if key == 0:
                                if char not in temp:
                                    page.loc[index, 'Сумма по кредиту'] = row['Сумма по кредиту'].replace(char, '')
                                    row['Сумма по кредиту'] = row['Сумма по кредиту'].replace(char, '')
                                    
                                    
                            else:
                                if char not in temp:
                                    for i, char in enumerate(iter(row['Сумма по кредиту'])):
                                        if char == ',':
                                            page.loc[index, 'Сумма по кредиту'] = row['Сумма по кредиту'][:i+3]
                                            break
                                    break
                                    
                                    
                            if char == ',':
                                temp = '1234567890'
                                key = 1


                    page.loc[index, 'Сумма по дебету'] = page.loc[index, 'Сумма по кредиту']
                    page.loc[index, 'Сумма по дебету'] = page.loc[index, 'Сумма по дебету'].replace(' ', '')
                    page.loc[index, 'Сумма по дебету'] = page.loc[index, 'Сумма по дебету'].replace(',', '.')

                else:
                    page.loc[index, 'Сумма по дебету'] = page.loc[index, 'Сумма по дебету'].replace(' ', '')
                    page.loc[index, 'Сумма по дебету'] = page.loc[index, 'Сумма по дебету'].replace(',', '.')
                    
            
            page.drop('Сумма по кредиту', axis=1, inplace=True, errors='warn')

            for index, row in page.iterrows():
                page.loc[index, 'Дата'] = self.format_date(page.loc[index, 'Дата'])
            
            for index, row in page.iterrows():
                page.loc[index, 'Счет'] = re.sub(r'ИНН \d+ Счет N \d+ ', '', page.loc[index, 'Счет'])
                page.loc[index, 'Счет'] = re.sub(r'ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ ', '', page.loc[index, 'Счет'])
                page.loc[index, 'Счет'] = re.sub(r'Требования банка по прочим операциям/', '', page.loc[index, 'Счет'])
                page.loc[index, 'Счет'] = re.sub(r'\d+', '', page.loc[index, 'Счет'])



            page_list = page.to_records(index=False)
            self.connect()


            query = "INSERT INTO register (id_user, date, сounterparty, summ, is_costs) VALUES (1, %s, %s, %s, %s)"
            try:
                cursor = self.connection.cursor()
                for pages in page_list:
                    values = pages.tolist()
                    cursor.execute(query, values)
                self.connection.commit()
                print("Данные успешно добавлены")
            
            except mysql.connector.Error as e:
                print(e)

    # Функция определения вида выписки
    def what_parsing(self, link):
        pdf_file = open(link, 'rb')
        reader = PyPDF2.PdfReader(pdf_file)
        page = reader.pages[0]
        text = page.extract_text()

        if 'СберБизнес' in text:
            self.parsing_sber(link)
        elif 'ПАО АКБ "Приморье"' in text:
            self.parsing_primorye(link)

    # функция вывода данных в таблицу
    def fetch_data(self, format_filter, first_date, second_date):
        if format_filter == 'Пополнение':
            format_filter = 0
        else:
            format_filter = 1
        
        first_date = self.format_date(first_date)
        second_date = self.format_date(second_date)

        self.connect()

        cursor = self.connection.cursor()
        query = "SELECT сounterparty, summ, date, is_costs FROM register WHERE date BETWEEN %s AND %s AND is_costs = %s"
        values = (first_date, second_date, format_filter)
        cursor.execute(query, values)
        rows = cursor.fetchall()
        return rows




        

        
        


'''
manager = DatabaseManager()
manager.connect()
manager.what_parsing('C:/Python/Python311/repos/bookkeeping_app/сводка-2вар-сбер.pdf')
manager.close()'''

'''manager = DatabaseManager()
manager.connect()
result = manager.login('rew', 'jsd')
if result:
    print("Пользователь существует\n")
else:
    print("Пользователя не существует\n")
manager.close()'''





