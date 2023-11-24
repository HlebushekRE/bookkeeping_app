from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty, ListProperty

from kivymd.app import MDApp
from kivymd.uix.list import OneLineIconListItem, MDList

from kivymd.font_definitions import fonts
from kivymd.icon_definitions import md_icons

from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.datatables import MDDataTable

from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp

from kivymd.uix.pickers import MDDatePicker
import datetime




KV = '''
<ContentNavigationDrawer>

    MDList:

        OneLineListItem:
            text: "Настройки"
            on_press:
                root.nav_drawer.set_state("close")
                root.screen_manager.current = "scr 1"

        OneLineListItem:
            text: "Ввод"
            on_press:
                root.nav_drawer.set_state("close")
                root.screen_manager.current = "scr 2"

        OneLineListItem:
            text: "Пополнения"
            on_press:
                root.nav_drawer.set_state("close")
                root.screen_manager.current = "scr 3"

        OneLineListItem:
            text: "Расходы"
            on_press:
                root.nav_drawer.set_state("close")
                root.screen_manager.current = "scr 4"  

        OneLineListItem:
            text: "Налоги"
            on_press:
                root.nav_drawer.set_state("close")
                root.screen_manager.current = "scr 5"                              


MDScreen:

    MDTopAppBar:
        pos_hint: {"top": 1}
        elevation: 4
        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]

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
                    padding: "10dp"
                    

                    MDLabel:
                        text: "Введите число, без знака %"
                        halign: "center" 

                    BoxLayout:
                        orientation: 'horizontal'
                        padding: [20, 0, 20, 80]

                        MDTextField:
                            id: tax
                            name: 'tax'
                            hint_text: 'Налоговый %'
                            color_mode: 'custom'

                            input_filter: 'float'

                    BoxLayout:
                        orientation: 'horizontal'
                        padding: [20, 0, 20, 100]

                        MDTextField:
                            id: deductible
                            name: 'deductible '
                            hint_text: 'Вычитаемый %'

                            input_filter: 'float'

                    MDFillRoundFlatButton:
                        text: "Очистить таблицу"
                        size_hint: (0.45, 0.45)
                        pos_hint: {"center_x": .5, "center_y": .5}
                        on_release: app.clear_table()


            MDScreen:  # Страница ввода, фронт
                name: "scr 2"

                # label - Выплывающий список, формат - поступления или расходы???

                # label - input, дата
                # label - input, имя
                # label - input, сумма

                #кнопка - ввод

                BoxLayout:
                    orientation: 'vertical'
                    padding: "10dp"

                    BoxLayout:
                        orientation: 'horizontal'

                        MDIconButton:
                            icon: "calendar-month"

                        MDTextField:
                            id: check_date
                            name: 'date'
                            hint_text: 'Дата'
                            on_focus: app.show_date_picker()
                            
                    BoxLayout:
                        orientation: 'horizontal'

                        MDIconButton:
                            icon: "nature"

                        MDTextField:
                            id: man_name
                            name: 'man_name'
                            hint_text: 'Имя'

                    BoxLayout:
                        orientation: 'horizontal'

                        MDIconButton:
                            icon: "cash"

                        MDTextField:
                            id: Summ
                            name: 'Summ'
                            hint_text: 'Сумма'

                            input_filter: 'int'

                    BoxLayout:
                        orientation: 'horizontal'

                        MDTextField:
                            id: format_type
                            name: 'format_type'
                            hint_text: 'Формат'
                            on_focus: if self.focus: app.menu.open()

                    MDFillRoundFlatButton:
                        text: "Ввод"
                        size_hint: (0.45, 0.45)
                        pos_hint: {"center_x": .5, "center_y": .5}
                        on_release: app.calc_table(*args)


            MDScreen:  # Страница таблицы, вывода, фронт
                name: "scr 3"           

                BoxLayout:
                    orientation: 'vertical'
                    
                    
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

            MDScreen:  # Страница Расходов
                name: "scr 4"           

                BoxLayout:
                    orientation: 'vertical'
                    
                    
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
                            id: table_list2      

            MDScreen:  # Страница Налогов
                name: "scr 5"           

                Label:
                    text: 'screen 5'                             
                             

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
        menu_items = [
            {
                "text": i,
                "on_release": lambda x = i: self.set_item(x),
            } for i in ['Пополнение', 'Расходы']]
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.format_type,
            items=menu_items,
            position="bottom",
        )



    def on_save(self, instance, value, date_range):
        self.screen.ids.check_date.text = value.strftime("%d.%m.%Y")
        '''
        Events called when the "OK" dialog box button is clicked.

        :type instance: <kivymd.uix.picker.MDDatePicker object>;
        :param value: selected date;
        :type value: <class 'datetime.date'>;
        :param date_range: list of 'datetime.date' objects in the selected range;
        :type date_range: <class 'list'>;
        '''

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''

    def show_date_picker(self):  # Есть баг? при нажатии в любое место, вызывает окно повторно, надо бы пофиксить
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def set_item(self, text_item):  #Вызывается функция, когда выбран элемент из списка, можно if ом определить и использовать
        self.screen.ids.format_type.text = text_item
        self.menu.dismiss()

    def build(self):
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.theme_style = "Dark"
        return self.screen
    
    def on_start(self):
        self.screen.ids.tax.text = '6'
        self.screen.ids.deductible.text = '10'
        self.screen.ids.check_date.text = datetime.date.today().strftime("%d.%m.%Y")


    
    def calc_table(self, *args):
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
            )


    def clear_table(self):
        self.screen.ids.table_list1.clear_widgets()
    

bookkeeping().run()