from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty, ListProperty

from kivymd.app import MDApp
from kivymd.uix.list import MDListItemHeadlineText, MDList

from kivymd.font_definitions import fonts
from kivymd.icon_definitions import md_icons

from kivymd.uix.scrollview import MDScrollView
import requests

from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp

import datetime
from kivymd.uix.pickers import MDModalDatePicker

from kivymd.uix.tab import MDTabsItemText, MDTabsItem
import backend
import __init__



import sys
from PyQt5.QtWidgets import QApplication, QFileDialog


KV = '''
<ContentNavigationDrawer>

    MDList:

        MDListItem:
            on_release:
                root.nav_drawer.set_state("close")
                root.screen_manager.current = "scr 1"
            MDListItemHeadlineText:
                text: "Настройки"

        MDListItem:
            on_release:
                root.nav_drawer.set_state("close")
                root.screen_manager.current = "scr 2"
            MDListItemHeadlineText:
                text: "Ввод"

        MDListItem:
            on_release:
                root.nav_drawer.set_state("close")
                root.screen_manager.current = "scr 3"
            MDListItemHeadlineText:
                text: "Таблица"
  
        MDListItem:
            on_release:
                root.nav_drawer.set_state("close")
                root.screen_manager.current = "scr 4" 
            MDListItemHeadlineText:
                text: "Расчёты"

        MDListItem:
            on_release:
                root.nav_drawer.set_state("close")
                root.screen_manager.current = "scr 5"
            MDListItemHeadlineText:
                text: "Регистрация"

        MDListItem:
            on_release:
                root.nav_drawer.set_state("close")
                root.screen_manager.current = "scr 6"
            MDListItemHeadlineText:
                text: "Вход"
                             
        MDListItem:
            on_release:
                root.nav_drawer.set_state("close")
                root.screen_manager.current = "scr 7"
            MDListItemHeadlineText:
                text: "Парсер"

MDScreen:

    md_bg_color: self.theme_cls.backgroundColor

    # MDTabsPrimary:
    #    id: tabs
    #    pos_hint: {"top": .9}
    #    size_hint_x: 1
    #    allow_stretch: True
    #    label_only: True

    #    MDDivider:

    MDTopAppBar:
        type: "small"
        pos_hint: {"top": 1}

        MDTopAppBarLeadingButtonContainer:
            
            MDActionTopAppBarButton:
                icon: "arrow-left"
                on_release: nav_drawer.set_state("open")

        MDTopAppBarTitle:
            text: "Bookkeeping"
            pos_hint: {"center_x": .5}

        MDTopAppBarTrailingButtonContainer:

            MDActionTopAppBarButton:
                icon: "theme-light-dark"
                on_release: app.switch_theme()

            MDActionTopAppBarButton:
                icon: "table-plus"
                on_release: app.print_table()
 

    MDNavigationLayout:

        MDScreenManager:
            id: screen_manager

            MDScreen:  # Страница настройки, фронт
                name: "scr 1"    

                # label, 'Налоговый %'
                # Напротив, input
                # label, 'Вычетаемый %'
                # Напротив, input

                # Снизу, кнопка 'Сохранить'                                               

                BoxLayout:
                    orientation: 'vertical'
                    padding: "50dp"
                    

                    MDLabel:
                        text: "Введите число, без знака %"
                        halign: "center" 

                    BoxLayout:
                        orientation: 'horizontal'
                        padding: [20, 0, 20, 80]

                        MDTextField:
                            id: tax
                            name: 'tax'
                            color_mode: 'custom'
                            input_filter: 'float'
                            MDTextFieldHintText:
                                text: 'Налоговый %'

                    BoxLayout:
                        orientation: 'horizontal'
                        padding: [20, 0, 20, 100]

                        MDTextField:
                            id: deductible
                            name: 'deductible '
                            input_filter: 'float'
                            MDTextFieldHintText:
                                text: 'Вычитаемый %'                         

                    MDButton:                        
                        size_hint: (0.45, 0.45)
                        pos_hint: {"center_x": .5, "center_y": .5}
                        on_release: app.clear_table()
                        MDButtonText:
                            text: "Очистить таблицу"


            MDScreen:  # Страница ввода, фронт
                name: "scr 2"

                # label - Выплывающий список, формат - поступления или расходы???

                # label - input, дата
                # label - input, имя
                # label - input, сумма

                #кнопка - ввод

                BoxLayout:
                    orientation: 'vertical'
                    padding: "65dp"

                    BoxLayout:
                        orientation: 'horizontal'

                        MDIconButton:
                            icon: "calendar-month"

                        MDTextField:
                            id: check_date
                            name: 'check_date'
                            on_focus: app.show_date_picker(self.focus, self.name)
                            MDTextFieldHintText:
                                text: 'Дата'
                            
                            
                    BoxLayout:
                        orientation: 'horizontal'

                        MDIconButton:
                            icon: "nature"

                        MDTextField:
                            id: man_name
                            name: 'man_name'
                            MDTextFieldHintText:
                                text: 'Имя'

                    BoxLayout:
                        orientation: 'horizontal'

                        MDIconButton:
                            icon: "cash"

                        MDTextField:
                            id: Summ
                            name: 'Summ'
                            input_filter: 'int'
                            MDTextFieldHintText:
                                text: 'Сумма'

                    BoxLayout:
                        orientation: 'horizontal'

                        MDTextField:
                            id: format_type
                            name: 'format_type'
                            on_focus: if self.focus: app.drop_format_input()
                            MDTextFieldHintText:
                                text: 'Формат'

                    MDButton:
                        size_hint: (0.45, 0.45)
                        pos_hint: {"center_x": .5, "center_y": .5}
                        on_release: app.manual_input()
                        MDButtonText:
                            text: "Ввод"


            MDScreen:  # Страница таблицы, вывода, фронт
                name: "scr 3"       

                BoxLayout:
                    orientation: 'vertical'

                    
                    BoxLayout:
                        orientation: 'horizontal'
                        padding: [0, 60, 0, 0] 
                        size_hint: (1, 0.4)


                        MDTextField:
                            id: format_type_filter
                            name: 'format_type_filter'
                            on_focus: if self.focus: app.drop_format_filter()
                            MDTextFieldHintText:
                                text: 'Формат вывода'
                        
                        MDTextField:
                            id: date_filter1
                            name: 'date_filter1'
                            on_focus: app.show_date_picker(self.focus, self.name)
                            MDTextFieldHintText:
                                text: 'От'

                        MDTextField:
                            id: date_filter2
                            name: 'date_filter2'
                            on_focus: app.show_date_picker(self.focus, self.name)
                            MDTextFieldHintText:
                                text: 'До'
                            
                    
                    BoxLayout:
                        orientation: 'horizontal'
                        padding: [0, 60, 0, 0] 
                        size_hint: (1, 0.2)


                        MDLabel:
                            text: "Дата"
                            halign: "center"
                        MDLabel:
                            text: "Контрагент"
                            halign: "center"
                        MDLabel:
                            text: "Сумма"
                            halign: "center"  
                        MDLabel:
                            text: "Формат"
                            halign: "center" 

                    ScrollView:

                        MDList:
                            id: table_list1

            MDScreen:  # Страница Налогов
                name: "scr 4"
                
                BoxLayout:
                    orientation: 'vertical'
                    padding: "65dp"

                    BoxLayout:
                        orientation: 'horizontal'

                        MDTextField:
                            id: date_filter3
                            name: 'date_filter3'
                            on_focus: app.show_date_picker(self.focus, self.name)
                            MDTextFieldHintText:
                                text: 'От'

                        MDTextField:
                            id: date_filter4
                            name: 'date_filter4'
                            on_focus: app.show_date_picker(self.focus, self.name)
                            MDTextFieldHintText:
                                text: 'До'

                    MDLabel:
                        id: lab_sum_replenishment
                        text: 'Сумма пополнения: 0' 

                    MDLabel:
                        id: lab_sum_costs
                        text: 'Сумма расходов: 0' 

                    MDLabel:
                        id: lab_sum_tax
                        text: 'Сумма налогов: 0' 

                    MDLabel:
                        id: lab_balance
                        text: 'Остаток средств: 0' 

                    MDButton:
                        size_hint: (0.45, 0.45)
                        pos_hint: {"center_x": .5, "center_y": .5}
                        on_release: app.print_results()
                        MDButtonText:
                            text: "Посчитать"                           

            MDScreen:  # Страница регистрации
                name: "scr 5"

                # label - Имя
                # label - Фамилия
                # label - Логин
                # label - пароль


                #кнопка - ввод

                BoxLayout:
                    orientation: 'vertical'
                    padding: "65dp"
                                                       
                    BoxLayout:
                        orientation: 'horizontal'

                        MDTextField:
                            id: usr_name
                            name: 'usr_name'
                            MDTextFieldHintText:
                                text: 'Имя?'

                    BoxLayout:
                        orientation: 'horizontal'

                        MDTextField:
                            id: family
                            name: 'family'
                            MDTextFieldHintText:
                                text: 'Фамилия?'

                    BoxLayout:
                        orientation: 'horizontal'

                        MDTextField:
                            id: login_reg
                            name: 'login_reg'
                            MDTextFieldHintText:
                                text: 'Логин?'

                    BoxLayout:
                        orientation: 'horizontal'

                        MDTextField:
                            id: pasw_reg
                            name: 'pasw_reg'
                            MDTextFieldHintText:
                                text: 'Пароль?'

                    MDButton:
                        size_hint: (0.45, 0.45)
                        pos_hint: {"center_x": .5, "center_y": .5}
                        on_release: app.reg_user(*args)
                        MDButtonText:
                            text: "Ввод"         

                            
            MDScreen:  # Страница входа
                name: "scr 6"

                # label - Логин
                # label - пароль

                #кнопка - ввод

                BoxLayout:
                    orientation: 'vertical'
                    padding: "65dp"
                                                        
                    BoxLayout:
                        orientation: 'horizontal'
                        padding: [20, 0, 20, 80]

                        MDTextField:
                            id: login_entry
                            name: 'login_entry'
                            MDTextFieldHintText:
                                text: 'Логин'

                    BoxLayout:
                        orientation: 'horizontal'
                        padding: [20, 0, 20, 200]

                        MDTextField:
                            id: pasw_entry
                            name: 'pasw_entry'
                            MDTextFieldHintText:
                                text: 'Пароль'


                    MDButton:
                        size_hint: (0.45, 0.45)
                        pos_hint: {"center_x": .5, "center_y": .5}
                        on_release: app.login_usr(*args)
                        MDButtonText:
                            text: "Ввод"    

            MDScreen:  # Страница парсера
                name: "scr 7"           

                MDButton: # Поменять, лучше это не в ввиде кнопки делать
                    size_hint: (0.45, 0.45)
                    pos_hint: {"center_x": .5, "center_y": .7}
                    on_release: app.file_selection()
                    MDButtonText:
                        text: "Выбор файла"  

                MDLabel:
                    id: id_label_selected_file
                    text: "Выбранный файл: Отсутствует"
                    halign: "center"
                    pos: (self.width / 2 - self.size[0] / 2, 50)
           
                MDButton:
                    size_hint: (0.45, 0.45)
                    pos_hint: {"center_x": .5, "center_y": .5}
                    on_release: app.send_file()
                    MDButtonText:
                        text: "Ввод"   

                MDLabel:
                    id: id_label_send_file
                    text: ""
                    halign: "center"
                    pos: (self.width / 2 - self.size[0] / 2, -40)                  
                             

        MDNavigationDrawer:
            id: nav_drawer
            radius: (0, 16, 16, 0)

            ContentNavigationDrawer:
                screen_manager: screen_manager
                nav_drawer: nav_drawer

<ItemTable>:
    size_hint_y: None
    height: "42dp"

    MDLabel:
        text: root.date
        halign: "center"
    MDLabel:
        text: root.name
        halign: "center"
    MDLabel:
        text: root.total
        halign: "center"  
    MDLabel:
        text: root.type_input
        halign: "center"                              
'''

class ItemTable(BoxLayout):
    date = StringProperty()
    name = StringProperty()
    total = StringProperty()
    type_input = StringProperty()

class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class bookkeeping(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(KV)
        
        date_picker = None
        selected_file = None

    def drop_format_input(self):
        menu_items = [
            {
                "text": i,
                "on_release": lambda x = i: self.set_item(x),
            } for i in ['Пополнение', 'Расходы']]
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.format_type,
            items=menu_items,
            pos_hint={'center_x': .7, 'center_y': .7},
            position="top",
        )
        self.menu.open()

    def drop_format_filter(self):
        menu_items = [
            {
                "text": i,
                "on_release": lambda x = i: self.set_item(x),
            } for i in ['Пополнение', 'Расходы']]
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.format_type_filter,
            items=menu_items,
            position="top",
        )
        self.menu.open()

    def switch_theme(self):
        self.theme_cls.switch_theme()

    def reg_user(self, *args):
        name = self.screen.ids.usr_name.text
        surname = self.screen.ids.family.text
        login = self.screen.ids.login_reg.text
        password = self.screen.ids.pasw_reg.text

        url = 'http://localhost:5000/login'
        payload = {
            'name': name,
            'surname': surname,
            'login': login,
            'password': password
        }
        response = requests.post(url, data=payload)

        '''db = backend.DatabaseManager()
        db.connect()
        db.register_user(name, surname, login, password)
        db.close()'''

    def login_usr(self, *args):
        username = self.screen.ids.login_entry.text
        password = self.screen.ids.pasw_entry.text

        # новый
        url = 'http://localhost:5000/login'
        payload = {
            'username': username,
            'password': password
        }
        response = requests.post(url, data=payload)

        # Старый
        '''db = backend.DatabaseManager()
        db.connect()
        db.login(username, password)
        db.close()'''

    def on_save(self, instance, value, date_range, id): 
        if id == 'date_filter1':
            self.screen.ids.date_filter1.text = self.date_picker.get_date()[0].strftime("%d.%m.%Y")
        elif id == 'date_filter2':
            self.screen.ids.date_filter2.text = self.date_picker.get_date()[0].strftime("%d.%m.%Y")
        elif id == 'date_filter3':
            self.screen.ids.date_filter3.text = self.date_picker.get_date()[0].strftime("%d.%m.%Y")
        elif id == 'date_filter4':
            self.screen.ids.date_filter4.text = self.date_picker.get_date()[0].strftime("%d.%m.%Y")
        elif id == 'check_date':
            self.screen.ids.check_date.text = self.date_picker.get_date()[0].strftime("%d.%m.%Y")
        self.on_cancel()

        '''
            Events called when the "OK" dialog box button is clicked.

            :type instance: <kivymd.uix.picker.MDModalDatePicker object>; 
            :param value: selected date; 
            :type value: <class 'datetime.date'>; 
            :param date_range: list of 'datetime.date' objects in the selected range; 
            :type date_range: <class 'list'>; 
        '''
        
    def on_cancel(self, *args):
        self.date_picker.dismiss()

    def show_date_picker(self, focus, id):
        if not focus:
            return        
        
        self.date_picker = MDModalDatePicker(
            min_date=None,
            max_date=None,
            mode="picker",
            mark_today=True,            
        )

        selected_date = self.date_picker.get_date()

        self.date_picker.bind(
            on_cancel=self.on_cancel, 
            on_ok=lambda *args: self.on_save(self.date_picker, selected_date[0], selected_date, id)
        )
        self.date_picker.open()

    def file_selection(self):
        app = QApplication(sys.argv)

        file_dialog = QFileDialog()
        file_dialog.setNameFilter("PDF files (*.pdf)")
        self.selected_file = file_dialog.getOpenFileName()[0]

        print("Вы выбрали файл:", self.selected_file)
        self.screen.ids.id_label_selected_file.text = "Выбранный файл: {}".format(self.selected_file)

    def send_file(self):
        self.screen.ids.id_label_send_file.text = "Файл отправлен"

        # новый
        url = 'http://localhost:5000/what_parsing'
        files = {'file': open(self.selected_file, 'rb')}
        response = requests.post(url, files=files)

        # старый
        '''db = backend.DatabaseManager()
        db.connect()
        db.what_parsing(self.selected_file)
        db.close()'''

    def set_item(self, text_item):
        self.screen.ids.format_type.text = text_item
        self.screen.ids.format_type_filter.text = text_item
        self.menu.dismiss()

    def build(self):
        return self.screen
    
    def on_start(self):
        self.screen.ids.tax.text = '6'
        self.screen.ids.deductible.text = '10'
        self.screen.ids.check_date.text = datetime.date.today().strftime("%d.%m.%Y")
        self.screen.ids.date_filter1.text = datetime.date(2000, 1, 1).strftime("%d.%m.%Y")
        self.screen.ids.date_filter2.text = datetime.date(2100, 12, 20).strftime("%d.%m.%Y")
        self.screen.ids.format_type_filter.text = 'Пополнение'

    def print_results(self):
        tax = float(self.screen.ids.tax.text)
        first_date = self.screen.ids.date_filter3.text
        second_date = self.screen.ids.date_filter4.text

        # Новый
        url = 'http://localhost:5000/calculations'
        payload = {
            'tax': tax,
            'first_date': first_date,
            'second_date': second_date
        }
        response = requests.post(url, data=payload)

        sum_replenishment, sum_costs, sum_tax, balance = response.json()

        # Старый
        '''db = backend.DatabaseManager()
        db.connect()
        sum_replenishment, sum_costs, sum_tax, balance = db.calculations(tax, first_date, second_date)
        db.close()'''

        self.screen.ids.lab_sum_replenishment.text = 'Сумма пополнений: ' + str(sum_replenishment)
        self.screen.ids.lab_sum_costs.text = 'Сумма расходов: ' + str(sum_costs)
        self.screen.ids.lab_sum_tax.text = 'Сумма налогов: ' + str(sum_tax)
        self.screen.ids.lab_balance.text = 'Остаток средств: ' + str(balance)

    def print_table(self):
        self.clear_table()
        format_filter = self.screen.ids.format_type_filter.text
        first_date = self.screen.ids.date_filter1.text
        second_date = self.screen.ids.date_filter2.text

        # Новый вариант
        url = 'http://localhost:5000/fetch_data'
        payload = {
            'format_filter': format_filter,
            'first_date': first_date,
            'second_date': second_date
        }
        response = requests.post(url, data=payload)
        rows = response.json()

        # старый вариант
        '''db = backend.DatabaseManager()
        db.connect()
        rows = db.fetch_data(format_filter, first_date, second_date)
        db.close()'''

        format = '%a, %d %b %Y %H:%M:%S GMT'
        

        for row in rows:
            if row[3] == 0:
                format_type = 'Пополнение'
            else:
                format_type = 'Расходы'

            self.screen.ids.table_list1.add_widget(
                ItemTable(
                    date = str(datetime.datetime.strptime(row[2], format).date()),
                    name = row[0],
                    total = str(row[1]),
                    type_input = format_type,
                )
            )

    def manual_input(self):
        check_date = self.screen.ids.check_date.text
        Summ = int(self.screen.ids.Summ.text)
        man_name = self.screen.ids.man_name.text
        format_type = self.screen.ids.format_type.text
        deductible = float(self.screen.ids.deductible.text)  

        if format_type == 'Пополнение':
            format_type = 0
            Summ = Summ - Summ / 100 * deductible
        else:
            format_type = 1

        # новый вариант
        url = 'http://localhost:5000/insert_data'
        payload = {
            'ids': 1,
            'date': check_date,
            'name': man_name,
            'total': Summ,
            'type_input': format_type
        }
        response = requests.post(url, data=payload)

        # test
        '''print('\n')
        print(response)
        print('\n')'''

        # старый вариант
        '''db = backend.DatabaseManager()
        db.connect()
        db.insert_data(1, check_date, man_name, Summ, format_type)
        db.close()'''

    '''def calc_table(self, *args): # Это расчёты, потом надо будет на сервер перенести
        tax = float(self.screen.ids.tax.text)
        deductible = float(self.screen.ids.deductible.text)
        check_date = self.screen.ids.check_date.text
        Summ = int(self.screen.ids.Summ.text)
        man_name = self.screen.ids.man_name.text
        format_type = self.screen.ids.format_type.text
        

        amount_tax = Summ / 100 * tax
        total_sum = Summ - Summ / 100 * deductible
        print(Summ, amount_tax, total_sum)




        if format_type == 'Пополнение':
            self.screen.ids.table_list1.add_widget(
                ItemTable(
                    date = check_date,
                    name = man_name,
                    total = str(total_sum),
                    type_input = format_type,
                )
            )
        else:
            self.screen.ids.table_list1.add_widget(
                ItemTable(
                    date = check_date,
                    name = man_name,
                    total = str(Summ),
                    type_input = format_type,
                )
            )'''


    def clear_table(self):
        self.screen.ids.table_list1.clear_widgets()
    
'''if __name__ == '__main__': 
    __init__.app.run()'''
bookkeeping().run()

