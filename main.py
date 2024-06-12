from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty, ListProperty

from kivymd.app import MDApp
from kivymd.uix.list import MDListItemHeadlineText, MDList

from kivymd.font_definitions import fonts
from kivymd.icon_definitions import md_icons

from kivymd.uix.scrollview import MDScrollView

from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp

import datetime
from kivymd.uix.pickers import MDModalDatePicker

from kivymd.uix.tab import MDTabsItemText, MDTabsItem
import backend



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
                text: "Пополнения"


        MDListItem:
            on_release:
                root.nav_drawer.set_state("close")
                root.screen_manager.current = "scr 4"
            MDListItemHeadlineText:
                text: "Расходы"
  

        MDListItem:
            on_release:
                root.nav_drawer.set_state("close")
                root.screen_manager.current = "scr 5" 
            MDListItemHeadlineText:
                text: "Налоги"

        MDListItem:
            on_release:
                root.nav_drawer.set_state("close")
                root.screen_manager.current = "scr 6"
            MDListItemHeadlineText:
                text: "Регистрация"

        MDListItem:
            on_release:
                root.nav_drawer.set_state("close")
                root.screen_manager.current = "scr 7"
            MDListItemHeadlineText:
                text: "Вход"
                             


MDScreen:

    md_bg_color: self.theme_cls.backgroundColor

    MDTabsPrimary:
        id: tabs
        pos_hint: {"top": .9}
        size_hint_x: 1
        allow_stretch: True
        label_only: True

        MDDivider:

    MDTopAppBar:
        type: "small"
        pos_hint: {"top": 1}

        MDTopAppBarLeadingButtonContainer:
            
            MDActionTopAppBarButton:
                icon: "arrow-left"
                on_release: nav_drawer.set_state("open")
 

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
                        on_release: app.switch_theme()
                        MDButtonText:
                            text: "Тема"                            

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
                            name: 'date'
                            on_focus: app.show_date_picker(self.focus)
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
                            on_focus: if self.focus: app.menu.open()
                            MDTextFieldHintText:
                                text: 'Формат'

                    MDButton:
                        size_hint: (0.45, 0.45)
                        pos_hint: {"center_x": .5, "center_y": .5}
                        on_release: app.calc_table(*args)
                        MDButtonText:
                            text: "Ввод"


            MDScreen:  # Страница таблицы, вывода, фронт
                name: "scr 3"           

                BoxLayout:
                    orientation: 'vertical'
                    padding: "60dp"
                    
                    
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
                    padding: "60dp"
                    
                    
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

            MDScreen:  # Страница регистрации
                name: "scr 6"

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

                        MDIconButton:
                            icon: "nature"

                        MDTextField:
                            id: usr_name
                            name: 'usr_name'
                            MDTextFieldHintText:
                                text: 'Имя?'

                    BoxLayout:
                        orientation: 'horizontal'

                        MDIconButton:
                            icon: "nature"

                        MDTextField:
                            id: family
                            name: 'family'
                            MDTextFieldHintText:
                                text: 'Фамилия?'

                    BoxLayout:
                        orientation: 'horizontal'

                        MDIconButton:
                            icon: "nature"

                        MDTextField:
                            id: login
                            name: 'login'
                            MDTextFieldHintText:
                                text: 'Логин?'

                    BoxLayout:
                        orientation: 'horizontal'

                        MDIconButton:
                            icon: "nature"

                        MDTextField:
                            id: pass
                            name: 'pass'
                            MDTextFieldHintText:
                                text: 'Пароль?'


                    MDButton:
                        size_hint: (0.45, 0.45)
                        pos_hint: {"center_x": .5, "center_y": .5}
                        on_release: app.calc_table(*args)
                        MDButtonText:
                            text: "Ввод"         

            MDScreen:  # Страница входа
                name: "scr 7"

                # label - Логин
                # label - пароль

                #кнопка - ввод

                BoxLayout:
                    orientation: 'vertical'
                    padding: "65dp"
                            
                            
                    BoxLayout:
                        orientation: 'horizontal'
                        padding: [20, 0, 20, 80]

                        MDIconButton:
                            icon: "nature"

                        MDTextField:
                            id: login
                            name: 'login'
                            MDTextFieldHintText:
                                text: 'Логин'

                    BoxLayout:
                        orientation: 'horizontal'
                        padding: [20, 0, 20, 200]

                        MDIconButton:
                            icon: "nature"

                        MDTextField:
                            id: pass
                            name: 'pass'
                            MDTextFieldHintText:
                                text: 'Пароль'


                    MDButton:
                        size_hint: (0.45, 0.45)
                        pos_hint: {"center_x": .5, "center_y": .5}
                        on_release: app.calc_table(*args)
                        MDButtonText:
                            text: "Ввод"                         
                             

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
        date_picker = None
       

    def switch_theme(self):
        self.theme_cls.switch_theme()

    def on_save(self, instance, value, date_range): 
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

    def show_date_picker(self, focus):
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
            on_ok=lambda *args: self.on_save(self.date_picker, selected_date[0], selected_date)
        )
        self.date_picker.open()

    def set_item(self, text_item):  #Вызывается функция, когда выбран элемент из списка, можно if ом определить и использовать
        self.screen.ids.format_type.text = text_item
        self.menu.dismiss()

    def build(self):
        return self.screen
    
    def on_start(self):
        for tab_name in [
            "Пополнение", "Расходы", "Итог"
        ]:
            self.root.ids.tabs.add_widget(
                MDTabsItem(
                    MDTabsItemText(
                        text=tab_name,
                    ),
                )
            )
        self.root.ids.tabs.switch_tab(text="Пополнение")
    
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