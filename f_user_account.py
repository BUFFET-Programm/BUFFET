import f_login
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDIconButton, MDRaisedButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.pickers import MDDatePicker
from b_buyer_log import read_logs, delete_log
from kivy.clock import Clock
import pygame
from b_product import read_product
from f_components import MDFlatButton, MDIconButton, MDPersianLabel
from b_charge_and_buy import buy, charge, read_charge
from f_create_numbers import create_numbers
from b_manage_buyers import check_name_is_new, change_buyer_name, change_buyer_face
from b_manage_users import user_type, current_user_name
from important_variables import FONT_PATH
from arabic_reshaper import reshape
from bidi.algorithm import get_display
import threading

last_was_operator = None
calculator_value = 0
user_name_ = ""
user_charge = 0
user_school = ""
user_class = ""
do = False
filter = []
date_filter = []
value_filter = []
type_filter = None

KV = """
<UserAccount>:
    MDFloatLayout:
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["edit"]
            icon: "account-cog"
            pos_hint: {"x": 0,"y": .9}
            size_hint: .4, .1
            on_release: root.go_to_setting_page()
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["home"]
            icon: "home"
            pos_hint: {"x": .4,"y": .9}
            size_hint: .4, .1
            on_release: root.manager.current = "home"
        MDPersianLabel:
            label_text: root.user_name
            id: user_name
            pos_hint: {"x": .6,"y": .8}
            size_hint: .2, .1
        MDLabel:
            id: user_charge
            text: root.user_charge
            pos_hint: {"x": 0,"y": .8}
            size_hint: .2, .1
            halign: "center"
            valign: "center"
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["history"]
            icon: "history"
            size_hint: .2, .1
            pos_hint: {"x": .8, "y": .9}
            on_release: root.manager.current = "log"
        MDIconButton:
            icon: "delete"
            pos_hint: {"x": 0,"y": .7}
            size_hint: .2, .1
            on_release: root.clear_products()
        MDPersianLabel:
            label_text: app.language_dialogs["buy"]
            pos_hint: {"x": .15,"y": .7}
            size_hint: .1, .1
        MDTextField:
            font_size: 20
            valign: "center"
            id: buy
            text: "0"
            pos_hint: {"x": .25,"y": .7125}
            size_hint: .3, .075
            readonly: True
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["buy"]
            font_size: 12
            icon: "credit-card"
            on_release: root.charge_or_buy(root.user_name, root.ids.buy.text, "buy")
            pos_hint: {"x": .55,"y": .7}
            size_hint: .2, .1
        MDFloatLayout:
            id: charge_or_hand_enter
            size_hint: 1, 1
            pos_hint: {"x": -1,"y": 0}
            MDIconButton:
                icon: "delete"
                pos_hint: {"x": 0,"y": .6}
                size_hint: .2, .1
                on_release: root.ids.charge.text = "0"
            MDPersianLabel:
                label_text: app.language_dialogs["charge"]
                pos_hint: {"x": .15,"y": .6}
                size_hint: .1, .1
            MDTextField:
                font_size: 20
                valign: "center"
                id: charge
                text: "0"
                pos_hint: {"x": .25,"y": .6125}
                size_hint: .3, .075
                readonly: True
            MDRectangleFlatIconButton:
                button_text: app.language_dialogs["charge"]
                font_size: 12
                icon: "battery-70"
                on_release: root.charge_or_buy(root.user_name, root.ids.charge.text, "charge")
                pos_hint: {"x": .55,"y": .6}
                size_hint: .2, .1
            Calculator:
                id: calculator
                pos_hint: {"x": 0,"y": .1}
                size_hint: .8, .5
            MDRectangleFlatIconButton:
                button_text: app.language_dialogs["enter_product"]
                font_size: 12
                pos_hint: {"x": 0,"y": 0}
                size_hint: .2, .1
                on_release: root.change_view("charge_or_hand_enter", "enter_products")
            MDRectangleFlatIconButton:
                button_text: app.language_dialogs["add_to_buy"]
                icon: "credit-card-plus"
                font_size: 12
                icon_size: 15
                on_release: root.add_to_buy()
                pos_hint: {"x": .2,"y": 0}
                size_hint: .3, .1
            MDRectangleFlatIconButton:
                button_text: app.language_dialogs["add_to_charge"]
                icon: "battery-plus"
                font_size: 12
                icon_size: 15
                on_release: root.add_to_charge()
                pos_hint: {"x": .5,"y": 0}
                size_hint: .3, .1
        MDFloatLayout:
            id: enter_products
            size_hint: 1, 1
            pos_hint: {"x": 0,"y": 0}
            MDPersianLabel:
                id: product_name
                pos_hint: {"x": .45,"y": .4}
                size_hint: .15, .1
            MDPersianLabel:
                id: product_price
                pos_hint: {"x": .3,"y": .4}
                size_hint: .15, .1
            MDIconButton:
                icon: "minus-circle"
                icon_size: 30
                pos_hint: {"x": .425,"y": .325}
                size_hint: .05, .05
                on_release: root.ids.number_of_products.text = str(int(root.ids.number_of_products.text) - 1) if int(root.ids.number_of_products.text) > 0 else root.ids.number_of_products.text
            MDLabel:
                id: number_of_products
                text: "0"
                pos_hint: {"x": .49,"y": .325}
                size_hint: .05, .05
                font_size: 30
            MDIconButton:
                icon: "plus-circle"
                icon_size: 30
                pos_hint: {"x": .525,"y": .325}
                size_hint: .05, .05
                on_release: root.ids.number_of_products.text = str(int(root.ids.number_of_products.text) + 1)
            MDRectangleFlatIconButton:
                button_text: app.language_dialogs["add"]
                icon: "arrow-left"
                pos_hint: {"x": .65,"y": .3}
                size_hint: .1, .1
                on_release: root.add_product()
            MDIconButton:
                icon: "delete"
                icon_size: 30
                pos_hint: {"x": .3,"y": .3}
                size_hint: .1, .1
                on_release: root.clear_product_input()
            MDTextFieldPersian:
                mode: "round"
                id: product_code
                pos_hint: {"x": .29,"y": .2}
                size_hint: .3, .1
                on_text: root.update_product_name(self.str)
                font_size: 30
                halign: "center"
            MDScrollView:
                id: products_list
                size_hint: .25, .5
                pos_hint: {'x': 0,'y': .15}
            MDRectangleFlatIconButton:
                button_text: app.language_dialogs["charge_or_import_manually"]
                font_size: 12
                pos_hint: {"x": 0,"y": 0}
                size_hint: .2, .1
                on_release: root.change_view("enter_products", "charge_or_hand_enter")
        MDPersianLabel:
            id: school
            pos_hint: {'x': .4, 'y': .8}
            size_hint: .2, .1
        MDPersianLabel:
            id: class_
            pos_hint: {'x': .2, 'y': .8}
            size_hint: .2, .1
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["reprocessing"]
            pos_hint: {"x": .8,"y": 0}
            size_hint: .2, .9
            on_release: root.manager.current = "login"

<Setting>:
    MDFloatLayout:
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["exit"]
            icon: "location-exit"
            on_release: root.manager.current = "user_account"
            pos_hint: {"x": 0, "y": .9}
            size_hint: .2, .1
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["change_name"]
            icon: "rename-box"
            on_release: root.manager.current = "change_user_name"
            pos_hint: {"x": .1,"y": .5}
            size_hint: .8,.2
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["change_face"]
            icon: "face-recognition"
            on_release: root.manager.current = "change_user_face_ask"
            pos_hint: {"x": .1,"y": .2}
            size_hint: .8,.2

<ChangeUserName>:
    FloatLayout:
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["exit"]
            icon: "location-exit"
            pos_hint: {"x": 0, "y": .9}
            size_hint: .2, .1
            on_release: root.manager.current = "setting"
        MDTextFieldPersian:
            id: new_name
            persian_hint_text: app.language_dialogs["new_name"]
            halign: "right"
            pos_hint: {"x": .1, "y": .5}
            size_hint: .8, .1
            font_size: 15
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["change"]
            pos_hint: {"x": .1, "y": .1}
            size_hint: .8, .2
            on_release: root.change_user_name()

<ChangeUserFaceAsk>:
    MDFloatLayout:
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["exit"]
            icon: "location-exit"
            pos_hint: {"x": 0, "y": .9}
            size_hint: .2, .1
            on_release: root.manager.current = "setting"
        MDPersianLabel:
            label_text: app.language_dialogs["are_you_sure"]
            pos_hint: {"x": .1, "y": .5}
            size_hint: .8, .1
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["yes"]
            pos_hint: {"x": .1, "y": .1}
            size_hint: .8, .2
            on_release: root.manager.current = "change_user_face_process"

<ChangeUserFaceProcess>:
    MDFloatLayout:
        MDPersianLabel:
            label_text: app.language_dialogs["taking_picture"] + "..."
            size_hint: .2, .1
            pos_hint: {"x": .4, "y": .45}
        MDSpinner:
            size_hint: None, None
            size: dp(46), dp(46)
            pos_hint: {'center_x': .5, 'center_y': .4}

<Log>:
    MDBoxLayout:
        orientation: "vertical"
        MDBoxLayout:
            orientation: "horizontal"
            size_hint: 1, .1
            MDRectangleFlatIconButton:
                button_text: app.language_dialogs["exit"]
                icon: "location-exit"
                on_release: root.manager.current = "user_account"
            MDLabel:
                size_hint: 1, 1
            MDRectangleFlatIconButton:
                button_text: app.language_dialogs["filter"]
                icon: "filter-outline"
                on_release: root.manager.current = "filter"
            MDLabel:
                size_hint: 1, 1
            MDRectangleFlatIconButton:
                button_text: app.language_dialogs["delete"]
                icon: "delete"
                on_release: root.delete_log()
        MDBoxLayout:
            size_hint_y: .2
            MDPersianLabel:
                label_text: app.language_dialogs["operation"]
                size_hint: .1, .2
                font_size: 30
            MDPersianLabel:
                label_text: app.language_dialogs["price"]
                size_hint: .1, .2
                font_size: 30
            MDPersianLabel:
                label_text: app.language_dialogs["date"]
                size_hint: .2, .2
                font_size: 30
            MDPersianLabel:
                label_text: app.language_dialogs["products"]
                size_hint: .2, .2
                font_size: 30
        MDBoxLayout:
            orientation: "horizontal"
            MDBoxLayout:
                id: log_type
                orientation: "vertical"
            MDBoxLayout:
                id: log_value
                orientation: "vertical"
            MDBoxLayout:
                id: log_date
                size_hint: 2, 1
                orientation: "vertical"
            MDBoxLayout:
                id: log_products
                size_hint: 2, 1
                orientation: "vertical"
        MDBoxLayout:
            orientation: "horizontal"
            size_hint: 1, .1
            MDIconButton:
                icon: "arrow-down"
                on_release: root.scroll_down()
            MDIconButton:
                icon: "arrow-up"
                on_release: root.scroll_up()

<Filter>:
    MDFloatLayout:
        MDCheckbox:
            id: check_date
            size_hint: .1, .1
            pos_hint: {'x': .9, 'y': .85}
        MDLabel:
            text: app.persian(app.language_dialogs["date"])
            font_name: app.FONT_PATH
            size_hint: .1, .1
            pos_hint: {'x': .85, 'y': .85}
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["select_date_from"]
            icon: "calendar"
            size_hint: .2, .1
            pos_hint: {'x': .6, 'y': .75}
            on_release: root.set_date_filter()
        MDLabel:
            id: from_date
            size_hint: .2, .1
            pos_hint: {'x': .6, 'y': .65}
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["select_date_to"]
            icon: "calendar"
            size_hint: .2, .1
            pos_hint: {'x': .35, 'y': .75}
            on_release: root.set_date_filter("to")
        MDLabel:
            id: to_date
            size_hint: .2, .1
            pos_hint: {'x': .35, 'y': .65}
        MDCheckbox:
            id: check_type
            on_active: root.set_type_filter(self.active)
            size_hint: .1, .1
            pos_hint: {'x': .9, 'y': .6}
        MDPersianLabel:
            label_text: app.language_dialogs["operation"]
            size_hint: .15, .1
            pos_hint: {'x': .78, 'y': .6}
        MDCheckbox:
            group: "type"
            id: is_buy
            on_active: root.set_type_filter(root.ids.check_type.active)
            size_hint: .1, .1
            pos_hint: {'x': .6, 'y': .5}
        MDCheckbox:
            group: "type"
            id: is_charge
            on_active: root.set_type_filter(root.ids.check_type.active)
            size_hint: .1, .1
            pos_hint: {'x': .3, 'y': .5}
        MDPersianLabel:
            label_text: app.language_dialogs["buy"]
            size_hint: .1, .1
            pos_hint: {'x': .55, 'y': .5}
        MDPersianLabel:
            label_text: app.language_dialogs["charge"]
            size_hint: .1, .1
            pos_hint: {'x': .25, 'y': .5}
        MDCheckbox:
            id: check_value
            size_hint: .1, .1
            pos_hint: {'x': .9, 'y': .35}
        MDPersianLabel:
            label_text: app.language_dialogs["price_log"]
            size_hint: .15, .1
            pos_hint: {'x': .78, 'y': .35}
        MDTextField:
            id: value_from
            font_size: 35
            input_filter: "int"
            size_hint: .3, .1
            pos_hint: {'x': .44, 'y': .3}
        MDTextField:
            id: value_to
            font_size: 35
            input_filter: "int"
            size_hint: .3, .1
            pos_hint: {'x': .04, 'y': .3}
        MDPersianLabel:
            label_text: app.language_dialogs["from"]
            size_hint: .1, .1
            pos_hint: {'x': .7, 'y': .3}
        MDPersianLabel:
            label_text: app.language_dialogs["to"]
            size_hint: .1, .1
            pos_hint: {'x': .3, 'y': .3}
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["cancel"]
            icon: "cancel"
            on_release: root.cancel()
            size_hint: .2, .1
            pos_hint: {'x': .25, 'y': .05}
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["done"]
            icon: "filter"
            on_release: root.set_filter()
            size_hint: .2, .1
            pos_hint: {'x': .05, 'y': .05}
"""


class UserAccount(MDScreen):
    user_name = ""
    show_user_name = ""
    user_charge = ""
    products_list = []
    do_shortcuts = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.event = Clock.schedule_interval(self.update, 1 / 10)

    def on_leave(self, *args):
        self.do_shortcuts = False
        return super().on_leave(*args)

    def update(self, dt):
        if self.do_shortcuts:
            keys = pygame.key.get_pressed()
            keys_ = [str(number) for number in range(10)]
            for key in keys_:
                if keys[eval(f"pygame.K_KP_{key}")]:
                    self.ids.calculator.on_button_press(MDFlatButton(text=key))

            if keys[pygame.K_KP_PLUS]:
                self.ids.calculator.on_button_press(MDFlatButton(text='+'))

            if keys[pygame.K_KP_MINUS]:
                self.ids.calculator.on_button_press(MDFlatButton(text='-'))

            if keys[pygame.K_KP_MULTIPLY]:
                self.ids.calculator.on_button_press(MDFlatButton(text='×'))

            if keys[pygame.K_KP_DIVIDE]:
                self.ids.calculator.on_button_press(MDFlatButton(text='÷'))

            if keys[pygame.K_KP_ENTER]:
                self.ids.calculator.on_solution('')

            if keys[pygame.K_HOME]:
                self.change_screen('home')

            if keys[pygame.K_s] and pygame.key.get_mods() & pygame.KMOD_CTRL:
                self.change_screen('setting')

            if keys[pygame.K_BACKSPACE]:
                self.ids.calculator.delete_last_character('')

            if keys[pygame.K_DELETE]:
                self.ids.calculator.on_button_press(MDFlatButton(text='C'))

            if keys[pygame.K_b] and pygame.key.get_mods() & pygame.KMOD_ALT:
                self.add_to_buy()

            if keys[pygame.K_b] and pygame.key.get_mods() & pygame.KMOD_CTRL:
                self.charge_or_buy(self.user_name, self.ids.buy.text, "buy")

            if keys[pygame.K_c] and pygame.key.get_mods() & pygame.KMOD_ALT:
                self.add_to_charge()

            if keys[pygame.K_c] and pygame.key.get_mods() & pygame.KMOD_CTRL:
                self.charge_or_buy(
                    self.user_name, self.ids.charge.text, "charge")

            if keys[pygame.K_r] and pygame.key.get_mods() & pygame.KMOD_CTRL:
                self.change_screen("login")

    def update_product_name(self, text):
        product = read_product(text)
        if product:
            self.ids.product_name.label_text = MDApp.get_running_app(
            ).language_dialogs["name"] + ": " + \
                product[0]
            self.ids.product_price.label_text = MDApp.get_running_app(
            ).language_dialogs["price"] + ": " + \
                str(product[2])
            self.ids.number_of_products.text = "1"
        else:
            self.ids.product_name.label_text = ""
            self.ids.product_price.label_text = ""
            self.ids.number_of_products.text = "0"

    def clear_product_input(self):
        self.ids.product_code.text = ""
        self.ids.product_code.str = ""
        self.ids.product_name.label_text = ""
        self.ids.product_price.label_text = ""
        self.ids.number_of_products.text = "0"

    def change_view(self, from_, to_):
        self.ids[from_].pos_hint = {"x": -1, "y": 0}
        self.ids[to_].pos_hint = {"x": 0, "y": 0}

    def change_screen(self, screen_name):
        self.manager.current = screen_name

    def reduce_products(self, instance):
        counted_items = []
        count_dict = {}
        for code, item in [[i[1], i] for i in self.products_list]:
            if code in counted_items:
                count_dict[code][0] += 1
            else:
                counted_items.append(code)
                count_dict[code] = [1, item[1], item[2], item[0]]
        code = instance.name
        self.products_list.remove(read_product(int(code)))
        if count_dict[int(code)][0] == 1:
            del count_dict[int(code)]
        else:
            count_dict[int(code)][0] -= 1
        items_layout = MDBoxLayout(
            spacing=30, size_hint_y=None, orientation='vertical')
        items_layout.bind(minimum_height=items_layout.setter('height'))
        last_price = 0
        for count, code, price, name in list(count_dict.values()):
            last_price += count * int(price)
            item_layout = MDBoxLayout(
                orientation="horizontal", size_hint_y=None, height=40)
            item_layout.add_widget(MDPersianLabel(
                label_text=f"{MDApp.get_running_app().language_dialogs["name"]}: {name}         {MDApp.get_running_app().language_dialogs["number"]}: {count}", size_hint_x=2))
            item_layout.add_widget(MDIconButton(
                name=str(code), icon="minus-circle", on_release=self.reduce_products))
            items_layout.add_widget(item_layout)
        self.ids.products_list.clear_widgets()
        self.ids.products_list.add_widget(items_layout)
        self.ids.buy.text = UserAccount.create_numbers(str(last_price))

    def add_product(self):
        if self.ids.product_code.str != "" and read_product(self.ids.product_code.str):
            for _ in range(int(self.ids.number_of_products.text)):
                self.products_list.append(read_product(
                    self.ids.product_code.str))
            counted_items = []
            count_dict = {}
            for code, item in [[i[1], i] for i in self.products_list]:
                if code in counted_items:
                    count_dict[code][0] += 1
                else:
                    counted_items.append(code)
                    count_dict[code] = [1, item[1], item[2],
                                        item[0]]
            items_layout = MDBoxLayout(
                spacing=30, size_hint_y=None, orientation='vertical')
            items_layout.bind(minimum_height=items_layout.setter('height'))
            last_price = 0
            for count, code, price, name in list(count_dict.values()):
                last_price += count * int(price)
                item_layout = MDBoxLayout(
                    orientation="horizontal", size_hint_y=None, height=40)
                item_layout.add_widget(MDPersianLabel(
                    label_text=f"{MDApp.get_running_app().language_dialogs["name"]}: {name}         {MDApp.get_running_app().language_dialogs["number"]}: {count}", size_hint_x=2))
                item_layout.add_widget(MDIconButton(
                    name=str(code), icon="minus-circle", on_release=self.reduce_products))
                items_layout.add_widget(item_layout)
            self.ids.products_list.clear_widgets()
            self.ids.products_list.add_widget(items_layout)
            self.ids.buy.text = UserAccount.create_numbers(str(last_price))
            self.clear_product_input()

    def clear_products(self):
        self.ids.products_list.clear_widgets()
        self.ids.buy.text = "0"
        self.products_list = []

    def on_enter(self):
        global user_name_, user_charge, user_school, user_class
        try:
            user_name_ = f_login.user_name
            charge_ = str(read_charge(user_name_))
            user_charge = charge_
            user_school = f_login.user_school
            user_class = f_login.user_class
            self.user_name = user_name_
            self.ids.school.label_text = MDApp.get_running_app().language_dialogs["school"] + " " + \
                f_login.user_school
            self.ids.class_.label_text = MDApp.get_running_app(
            ).language_dialogs["class"] + " " + f_login.user_class
            self.show_user_name = self.user_name
            self.ids.user_name.label_text = self.show_user_name
            self.user_charge = self.create_numbers(int(user_charge))
            self.ids.user_charge.text = self.user_charge
            self.products_list = []
            self.do_shortcuts = True
        except KeyError:
            pass

    @staticmethod
    def create_numbers(number, extract: bool = False):
        return create_numbers(number, extract)

    def charge_or_buy(self, name: str, value: str, type: str) -> None:
        global user_charge
        value = self.create_numbers(value, True)
        if type == "buy":
            products_names_list = [item[0] for item in self.products_list]
            buy(name, products_names_list, value)
            self.clear_products()
        elif type == "charge":
            charge(name, value)
        charge_ = str(read_charge(name))
        self.ids.buy.text = "0"
        self.ids.charge.text = "0"
        self.ids.user_charge.text = self.create_numbers(charge_)
        user_charge = charge_

    def add_to_buy(self):
        self.ids.calculator.on_solution("=")
        try:
            self.ids.buy.text = self.create_numbers(
                self.create_numbers(self.ids.buy.text, True) + calculator_value)
            if self.create_numbers(self.ids.buy.text, True) < 0:
                self.ids.buy.text = "0"
        except ValueError:
            self.ids.buy.text = str(calculator_value)
        self.ids.calculator.solution.text = "0"

    def add_to_charge(self):
        self.ids.calculator.on_solution("=")
        try:
            self.ids.charge.text = self.create_numbers(
                self.create_numbers(self.ids.charge.text, True) + calculator_value)
            if self.create_numbers(self.ids.charge.text, True) < 0:
                self.ids.charge.text = "0"
        except ValueError:
            self.ids.charge.text = str(calculator_value)
        self.ids.calculator.solution.text = "0"

    def go_to_setting_page(self):
        if user_type(current_user_name()) in ("creator", "admin"):
            self.manager.current = "setting"
        else:
            persian_text = MDApp.get_running_app(
            ).language_dialogs["admin_and_manager"]
            text = "[font={}]{}[/font]".format(FONT_PATH,
                                               get_display(reshape(persian_text)))
            self.dialog = MDDialog(
                title=text,
                buttons=[
                    MDFlatButton(
                        text=get_display(
                            reshape(
                                MDApp.get_running_app(
                                ).language_dialogs["i_got_it"]
                            )
                        ),
                        font_name=FONT_PATH,
                        on_release=lambda instance: self.dialog.dismiss()
                    )
                ]
            )
            self.dialog.open()


class Calculator(MDBoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.solution = MDTextField(
            text="0", multiline=False, readonly=True,
            halign="right", font_size=25
        )
        self.add_widget(self.solution)
        buttons = [
            ["7", "8", "9", "Del"],
            ["4", "5", "6", "C"],
            ["1", "2", "3", "÷"],
            ["00", "0", "000", "×"],
            ["=", "+", "-"]
        ]
        for row in buttons:
            h_layout = MDBoxLayout()
            for label in row:
                if label not in ["=", "Del"]:
                    button = MDRaisedButton(
                        text=label,
                        font_size=25,
                        size_hint=(1, 1)
                    )
                elif label == "Del":
                    button = MDIconButton(
                        icon="backspace",
                        icon_size=40,
                        size_hint=(1, 1)
                    )
                else:
                    button = MDRaisedButton(
                        text=label,
                        font_size=25,
                        size_hint=(2, 1)
                    )
                if label in ("+", "-", "×", "÷"):
                    button.md_bg_color = (0, 1, 0, 1)
                elif label == "C":
                    button.md_bg_color = (1, 0, 0, 1)
                elif label == "Del":
                    button.md_bg_color = (0, 0, 0, 0)
                else:
                    button.md_bg_color = (.4, .4, 1, 1)
                if label == "000":
                    button.font_size = 20
                if label not in ("=", "Del"):
                    button.bind(on_press=self.on_button_press)
                elif label == "Del":
                    button.bind(on_press=self.delete_last_character)
                else:
                    button.md_bg_color = (1, 1, 0, 1)
                    button.bind(on_press=self.on_solution)
                h_layout.add_widget(button)
            self.add_widget(h_layout)

    def delete_last_character(self, instance):
        self.solution.text = self.solution.text[:-1]
        if self.solution.text == "":
            self.solution.text = "0"

    def on_button_press(self, instance):
        global last_was_operator
        button_text = instance.text
        if button_text in ["÷", "×"]:
            button_text = {"×": "*", "÷": "/"}[button_text]
        operators = ["/", "*", "+", "-"]
        current = self.solution.text
        if button_text == "C":
            self.solution.text = "0"
        else:
            if self.solution.text == "Error":
                return
            if last_was_operator and button_text in operators:
                return
            elif current == "" and button_text in operators:
                return
            elif (current.endswith(("-0", "+0", "*0", "/0"))
                    or current == "0") and button_text in ("0", "00", "000"):
                return
            elif last_was_operator and button_text in ("00", "000"):
                return
            else:
                if (current.endswith(("-0", "+0", "*0", "/0")) or current ==
                        "0") and button_text in [str(x + 1) for x in range(9)]:
                    current = current[:-1]
                new_text = current + button_text
                self.solution.text = new_text.replace(
                    "/", "÷", new_text.count("/")).replace("*", "×", new_text.count("*"))
                last_was_operator = button_text in operators

    def on_solution(self, instance):
        global calculator_value
        text = self.solution.text
        try:
            if text:
                if text != "Error":
                    calculator_value = int(eval(self.solution.text.replace(
                        "÷", "/", self.solution.text.count("÷")).replace("×", "*", self.solution.text.count("×"))))
                    solution = str(calculator_value)
                    self.solution.text = solution
                else:
                    self.solution.text = "0"
        except (SyntaxError, ZeroDivisionError):
            self.solution.text = "Error"


class Setting(MDScreen):
    pass


class ChangeUserName(MDScreen):
    do_shortcuts = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.event = Clock.schedule_interval(self.update, 1 / 10)

    def on_leave(self, *args):
        self.do_shortcuts = False
        return super().on_leave(*args)

    def update(self, dt):
        if self.do_shortcuts:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                self.change_user_name()

    def on_enter(self):
        self.do_shortcuts = True

    def close_dialog(self, instance):
        self.dialog.dismiss()

    def change_user_name(self):
        new_name = self.ids.new_name.str
        if new_name != "" and check_name_is_new(new_name):
            change_buyer_name(user_name_, new_name)
            f_login.user_name = new_name
            self.ids.new_name.str = ""
            self.manager.current = "user_account"
        else:
            persian_text = MDApp.get_running_app(
            ).language_dialogs["name_wrong_error"]
            text = "[font={}]{}[/font]".format(FONT_PATH,
                                               get_display(reshape(persian_text)))
            self.dialog = MDDialog(
                title=text,
                buttons=[
                    MDFlatButton(
                        text=get_display(
                            reshape(
                                MDApp.get_running_app(
                                ).language_dialogs["i_got_it"]
                            )
                        ),
                        font_name=FONT_PATH,
                        on_release=self.close_dialog
                    )
                ]
            )
            self.dialog.open()


class ChangeUserFaceAsk(MDScreen):
    pass


class ChangeUserFaceProcess(MDScreen):

    def process(self):
        global user_name_
        change_buyer_face(user_name_)

    def on_enter(self):
        thread = threading.Thread(target=self.process)
        thread.start()
        self.manager.current = "user_account"


class Log(MDScreen):
    first_item_index = 0
    items = []

    def delete_log(self):
        global filter, date_filter, type_filter, value_filter
        if user_type(current_user_name()) in ("creator", "admin"):
            delete_log(self.items)
            filter = []
            date_filter = []
            value_filter = []
            type_filter = None
            self.on_enter()
        else:
            persian_text = MDApp.get_running_app().language_dialogs["admin_and_manager"]
            text = "[font={}]{}[/font]".format(FONT_PATH,
                                               get_display(reshape(persian_text)))
            self.dialog = MDDialog(
                title=text,
                buttons=[
                    MDFlatButton(
                        text=get_display(
                            reshape(
                                MDApp.get_running_app(
                                ).language_dialogs["i_got_it"]
                            )
                        ),
                        font_name=FONT_PATH,
                        on_release=lambda instance: self.dialog.dismiss()
                    )
                ]
            )
            self.dialog.open()

    def scroll_up(self):
        self.first_item_index -= 5
        self.update()

    def scroll_down(self):
        self.first_item_index += 5
        self.update()

    def on_enter(self):
        global filter, date_filter, type_filter, value_filter
        self.first_item_index = 0
        try:
            self.items = read_logs(by="name", name=user_name_)
            for filter_item in filter:
                if filter_item == "operation":
                    self.items = read_logs(
                        by=filter_item, logs=self.items, operation={"c": "charge", "b": "buy"}[type_filter])

                elif filter_item == "price":
                    self.items = read_logs(
                        by=filter_item, logs=self.items, start_price=value_filter[0], end_price=value_filter[1])

                elif filter_item == "date":
                    self.items = read_logs(
                        by=filter_item, logs=self.items, start_date=date_filter[0], end_date=date_filter[1])
            self.update()
        except:
            self.items = read_logs(by="name", name=user_name_)
            self.update()

    def update(self):
        if self.first_item_index < 0:
            self.first_item_index = 0
        self.ids.log_value.clear_widgets()
        self.ids.log_type.clear_widgets()
        self.ids.log_date.clear_widgets()
        self.ids.log_products.clear_widgets()
        products_str = ""
        for item in self.items[self.first_item_index:self.first_item_index + 5]:
            try:
                for product in eval(item[4]):
                    products_str += product + " - "
                products_str = products_str[:-3]
            except:
                pass
            products_str = "------" if products_str == "" else products_str
            self.ids.log_products.add_widget(MDPersianLabel(
                label_text=products_str, size_hint=(1, 1)))
            products_str = ""
            self.ids.log_value.add_widget(
                MDLabel(text=str(item[2]), size_hint=(1, 1), halign="center"))
            self.ids.log_type.add_widget(MDPersianLabel(
                label_text=MDApp.get_running_app().language_dialogs['buy_or_charge'][item[1]], size_hint=(1, 1)))
            self.ids.log_date.add_widget(
                MDLabel(text=str(item[3]), size_hint=(1, 1), halign="center"))


class Filter(MDScreen):
    date_filter = {"from": "", "to": ""}
    date_filter_type = None

    def open_picker(self):
        self.picker = MDDatePicker()
        self.picker.on_ok_button_pressed = lambda: self.get_date(
            self.picker.year, self.picker.month, self.picker.sel_day)
        self.picker.open()

    def get_date(self, year, month, day):
        self.picker.dismiss()
        self.date_filter[self.date_filter_type] = f"{year}-{month}-{day}"
        self.ids.from_date.text = self.date_filter["from"]
        self.ids.to_date.text = self.date_filter["to"]

    def set_date_filter(self, type="from"):
        if self.ids.check_date.active:
            self.date_filter_type = type
            self.open_picker()

    def set_type_filter(self, active):
        if not active:
            self.ids.is_buy.active = False
            self.ids.is_charge.active = False

    def cancel(self):
        global filter, date_filter, type_filter, value_filter
        filter = []
        date_filter = []
        value_filter = []
        type_filter = None
        self.manager.current = "log"

    def set_filter(self):
        global filter, date_filter, type_filter, value_filter
        filter = []
        date_filter = []
        value_filter = []
        type_filter = None
        for checkbox_id in ("check_type", "check_date", "check_value"):
            if self.ids[checkbox_id].active:
                filter.append({"type": "operation", "value": "price", "date": "date"}
                              [checkbox_id.replace("check_", "")])
        date_filter += [self.ids.from_date.text, self.ids.to_date.text]
        value_filter += [self.ids.value_from.text, self.ids.value_to.text]
        type_filter = "b" if self.ids.is_buy.active else "c" if self.ids.is_charge.active else None
        self.manager.current = "log"
