import threading
import queue
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
import pygame
import cv2
from important_variables import FONT_PATH
from b_schools_and_classes import read_classes, read_schools
from b_manage_buyers import check_name_is_new, register_buyer
from f_create_numbers import create_numbers
from arabic_reshaper import reshape
from bidi.algorithm import get_display

do = False
register_name = ""
register_charge = ""
register_class = ""
register_school = ""

KV = """
<RegisterGetName>:
    MDFloatLayout:
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["exit"]
            icon: "location-exit"
            pos_hint: {"x": 0, "y": .9}
            size_hint: .2, .1
            on_release: root.manager.current = "home"
        MDTextFieldPersian:
            id: register_user_name
            halign: "right"
            persian_hint_text: app.language_dialogs["name"]
            pos_hint: {"x": .2,"y": .65}
            size_hint: .6, .1
            font_size: 15
        MDTextField:
            id: register_user_charge
            text: "0"
            multiline: False
            mode: "rectangle"
            hint_text: app.persian(app.language_dialogs["charge"])
            font_name_hint_text: app.FONT_PATH
            on_text: root.create_numbers()
            pos_hint: {"x": .2,"y": .52}
            size_hint: .6, .1
            font_size: 20
        MDPersianLabel:
            label_text: app.language_dialogs["school"]
            pos_hint: {"x": .6,"y": .34}
            size_hint: .3, .2
        MDPersianLabel:
            label_text: app.language_dialogs["class"]
            pos_hint: {"x": .6,"y": .21}
            size_hint: .3, .2
        MDRectangleFlatIconButton:
            button_text: app.language_dialogs["register"]
            icon: "account-plus"
            pos_hint: {"x": .1,"y": .1}
            size_hint: .8, .1
            on_release: root.next_step()

<RegisterGetFace>:
    MDFloatLayout:
        MDPersianLabel:
            label_text: app.language_dialogs["taking_picture"] + "..."
            size_hint: .2, .1
            pos_hint: {"x": .4, "y": .45}
        MDSpinner:
            size_hint: None, None
            size: dp(46), dp(46)
            pos_hint: {'center_x': .5, 'center_y': .4}
"""


class RegisterGetName(MDScreen):
    class_auto = True
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
                self.next_step()

    def on_enter(self):
        self.do_shortcuts = True
        self.school_name = ""
        self.class_name = ""
        self.set_dropdowns()

    def menu_callback(self, text_item):
        self.school_name_button.text = get_display(reshape(text_item))
        self.school_name = text_item
        self.class_auto = False
        self.set_dropdowns()

    def menu_callback2(self, text_item):
        self.class_name_button.text = text_item
        self.class_name = text_item

    def set_dropdowns(self):
        try:
            schools_list = read_schools()
            items = [
                {
                    "viewclass": "MDItemButton2",
                    "text_": school
                } for school in schools_list
            ]
            if self.class_auto:
                self.school_name = schools_list[0]
            classes_list = read_classes(self.school_name)
            self.school_name_button = MDRaisedButton(text=get_display(reshape(
                self.school_name)), font_name=FONT_PATH, on_press=lambda instance: self.dropdown.open(), pos_hint={"x": .2, "y": .39}, size_hint=(.2, .1))
            self.dropdown = MDDropdownMenu(
                caller=self.school_name_button, items=items)
            self.add_widget(self.school_name_button)
            if not classes_list == [""] and not classes_list == []:
                items = [
                    {
                        "viewclass": "MDItemButton3",
                        "text": class_
                    } for class_ in classes_list
                ]
                self.class_name = classes_list[0]
                self.class_name_button = MDRaisedButton(text=classes_list[0], on_press=lambda instance: self.dropdown2.open(
                ), pos_hint={"x": .2, "y": .26}, size_hint=(.2, .1))
                self.dropdown2 = MDDropdownMenu(
                    caller=self.class_name_button, items=items)
                self.add_widget(self.class_name_button)
        except:
            pass

    def create_numbers(self):
        if self.ids.register_user_charge.text == "":
            self.ids.register_user_charge.text = "0"
        extracted = create_numbers(
            self.ids.register_user_charge.text, True)
        text = create_numbers(extracted)
        self.ids.register_user_charge.text = "".join(
            i for i in text if i in "0123456789,")

    def close_dialog(self, instance):
        self.dialog.dismiss()

    def next_step(self):
        global register_name, register_charge, register_school, register_class
        register_name = self.ids.register_user_name.str
        register_charge = self.ids.register_user_charge.text
        register_school = self.school_name
        register_class = self.class_name
        register_charge = create_numbers(register_charge, True)
        capture = cv2.VideoCapture(0)
        schools = read_schools()
        try:
            classes = read_classes(register_school)
        except KeyError:
            classes = []
        if check_name_is_new(register_name) and register_charge != "" and register_charge != None and capture.isOpened() and register_school in schools and register_school != "" and register_school != None and register_class in classes and register_class != "" and register_class != None:
            self.ids.register_user_name.str = ""
            self.ids.register_user_name.str = ""
            self.manager.current = "register_get_face"
        else:
            if not capture.isOpened():
                persian_text = MDApp.get_running_app(
                ).language_dialogs["webcam_error"]
            else:
                persian_text = MDApp.get_running_app(
                ).language_dialogs["n_or_c_or_s_or_c_error"]
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


class RegisterGetFace(MDScreen):

    def start_worker_thread(self):
        def worker():
            register_buyer(
                register_name, register_charge,
                register_school, register_class)
            self.queue.put(lambda: setattr(self.manager, 'current', 'home'))

        threading.Thread(target=worker).start()

    def process_queue(self, dt):
        while not self.queue.empty():
            callback = self.queue.get()
            callback()

    def on_enter(self):
        self.queue = queue.Queue()
        Clock.schedule_interval(self.process_queue, 0.1)
        self.start_worker_thread()
