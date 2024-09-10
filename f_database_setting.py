from b_product import delete_product, is_new, read_all_products, save_product
from b_schools_and_classes import read_classes, read_schools, save_class, save_school, delete_class, delete_school
from b_manage_users import all_users, change_user_type, current_user_name, user_type
from important_variables import FONT_PATH, LANGUAGE_PATH
from arabic_reshaper import reshape
from bidi.algorithm import get_display
import pygame
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu

from f_components import MDFlatButton, MDIconButton, MDPersianLabel, MDTextFieldPersian, MDRectangleFlatIconButton

KV = """
<DatabaseSetting>:
    MDFloatLayout:
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["exit"]
            icon: "location-exit"
            pos_hint: {"x": 0, "y": .9}
            size_hint: .2, .1
            on_release: root.manager.current = "settings"
        MDBottomNavigation:
            id: bottom_navigation
            pos_hint: {"x": 0, "y": 0}
            size_hint: 1, .9
            font_name: app.FONT_PATH
            MDBottomNavigationItem:
                name: "screen 4"
                text: app.persian(app.language_dialogs["users"])
                icon: "account-multiple"
                on_tab_press: root.on_users_press()

                MDFloatLayout:
                    id: database_users

            MDBottomNavigationItem:
                name: "screen 3"
                text: app.persian(app.language_dialogs["products"])
                icon: "cart"
                on_tab_press: root.on_products_press()

                MDFloatLayout:
                    id: database_products

            MDBottomNavigationItem:
                name: "screen 2"
                text: app.persian(app.language_dialogs["classes"])
                icon: "chair-school"
                on_tab_press: root.on_class_press()

                MDFloatLayout:
                    id: database_classes

            MDBottomNavigationItem:
                name: "screen 1"
                text: app.persian(app.language_dialogs["schools"])
                icon: "school"
                on_tab_press: root.on_school_press()

                MDFloatLayout:
                    id: database_schools
"""


class DatabaseSetting(MDScreen):
    school_name = ""
    class_auto = True
    is_in_class = False
    is_in_schools = False
    is_in_products = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Clock.schedule_interval(self.update_text, 1 / 30)

    def on_enter(self, *args):
        self.is_in_schools = True
        self.on_school_press()
        return super().on_enter(*args)

    def on_leave(self, *args):
        self.is_in_schools = False
        self.is_in_class = False
        return super().on_leave(*args)

    def update_text(self, dt):
        if self.is_in_class:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                self.class_name.text = self.class_name.text
                self.add_class("")
        elif self.is_in_schools:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                self.school_name_.str = self.school_name_.str
                self.add_school("")
        elif self.is_in_products:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                self.add_product("")

    def add_class(self, instance):
        save_class(
            self.school_name, self.class_name.text)
        self.on_class_press()

    def remove_class(self, instance):
        delete_class(
            self.school_name, instance.name)
        self.on_class_press()

    def menu_callback(self, text_item):
        self.school_name_button.text = get_display(reshape(text_item))
        self.school_name = text_item
        self.class_auto = False
        self.on_class_press()

    def on_class_press(self):
        self.is_in_class = True
        self.is_in_schools = False
        self.is_in_products = False
        schools_list = read_schools()
        if not schools_list == [""] and not schools_list == []:
            items = [
                {
                    "viewclass": "MDItemButton1",
                    "text_": school
                } for school in schools_list
            ]
            if self.class_auto:
                self.school_name = schools_list[0]
            self.school_name_button = MDRaisedButton(text=get_display(reshape(
                self.school_name)), font_name=FONT_PATH, on_press=lambda instance: self.dropdown.open(), pos_hint={'x': .7, 'y': .8}, size_hint=(.2, .1))
            self.dropdown = MDDropdownMenu(
                caller=self.school_name_button, items=items)
            classes_list = read_classes((self.school_name))
            self.ids.database_classes.clear_widgets()
            layout = MDBoxLayout(
                spacing=5, size_hint_y=None, orientation="vertical")
            layout.bind(minimum_height=layout.setter("height"))
            for class_name in classes_list:
                sub_layout = MDBoxLayout(
                    orientation="horizontal", size_hint_y=None, height=40)
                label = MDPersianLabel(label_text=class_name)
                sub_layout.add_widget(label)
                btn = MDIconButton(
                    icon="delete", name=class_name, on_release=self.remove_class)
                sub_layout.add_widget(btn)
                layout.add_widget(sub_layout)
            root = MDScrollView(size_hint=(.5, .5), pos_hint={"x": 0, "y": .2})
            root.add_widget(layout)
            self.ids.database_classes.add_widget(root)
            self.ids.database_classes.add_widget(self.school_name_button)
            self.class_name = MDTextField(size_hint=(.2, .075), pos_hint={
                                          'x': .7, 'y': .6}, input_filter="int")
            self.ids.database_classes.add_widget(self.class_name)
            self.ids.database_classes.add_widget(
                MDRectangleFlatIconButton(
                    button_text=MDApp.get_running_app(
                    ).language_dialogs["add_class"],
                    icon="plus-circle",
                    size_hint=(.2, .075),
                    pos_hint={'x': .7, 'y': .5},
                    on_release=self.add_class
                )
            )
            with open(LANGUAGE_PATH, 'r') as file:
                lang = file.read()
            if lang=='eng':
                MDApp.get_running_app().reverse_widgets(self.ids.database_classes)
        else:
            self.ids.database_classes.clear_widgets()

    def add_school(self, instance):
        save_school(self.school_name_.str)
        self.on_school_press()

    def remove_school(self, instance):
        delete_school(instance.name)
        self.class_auto = True
        self.on_school_press()

    def on_school_press(self):
        self.is_in_class = False
        self.is_in_schools = True
        self.is_in_products = False
        schools_list = read_schools()
        self.ids.database_schools.clear_widgets()
        layout = MDBoxLayout(spacing=5, size_hint_y=None,
                             orientation="vertical")
        layout.bind(minimum_height=layout.setter("height"))
        for schools_name in schools_list:
            if schools_name != "":
                sub_layout = MDBoxLayout(
                    orientation="horizontal", size_hint_y=None, height=40)
                label = MDPersianLabel(label_text=schools_name)
                sub_layout.add_widget(label)
                btn = MDIconButton(
                    icon="delete", name=schools_name, on_release=self.remove_school)
                sub_layout.add_widget(btn)
                layout.add_widget(sub_layout)
        root = MDScrollView(size_hint=(.5, .5), pos_hint={"x": 0, "y": .2})
        root.add_widget(layout)
        self.ids.database_schools.add_widget(root)
        self.school_name_ = MDTextFieldPersian(mode="round",
                                               size_hint=(.2, .075), pos_hint={'x': .7, 'y': .6})
        self.ids.database_schools.add_widget(self.school_name_)
        self.ids.database_schools.add_widget(
            MDRectangleFlatIconButton(
                button_text=MDApp.get_running_app(
                ).language_dialogs["add_school"],
                icon="plus-circle",
                size_hint=(.2, .075),
                pos_hint={'x': .7, 'y': .5},
                on_release=self.add_school
            )
        )
        with open(LANGUAGE_PATH, 'r') as file:
            lang = file.read()
        if lang=='eng':
            MDApp.get_running_app().reverse_widgets(self.ids.database_schools)

    def add_product(self, instance):
        product_code = self.product_code.str
        product_name = self.product_name.str
        product_price = self.product_price.str
        if not "" in [product_code, product_name, product_price] and is_new(product_name, int(product_code))[0]:
            save_product(product_name, product_code, product_price)
        elif not "" in [product_code, product_name, product_price]:
            persian_text = MDApp.get_running_app().language_dialogs["product_duplicated_error"](
                is_new, product_name, product_code)
            text = "[font={}]{}[/font]".format(FONT_PATH,
                                               get_display(reshape(persian_text)))
            self.dialog = MDDialog(
                title=text,
                buttons=[
                    MDFlatButton(
                        text=get_display(
                            reshape(MDApp.get_running_app().language_dialogs["i_got_it"])),
                        font_name=FONT_PATH,
                        on_release=lambda instance: self.dialog.dismiss()
                    )
                ]
            )
            self.dialog.open()
        self.on_products_press()

    def delete_product(self, instance):
        delete_product(instance.name)
        self.on_products_press()

    def on_products_press(self):
        self.is_in_class = False
        self.is_in_schools = False
        self.is_in_products = True
        self.ids.database_products.clear_widgets()
        all_products_list = read_all_products()
        layout = MDBoxLayout(spacing=5, size_hint_y=None,
                             orientation="vertical")
        layout.bind(minimum_height=layout.setter("height"))
        for name, code, price in all_products_list:
            sub_layout = MDBoxLayout(
                orientation="horizontal", size_hint_y=None, height=40)
            label2 = MDPersianLabel(
                label_text=f"{MDApp.get_running_app().language_dialogs["price"]}: {price}")
            sub_layout.add_widget(label2)
            label3 = MDPersianLabel(
                label_text=f"{MDApp.get_running_app().language_dialogs["code"]}: {code}")
            sub_layout.add_widget(label3)
            label = MDPersianLabel(label_text=f"{MDApp.get_running_app(
            ).language_dialogs["name"]}: {name}")
            sub_layout.add_widget(label)
            btn = MDIconButton(icon="delete", name=str(code),
                               on_release=self.delete_product)
            sub_layout.add_widget(btn)
            layout.add_widget(sub_layout)
        root = MDScrollView(size_hint=(.5, .5), pos_hint={"x": 0, "y": .2})
        root.add_widget(layout)
        self.ids.database_products.add_widget(root)
        self.product_code = MDTextFieldPersian(
            mode="round",
            size_hint=(.2, .075),
            pos_hint={'x': .6, 'y': .6},
            valid_chars="1234567890")
        self.ids.database_products.add_widget(MDPersianLabel(
            label_text=MDApp.get_running_app()
            .language_dialogs["product_code"],
            pos_hint={'x': .8, 'y': .6}, size_hint=(.15, .1)))
        self.ids.database_products.add_widget(self.product_code)
        self.product_name = MDTextFieldPersian(
            mode="round",
            size_hint=(.2, .075),
            pos_hint={'x': .6, 'y': .5})
        self.ids.database_products.add_widget(MDPersianLabel(
            label_text=MDApp.get_running_app()
            .language_dialogs["product_name"],
            pos_hint={'x': .8, 'y': .5}, size_hint=(.15, .1)))
        self.ids.database_products.add_widget(self.product_name)
        self.product_price = MDTextFieldPersian(
            mode="round",
            size_hint=(.2, .075),
            pos_hint={'x': .6, 'y': .4},
            valid_chars="1234567890")
        self.ids.database_products.add_widget(MDPersianLabel(
            label_text=MDApp.get_running_app()
            .language_dialogs["product_price"],
            pos_hint={'x': .8, 'y': .4}, size_hint=(.15, .1)))
        self.ids.database_products.add_widget(self.product_price)
        self.ids.database_products.add_widget(
            MDRectangleFlatIconButton(
                button_text=MDApp.get_running_app(
                ).language_dialogs["add_product"],
                icon="plus-circle",
                size_hint=(.2, .075),
                pos_hint={'x': .7, 'y': .3},
                on_release=self.add_product
            )
        )
        with open(LANGUAGE_PATH, 'r') as file:
            lang = file.read()
        if lang=='eng':
            MDApp.get_running_app().reverse_widgets(self.ids.database_products)

    def change_user_type(self, instance):
        change_user_type(instance.name)
        self.on_users_press()

    def on_users_press(self):
        self.is_in_class = False
        self.is_in_schools = False
        self.is_in_products = False
        if user_type(current_user_name()) == "creator":
            users_list = all_users()
            self.ids.database_users.clear_widgets()
            layout = MDBoxLayout(spacing=5, size_hint_y=None,
                                 orientation="vertical")
            layout.bind(minimum_height=layout.setter("height"))
            for user in users_list:
                sub_layout = MDBoxLayout(
                    orientation="horizontal", size_hint_y=None, height=40)
                label = MDPersianLabel(label_text="{}: {}      {}: {}".format(
                    MDApp.get_running_app().language_dialogs["name"], user,
                    MDApp.get_running_app().language_dialogs["role"],
                    {"normal": MDApp.get_running_app()
                     .language_dialogs["normal"],
                     "admin": MDApp.get_running_app()
                     .language_dialogs["admin"]}[user_type(user)]))
                sub_layout.add_widget(label)
                btn = MDRectangleFlatIconButton(
                    button_text=MDApp.get_running_app().language_dialogs["change_role"],
                    font_name=FONT_PATH,
                    name=user,
                    on_release=self.change_user_type)
                sub_layout.add_widget(btn)
                layout.add_widget(sub_layout)
            root = MDScrollView(size_hint=(.5, .5), pos_hint={"x": 0, "y": .2})
            root.add_widget(layout)
            self.ids.database_users.add_widget(root)
            with open(LANGUAGE_PATH, 'r') as file:
                lang = file.read()
            if lang=='eng':
                MDApp.get_running_app().reverse_widgets(self.ids.database_users)
        else:
            persian_text = MDApp.get_running_app().language_dialogs["only_manager"]
            text = "[font={}]{}[/font]".format(FONT_PATH,
                                               get_display(reshape(persian_text)))
            self.dialog = MDDialog(
                title=text,
                buttons=[
                    MDFlatButton(
                        text=get_display(reshape(MDApp.get_running_app().language_dialogs["i_got_it"])),
                        font_name=FONT_PATH,
                        on_release=self.close_dialog
                    )
                ]
            )
            self.dialog.open()

    def close_dialog(self, instance):
        self.dialog.dismiss()
